# ======================
# 0) IMPORTS Y CONSTANTES
# ======================

import os
import re
import html
import json
import logging
import unicodedata
from logging.handlers import RotatingFileHandler

# Manejo de texto y utilidades
import ftfy
from unidecode import unidecode
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

# Manejo de datos y análisis
import numpy as np
import pandas as pd

# Visualización
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tabulate import tabulate

# Hugging Face (solo para tokenizador/encoder y logs)
from transformers import AutoTokenizer, AutoModel, logging as hf_logging
hf_logging.set_verbosity_error()

# Scikit-learn: extracción de características, modelado y métricas
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

# Persistencia baseline
from joblib import dump as joblib_dump, load as joblib_load

# PyTorch (para la parte BERT+CNN)
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# ========== CONFIG GENERAL ==========
os.environ["TOKENIZERS_PARALLELISM"] = "false"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

LOGGING_ENABLED   = True
LOG_TO_CONSOLE    = True
LOG_DIR           = "./logs"
LOG_FILE_NAME     = "pipeline.log"
LOG_LEVEL         = logging.INFO
LOG_MAX_BYTES     = 2 * 1024 * 1024       # 2MB
LOG_BACKUP_COUNT  = 3
LOG_SAMPLE_N      = 8

# --------- EJECUCIÓN (on/off) ----------
RUN_FREQUENCIES = True
RUN_NGRAMS      = True
RUN_PLOTS       = True
RUN_MODELS      = True
RUN_THRESHOLD   = False
RUN_BERTCNN     = True   # ⬅️ PyTorch BERT+CNN

# --------- RUTAS / ARCHIVOS ------------
DATA_DIR     = "data"
RAW_FILE     = "train.csv"
CLEAN_FILE   = "cleaned_train.csv"
USE_CLEANED  = False
DO_CLEANING  = True
SAVE_CLEANED = True

# --------- LIMPIEZA (control fino) -----
REMOVE_URLS       = True
REMOVE_MENTIONS   = True
REMOVE_HASHTAGS   = True
REMOVE_EMOJIS     = True
REMOVE_PUNCT      = True
LOWERCASE         = True
REMOVE_STOPWORDS  = True
STOPWORDS_LANG    = "english"

# --------- BOW / NGRAMS ----------------
VEC_MIN_DF        = 2
NGRAM_MAX         = 2
CHAR_NGRAM_RANGE  = (3,5)

# --------- TRAIN/TEST -------------------
TEST_SIZE         = 0.20
RANDOM_STATE      = 42
CALIBRATE_SVC     = True

# --------- PLOTS ------------------------
SAVE_FIGS         = True
IMAGES_DIR        = "./images"
TOPK_FREQ         = 30
TOPK_NGRAMS       = 20

# --------- BERT + CNN (PyTorch) --------
BERT_MODEL_NAME   = "distilbert-base-uncased"   # funciona bien en PyTorch
BERT_MAX_LEN      = 128
BERT_BATCH        = 32
BERT_EPOCHS       = 10
BERT_LR           = 1e-3        # cabeza CNN + linear; el encoder va congelado por defecto
CNN_FILTERS       = 32
CNN_KERNEL_SIZE   = 3
CNN_DROPOUT       = 0.5
BERT_TRAINABLE    = False       # True para fine-tuning del encoder (mejor con GPU)
BERT_THRESHOLD    = 0.50
EARLY_STOP_PATIENCE = 2

# Heurística: ¿mojibake?
MOJIBAKE_PAT = re.compile(
    r"[\uFFFD\u0080-\u009F]"      # U+FFFD o control C1
    r"|Ã.|Â.|â.|Û.|Ò|Ó"
)

# --------- MODELOS (guardar/cargar) ----------
MODELS_DIR              = "./models"

# Baseline (scikit-learn)
SAVE_BASELINE_MODEL     = True
BASELINE_MODEL_FILE     = "baseline_best.joblib"
BASELINE_LOAD_PATH      = os.path.join(MODELS_DIR, BASELINE_MODEL_FILE)

# BERT + CNN (PyTorch + tokenizer)
SAVE_BERT_MODEL         = True
BERT_ARTIFACT_DIR       = "bert_cnn"
BERT_MODEL_SUBDIR       = "model"       # guardamos state_dict + meta.json
BERT_TOKENIZER_SUBDIR   = "tokenizer"

BERT_MODEL_LOAD_PATH    = os.path.join(MODELS_DIR, BERT_ARTIFACT_DIR, BERT_MODEL_SUBDIR)
BERT_TOKENIZER_LOAD_PATH= os.path.join(MODELS_DIR, BERT_ARTIFACT_DIR, BERT_TOKENIZER_SUBDIR)


# ======================
# 1) LOGGING / UTILS
# ======================
def ensureDir(path: str) -> bool:
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"[ensureDir] Error: {e}")
        return False

def initLogger(name: str = "lab6") -> logging.Logger:
    ensureDir(LOG_DIR)
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.handlers.clear()
    fh = RotatingFileHandler(os.path.join(LOG_DIR, LOG_FILE_NAME),
                             maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT,
                             encoding="utf-8")
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt); logger.addHandler(fh)
    if LOG_TO_CONSOLE:
        ch = logging.StreamHandler(); ch.setFormatter(fmt); logger.addHandler(ch)
    logger.propagate = False
    if LOGGING_ENABLED:
        logger.info("=== Logger inicializado ===")
    return logger

