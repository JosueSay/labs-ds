import plotly.graph_objects as go
import plotly.io as pio
import panel as pn

PALETTE = {
    "dominante": "#1B3B5F",  # Azul petróleo (títulos/elementos principales)
    "secundario": "#2E5984",  # Azul medio (líneas principales)
    "mediacion": "#5C7EA3",  # Celeste grisáceo (áreas/etiquetas)
    "neutro": "#B0BEC5",  # Gris metálico (fondo/separadores)
    "acento": "#F28C38",  # Naranja (eventos/picos)
    "confirmacion": "#3D8361",  # Verde (confirmación)
    "warning": "#C14953",  # Rojo terracota para alertas
    "background": "#F7F9FC",  # Gris para fondos generales
}

PYTHON_THEME_CSS = f"""
/* Base styling */
body {{
    background-color: {PALETTE["background"]};
    color: {PALETTE["dominante"]};
    font-family: Inter, system-ui, -apple-system, sans-serif;
}}

/* Panel components base */
.bk-root {{
    color: {PALETTE["dominante"]};
}}

/* Headers and titles */
h1, h2, h3, h4, h5, h6 {{
    color: {PALETTE["dominante"]};
}}

/* Cards and panels */
.card {{
    background: white;
    border: 1px solid {PALETTE["neutro"]};
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(27, 59, 95, 0.08);
}}

.card-header {{
    background: {PALETTE["dominante"]};
    color: white;
    padding: 12px 16px;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
}}

/* Buttons */
.bk-btn {{
    border-radius: 6px;
    font-weight: 500;
    padding: 8px 16px;
    transition: all 0.2s;
}}

.bk-btn-primary {{
    background-color: {PALETTE["dominante"]} !important;
    border-color: {PALETTE["dominante"]} !important;
    color: white !important;
}}

.bk-btn-primary:hover {{
    background-color: {PALETTE["secundario"]} !important;
    border-color: {PALETTE["secundario"]} !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(27, 59, 95, 0.2);
}}

.bk-btn-success {{
    background-color: {PALETTE["confirmacion"]} !important;
    border-color: {PALETTE["confirmacion"]} !important;
    color: white !important;
}}

.bk-btn-success:hover {{
    background-color: #2F6E4F !important;
    border-color: #2F6E4F !important;
}}

.bk-btn-warning {{
    background-color: {PALETTE["warning"]} !important;
    border-color: {PALETTE["warning"]} !important;
    color: white !important;
}}

.bk-btn-warning:hover {{
    background-color: #A63D46 !important;
    border-color: #A63D46 !important;
}}

.bk-btn-default {{
    background-color: white !important;
    border-color: {PALETTE["neutro"]} !important;
    color: {PALETTE["dominante"]} !important;
}}

.bk-btn-default:hover {{
    background-color: {PALETTE["background"]} !important;
    border-color: {PALETTE["mediacion"]} !important;
}}

/* Inputs and textareas */
input, textarea, select {{
    border: 1px solid {PALETTE["neutro"]};
    border-radius: 6px;
    padding: 8px 12px;
    transition: all 0.2s;
}}

input:focus, textarea:focus, select:focus {{
    outline: none;
    border-color: {PALETTE["acento"]};
    box-shadow: 0 0 0 3px rgba(242, 140, 56, 0.1);
}}

/* Tabs */
.bk-tabs-header .bk-tab {{
    background: white;
    color: {PALETTE["mediacion"]};
    border: 1px solid {PALETTE["neutro"]};
    border-bottom: none;
    padding: 10px 20px;
    margin-right: 4px;
    border-radius: 6px 6px 0 0;
    transition: all 0.2s;
}}

.bk-tabs-header .bk-tab:hover {{
    background: {PALETTE["background"]};
    color: {PALETTE["dominante"]};
}}

.bk-tabs-header .bk-tab.bk-active {{
    background: {PALETTE["dominante"]};
    color: white;
    border-color: {PALETTE["dominante"]};
    border-bottom: 3px solid {PALETTE["acento"]};
}}

/* Sliders */
.bk-slider-title {{
    color: {PALETTE["dominante"]};
    font-weight: 500;
}}

.noUi-connect {{
    background: {PALETTE["acento"]} !important;
}}

.noUi-handle {{
    border-color: {PALETTE["acento"]} !important;
    background: white !important;
    box-shadow: 0 2px 4px rgba(242, 140, 56, 0.3);
}}

.noUi-target {{
    background: {PALETTE["neutro"]};
    border-color: {PALETTE["neutro"]};
}}

/* Progress bars */
.bk-progress {{
    background: {PALETTE["neutro"]};
    border-radius: 10px;
    overflow: hidden;
}}

.bk-progress-bar {{
    background: {PALETTE["acento"]};
}}

/* Tables */
.bk-data-table {{
    border: 1px solid {PALETTE["neutro"]};
}}

.bk-data-table thead {{
    background: {PALETTE["dominante"]};
    color: white;
}}

.bk-data-table tbody tr:nth-child(even) {{
    background: {PALETTE["background"]};
}}

.bk-data-table tbody tr:hover {{
    background: rgba(92, 126, 163, 0.1);
}}

/* Checkboxes and radio buttons */
input[type="checkbox"]:checked,
input[type="radio"]:checked {{
    accent-color: {PALETTE["acento"]};
}}

/* Alerts and notifications */
.alert {{
    padding: 12px 16px;
    border-radius: 6px;
    margin: 10px 0;
}}

.alert-info {{
    background: rgba(92, 126, 163, 0.1);
    border-left: 4px solid {PALETTE["mediacion"]};
    color: {PALETTE["dominante"]};
}}

.alert-success {{
    background: rgba(61, 131, 97, 0.1);
    border-left: 4px solid {PALETTE["confirmacion"]};
    color: {PALETTE["dominante"]};
}}

.alert-warning {{
    background: rgba(193, 73, 83, 0.1);
    border-left: 4px solid {PALETTE["warning"]};
    color: {PALETTE["dominante"]};
}}

/* Tooltips */
.bk-tooltip {{
    background: {PALETTE["dominante"]};
    color: white;
    border-radius: 4px;
    padding: 6px 10px;
}}

/* Accordions */
.bk-panel-models-layout-Accordion .bk-header {{
    background: {PALETTE["background"]};
    border: 1px solid {PALETTE["neutro"]};
    color: {PALETTE["dominante"]};
    font-weight: 500;
}}

.bk-panel-models-layout-Accordion .bk-header:hover {{
    background: {PALETTE["mediacion"]};
    color: white;
}}

/* Dividers */
hr {{
    border-color: {PALETTE["neutro"]};
}}

/* Links */
a {{
    color: {PALETTE["acento"]};
    text-decoration: none;
}}

a:hover {{
    color: {PALETTE["dominante"]};
    text-decoration: underline;
}}

/* Loading indicators */
.bk-loading {{
    color: {PALETTE["acento"]};
}}
"""


