import os
import pandas as pd
import unidecode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directorio del script
OUT_BASE = os.path.join(BASE_DIR, "data")
CACHE_BASE = os.path.join(BASE_DIR, "cache")
CACHE_CSV_BASE = "cache_csv_base.txt"


# Datos de departamentos
departamentos_data = [
    (1, "Guatemala"),
    (2, "El Progreso"),
    (3, "Sacatepéquez"),
    (4, "Chimaltenango"),
    (5, "Escuintla"),
    (6, "Santa Rosa"),
    (7, "Sololá"),
    (8, "Totonicapán"),
    (9, "Quetzaltenango"),
    (10, "Suchitepéquez"),
    (11, "Retalhuleu"),
    (12, "San Marcos"),
    (13, "Huehuetenango"),
    (14, "Quiché"),
    (15, "Baja Verapaz"),
    (16, "Alta Verapaz"),
    (17, "Petén"),
    (18, "Izabal"),
    (19, "Zacapa"),
    (20, "Chiquimula"),
    (21, "Jalapa"),
    (22, "Jutiapa")
]

# Datos de municipios
municipios_data = [
    (101,"Guatemala"), (102,"Santa Catarina Pinula"), (103,"San José Pinula"),
    (104,"San José del Golfo"), (105,"Palencia"), (106,"Chinautla"), (107,"San Pedro Ayampuc"),
    (108,"Mixco"), (109,"San Pedro Sacatepéquez"), (110,"San Juan Sacatepéquez"), (111,"San Raymundo"),
    (112,"Chuarrancho"), (113,"Fraijanes"), (114,"Amatitlán"), (115,"Villa Nueva"),
    (116,"Villa Canales"), (117,"Petapa"), (201,"Guastatoya"), (202,"Morazán"),
    (203,"San Agustín Acasaguastlán"), (204,"San Cristóbal Acasaguastlán"), (205,"El Jícaro"),
    (206,"Sansare"), (207,"Sanarate"), (208,"San Antonio la Paz"), (301,"Antigua Guatemala"),
    (302,"Jocotenango"), (303,"Pastores"), (304,"Sumpango"), (305,"Santo Domingo Xenacoj"),
    (306,"Santiago Sacatepéquez"), (307,"San Bartolomé Milpas Altas"), (308,"San Lucas Sacatepéquez"),
    (309,"Santa Lucía Milpas Altas"), (310,"Magdalena Milpas Altas"), (311,"Santa María de Jesús"),
    (312,"Ciudad Vieja"), (313,"San Miguel Dueñas"), (314,"San Juan Alotenango"), (315,"San Antonio Aguas Calientes"),
    (316,"Santa Catarina Barahona"), (401,"Chimaltenango"), (402,"San José Poaquíl"),
    (403,"San Martín Jilotepeque"), (404,"Comalapa"), (405,"Santa Apolonia"), (406,"Tecpán Guatemala"),
    (407,"Patzún"), (408,"San Miguel Pochuta"), (409,"Patzicía"), (410,"Santa Cruz Balanyá"),
    (411,"Acatenango"), (412,"Yepocapa"), (413,"San Andrés Itzapa"), (414,"Parramos"),
    (415,"Zaragoza"), (416,"El Tejar"), (501,"Escuintla"), (502,"Santa Lucía Cotzumalguapa"),
    (503,"La Democracia"), (504,"Siquinalá"), (505,"Masagua"), (506,"Tiquisate"), (507,"La Gomera"),
    (508,"Guanagazapa"), (509,"San José"), (510,"Iztapa"), (511,"Palín"), (512,"San Vicente Pacaya"),
    (513,"Nueva Concepción"), (514,"Sipacate"), (601,"Cuilapa"), (602,"Barberena"),
    (603,"Santa Rosa de Lima"), (604,"Casillas"), (605,"San Rafael las Flores"), (606,"Oratorio"),
    (607,"San Juan Tecuaco"), (608,"Chiquimulilla"), (609,"Taxisco"), (610,"Santa María Ixhuatán"),
    (611,"Guazacapán"), (612,"Santa Cruz el Naranjo"), (613,"Pueblo Nuevo Viñas"), (614,"Nueva Santa Rosa"),
    (701,"Sololá"), (702,"San José Chacayá"), (703,"Santa María Visitación"), (704,"Santa Lucía Utatlán"),
    (705,"Nahualá"), (706,"Santa Catarina Ixtahuacán"), (707,"Santa Clara la Laguna"), (708,"Concepción"),
    (709,"San Andrés Semetabaj"), (710,"Panajachel"), (711,"Santa Catarina Palopó"), (712,"San Antonio Palopó"),
    (713,"San Lucas Tolimán"), (714,"Santa Cruz la Laguna"), (715,"San Pablo la Laguna"), (716,"San Marcos la Laguna"),
    (717,"San Juan la Laguna"), (718,"San Pedro la Laguna"), (719,"Santiago Atitlán"), (801,"Totonicapán"),
    (802,"San Cristóbal Totonicapán"), (803,"San Francisco el Alto"), (804,"San Andrés Xecul"),
    (805,"Momostenango"), (806,"Santa María Chiquimula"), (807,"Santa Lucía la Reforma"), (808,"San Bartolo Aguas Calientes"),
    (901,"Quetzaltenango"), (902,"Salcajá"), (903,"Olintepeque"), (904,"San Carlos Sija"), (905,"Sibilia"),
    (906,"Cabricán"), (907,"Cajolá"), (908,"San Miguel Siguilá"), (909,"San Juan Ostuncalco"), (910,"San Mateo"),
    (911,"Concepción Chiquirichapa"), (912,"San Martín Sacatepéquez"), (913,"Almolonga"), (914,"Cantel"),
    (915,"Huitán"), (916,"Zunil"), (917,"Colomba"), (918,"San Francisco la Unión"), (919,"El Palmar"),
    (920,"Coatepeque"), (921,"Génova"), (922,"Flores Costa Cuca"), (923,"La Esperanza"), (924,"Palestina de los Altos"),
    (1001,"Mazatenango"), (1002,"Cuyotenango"), (1003,"San Francisco Zapotitlán"), (1004,"San Bernardino"),
    (1005,"San José el Ídolo"), (1006,"Santo Domingo Suchitepéquez"), (1007,"San Lorenzo"), (1008,"Samayac"),
    (1009,"San Pablo Jocopilas"), (1010,"San Antonio Suchitepéquez"), (1011,"San Miguel Panán"), (1012,"San Gabriel"),
    (1013,"Chicacao"), (1014,"Patulul"), (1015,"Santa Bárbara"), (1016,"San Juan Bautista"), (1017,"Santo Tomas la Unión"),
    (1018,"Zunilito"), (1019,"Pueblo Nuevo"), (1020,"Río Bravo"), (1021,"San José La Máquina"), (1101,"Retalhuleu"),
    (1102,"San Sebastián"), (1103,"Santa Cruz Muluá"), (1104,"San Martín Zapotitlán"), (1105,"San Felipe Retalhuleu"),
    (1106,"San Andrés Villa Seca"), (1107,"Champerico"), (1108,"Nuevo San Carlos"), (1109,"El Asintal"),
    (1201,"San Marcos"), (1202,"San Pedro Sacatepéquez"), (1203,"San Antonio Sacatepéquez"), (1204,"Comitancillo"),
    (1205,"San Miguel Ixtahuacán"), (1206,"Concepción Tutuapa"), (1207,"Tacaná"), (1208,"Sibinal"), (1209,"Tajumulco"),
    (1210,"Tejutla"), (1211,"San Rafael Pie de la Cuesta"), (1212,"Nuevo Progreso"), (1213,"El Tumbador"), (1214,"El Rodeo"),
    (1215,"Malacatán"), (1216,"Catarina"), (1217,"Ayutla"), (1218,"Ocós"), (1219,"San Pablo"), (1220,"El Quetzal"),
    (1221,"La Reforma"), (1222,"Pajapita"), (1223,"Ixchiguán"), (1224,"San José Ojetenam"), (1225,"San Cristóbal Cucho"),
    (1226,"Sipacapa"), (1227,"Esquipulas Palo Gordo"), (1228,"Río Blanco"), (1229,"San Lorenzo"), (1230,"La Blanca"),
    (1301,"Huehuetenango"), (1302,"Chiantla"), (1303,"Malacatancito"), (1304,"Cuilco"), (1305,"Nentón"),
    (1306,"San Pedro Necta"), (1307,"Jacaltenango"), (1308,"San Pedro Soloma"), (1309,"San Ildefonso Ixtahuacán"),
    (1310,"Santa Bárbara"), (1311,"La Libertad"), (1312,"La Democracia"), (1313,"San Miguel Acatán"),
    (1314,"San Rafael La Independencia"), (1315,"Todos Santos Cuchumatán"), (1316,"San Juan Atitán"),
    (1317,"Santa Eulalia"), (1318,"San Mateo Ixtatán"), (1319,"Colotenango"), (1320,"San Sebastián Huehuetenango"),
    (1321,"Tectitán"), (1322,"Concepción Huista"), (1323,"San Juan Ixcoy"), (1324,"San Antonio Huista"),
    (1325,"San Sebastián Coatán"), (1326,"Barrillas"), (1327,"Aguacatán"), (1328,"San Rafael Petzal"),
    (1329,"San Gaspar Ixchil"), (1330,"Santiago Chimaltenango"), (1331,"Santa Ana Huista"), (1332,"Unión Cantinil"),
    (1333,"Petatán"), (1401,"Santa Cruz del Quiché"), (1402,"Chiché"), (1403,"Chinique"), (1404,"Zacualpa"),
    (1405,"Chajul"), (1406,"Chichicastenango"), (1407,"Patzité"), (1408,"San Antonio Ilotenango"), (1409,"San Pedro Jocopilas"),
    (1410,"Cunén"), (1411,"San Juan Cotzal"), (1412,"Joyabaj"), (1413,"Santa María Nebaj"), (1414,"San Andrés Sajcabajá"),
    (1415,"San Miguel Uspantán"), (1416,"Sacapulas"), (1417,"San Bartolomé Jocotenango"), (1418,"Canillá"),
    (1419,"Chicamán"), (1420,"Ixcán"), (1421,"Pachalum"), (1501,"Salamá"), (1502,"San Miguel Chicaj"),
    (1503,"Rabinal"), (1504,"Cubulco"), (1505,"Granados"), (1506,"El Chol"), (1507,"San Jerónimo"),
    (1508,"Purulhá"), (1601,"Cobán"), (1602,"Santa Cruz Verapaz"), (1603,"San Cristóbal Verapaz"),
    (1604,"Tactic"), (1605,"Tamahú"), (1606,"Tucurú"), (1607,"Panzós"), (1608,"Senahú"),
    (1609,"San Pedro Carchá"), (1610,"San Juan Chamelco"), (1611,"Lanquín"), (1612,"Cahabón"),
    (1613,"Chisec"), (1614,"Chahal"), (1615,"Fray Bartolomé de las Casas"), (1616,"Santa Catarina La Tinta"),
    (1617,"Raxruhá"), (1701,"Flores"), (1702,"San José"), (1703,"San Benito"), (1704,"San Andrés"),
    (1705,"La Libertad"), (1706,"San Francisco"), (1707,"Santa Ana"), (1708,"Dolores"), (1709,"San Luis"),
    (1710,"Sayaxché"), (1711,"Melchor de Mencos"), (1712,"Poptún"), (1713,"Las Cruces"), (1714,"El Chal"),
    (1801,"Puerto Barrios"), (1802,"Livingston"), (1803,"El Estor"), (1804,"Morales"), (1805,"Los Amates"),
    (1901,"Zacapa"), (1902,"Estanzuela"), (1903,"Río Hondo"), (1904,"Gualán"), (1905,"Teculután"),
    (1906,"Usumatlán"), (1907,"Cabañas"), (1908,"San Diego"), (1909,"La Unión"), (1910,"Huité"),
    (1911,"San Jorge"), (2001,"Chiquimula"), (2002,"San José la Arada"), (2003,"San Juan Ermita"),
    (2004,"Jocotán"), (2005,"Camotán"), (2006,"Olopa"), (2007,"Esquipulas"), (2008,"Concepción las Minas"),
    (2009,"Quezaltepeque"), (2010,"San Jacinto"), (2011,"Ipala"), (2101,"Jalapa"), (2102,"San Pedro Pinula"),
    (2103,"San Luis Jilotepeque"), (2104,"San Manuel Chaparrón"), (2105,"San Carlos Alzatate"), (2106,"Monjas"),
    (2107,"Mataquescuintla"), (2201,"Jutiapa"), (2202,"El Progreso"), (2203,"Santa Catarina Mita"),
    (2204,"Agua Blanca"), (2205,"Asunción Mita"), (2206,"Yupiltepeque"), (2207,"Atescatempa"), (2208,"Jerez"),
    (2209,"El Adelanto"), (2210,"Zapotitlán"), (2211,"Comapa"), (2212,"Jalpatagua"), (2213,"Conguaco"),
    (2214,"Moyuta"), (2215,"Pasaco"), (2216,"San José Acatempa"), (2217,"Quesada")
]