def logSection(logger: logging.Logger, title: str):
    if LOGGING_ENABLED:
        logger.info("")
        logger.info("=" * (len(title) + 8))
        logger.info(f"==  {title}  ==")
        logger.info("=" * (len(title) + 8))


# ======================
# 2) LIMPIEZA DE TEXTO
# ======================
def looksMojibake(t: str) -> bool:
    return bool(MOJIBAKE_PAT.search(t))

def autoFixEncoding(t: str) -> str:
    if not t:
        return t
    try:
        fixed = ftfy.fix_text(t)
        if fixed != t:
            return fixed
    except Exception:
        pass
    if looksMojibake(t):
        for enc in ("latin1", "cp1252"):
            try:
                b = t.encode('latin1', errors='ignore')
                return b.decode('utf-8', errors='ignore')
            except Exception:
                pass
    return t

def cleaningData(df: pd.DataFrame,
                 log: bool = LOGGING_ENABLED,
                 logger: logging.Logger | None = None,
                 sample_n: int = LOG_SAMPLE_N) -> pd.DataFrame:
    if logger is None:
        logger = logging.getLogger("lab6")
    if log:
        logSection(logger, "LIMPIEZA")
        logger.info(f"Filas: {len(df)} | nulos(text): {df['text'].isna().sum()}")

    has_id = 'id' in df.columns
    if log:
        sample = df.sample(min(sample_n, len(df)), random_state=RANDOM_STATE)[['text']].copy()
        if has_id:
            sample = df[['id','text']].loc[sample.index].copy()

    s = df['text'].fillna('').astype(str).apply(html.unescape)
    s = s.apply(autoFixEncoding)
    s = s.apply(lambda t: unicodedata.normalize("NFKC", t))
    if REMOVE_URLS:       s = s.str.replace(r'(https?://\S+|www\.\S+)', ' ', regex=True)
    if REMOVE_MENTIONS:   s = s.str.replace(r'@\w+', ' ', regex=True)
    if REMOVE_HASHTAGS:   s = s.str.replace(r'#\w+', ' ', regex=True)
    if REMOVE_EMOJIS:     s = s.str.replace(r'[\U0001F300-\U0001FAFF\u2600-\u26FF]+', ' ', regex=True)
    if REMOVE_PUNCT:      s = s.str.replace(r"[^\w\s]", " ", regex=True)
    s = s.str.replace(r"_+", " ", regex=True)
    try:
        if True: s = s.apply(unidecode)
    except Exception:
        pass
    s = s.str.replace(r"[^\x00-\x7F]+", " ", regex=True) if False else s
    if LOWERCASE:         s = s.str.lower()
    s = s.str.replace(r"\s+", " ", regex=True).str.strip()
    if REMOVE_STOPWORDS:
        stp = set(stopwords.words(STOPWORDS_LANG))
        s = s.apply(lambda t: " ".join(w for w in t.split() if w not in stp))

    out = df.copy(); out['text'] = s

    if log:
        lens_before = df['text'].fillna("").astype(str).str.len()
        lens_after  = out['text'].str.len()
        red_mean = (1 - (lens_after.mean() / (lens_before.replace(0,1)).mean())) * 100
        logger.info(f"Longitud media antes: {lens_before.mean():.1f} | después: {lens_after.mean():.1f} | reducción≈{red_mean:.1f}%")
        logger.info("Muestras de limpieza (antes -> después):")
        for idx in sample.index:
            orig = df.loc[idx, 'text']; clean = out.loc[idx, 'text']
            pre = (orig[:180] + "…") if len(orig) > 180 else orig
            pos = (clean[:180] + "…") if len(clean) > 180 else clean
            if has_id: logger.info(f"[id={df.loc[idx,'id']}]")
            logger.info(f"  BEFORE: {pre}"); logger.info(f"  AFTER : {pos}")
    return out


# ======================
# 3) CARGA DEL DATASET
# ======================
def loadDataset(dataDir: str = DATA_DIR,
                rawFile: str = RAW_FILE,
                cleanFile: str = CLEAN_FILE,
                useCleaned: bool = True,
                doCleaning: bool = False,
                saveCleaned: bool = False,
                cleaningFn=cleaningData) -> dict:
    clean_path = os.path.join(dataDir, cleanFile)
    raw_path   = os.path.join(dataDir, rawFile)
    artifacts, did_clean = [], False

    if useCleaned and os.path.exists(clean_path):
        df = pd.read_csv(clean_path); used = clean_path
    else:
        df = pd.read_csv(raw_path); used = raw_path
        if doCleaning and (cleaningFn is not None):
            df = cleaningFn(df); did_clean = True
            if saveCleaned:
                ensureDir(dataDir); df.to_csv(clean_path, index=False); artifacts.append(clean_path)

    if 'text' not in df.columns or 'target' not in df.columns:
        raise ValueError("El CSV debe contener 'text' y 'target'.")
    df['text'] = df['text'].fillna('')
    df['target'] = df['target'].astype(int)
    return {'df': df, 'usedFile': used, 'didCleaning': did_clean, 'artifacts': artifacts}


# ======================
# 4) UTILS DE PRINT
# ======================
def printTable(df: pd.DataFrame, title: str = "", n: int = 20) -> None:
    if title: print(f"\n=== {title} ===")
    print(tabulate(df.head(n), headers='keys', tablefmt='github', showindex=False))