# Paleta de colores para series múltiples (secuencia recomendada)
COLOR_SEQUENCE = [
    PALETTE["dominante"],
    PALETTE["acento"],
    PALETTE["confirmacion"],
    PALETTE["secundario"],
    PALETTE["mediacion"],
    PALETTE["warning"],
    "#7FA3C7",  # Azul claro adicional
    "#F5A962",  # Naranja claro adicional
]

# Definir el tema personalizado de Plotly
python_theme = {
    "layout": {
        # Colores de fondo
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": PALETTE["background"],
        # Fuentes
        "font": {
            "family": "Inter, system-ui, -apple-system, sans-serif",
            "size": 13,
            "color": PALETTE["dominante"],
        },
        # Títulos
        "title": {
            "font": {
                "family": "Inter, system-ui, -apple-system, sans-serif",
                "size": 18,
                "color": PALETTE["dominante"],
            },
            "x": 0.5,
            "xanchor": "center",
        },
        # Colores de secuencia
        "colorway": COLOR_SEQUENCE,
        # Ejes
        "xaxis": {
            "gridcolor": PALETTE["neutro"],
            "linecolor": PALETTE["neutro"],
            "zerolinecolor": PALETTE["neutro"],
            "tickfont": {"color": PALETTE["dominante"]},
            "titlefont": {"color": PALETTE["acento"], "size": 14},
            "showgrid": True,
            "zeroline": True,
        },
        "yaxis": {
            "gridcolor": PALETTE["neutro"],
            "linecolor": PALETTE["neutro"],
            "zerolinecolor": PALETTE["neutro"],
            "tickfont": {"color": PALETTE["dominante"]},
            "titlefont": {"color": PALETTE["acento"], "size": 14},
            "showgrid": True,
            "zeroline": True,
        },
        # Leyenda
        "legend": {
            "bgcolor": "rgba(255, 255, 255, 0.9)",
            "bordercolor": PALETTE["neutro"],
            "borderwidth": 1,
            "font": {"color": PALETTE["dominante"]},
        },
        # Hover
        "hoverlabel": {
            "bgcolor": PALETTE["dominante"],
            "font": {
                "family": "Inter, system-ui, -apple-system, sans-serif",
                "color": "white",
            },
            "bordercolor": "white",
        },
        # Anotaciones
        "annotationdefaults": {"font": {"color": PALETTE["dominante"]}},
        # Mapas de calor
        "colorscale": {
            "sequential": [
                [0.0, PALETTE["background"]],
                [0.5, PALETTE["mediacion"]],
                [1.0, PALETTE["dominante"]],
            ],
            "sequentialminus": [
                [0.0, PALETTE["dominante"]],
                [0.5, PALETTE["background"]],
                [1.0, PALETTE["acento"]],
            ],
            "diverging": [
                [0.0, PALETTE["dominante"]],
                [0.5, PALETTE["background"]],
                [1.0, PALETTE["acento"]],
            ],
        },
    },
    # Estilos de trazas por defecto
    "data": {
        "scatter": [{"marker": {"line": {"width": 0}, "opacity": 0.8}}],
        "bar": [
            {
                "marker": {
                    "line": {"width": 0.5, "color": PALETTE["background"]},
                    "opacity": 0.9,
                }
            }
        ],
        # "cone": [{"line": {"width": 3}}],
        "box": [
            {
                "marker": {"color": PALETTE["dominante"]},
                "line": {"color": PALETTE["dominante"]},
            }
        ],
        "violin": [
            {
                "marker": {"color": PALETTE["dominante"]},
                "line": {"color": PALETTE["dominante"]},
            }
        ],
        "histogram": [
            {"marker": {"line": {"width": 0.5, "color": PALETTE["background"]}}}
        ],
        "pie": [{"marker": {"line": {"width": 1, "color": "white"}}}],
    },
}

# Registrar el tema en Plotly
# PLOTLY_THEME_NAME = "dashboard_theme"
# pio.templates[PLOTLY_THEME_NAME] = go.layout.Template(python_theme)


def create_custom_colorscale(color1_key, color2_key):
    """
    Crea una escala de colores personalizada entre dos colores de la paleta.

    Args:
        color1_key (str): Clave del primer color
        color2_key (str): Clave del segundo color

    Returns:
        list: Escala de colores para usar en Plotly
    """
    return [
        [0.0, PALETTE[color1_key]],
        [0.5, PALETTE["background"]],
        [1.0, PALETTE[color2_key]],
    ]


def apply_theme():
    """
    Apply the Python custom theme to Panel.
    Call this function before creating your Panel components.
    """
    pn.extension(raw_css=[PYTHON_THEME_CSS])
    # pio.templates.default = PLOTLY_THEME_NAME
    print("Python theme applied successfully!")