def main(departamentos=departamentos_data, municipios=municipios_data,
         file_departamentos=OUT_BASE+"/departamentos.csv",
         file_municipios=OUT_BASE+"/municipios.csv"):

    cacheFilePath = os.path.join(CACHE_BASE, CACHE_CSV_BASE)

    # Revisar si existe cache
    if os.path.exists(cacheFilePath):
        print(f"Cache encontrado en {cacheFilePath}, saltando generación de CSVs.")
        return

    # Función para normalizar texto
    def normalize_text(text):
        if pd.isna(text):
            return ""
        text = unidecode.unidecode(str(text))  # quita tildes
        text = text.lower().strip()            # minúsculas y quitar espacios
        return text

    # Crear DataFrames
    df_departamentos = pd.DataFrame(departamentos, columns=["codigo","departamento"])
    df_departamentos["departamento"] = df_departamentos["departamento"].apply(normalize_text)

    df_municipios = pd.DataFrame(municipios, columns=["codigo","municipio"])
    df_municipios["municipio"] = df_municipios["municipio"].apply(normalize_text)

    # Guardar CSVs
    df_departamentos.to_csv(file_departamentos, index=False, encoding="utf-8")
    df_municipios.to_csv(file_municipios, index=False, encoding="utf-8")

    print(f"CSV generados: {file_departamentos} y {file_municipios}")

    # Crear cache al final
    with open(cacheFilePath, "w", encoding="utf-8") as f:
        f.write("Generación de CSV completada.\n")

    print(f"Cache creado en {cacheFilePath}")

if __name__ == "__main__":
    main()