# ======================
# 5) FRECUENCIAS
# ======================
def computeFrequencies(df: pd.DataFrame, minDf: int = VEC_MIN_DF, topK: int = TOPK_FREQ,
                       verbose: bool = True, log: bool = LOGGING_ENABLED, logger=None):
    if logger is None: logger = logging.getLogger("lab6")
    if log: logSection(logger, "FRECUENCIAS (unigramas)")
    cv = CountVectorizer(ngram_range=(1,1), min_df=minDf)
    X = cv.fit_transform(df['text']); vocab = cv.get_feature_names_out()
    if log: logger.info(f"Vocabulario (uni): {len(vocab)} | min_df={minDf}")

    mask_pos = (df['target']==1).values; mask_neg = ~mask_pos
    counts_pos = X[mask_pos].sum(axis=0).A1
    counts_neg = X[mask_neg].sum(axis=0).A1
    counts_all = X.sum(axis=0).A1

    freq_df = pd.DataFrame({'token': vocab,'pos':counts_pos,'neg':counts_neg,'total':counts_all})
    freq_df['lift_pos'] = (freq_df['pos']+1)/(freq_df['neg']+1)
    freq_df['lift_neg'] = (freq_df['neg']+1)/(freq_df['pos']+1)

    top_pos = freq_df.sort_values(['pos','lift_pos'], ascending=False).head(topK)
    top_neg = freq_df.sort_values(['neg','lift_neg'], ascending=False).head(topK)
    intersect = freq_df[(freq_df['pos']>0)&(freq_df['neg']>0)].sort_values('total', ascending=False).head(topK)

    if log:
        logger.info(f"TOP{topK} pos: {', '.join(top_pos['token'].tolist()[:15])}…")
        logger.info(f"TOP{topK} neg: {', '.join(top_neg['token'].tolist()[:15])}…")
        logger.info(f"Intersección TOP{topK}: {', '.join(intersect['token'].tolist()[:15])}…")

    if verbose:
        printTable(top_pos[['token','pos','lift_pos']], "Top en DESASTRES (pos)", n=topK)
        printTable(top_neg[['token','neg','lift_neg']], "Top en NO DESASTRES (neg)", n=topK)
        printTable(intersect[['token','pos','neg','total']], "Términos en ambas categorías", n=topK)

    return {'params': {'minDf': minDf, 'topK': topK},
            'freqDf': freq_df, 'topPos': top_pos, 'topNeg': top_neg,
            'intersect': intersect, 'vectorizer': cv}


# ======================
# 6) N-GRAMAS
# ======================
def analyzeNgrams(df: pd.DataFrame, nMax: int = NGRAM_MAX, minDf: int = VEC_MIN_DF,
                  topK: int = TOPK_NGRAMS, verbose: bool = True):
    cv = CountVectorizer(ngram_range=(1, nMax), min_df=minDf)
    X = cv.fit_transform(df['text']); vocab = cv.get_feature_names_out()
    mask_pos = (df['target'] == 1).values; mask_neg = (df['target'] == 0).values
    pos_n = X[mask_pos].sum(axis=0).A1; neg_n = X[mask_neg].sum(axis=0).A1
    total = pos_n + neg_n

    df_all = pd.DataFrame({'token': vocab, 'pos': pos_n, 'neg': neg_n, 'total': total})
    df_all['n'] = df_all['token'].str.count(' ') + 1

    byN, tops = {}, {}
    for k in range(2, nMax+1):
        filt = df_all[df_all['n'] == k].sort_values('total', ascending=False)
        tops[k] = filt.head(topK).copy(); byN[k] = filt
        if verbose: printTable(tops[k][['token','pos','neg','total']], f"Top {k}-gramas", n=topK)
    return {'params': {'nMax': nMax, 'minDf': minDf, 'topK': topK}, 'byN': byN, 'tops': tops, 'vectorizer': cv}


# ======================
# 7) VISUALIZACIONES
# ======================
def generateWordClouds(topPos: pd.DataFrame, topNeg: pd.DataFrame,
                       saveFigures: bool = SAVE_FIGS, imagesDir: str = IMAGES_DIR, prefix: str = "wc_"):
    artifacts = [];  ensureDir(imagesDir) if saveFigures else None
    # POS
    freq_pos = dict(zip(topPos['token'], topPos['pos']))
    plt.figure(figsize=(8,5))
    wc_pos = WordCloud(width=900, height=400, background_color='white').generate_from_frequencies(freq_pos)
    plt.imshow(wc_pos); plt.axis('off'); plt.title('Desastres (Top Unigramas)')
    if saveFigures:
        path = os.path.join(imagesDir, f"{prefix}desastres.png")
        plt.savefig(path, bbox_inches='tight', dpi=150); artifacts.append(path)
    plt.show()
    # NEG
    freq_neg = dict(zip(topNeg['token'], topNeg['neg']))
    plt.figure(figsize=(8,5))
    wc_neg = WordCloud(width=900, height=400, background_color='white').generate_from_frequencies(freq_neg)
    plt.imshow(wc_neg); plt.axis('off'); plt.title('No desastres (Top Unigramas)')
    if saveFigures:
        path = os.path.join(imagesDir, f"{prefix}no_desastres.png")
        plt.savefig(path, bbox_inches='tight', dpi=150); artifacts.append(path)
    plt.show()
    return {'artifacts': artifacts, 'figures': ['wc_pos','wc_neg']}

