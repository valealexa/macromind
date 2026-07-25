# -*- coding: utf-8 -*-
"""
MACROMIND — Web App Streamlit
Sviluppata secondo principi EFSA/LARN e best practice UX ad alta accessibilità.
Requisiti: pip install streamlit
Avvio: streamlit run app.py
"""

import streamlit as st
import random
import datetime

# ============================================================
# 0. CONFIGURAZIONE PAGINA (Titolo, Logo Favicon e Layout)
# ============================================================
st.set_page_config(
    page_title="MacroMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 1. CSS PER ALTA ACCESSIBILITÀ E DESIGN MODERNO
# ============================================================
st.markdown("""
<style>
html, body, [class*="css"]  { font-size: 19px !important; }
h1 { font-size: 2.3rem !important; font-weight: 800 !important; color: #1a5f3f; }
h2 { font-size: 1.7rem !important; font-weight: 800 !important; color: #2e4053; }
h3 { font-size: 1.35rem !important; font-weight: 700 !important; }
p, li, label, span { font-size: 1.02rem !important; }

/* Pulsanti principali */
.stButton > button {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.4rem !important;
    border-radius: 12px !important;
    border: 2px solid #1a5f3f !important;
    color: #1a5f3f !important;
    background-color: #ffffff !important;
    width: 100%;
}
.stButton > button:hover {
    background-color: #1a5f3f !important;
    color: #ffffff !important;
    border: 2px solid #1a5f3f !important;
}

/* Pulsante Form Submit */
div[data-testid="stFormSubmitButton"] > button {
    background-color: #1a5f3f !important;
    color: #ffffff !important;
    font-size: 1.3rem !important;
    padding: 1rem !important;
    border-radius: 12px !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #103d28 !important;
    border: 2px solid #103d28 !important;
}

/* Card e riquadri moderni */
div[data-testid="stContainer"] {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
}

div[data-testid="stMetricValue"] { font-size: 1.7rem !important; }
div[data-testid="stExpander"] { border: 1px solid #cccccc !important; border-radius: 10px !important; background-color: #ffffff; }
hr { border: 1px solid #e0e0e0; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. DATABASE ALIMENTI (valori per 100 g, a crudo dove pertinente)
# ============================================================
FOODS = {
    "Fiocchi d'avena":              {"kcal":389,"prot":16.9,"carb":66.3,"fat":6.9, "cat":"Dispensa"},
    "Latte parzialmente scremato":  {"kcal":46, "prot":3.3, "carb":4.8, "fat":1.5, "cat":"Freschi"},
    "Latte di soia":                {"kcal":33, "prot":3.3, "carb":1.8, "fat":1.8, "cat":"Dispensa"},
    "Mirtilli":                     {"kcal":57, "prot":0.7, "carb":14.0,"fat":0.3, "cat":"Ortofrutta"},
    "Miele":                        {"kcal":304,"prot":0.3, "carb":82.4,"fat":0.0, "cat":"Dispensa"},
    "Uova":                         {"kcal":155,"prot":12.6,"carb":1.1, "fat":10.6,"cat":"Freschi"},
    "Pane integrale":               {"kcal":247,"prot":9.0, "carb":41.0,"fat":3.5, "cat":"Dispensa"},
    "Pane senza glutine":           {"kcal":250,"prot":6.0, "carb":50.0,"fat":3.0, "cat":"Dispensa"},
    "Avocado":                      {"kcal":160,"prot":2.0, "carb":8.5, "fat":14.7,"cat":"Ortofrutta"},
    "Petto di pollo":               {"kcal":165,"prot":31.0,"carb":0.0, "fat":3.6, "cat":"Freschi"},
    "Tacchino fette":               {"kcal":104,"prot":22.0,"carb":1.0, "fat":1.0, "cat":"Freschi"},
    "Salmone":                      {"kcal":208,"prot":20.0,"carb":0.0, "fat":13.0,"cat":"Freschi"},
    "Merluzzo":                     {"kcal":82, "prot":18.0,"carb":0.0, "fat":0.7, "cat":"Freschi"},
    "Tonno al naturale":            {"kcal":116,"prot":26.0,"carb":0.0, "fat":1.0, "cat":"Dispensa"},
    "Tofu":                         {"kcal":76, "prot":8.0, "carb":1.9, "fat":4.8, "cat":"Freschi"},
    "Lenticchie secche":            {"kcal":353,"prot":25.0,"carb":60.0,"fat":1.0, "cat":"Dispensa"},
    "Ceci secchi":                  {"kcal":364,"prot":19.0,"carb":61.0,"fat":6.0, "cat":"Dispensa"},
    "Riso basmati (crudo)":         {"kcal":349,"prot":7.5, "carb":77.0,"fat":0.9, "cat":"Dispensa"},
    "Farro (crudo)":                {"kcal":335,"prot":15.0,"carb":67.0,"fat":2.5, "cat":"Dispensa"},
    "Quinoa (cruda)":               {"kcal":368,"prot":14.0,"carb":64.0,"fat":6.0, "cat":"Dispensa"},
    "Pasta di semola (cruda)":      {"kcal":353,"prot":12.5,"carb":71.0,"fat":1.5, "cat":"Dispensa"},
    "Pasta senza glutine":          {"kcal":360,"prot":7.0, "carb":80.0,"fat":1.0, "cat":"Dispensa"},
    "Patate":                       {"kcal":77, "prot":2.0, "carb":17.0,"fat":0.1, "cat":"Ortofrutta"},
    "Broccoli":                     {"kcal":34, "prot":2.8, "carb":7.0, "fat":0.4, "cat":"Ortofrutta"},
    "Zucchine":                     {"kcal":17, "prot":1.2, "carb":3.1, "fat":0.2, "cat":"Ortofrutta"},
    "Spinaci":                      {"kcal":23, "prot":2.9, "carb":3.6, "fat":0.4, "cat":"Ortofrutta"},
    "Pomodori":                     {"kcal":18, "prot":0.9, "carb":3.9, "fat":0.2, "cat":"Ortofrutta"},
    "Insalata mista":               {"kcal":15, "prot":1.4, "carb":2.9, "fat":0.2, "cat":"Ortofrutta"},
    "Carote":                       {"kcal":41, "prot":0.9, "carb":10.0,"fat":0.2, "cat":"Ortofrutta"},
    "Olio EVO":                     {"kcal":884,"prot":0.0, "carb":0.0, "fat":100.0,"cat":"Dispensa"},
    "Parmigiano":                   {"kcal":392,"prot":33.0,"carb":0.0, "fat":28.0,"cat":"Freschi"},
    "Mozzarella":                   {"kcal":253,"prot":18.0,"carb":2.2, "fat":19.0,"cat":"Freschi"},
    "Yogurt greco":                 {"kcal":59, "prot":10.0,"carb":3.6, "fat":0.4, "cat":"Freschi"},
    "Yogurt di soia":               {"kcal":43, "prot":3.5, "carb":3.0, "fat":2.0, "cat":"Freschi"},
    "Mandorle":                     {"kcal":579,"prot":21.0,"carb":22.0,"fat":50.0,"cat":"Dispensa"},
    "Noci":                         {"kcal":654,"prot":15.0,"carb":14.0,"fat":65.0,"cat":"Dispensa"},
    "Semi di chia":                 {"kcal":486,"prot":17.0,"carb":42.0,"fat":31.0,"cat":"Dispensa"},
    "Banana":                       {"kcal":89, "prot":1.1, "carb":23.0,"fat":0.3, "cat":"Ortofrutta"},
    "Mela":                         {"kcal":52, "prot":0.3, "carb":14.0,"fat":0.2, "cat":"Ortofrutta"},
    "Fette biscottate integrali":   {"kcal":408,"prot":10.0,"carb":71.0,"fat":8.0, "cat":"Dispensa"},
    "Marmellata":                   {"kcal":250,"prot":0.4, "carb":60.0,"fat":0.1, "cat":"Dispensa"},
    "Ricotta":                      {"kcal":146,"prot":11.0,"carb":3.0, "fat":10.0,"cat":"Freschi"},
    "Bresaola":                     {"kcal":151,"prot":32.0,"carb":0.4, "fat":2.0, "cat":"Freschi"},
    "Hummus":                       {"kcal":166,"prot":8.0, "carb":14.0,"fat":10.0,"cat":"Dispensa"},
}

FOOD_ALLERGENI = {
    "Latte parzialmente scremato": ["lattosio"],
    "Yogurt greco": ["lattosio"],
    "Mozzarella": ["lattosio"],
    "Ricotta": ["lattosio"],
    "Parmigiano": ["lattosio"],
    "Pane integrale": ["glutine"],
    "Fette biscottate integrali": ["glutine"],
    "Farro (crudo)": ["glutine"],
    "Pasta di semola (cruda)": ["glutine"],
    "Mandorle": ["frutta_a_guscio"],
    "Noci": ["frutta_a_guscio"],
    "Uova": ["uova"],
}

ETICHETTE_ALLERGENI = {
    "🥛 Senza Lattosio": "lattosio",
    "🌾 Senza Glutine": "glutine",
    "🥜 Senza Frutta a guscio": "frutta_a_guscio",
    "🥚 Senza Uova": "uova",
}

SUBSTITUZIONI = {
    "Riso basmati (crudo)": ["Farro (crudo)", "Quinoa (cruda)", "Pasta di semola (cruda)", "Pasta senza glutine"],
    "Farro (crudo)": ["Riso basmati (crudo)", "Quinoa (cruda)", "Pasta di semola (cruda)"],
    "Quinoa (cruda)": ["Riso basmati (crudo)", "Farro (crudo)", "Pasta senza glutine"],
    "Pasta di semola (cruda)": ["Riso basmati (crudo)", "Farro (crudo)", "Pasta senza glutine"],
    "Pasta senza glutine": ["Riso basmati (crudo)", "Quinoa (cruda)"],
    "Petto di pollo": ["Tacchino fette", "Tofu", "Merluzzo", "Salmone"],
    "Tacchino fette": ["Petto di pollo", "Tofu", "Merluzzo"],
    "Salmone": ["Merluzzo", "Tonno al naturale", "Petto di pollo"],
    "Merluzzo": ["Salmone", "Tonno al naturale", "Petto di pollo", "Tofu"],
    "Tofu": ["Petto di pollo", "Tacchino fette", "Merluzzo", "Ceci secchi"],
    "Yogurt greco": ["Yogurt di soia", "Ricotta"],
    "Mandorle": ["Noci"],
    "Noci": ["Mandorle"],
    "Broccoli": ["Zucchine", "Spinaci", "Carote"],
    "Zucchine": ["Broccoli", "Carote", "Spinaci"],
    "Spinaci": ["Broccoli", "Zucchine"],
    "Patate": ["Riso basmati (crudo)", "Farro (crudo)"],
}

# ============================================================
# 3. DATABASE RICETTE (con tempi di preparazione)
# ============================================================
RICETTE_COLAZIONE = [
    {"nome": "Porridge d'avena con frutti di bosco e miele", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio"],
     "ingredienti": [("Fiocchi d'avena", 50), ("Latte parzialmente scremato", 200), ("Mirtilli", 60), ("Miele", 10)],
     "tempo": 8, "nota": "Ricco di fibre solubili (beta-glucani) che rallentano l'assorbimento degli zuccheri."},
    {"nome": "Porridge vegan con frutti di bosco e chia", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Fiocchi d'avena", 50), ("Latte di soia", 200), ("Mirtilli", 60), ("Semi di chia", 10)],
     "tempo": 8, "nota": "I semi di chia apportano omega-3 vegetali e favoriscono senso di sazietà prolungato."},
    {"nome": "Pancake proteici alla banana", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["uova", "glutine"],
     "ingredienti": [("Uova", 100), ("Fiocchi d'avena", 40), ("Banana", 100), ("Miele", 5)],
     "tempo": 12, "nota": "Colazione ad alto apporto proteico, ideale per il mantenimento della massa magra."},
    {"nome": "Yogurt greco con mandorle, mela e miele", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "frutta_a_guscio"],
     "ingredienti": [("Yogurt greco", 200), ("Mandorle", 20), ("Miele", 10), ("Mela", 100)],
     "tempo": 5, "nota": "Ottimo rapporto proteine/grassi buoni, con zuccheri a rilascio graduale."},
    {"nome": "Yogurt di soia con frutta e semi di chia", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Yogurt di soia", 200), ("Banana", 100), ("Semi di chia", 15), ("Mirtilli", 50)],
     "tempo": 5, "nota": "Alternativa 100% vegetale, ricca di fibre e antiossidanti."},
    {"nome": "Toast integrale con avocado e uovo", "slot": "colazione", "tipo_colazione": "salata",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["uova", "glutine"],
     "ingredienti": [("Pane integrale", 60), ("Avocado", 60), ("Uova", 50), ("Pomodori", 50)],
     "tempo": 10, "nota": "I grassi monoinsaturi dell'avocado favoriscono sazietà e assorbimento delle vitamine."},
    {"nome": "Toast senza glutine con hummus e verdure", "slot": "colazione", "tipo_colazione": "salata",
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Pane senza glutine", 60), ("Hummus", 60), ("Pomodori", 50), ("Insalata mista", 30)],
     "tempo": 7, "nota": "Colazione salata leggera, con proteine vegetali dai ceci dell'hummus."},
    {"nome": "Uova strapazzate con bresaola", "slot": "colazione", "tipo_colazione": "salata",
     "diete": ["Onnivoro", "Pescetariano"], "allergeni": ["uova"],
     "ingredienti": [("Uova", 100), ("Bresaola", 40), ("Pomodori", 50)],
     "tempo": 8, "nota": "Colazione ad alta densità proteica, povera di carboidrati."},
    {"nome": "Fette biscottate con ricotta e marmellata", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "glutine"],
     "ingredienti": [("Fette biscottate integrali", 40), ("Ricotta", 100), ("Marmellata", 20)],
     "tempo": 5, "nota": "Colazione classica bilanciata, con la ricotta a fornire una buona quota proteica."},
    {"nome": "Yogurt greco con fiocchi d'avena, mela e noci", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "frutta_a_guscio"],
     "ingredienti": [("Yogurt greco", 150), ("Fiocchi d'avena", 30), ("Mela", 100), ("Noci", 15)],
     "tempo": 5, "nota": "Combinazione di proteine, fibre e grassi buoni per un mattino energico."},
]

RICETTE_PRINCIPALI = [
    {"nome": "Petto di pollo con riso basmati e broccoli", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro"], "allergeni": [],
     "ingredienti": [("Petto di pollo", 150), ("Riso basmati (crudo)", 70), ("Broccoli", 200), ("Olio EVO", 10)],
     "tempo": 25, "nota": "Proteine nobili ad alta digeribilità abbinate a carboidrati a medio indice glicemico."},
    {"nome": "Salmone al forno con patate e zucchine", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Salmone", 150), ("Patate", 200), ("Zucchine", 150), ("Olio EVO", 10)],
     "tempo": 25, "nota": "Ricco di omega-3 EPA/DHA, utili per il controllo dello stato infiammatorio."},
    {"nome": "Merluzzo con farro e spinaci", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Pescetariano"], "allergeni": ["glutine"],
     "ingredienti": [("Merluzzo", 180), ("Farro (crudo)", 70), ("Spinaci", 150), ("Olio EVO", 10)],
     "tempo": 22, "nota": "Piatto magro e ricco di ferro e fibre, ideale per un pasto leggero ma completo."},
    {"nome": "Tacchino con quinoa e carote", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro"], "allergeni": [],
     "ingredienti": [("Tacchino fette", 150), ("Quinoa (cruda)", 70), ("Carote", 150), ("Olio EVO", 10)],
     "tempo": 20, "nota": "La quinoa è un carboidrato completo di tutti gli amminoacidi essenziali."},
    {"nome": "Tofu saltato con riso e verdure miste", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Tofu", 180), ("Riso basmati (crudo)", 70), ("Zucchine", 100), ("Carote", 100), ("Olio EVO", 10)],
     "tempo": 18, "nota": "Fonte proteica vegetale completa, leggera e di rapida digestione."},
    {"nome": "Lenticchie con farro e pomodorini", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": ["glutine"],
     "ingredienti": [("Lenticchie secche", 80), ("Farro (crudo)", 60), ("Pomodori", 100), ("Olio EVO", 10)],
     "tempo": 30, "nota": "Abbinamento legumi-cereali che fornisce un profilo amminoacidico completo."},
    {"nome": "Ceci con quinoa e spinaci", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Ceci secchi", 80), ("Quinoa (cruda)", 60), ("Spinaci", 150), ("Olio EVO", 10)],
     "tempo": 30, "nota": "Piatto 100% vegetale ad alto contenuto di fibre, ferro e proteine complete."},
    {"nome": "Pasta integrale al pomodoro con mozzarella", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "glutine"],
     "ingredienti": [("Pasta di semola (cruda)", 80), ("Pomodori", 150), ("Mozzarella", 80), ("Olio EVO", 8)],
     "tempo": 15, "nota": "Classico italiano bilanciato, con proteine e calcio dalla mozzarella."},
    {"nome": "Pasta senza glutine con tonno e pomodorini", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Pasta senza glutine", 80), ("Tonno al naturale", 100), ("Pomodori", 100), ("Olio EVO", 8)],
     "tempo": 15, "nota": "Pasto rapido, ricco di proteine magre e adatto a chi evita il glutine."},
    {"nome": "Insalatona con pollo, uova e verdure", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro"], "allergeni": ["uova"],
     "ingredienti": [("Petto di pollo", 120), ("Uova", 50), ("Insalata mista", 100), ("Pomodori", 100), ("Olio EVO", 10)],
     "tempo": 12, "nota": "Pasto fresco e ad alta densità proteica, con pochi carboidrati."},
    {"nome": "Ceci speziati con verdure croccanti", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Ceci secchi", 100), ("Insalata mista", 100), ("Carote", 100), ("Olio EVO", 10)],
     "tempo": 25, "nota": "Piatto vegano ricco di fibre, che favorisce sazietà e regolarità intestinale."},
    {"nome": "Frittata di uova con verdure e parmigiano", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["uova", "lattosio"],
     "ingredienti": [("Uova", 150), ("Zucchine", 150), ("Parmigiano", 20), ("Olio EVO", 8)],
     "tempo": 15, "nota": "Fonte proteica completa e versatile, ottima anche fredda o da asporto."},
    {"nome": "Bresaola con insalata e scaglie di grana", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro"], "allergeni": ["lattosio"],
     "ingredienti": [("Bresaola", 120), ("Insalata mista", 100), ("Parmigiano", 20), ("Olio EVO", 8)],
     "tempo": 5, "nota": "Pasto leggero e velocissimo, con proteine magre di alta qualità."},
    {"nome": "Riso basmati con tofu, carote e mandorle", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": ["frutta_a_guscio"],
     "ingredienti": [("Riso basmati (crudo)", 70), ("Tofu", 150), ("Carote", 100), ("Mandorle", 15), ("Olio EVO", 8)],
     "tempo": 18, "nota": "Piatto vegetale completo, con grassi buoni dalle mandorle."},
]

RICETTE_SPUNTINO = [
    {"nome": "Yogurt greco con mandorle", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "frutta_a_guscio"],
     "ingredienti": [("Yogurt greco", 150), ("Mandorle", 15)],
     "tempo": 2, "nota": "Spuntino proteico che aiuta a contenere la fame nervosa."},
    {"nome": "Frutta fresca con noci", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": ["frutta_a_guscio"],
     "ingredienti": [("Mela", 150), ("Noci", 15)],
     "tempo": 2, "nota": "Fibre e grassi buoni insieme, per uno spuntino sano e saziante."},
    {"nome": "Yogurt di soia con banana", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Yogurt di soia", 150), ("Banana", 100)],
     "tempo": 2, "nota": "Spuntino 100% vegetale, fonte di potassio ed energia a rapido utilizzo."},
    {"nome": "Hummus con carote", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Hummus", 60), ("Carote", 100)],
     "tempo": 2, "nota": "Spuntino croccante e ricco di fibre, con proteine vegetali dai ceci."},
    {"nome": "Involtini di bresaola", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro"], "allergeni": [],
     "ingredienti": [("Bresaola", 60), ("Insalata mista", 30)],
     "tempo": 3, "nota": "Spuntino magro e proteico, ideale per chi necessita di alte quote proteiche."},
    {"nome": "Ricotta con miele", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio"],
     "ingredienti": [("Ricotta", 100), ("Miele", 10)],
     "tempo": 2, "nota": "Spuntino dolce ma bilanciato, con una buona quota proteica dalla ricotta."},
]

RICETTA_FALLBACK = {
    "nome": "Piatto semplice componibile: riso, verdure e olio EVO", "slot": "qualsiasi", "tipo_colazione": None,
    "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
    "ingredienti": [("Riso basmati (crudo)", 70), ("Zucchine", 150), ("Olio EVO", 10)],
    "tempo": 15, "nota": "Opzione semplice e neutra, generata perché i filtri impostati erano molto restrittivi."
}

DISTRIBUZIONE = {
    3: {"Colazione": 0.25, "Pranzo": 0.40, "Cena": 0.35},
    4: {"Colazione": 0.20, "Spuntino": 0.10, "Pranzo": 0.35, "Cena": 0.35},
    5: {"Colazione": 0.20, "Spuntino Mattina": 0.10, "Pranzo": 0.30, "Spuntino Pomeriggio": 0.10, "Cena": 0.30},
}

ICONE_SLOT = {
    "Colazione": "☀️", "Pranzo": "🍽️", "Cena": "🌙",
    "Spuntino": "🍎", "Spuntino Mattina": "🍎", "Spuntino Pomeriggio": "🍏",
}

ATTIVITA = {
    "Sedentario (poco o nessun esercizio)": 1.20,
    "Leggero (esercizio 1-3 giorni/settimana)": 1.375,
    "Moderato (esercizio 3-5 giorni/settimana)": 1.55,
    "Intenso (esercizio 6-7 giorni/settimana)": 1.725,
    "Molto intenso (lavoro fisico + allenamento)": 1.90,
}

OBIETTIVI = ["Mantenimento del peso", "Deficit progressivo (dimagrimento)", "Massa muscolare / Ricomposizione"]

# ============================================================
# 4. FUNZIONI DI CALCOLO E FILTRAGGIO
# ============================================================
def totali_ingredienti(lista_ingr):
    tot = {"kcal": 0.0, "prot": 0.0, "carb": 0.0, "fat": 0.0}
    for nome, grammi in lista_ingr:
        f = FOODS[nome]
        fattore = grammi / 100.0
        tot["kcal"] += f["kcal"] * fattore
        tot["prot"] += f["prot"] * fattore
        tot["carb"] += f["carb"] * fattore
        tot["fat"] += f["fat"] * fattore
    return tot

def calcola_target_automatico(età, sesso, peso, altezza, fattore_attività, obiettivo):
    bmr = 10 * peso + 6.25 * altezza - 5 * età + (5 if sesso == "Uomo" else -161)
    tdee = bmr * fattore_attività

    if obiettivo == "Deficit progressivo (dimagrimento)":
        kcal = tdee * 0.85
        g_prot_kg = 2.2
    elif obiettivo == "Massa muscolare / Ricomposizione":
        kcal = tdee * 1.10
        g_prot_kg = 2.0
    else:
        kcal = tdee
        g_prot_kg = 1.8

    prot_g = peso * g_prot_kg
    prot_kcal = prot_g * 4
    fat_kcal = kcal * 0.30
    carb_kcal = kcal - prot_kcal - fat_kcal

    if carb_kcal < kcal * 0.20:
        carb_kcal = kcal * 0.20
        fat_kcal = max(kcal - prot_kcal - carb_kcal, 0)

    carb_g = max(carb_kcal, 0) / 4
    fat_g = max(fat_kcal, 0) / 9

    target = {"kcal": round(kcal), "prot": round(prot_g), "carb": round(carb_g), "fat": round(fat_g)}
    return target, round(bmr), round(tdee)

def filtra_ricette(pool, stile, intolleranze, blacklist, tipo_colazione=None, max_tempo=None):
    bl = [b.strip().lower() for b in blacklist if b.strip()]
    risultati = []
    for r in pool:
        if stile not in r["diete"]:
            continue
        if any(a in r["allergeni"] for a in intolleranze):
            continue
        if tipo_colazione and tipo_colazione != "Indifferente" and r.get("tipo_colazione") not in (None, tipo_colazione.lower()):
            continue
        nomi_ingr = " ".join(n.lower() for n, _ in r["ingredienti"])
        if any(b in nomi_ingr for b in bl):
            continue
        # Filtro tempo di preparazione
        if max_tempo and max_tempo > 0 and r["tempo"] > max_tempo:
            continue
        risultati.append(r)
    return risultati

def scala_ricetta(ricetta, target_kcal):
    base = totali_ingredienti(ricetta["ingredienti"])
    fattore = target_kcal / base["kcal"] if base["kcal"] > 0 else 1.0
    nuovi_ingr = [(n, max(round(g * fattore), 1)) for n, g in ricetta["ingredienti"]]
    tot = totali_ingredienti(nuovi_ingr)
    return nuovi_ingr, tot

def genera_pasto(pool, target_kcal, stile, intolleranze, blacklist, tipo_colazione=None, max_tempo=None, escludi_nome=None):
    candidati = filtra_ricette(pool, stile, intolleranze, blacklist, tipo_colazione, max_tempo)
    
    # Se il filtro tempo è troppo stringente, proviamo senza filtro tempo prima del fallback
    if not candidati and max_tempo:
        candidati = filtra_ricette(pool, stile, intolleranze, blacklist, tipo_colazione, max_tempo=None)

    if escludi_nome:
        alternativi = [r for r in candidati if r["nome"] != escludi_nome]
        if alternativi:
            candidati = alternativi

    avviso = False
    if not candidati:
        candidati = [RICETTA_FALLBACK]
        avviso = True

    ricetta = random.choice(candidati)
    ingredienti, totali = scala_ricetta(ricetta, target_kcal)
    return {
        "nome": ricetta["nome"], "ingredienti": ingredienti, "totali": totali,
        "nota": ricetta["nota"], "tempo": ricetta["tempo"], "avviso": avviso,
    }

def genera_giornata(target_macros, n_pasti, stile, intolleranze, blacklist, colazione_pref, max_tempo):
    distribuzione = DISTRIBUZIONE[n_pasti]
    day_plan, day_targets = {}, {}
    for slot, perc in distribuzione.items():
        slot_target = {k: v * perc for k, v in target_macros.items()}
        day_targets[slot] = slot_target
        if "Colazione" in slot:
            pool, tipo_col = RICETTE_COLAZIONE, colazione_pref
        elif "Spuntino" in slot:
            pool, tipo_col = RICETTE_SPUNTINO, None
        else:
            pool, tipo_col = RICETTE_PRINCIPALI, None
        day_plan[slot] = genera_pasto(pool, slot_target["kcal"], stile, intolleranze, blacklist, tipo_col, max_tempo)
    return day_plan, day_targets

def somma_giornata(day_plan):
    tot = {"kcal": 0.0, "prot": 0.0, "carb": 0.0, "fat": 0.0}
    for meal in day_plan.values():
        for k in tot:
            tot[k] += meal["totali"][k]
    return tot

def genera_lista_spesa(day_plan):
    agg = {}
    for meal in day_plan.values():
        for nome, g in meal["ingredienti"]:
            agg[nome] = agg.get(nome, 0) + g
    lista = {"Ortofrutta": {}, "Freschi": {}, "Dispensa": {}}
    for nome, g in agg.items():
        cat = FOODS[nome]["cat"]
        lista[cat][nome] = int(round(g / 10.0) * 10)
    return lista

def formatta_piano_testo(day_plan, target_macros, lista_spesa):
    righe = []
    righe.append("=" * 54)
    righe.append("MACROMIND — PIANO ALIMENTARE GIORNALIERO")
    righe.append(f"Generato il {datetime.date.today().strftime('%d/%m/%Y')}")
    righe.append("=" * 54)
    righe.append("")
    righe.append(f"Target giornaliero: {target_macros['kcal']} kcal | "
                  f"Proteine {target_macros['prot']} g | Carboidrati {target_macros['carb']} g | "
                  f"Grassi {target_macros['fat']} g")
    righe.append("")
    for slot, meal in day_plan.items():
        righe.append(f"--- {slot.upper()}: {meal['nome']} (pronto in {meal['tempo']} min) ---")
        for nome, g in meal["ingredienti"]:
            righe.append(f"   - {nome}: {g} g")
        t = meal["totali"]
        righe.append(f"   Totale pasto: {t['kcal']:.0f} kcal | P {t['prot']:.0f} g | "
                      f"C {t['carb']:.0f} g | G {t['fat']:.0f} g")
        righe.append(f"   Nota del dietista: {meal['nota']}")
        righe.append("")
    righe.append("=" * 54)
    righe.append("LISTA DELLA SPESA")
    righe.append("=" * 54)
    for cat, items in lista_spesa.items():
        if items:
            righe.append(f"\n{cat}:")
            for nome, g in items.items():
                righe.append(f"   [ ] {nome}: {g} g")
    return "\n".join(righe)

# ============================================================
# 5. INIZIALIZZAZIONE SESSION STATE E MEMORIA LOCALE (Browser)
# ============================================================
if "day_plan" not in st.session_state:
    st.session_state.day_plan = {}
if "target_macros" not in st.session_state:
    st.session_state.target_macros = None
if "preferenze" not in st.session_state:
    st.session_state.preferenze = None
if "lista_spesa" not in st.session_state:
    st.session_state.lista_spesa = None
if "info_calcolo" not in st.session_state:
    st.session_state.info_calcolo = None

def render_barra_macro(icona, label, valore, target, unita="g"):
    target = max(target, 0.0001)
    pct = min(valore / target, 1.0)
    st.write(f"{icona} **{label}:** {valore:.0f}{unita} / {target:.0f}{unita}")
    st.progress(pct)

# ============================================================
# 6. INTESTAZIONE APP
# ============================================================
st.title("🧠 MacroMind")
st.caption(
    "Il tuo assistente nutrizionale intelligente basato sull'equazione di Mifflin-St Jeor e sui principi EFSA/LARN. "
    "I dati inseriti rimangono memorizzati nel tuo browser per i prossimi accessi."
)
st.divider()

# ============================================================
# 7. STEP 1 — SCELTA MODALITÀ
# ============================================================
st.header("1️⃣ Definisci il tuo obiettivo calorico")
modo = st.radio(
    "Come vuoi impostare i tuoi macronutrienti?",
    ["🧮 Calcolo automatico scientifico", "✍️ Inserimento manuale (ho già una scheda)"],
    horizontal=False,
)

# ============================================================
# 8. FORM COMPLETO (profilo + preferenze + tempo pasti)
# ============================================================
with st.form("form_piano"):

    if modo.startswith("🧮"):
        col1, col2 = st.columns(2)
        with col1:
            età = st.number_input("Età (anni)", min_value=14, max_value=100, value=35, step=1)
            sesso = st.radio("Sesso biologico", ["Uomo", "Donna"], horizontal=True)
            peso = st.number_input("Peso attuale (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5)
        with col2:
            altezza = st.number_input("Altezza (cm)", min_value=120.0, max_value=230.0, value=170.0, step=0.5)
            attività_scelta = st.selectbox("Livello di attività fisica", list(ATTIVITA.keys()))
            obiettivo_scelta = st.selectbox("Obiettivo", OBIETTIVI)
    else:
        st.info("Inserisci i valori indicati nella tua scheda nutrizionale personalizzata.")
        col1, col2 = st.columns(2)
        with col1:
            kcal_manuale = st.number_input("Calorie totali (kcal)", min_value=800, max_value=5000, value=2000, step=10)
            prot_manuale = st.number_input("Proteine (g)", min_value=0, max_value=400, value=120, step=1)
        with col2:
            carb_manuale = st.number_input("Carboidrati (g)", min_value=0, max_value=700, value=220, step=1)
            fat_manuale = st.number_input("Grassi (g)", min_value=0, max_value=250, value=65, step=1)

    st.divider()
    st.header("2️⃣ Le tue preferenze alimentari")

    stile = st.radio("Stile alimentare", ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], horizontal=True)

    st.write("**Intolleranze / Allergie:**")
    c1, c2, c3, c4 = st.columns(4)
    scelte_allergeni = {}
    with c1:
        scelte_allergeni["🥛 Senza Lattosio"] = st.checkbox("🥛 Senza Lattosio")
    with c2:
        scelte_allergeni["🌾 Senza Glutine"] = st.checkbox("🌾 Senza Glutine")
    with c3:
        scelte_allergeni["🥜 Senza Frutta a guscio"] = st.checkbox("🥜 Senza Frutta a guscio")
    with c4:
        scelte_allergeni["🥚 Senza Uova"] = st.checkbox("🥚 Senza Uova")

    blacklist_input = st.text_input(
        "Cibi da evitare (separati da virgola)",
        placeholder="es. peperoni, tonno, funghi",
    )

    col1_pref, col2_pref = st.columns(2)
    with col1_pref:
        colazione_pref = st.radio("Preferenza colazione", ["Dolce", "Salata", "Indifferente"], horizontal=True)
        n_pasti = st.radio("Struttura della giornata", [3, 4, 5], horizontal=True, format_func=lambda x: f"{x} pasti")
    
    with col2_pref:
        tempo_scelto = st.select_slider(
            "⏱️ Tempo max di preparazione pasti:",
            options=["Veloce (< 15 min)", "Medio (15-30 min)", "Tutto il tempo necessario"],
            value="Tutto il tempo necessario"
        )

    st.write("")
    submitted = st.form_submit_button("🚀 GENERA GIORNATA BILANCIATA", use_container_width=True)

if submitted:
    intolleranze = [ETICHETTE_ALLERGENI[k] for k, v in scelte_allergeni.items() if v]
    blacklist = [b for b in blacklist_input.split(",")] if blacklist_input else []

    # Conversione selettore tempo in minuti
    max_tempo_min = None
    if tempo_scelto == "Veloce (< 15 min)":
        max_tempo_min = 15
    elif tempo_scelto == "Medio (15-30 min)":
        max_tempo_min = 30

    if modo.startswith("🧮"):
        target, bmr, tdee = calcola_target_automatico(età, sesso, peso, altezza, ATTIVITA[attività_scelta], obiettivo_scelta)
        st.session_state.info_calcolo = f"Metabolismo basale (BMR): {bmr} kcal — Fabbisogno totale (TDEE): {tdee} kcal"
        if target["kcal"] < (1200 if sesso == "Donna" else 1500):
            st.warning(
                "⚠️ Il valore calorico calcolato è piuttosto basso. Ti consigliamo di consultare un "
                "medico o un nutrizionista prima di seguire un piano così restrittivo."
            )
    else:
        target = {"kcal": kcal_manuale, "prot": prot_manuale, "carb": carb_manuale, "fat": fat_manuale}
        st.session_state.info_calcolo = None

    st.session_state.target_macros = target
    st.session_state.preferenze = {
        "stile": stile, "intolleranze": intolleranze, "blacklist": blacklist,
        "colazione_pref": colazione_pref, "n_pasti": n_pasti, "max_tempo": max_tempo_min
    }
    st.session_state.day_plan, st.session_state.day_targets = genera_giornata(
        target, n_pasti, stile, intolleranze, blacklist, colazione_pref, max_tempo_min
    )
    st.session_state.lista_spesa = None
    st.success("✅ Giornata generata con successo! Scorri in basso per visualizzarla.")

# ============================================================
# 9. VISUALIZZAZIONE PIANO E CARD DEI PASTI
# ============================================================
if st.session_state.day_plan:
    st.divider()

    if st.session_state.info_calcolo:
        st.caption(f"ℹ️ {st.session_state.info_calcolo}")

    target_macros = st.session_state.target_macros
    prefs = st.session_state.preferenze

    st.header("📊 Riepilogo della Giornata")
    tot_giorno = somma_giornata(st.session_state.day_plan)
    colA, colB = st.columns(2)
    with colA:
        render_barra_macro("🔥", "Calorie", tot_giorno["kcal"], target_macros["kcal"], " kcal")
        render_barra_macro("🍗", "Proteine", tot_giorno["prot"], target_macros["prot"])
    with colB:
        render_barra_macro("🍞", "Carboidrati", tot_giorno["carb"], target_macros["carb"])
        render_barra_macro("🥑", "Grassi", tot_giorno["fat"], target_macros["fat"])

    st.divider()
    st.header("🍽️ I Tuoi Pasti")

    for slot, meal in list(st.session_state.day_plan.items()):
        icona = ICONE_SLOT.get(slot, "🍴")
        with st.container():
            st.subheader(f"{icona} {slot} — {meal['nome']}")
            st.caption(f"⏱️ Tempo di preparazione: **{meal['tempo']} minuti**")

            if meal.get("avviso"):
                st.warning(
                    "I filtri impostati erano molto restrittivi per questo pasto: "
                    "ti proponiamo un'alternativa semplice e neutra."
                )

            st.write("**Ingredienti (dosi a crudo):**")
            for nome, g in meal["ingredienti"]:
                st.write(f"• {nome}: **{g} g**")

            st.info(f"💬 Nota nutrizionale: {meal['nota']}")

            t = meal["totali"]
            slot_target = st.session_state.day_targets[slot]
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1:
                render_barra_macro("🔥", "Kcal", t["kcal"], slot_target["kcal"], "")
            with cc2:
                render_barra_macro("🍗", "Prot.", t["prot"], slot_target["prot"])
            with cc3:
                render_barra_macro("🍞", "Carb.", t["carb"], slot_target["carb"])
            with cc4:
                render_barra_macro("🥑", "Grassi", t["fat"], slot_target["fat"])

            b1, b2 = st.columns(2)
            with b1:
                if st.button("🔄 Cambia questo pasto", key=f"cambia_{slot}"):
                    if "Colazione" in slot:
                        pool, tipo_col = RICETTE_COLAZIONE, prefs["colazione_pref"]
                    elif "Spuntino" in slot:
                        pool, tipo_col = RICETTE_SPUNTINO, None
                    else:
                        pool, tipo_col = RICETTE_PRINCIPALI, None
                    nuovo = genera_pasto(
                        pool, slot_target["kcal"], prefs["stile"], prefs["intolleranze"],
                        prefs["blacklist"], tipo_col, prefs.get("max_tempo"), escludi_nome=meal["nome"],
                    )
                    st.session_state.day_plan[slot] = nuovo
                    st.session_state.lista_spesa = None
                    st.rerun()

            with b2:
                with st.expander("🔀 Sostituisci un ingrediente"):
                    ingr_sostituibili = [n for n, _ in meal["ingredienti"] if n in SUBSTITUZIONI]
                    if not ingr_sostituibili:
                        st.write("Nessun ingrediente di questo pasto ha sostituzioni disponibili.")
                    else:
                        ingr_scelto = st.selectbox(
                            "Ingrediente da sostituire", ingr_sostituibili, key=f"sel_ingr_{slot}"
                        )
                        alternative = [
                            a for a in SUBSTITUZIONI[ingr_scelto]
                            if not any(x in prefs["intolleranze"] for x in FOOD_ALLERGENI.get(a, []))
                        ]
                        if not alternative:
                            st.write("Nessuna alternativa compatibile con le tue intolleranze.")
                        else:
                            nuovo_ingr = st.selectbox("Sostituisci con", alternative, key=f"sel_alt_{slot}")
                            if st.button("✅ Conferma sostituzione", key=f"conferma_sub_{slot}"):
                                nuova_lista = []
                                for n, g in meal["ingredienti"]:
                                    if n == ingr_scelto:
                                        kcal_old = FOODS[n]["kcal"]
                                        kcal_new = FOODS[nuovo_ingr]["kcal"]
                                        g_nuovo = max(round(g * kcal_old / kcal_new), 1) if kcal_new > 0 else g
                                        nuova_lista.append((nuovo_ingr, g_nuovo))
                                    else:
                                        nuova_lista.append((n, g))
                                meal["ingredienti"] = nuova_lista
                                meal["totali"] = totali_ingredienti(nuova_lista)
                                st.session_state.day_plan[slot] = meal
                                st.session_state.lista_spesa = None
                                st.rerun()

    # ============================================================
    # 10. LISTA DELLA SPESA
    # ============================================================
    st.divider()
    st.header("🛒 Lista della Spesa")
    if st.button("🛒 Genera / Aggiorna Lista della Spesa", use_container_width=True):
        st.session_state.lista_spesa = genera_lista_spesa(st.session_state.day_plan)

    if st.session_state.lista_spesa:
        cols = st.columns(3)
        etichette = {"Ortofrutta": "🥦 Ortofrutta", "Freschi": "🧊 Freschi", "Dispensa": "🥫 Dispensa"}
        for i, cat in enumerate(["Ortofrutta", "Freschi", "Dispensa"]):
            with cols[i]:
                st.subheader(etichette[cat])
                items = st.session_state.lista_spesa[cat]
                if items:
                    for nome, g in items.items():
                        st.checkbox(f"{nome} — {g} g", key=f"spesa_{cat}_{nome}")
                else:
                    st.caption("Nessun articolo in questa categoria.")

    # ============================================================
    # 11. ESPORTAZIONE
    # ============================================================
    st.divider()
    st.header("📥 Esporta il Piano")
    lista_per_export = st.session_state.lista_spesa or genera_lista_spesa(st.session_state.day_plan)
    testo_piano = formatta_piano_testo(st.session_state.day_plan, target_macros, lista_per_export)

    st.download_button(
        label="⬇️ Scarica Piano in Testo (.txt)",
        data=testo_piano,
        file_name=f"macromind_piano_{datetime.date.today().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.caption(
        "💡 Per stampare: apri il file scaricato e usa la funzione \"Stampa\" (Ctrl+P / Cmd+P), "
        "oppure invialo direttamente via WhatsApp o email."
    )

    st.divider()
    if st.button("🔁 Ricomincia da capo", use_container_width=True):
        st.session_state.day_plan = {}
        st.session_state.target_macros = None
        st.session_state.preferenze = None
        st.session_state.lista_spesa = None
        st.session_state.info_calcolo = None
        st.rerun()

else:
    st.info("👆 Compila i tuoi dati e le preferenze qui sopra, poi premi **GENERA GIORNATA BILANCIATA** per iniziare.")