def plotTopHistograms(topPos: pd.DataFrame, topNeg: pd.DataFrame,
                      saveFigures: bool = SAVE_FIGS, imagesDir: str = IMAGES_DIR, prefix: str = "hist_"):
    artifacts = []; ensureDir(imagesDir) if saveFigures else None
    # DESASTRES
    tp = topPos.sort_values('pos', ascending=False).head(20)
    plt.figure(figsize=(10,5))
    plt.bar(tp['token'], tp['pos']); plt.xticks(rotation=70, ha='right')
    plt.title('Top-20 palabras en DESASTRES'); plt.ylabel('Frecuencia'); plt.xlabel('Término')
    plt.tight_layout()
    if saveFigures:
        path = os.path.join(imagesDir, f"{prefix}desastres.png")
        plt.savefig(path, bbox_inches='tight', dpi=150); artifacts.append(path)
    plt.show()
    # NO DESASTRES
    tn = topNeg.sort_values('neg', ascending=False).head(20)
    plt.figure(figsize=(10,5))
    plt.bar(tn['token'], tn['neg']); plt.xticks(rotation=70, ha='right')
    plt.title('Top-20 palabras en NO DESASTRES'); plt.ylabel('Frecuencia'); plt.xlabel('Término')
    plt.tight_layout()
    if saveFigures:
        path = os.path.join(imagesDir, f"{prefix}no_desastres.png")
        plt.savefig(path, bbox_inches='tight', dpi=150); artifacts.append(path)
    plt.show()
    return {'artifacts': artifacts}


# ======================
# 8) MODELADO CLÁSICO (baseline)
# ======================
def saveBaselineModel(pipeline, modelsDir: str = MODELS_DIR, filename: str = BASELINE_MODEL_FILE) -> str:
    ensureDir(modelsDir); path = os.path.join(modelsDir, filename); joblib_dump(pipeline, path); return path

def loadBaselineModel(path: str = BASELINE_LOAD_PATH):
    return joblib_load(path)

def trainEvaluateModels(df: pd.DataFrame, testSize: float = TEST_SIZE, randomState: int = RANDOM_STATE,
                        calibrateSVC: bool = CALIBRATE_SVC, saveFigures: bool = SAVE_FIGS,
                        imagesDir: str = IMAGES_DIR, prefix: str = "cm_", verbose: bool = True,
                        log: bool = LOGGING_ENABLED, logger=None):
    if logger is None: logger = logging.getLogger("lab6")
    if log:
        logSection(logger, "MODELOS (baseline)")
        logger.info(f"Split test={testSize} | seed={randomState} | calibrateSVC={calibrateSVC}")

    X_text = df['text'].values; y = df['target'].values
    Xtr, Xte, ytr, yte = train_test_split(X_text, y, test_size=testSize,
                                          random_state=randomState, stratify=y)
    if log:
        logger.info(f"Train: {len(Xtr)} | Test: {len(Xte)} | Pos(train)={int(ytr.sum())} | Pos(test)={int(yte.sum())}")

    vec_uni   = TfidfVectorizer(ngram_range=(1,1), min_df=VEC_MIN_DF)
    vec_unibi = TfidfVectorizer(ngram_range=(1,NGRAM_MAX), min_df=VEC_MIN_DF)
    vec_char  = TfidfVectorizer(analyzer='char', ngram_range=CHAR_NGRAM_RANGE)

    configs = {'tfidf_uni': vec_uni, 'tfidf_unibi': vec_unibi, 'tfidf_char': vec_char}
    clfs = {'LogReg': LogisticRegression(max_iter=200, class_weight='balanced'),
            'NB': MultinomialNB(),
            'LinSVC': LinearSVC(class_weight='balanced')}

    resultados, best, best_pipeline, best_pred = [], None, None, None

    for cfg_name, vec in configs.items():
        for clf_name, clf in clfs.items():
            clf_model = CalibratedClassifierCV(LinearSVC(class_weight='balanced'), cv=5) \
                        if (clf_name=='LinSVC' and calibrateSVC) else clf
            pipe = Pipeline([('vec', vec), ('clf', clf_model)])
            pipe.fit(Xtr, ytr)
            pred = pipe.predict(Xte)
            f1 = f1_score(yte, pred); acc = accuracy_score(yte, pred)
            resultados.append({'vectorizer': cfg_name, 'model': clf_name, 'f1': f1, 'acc': acc})

            if log: logger.info(f"[{cfg_name}+{clf_name}] F1={f1:.3f} ACC={acc:.3f}")
            if verbose:
                print(f"\n[{cfg_name} + {clf_name}]  F1={f1:.3f}  ACC={acc:.3f}")
                print(classification_report(yte, pred, digits=3))

            if (best is None) or (f1 > (best['f1'] if best else -1)):
                best = {'vectorizer': cfg_name, 'model': clf_name, 'f1': f1, 'acc': acc}
                best_pipeline, best_pred = pipe, pred

    results_df = pd.DataFrame(resultados).sort_values('f1', ascending=False)
    if verbose: printTable(results_df, "Resumen modelos (ordenado por F1)", n=len(results_df))
    if log and best: logger.info(f"MEJOR -> {best['vectorizer']} + {best['model']} | F1={best['f1']:.3f} ACC={best['acc']:.3f}")

    rep = classification_report(yte, best_pred, digits=3, output_dict=True)
    cm = confusion_matrix(yte, best_pred)
    if log:
        tn, fp, fn, tp = cm.ravel().tolist()
        logger.info(f"CM: tn={tn} fp={fp} fn={fn} tp={tp}")

    artifacts = []
    if saveFigures:
        ensureDir(imagesDir)
        plt.figure(figsize=(4,4))
        plt.imshow(cm)
        plt.title('Matriz de confusión (mejor modelo)')
        plt.xlabel('Predicción'); plt.ylabel('Real')
        for (i, j), v in np.ndenumerate(cm):
            plt.text(j, i, str(v), ha='center', va='center')
        path = os.path.join(imagesDir, f"{prefix}{best['vectorizer']}_{best['model']}.png")
        plt.savefig(path, bbox_inches='tight', dpi=150); artifacts.append(path)
        plt.show()
        if log: logger.info(f"Guardada figura CM en: {path}")

    return {'params': {'testSize': testSize, 'randomState': randomState, 'calibrateSVC': calibrateSVC},
            'resultsDf': results_df, 'best': best, 'bestPipeline': best_pipeline,
            'test': {'Xtest': Xte, 'y_true': y, 'y_pred': best_pred, 'report': rep, 'cm': cm},
            'artifacts': artifacts}

def optimizeThreshold(pipeline: Pipeline, Xtest: np.ndarray, ytest: np.ndarray,
                      start: float = 0.30, end: float = 0.70, step: float = 0.01,
                      verbose: bool = True):
    if not hasattr(pipeline.named_steps['clf'], "predict_proba"):
        raise ValueError("El clasificador no expone predict_proba.")
    probs = pipeline.predict_proba(Xtest)[:,1]
    ths = np.arange(start, end + 1e-9, step)
    rows = []
    for th in ths:
        pred = (probs >= th).astype(int)
        rows.append({'th': round(th,3), 'f1': f1_score(ytest, pred), 'acc': accuracy_score(ytest, pred)})
    scores_df = pd.DataFrame(rows).sort_values('f1', ascending=False)
    if verbose: printTable(scores_df.head(10), "Top umbrales por F1", n=10)
    return {'bestTh': float(scores_df.iloc[0]['th']), 'scoresDf': scores_df}

def classifyTweet(pipeline: Pipeline, tweet: str, threshold: float = 0.50) -> dict:
    label = int(pipeline.predict([tweet])[0]); prob = None
    if hasattr(pipeline.named_steps['clf'], "predict_proba"):
        prob = float(pipeline.predict_proba([tweet])[0][1]); label = int(prob >= threshold)
    return {'text': tweet, 'label': label, 'probDesastre': prob, 'threshold': threshold}


# ======================
# 9) BERT + CNN (PyTorch)
# ======================
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len: int):
        self.texts = list(texts)
        self.labels = torch.tensor(labels, dtype=torch.float32)
        self.tok = tokenizer
        self.max_len = max_len
    def __len__(self): return len(self.texts)
    def __getitem__(self, idx):
        enc = self.tok(self.texts[idx],
                       truncation=True, padding='max_length',
                       max_length=self.max_len, return_tensors='pt')
        item = {
            'input_ids': enc['input_ids'].squeeze(0),
            'attention_mask': enc['attention_mask'].squeeze(0),
            'labels': self.labels[idx]
        }
        return item

class BertCnnClassifier(nn.Module):
    def __init__(self, model_name: str, filters: int, kernel_size: int, dropout: float, trainable_encoder: bool):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        for p in self.encoder.parameters():
            p.requires_grad = bool(trainable_encoder)
        hidden = self.encoder.config.hidden_size  # e.g., 768
        # Conv1d: entrada (B, C=hidden, L). Usamos padding='same' con cálculo manual
        self.conv = nn.Conv1d(in_channels=hidden, out_channels=filters, kernel_size=kernel_size, padding=kernel_size//2)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(filters, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden = outputs.last_hidden_state  # (B, L, H)
        x = last_hidden.transpose(1, 2)          # (B, H, L)
        x = torch.relu(self.conv(x))             # (B, F, L)
        x = torch.max(x, dim=2).values           # GlobalMaxPool1D -> (B, F)
        x = self.dropout(x)
        logits = self.classifier(x).squeeze(-1)  # (B,)
        return logits

def saveBertArtifacts(tokenizer, model,
                      modelsDir: str = MODELS_DIR,
                      artifactDir: str = BERT_ARTIFACT_DIR,
                      modelSub: str = BERT_MODEL_SUBDIR,
                      tokSub: str = BERT_TOKENIZER_SUBDIR,
                      meta_extra: dict | None = None) -> dict:
    base = os.path.join(modelsDir, artifactDir)
    tok_dir = os.path.join(base, tokSub)
    mdl_dir = os.path.join(base, modelSub)
    ensureDir(tok_dir); ensureDir(mdl_dir)

    # Guardar tokenizer
    tokenizer.save_pretrained(tok_dir)

    # Guardar pesos del modelo (state_dict) + meta para reconstrucción
    state_path = os.path.join(mdl_dir, "model_state.pt")
    torch.save(model.state_dict(), state_path)

    meta = {
        "bert_name": model.encoder.name_or_path if hasattr(model.encoder, "name_or_path") else BERT_MODEL_NAME,
        "filters": model.conv.out_channels,
        "kernel_size": model.conv.kernel_size[0],
        "dropout": model.dropout.p,
        "trainable_encoder": any(p.requires_grad for p in model.encoder.parameters())
    }
    if meta_extra:
        meta.update(meta_extra)
    with open(os.path.join(mdl_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    return {'tokenizer_dir': tok_dir, 'model_dir': mdl_dir}

def loadBertArtifacts(tokenizerDir: str = BERT_TOKENIZER_LOAD_PATH,
                      modelDir: str = BERT_MODEL_LOAD_PATH):
    tok = AutoTokenizer.from_pretrained(tokenizerDir)
    with open(os.path.join(modelDir, "meta.json"), "r", encoding="utf-8") as f:
        meta = json.load(f)
    mdl = BertCnnClassifier(
        model_name=meta["bert_name"],
        filters=int(meta["filters"]),
        kernel_size=int(meta["kernel_size"]),
        dropout=float(meta["dropout"]),
        trainable_encoder=bool(meta["trainable_encoder"])
    )
    state = torch.load(os.path.join(modelDir, "model_state.pt"), map_location=DEVICE)
    mdl.load_state_dict(state)
    mdl.to(DEVICE)
    mdl.eval()
    return tok, mdl

def trainEvaluateBertCnn(df: pd.DataFrame,
                         testSize: float = TEST_SIZE,
                         randomState: int = RANDOM_STATE,
                         max_len: int = BERT_MAX_LEN,
                         batch_size: int = BERT_BATCH,
                         epochs: int = BERT_EPOCHS,
                         lr: float = BERT_LR,
                         filters: int = CNN_FILTERS,
                         kernel_size: int = CNN_KERNEL_SIZE,
                         dropout: float = CNN_DROPOUT,
                         bert_name: str = BERT_MODEL_NAME,
                         trainable_bert: bool = BERT_TRAINABLE,
                         threshold: float = BERT_THRESHOLD):

    logger = logging.getLogger("lab6")
    if LOGGING_ENABLED:
        logSection(logger, "BERT+CNN (PyTorch)")
        logger.info(f"Modelo={bert_name} | max_len={max_len} | epochs={epochs} "
                    f"| trainable_bert={trainable_bert} | batch={batch_size} | lr={lr} | device={DEVICE}")

    # Split
    X_text = df['text'].values
    y = df['target'].values.astype('float32')
    Xtr, Xte, ytr, yte = train_test_split(X_text, y, test_size=testSize,
                                          random_state=randomState, stratify=y)

    # Tokenizer y datasets
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
    tr_ds = TextDataset(Xtr, ytr, tokenizer, max_len)
    te_ds = TextDataset(Xte, yte, tokenizer, max_len)

    # Validación interna (10% de train)
    val_size = max(1, int(0.1 * len(tr_ds)))
    train_size = len(tr_ds) - val_size
    tr_ds, va_ds = torch.utils.data.random_split(tr_ds, [train_size, val_size],
                                                 generator=torch.Generator().manual_seed(randomState))

    tr_dl = DataLoader(tr_ds, batch_size=batch_size, shuffle=True)
    va_dl = DataLoader(va_ds, batch_size=batch_size, shuffle=False)
    te_dl = DataLoader(te_ds, batch_size=batch_size, shuffle=False)

    # Modelo
    model = BertCnnClassifier(bert_name, filters, kernel_size, dropout, trainable_bert).to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.RMSprop(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)

    best_val = float('inf')
    patience = EARLY_STOP_PATIENCE
    patience_ctr = 0
    best_state = None

    for ep in range(1, epochs+1):
        model.train()
        total_loss = 0.0
        for batch in tr_dl:
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)

            optimizer.zero_grad()
            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * input_ids.size(0)

        # Validación
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch in va_dl:
                input_ids = batch['input_ids'].to(DEVICE)
                attention_mask = batch['attention_mask'].to(DEVICE)
                labels = batch['labels'].to(DEVICE)
                logits = model(input_ids, attention_mask)
                loss = criterion(logits, labels)
                val_loss += loss.item() * input_ids.size(0)

        tr_loss = total_loss / len(tr_ds)
        va_loss = val_loss / len(va_ds)
        if LOGGING_ENABLED:
            logger.info(f"Epoch {ep}/{epochs} | train_loss={tr_loss:.4f} | val_loss={va_loss:.4f}")

        if va_loss < best_val - 1e-4:
            best_val = va_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            patience_ctr = 0
        else:
            patience_ctr += 1
            if patience_ctr >= patience:
                if LOGGING_ENABLED: logger.info("Early stopping por paciencia alcanzada.")
                break

    if best_state is not None:
        model.load_state_dict(best_state)
        model.to(DEVICE)
        model.eval()

    # Evaluación en test
    probs_list, y_true = [], []
    with torch.no_grad():
        for batch in te_dl:
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)
            logits = model(input_ids, attention_mask)
            probs = torch.sigmoid(logits)
            probs_list.extend(probs.cpu().numpy().tolist())
            y_true.extend(labels.cpu().numpy().tolist())

    probs = np.array(probs_list)
    y_pred = (probs >= threshold).astype(int)

    f1 = f1_score(y_true, y_pred); acc = accuracy_score(y_true, y_pred)
    print(f"\n[BERT+CNN] F1={f1:.3f}  ACC={acc:.3f}")
    print(classification_report(y_true, y_pred, digits=3))

    if LOGGING_ENABLED:
        logger.info(f"[BERT] F1={f1:.3f} ACC={acc:.3f} | threshold={threshold}")
        cm = confusion_matrix(y_true, y_pred)
        try:
            tn, fp, fn, tp = cm.ravel().tolist()
            logger.info(f"[BERT] CM tn={tn} fp={fp} fn={fn} tp={tp}")
        except Exception:
            logger.info(f"[BERT] CM=\n{cm}")

    history = {"best_val_loss": best_val}
    return {
        'params': {
            'bert_name': bert_name, 'max_len': max_len, 'batch': batch_size,
            'epochs': epochs, 'lr': lr, 'filters': filters, 'kernel': kernel_size,
            'dropout': dropout, 'trainable_bert': trainable_bert, 'threshold': threshold
        },
        'tokenizer': tokenizer,
        'model': model,
        'test': {
            'Xtest': Xte, 'y_true': np.array(y_true), 'probs': probs, 'y_pred': y_pred,
            'report': classification_report(y_true, y_pred, digits=3, output_dict=True),
            'cm': confusion_matrix(y_true, y_pred)
        },
        'history': history
    }

def classifyTweetBert(tokenizer, model, tweet: str, threshold: float = BERT_THRESHOLD, max_len: int = BERT_MAX_LEN):
    model.eval()
    enc = tokenizer(tweet, truncation=True, padding='max_length', max_length=max_len, return_tensors='pt')
    with torch.no_grad():
        logits = model(enc['input_ids'].to(DEVICE), enc['attention_mask'].to(DEVICE))
        prob = torch.sigmoid(logits).item()
    label = int(prob >= threshold)
    return {'text': tweet, 'label': label, 'probDesastre': float(prob), 'threshold': threshold}


# ======================
# 10) CLASIFICADOR UNIFICADO (disco/memoria)
# ======================
def predictWithModel(text: str,
                     modelKind: str = "baseline",          # "baseline" | "bert"
                     useSaved: bool = False,
                     threshold: float = 0.50,
                     pipeline=None,                         # baseline en memoria
                     tokenizer=None, model=None,            # bert (PyTorch) en memoria
                     paths: dict = None                     # {'baseline':...} o {'tokenizer':..., 'model':...}
                     ) -> dict:
    if modelKind == "baseline":
        if useSaved:
            pth = (paths or {}).get('baseline', BASELINE_LOAD_PATH)
            pipe = loadBaselineModel(pth)
            res = classifyTweet(pipe, text, threshold)
            res.update({'modelKind': 'baseline', 'source': 'disk', 'path': pth})
            return res
        else:
            if pipeline is None:
                raise ValueError("Se requiere 'pipeline' en memoria para baseline.")
            res = classifyTweet(pipeline, text, threshold)
            res.update({'modelKind': 'baseline', 'source': 'memory'})
            return res

    elif modelKind == "bert":
        if useSaved:
            tok_dir = (paths or {}).get('tokenizer', BERT_TOKENIZER_LOAD_PATH)
            mdl_dir = (paths or {}).get('model', BERT_MODEL_LOAD_PATH)
            tok, mdl = loadBertArtifacts(tok_dir, mdl_dir)
            res = classifyTweetBert(tok, mdl, text, threshold, max_len=BERT_MAX_LEN)
            res.update({'modelKind': 'bert', 'source': 'disk',
                        'tokenizer_path': tok_dir, 'model_path': mdl_dir})
            return res
        else:
            if (tokenizer is None) or (model is None):
                raise ValueError("Se requieren 'tokenizer' y 'model' en memoria para BERT.")
            res = classifyTweetBert(tokenizer, model, text, threshold, max_len=BERT_MAX_LEN)
            res.update({'modelKind': 'bert', 'source': 'memory'})
            return res
    else:
        raise ValueError("modelKind inválido. Use 'baseline' o 'bert'.")


# ======================
# 11) DRIVER
# ======================
LOGGER = initLogger("lab6") if LOGGING_ENABLED else None
if LOGGING_ENABLED:
    logSection(LOGGER, "CONFIG")
    LOGGER.info(f"DATA_DIR={DATA_DIR} RAW_FILE={RAW_FILE} CLEAN_FILE={CLEAN_FILE}")
    LOGGER.info(f"USE_CLEANED={USE_CLEANED} DO_CLEANING={DO_CLEANING} SAVE_CLEANED={SAVE_CLEANED}")
    LOGGER.info(f"RUN_FREQUENCIES={RUN_FREQUENCIES} RUN_NGRAMS={RUN_NGRAMS} RUN_PLOTS={RUN_PLOTS} "
                f"RUN_MODELS={RUN_MODELS} RUN_THRESHOLD={RUN_THRESHOLD} RUN_BERTCNN={RUN_BERTCNN}")
    LOGGER.info(f"Models dir: {MODELS_DIR} | Logs: {os.path.join(LOG_DIR, LOG_FILE_NAME)}")
    LOGGER.info(f"PyTorch device: {DEVICE}")

pack = loadDataset(dataDir=DATA_DIR, rawFile=RAW_FILE, cleanFile=CLEAN_FILE,
                   useCleaned=USE_CLEANED, doCleaning=DO_CLEANING,
                   saveCleaned=SAVE_CLEANED, cleaningFn=cleaningData)

data = pack['df']
print(f"Cargado: {pack['usedFile']} | didCleaning={pack['didCleaning']} | rows={len(data)}")
assert {'text','target'}.issubset(set(data.columns)), "Faltan columnas requeridas."
data['text'] = data['text'].fillna('')

# ---- Frecuencias / n-gramas / plots
freq_out = ngrams_out = plots_wc = plots_hist = model_out = th_out = None

if RUN_FREQUENCIES:
    freq_out = computeFrequencies(data, minDf=VEC_MIN_DF, topK=TOPK_FREQ,
                                  verbose=True, log=LOGGING_ENABLED, logger=LOGGER)

if RUN_NGRAMS:
    ngrams_out = analyzeNgrams(data, nMax=NGRAM_MAX, minDf=VEC_MIN_DF,
                               topK=TOPK_NGRAMS, verbose=True)

if RUN_PLOTS and freq_out is not None:
    plots_wc  = generateWordClouds(freq_out['topPos'], freq_out['topNeg'],
                                   saveFigures=SAVE_FIGS, imagesDir=IMAGES_DIR, prefix="wc_")
    plots_hist= plotTopHistograms(freq_out['topPos'], freq_out['topNeg'],
                                  saveFigures=SAVE_FIGS, imagesDir=IMAGES_DIR, prefix="hist_")

# --- Baseline ---
if RUN_MODELS:
    model_out = trainEvaluateModels(data, testSize=TEST_SIZE, randomState=RANDOM_STATE,
                                    calibrateSVC=CALIBRATE_SVC, saveFigures=SAVE_FIGS,
                                    imagesDir=IMAGES_DIR, prefix="cm_", verbose=True,
                                    log=LOGGING_ENABLED, logger=LOGGER)

    if SAVE_BASELINE_MODEL and model_out and model_out.get('bestPipeline'):
        saved_path = saveBaselineModel(model_out['bestPipeline'])
        print(f"[baseline] Guardado en: {saved_path}")
        if LOGGING_ENABLED and LOGGER:
            LOGGER.info(f"[baseline] Guardado en: {saved_path}")

    neg = "Great day at the park with friends, coffee and music."
    pos = "Breaking: flash flooding downtown, roads closed and rescue teams deployed."
    print("\n[BASELINE - memoria]")
    print("NO desastre →", predictWithModel(neg, modelKind="baseline",
                                           useSaved=False, threshold=0.5,
                                           pipeline=model_out['bestPipeline']))
    print("SÍ desastre →", predictWithModel(pos, modelKind="baseline",
                                           useSaved=False, threshold=0.5,
                                           pipeline=model_out['bestPipeline']))

    print("\n[BASELINE - disco]")
    print("NO desastre →", predictWithModel(neg, modelKind="baseline",
                                           useSaved=True, threshold=0.5,
                                           paths={'baseline': BASELINE_LOAD_PATH}))
    print("SÍ desastre →", predictWithModel(pos, modelKind="baseline",
                                           useSaved=True, threshold=0.5,
                                           paths={'baseline': BASELINE_LOAD_PATH}))

# --- BERT + CNN (PyTorch) ---
if RUN_BERTCNN:
    bert_out = trainEvaluateBertCnn(data,
                                    testSize=TEST_SIZE, randomState=RANDOM_STATE,
                                    max_len=BERT_MAX_LEN, batch_size=BERT_BATCH,
                                    epochs=BERT_EPOCHS, lr=BERT_LR,
                                    filters=CNN_FILTERS, kernel_size=CNN_KERNEL_SIZE,
                                    dropout=CNN_DROPOUT, bert_name=BERT_MODEL_NAME,
                                    trainable_bert=BERT_TRAINABLE, threshold=BERT_THRESHOLD)

    if SAVE_BERT_MODEL and bert_out:
        arts = saveBertArtifacts(bert_out['tokenizer'], bert_out['model'],
                                 meta_extra={'threshold': BERT_THRESHOLD})
        print(f"[bert] Guardado tokenizer en: {arts['tokenizer_dir']}")
        print(f"[bert] Guardado modelo en:    {arts['model_dir']}")
        if LOGGING_ENABLED and LOGGER:
            LOGGER.info(f"[bert] Guardado tokenizer en: {arts['tokenizer_dir']}")
            LOGGER.info(f"[bert] Guardado modelo en:    {arts['model_dir']}")

    neg = "Great day at the park with friends, coffee and music."
    pos = "Breaking: flash flooding downtown, roads closed and rescue teams deployed."

    print("\n[BERT - memoria]")
    print("NO desastre →", predictWithModel(neg, modelKind="bert",
                                           useSaved=False, threshold=BERT_THRESHOLD,
                                           tokenizer=bert_out['tokenizer'], model=bert_out['model']))
    print("SÍ desastre →", predictWithModel(pos, modelKind="bert",
                                           useSaved=False, threshold=BERT_THRESHOLD,
                                           tokenizer=bert_out['tokenizer'], model=bert_out['model']))

    print("\n[BERT - disco]")
    print("NO desastre →", predictWithModel(neg, modelKind="bert",
                                           useSaved=True, threshold=BERT_THRESHOLD,
                                           paths={'tokenizer': BERT_TOKENIZER_LOAD_PATH,
                                                  'model': BERT_MODEL_LOAD_PATH}))
    print("SÍ desastre →", predictWithModel(pos, modelKind="bert",
                                           useSaved=True, threshold=BERT_THRESHOLD,
                                           paths={'tokenizer': BERT_TOKENIZER_LOAD_PATH,
                                                  'model': BERT_MODEL_LOAD_PATH}))

# --- Cierre ---
if LOGGING_ENABLED and LOGGER:
    logSection(LOGGER, "FIN DE EJECUCIÓN")
    LOGGER.info("Pipeline completado correctamente.")
    for h in LOGGER.handlers:
        try: h.flush()
        except Exception: pass
print(f"Logs en: {os.path.join(LOG_DIR, LOG_FILE_NAME)}")
