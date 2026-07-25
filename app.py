# -*- coding: utf-8 -*-
"""
MACROMIND — Web App Streamlit
Con Salvataggio Dati Persistente e Modifica Titolo iOS.
"""

import streamlit as st
import random
import datetime
import json
import os

# ============================================================
# 0. CONFIGURAZIONE PAGINA
# ============================================================
st.set_page_config(
    page_title="MacroMind",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SAVE_FILE = "user_data.json"

def salva_dati_locali(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

def carica_dati_locali():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

# ============================================================
# 1. STILE E CSS
# ============================================================
st.markdown("""
<style>
html, body, [class*="css"]  { font-size: 19px !important; }
h1 { font-size: 2.3rem !important; font-weight: 800 !important; color: #1a5f3f; }
h2 { font-size: 1.7rem !important; font-weight: 800 !important; color: #2e4053; }
p, li, label, span { font-size: 1.02rem !important; }

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
}

div[data-testid="stFormSubmitButton"] > button {
    background-color: #1a5f3f !important;
    color: #ffffff !important;
    font-size: 1.3rem !important;
    padding: 1rem !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. DATABASE ALIMENTI E RICETTE
# ============================================================
FOODS = {
    "Fiocchi d'avena":              {"kcal":389,"prot":16.9,"carb":66.3,"fat":6.9, "cat":"Dispensa"},
    "Latte parzialmente scremato":  {"kcal":46, "prot":3.3, "carb":4.8, "fat":1.5, "cat":"Freschi"},
    "Latte di soia":                {"kcal":33, "prot":3.3, "carb":1.8, "fat":1.8, "cat":"Dispensa"},
    "Mirtilli":                     {"kcal":57, "prot":0.7, "carb":14.0,"fat":0.3, "cat":"Ortofrutta"},
    "Miele":                        {"kcal":304,"prot":0.3, "carb":82.4,"fat":0.0, "cat":"Dispensa"},
    "Uova":                         {"kcal":155,"prot":12.6,"carb":1.1, "fat":10.6,"cat":"Freschi"},
    "Pane integrale":               {"kcal":247,"prot":9.0, "carb":41.0,"fat":3.5, "cat":"Dispensa"},
    "Avocado":                      {"kcal":160,"prot":2.0, "carb":8.5, "fat":14.7,"cat":"Ortofrutta"},
    "Petto di pollo":               {"kcal":165,"prot":31.0,"carb":0.0, "fat":3.6, "cat":"Freschi"},
    "Tacchino fette":               {"kcal":104,"prot":22.0,"carb":1.0, "fat":1.0, "cat":"Freschi"},
    "Salmone":                      {"kcal":208,"prot":20.0,"carb":0.0, "fat":13.0,"cat":"Freschi"},
    "Merluzzo":                     {"kcal":82, "prot":18.0,"carb":0.0, "fat":0.7, "cat":"Freschi"},
    "Tofu":                         {"kcal":76, "prot":8.0, "carb":1.9, "fat":4.8, "cat":"Freschi"},
    "Riso basmati (crudo)":         {"kcal":349,"prot":7.5, "carb":77.0,"fat":0.9, "cat":"Dispensa"},
    "Farro (crudo)":                {"kcal":335,"prot":15.0,"carb":67.0,"fat":2.5, "cat":"Dispensa"},
    "Quinoa (cruda)":               {"kcal":368,"prot":14.0,"carb":64.0,"fat":6.0, "cat":"Dispensa"},
    "Patate":                       {"kcal":77, "prot":2.0, "carb":17.0,"fat":0.1, "cat":"Ortofrutta"},
    "Broccoli":                     {"kcal":34, "prot":2.8, "carb":7.0, "fat":0.4, "cat":"Ortofrutta"},
    "Zucchine":                     {"kcal":17, "prot":1.2, "carb":3.1, "fat":0.2, "cat":"Ortofrutta"},
    "Spinaci":                      {"kcal":23, "prot":2.9, "carb":3.6, "fat":0.4, "cat":"Ortofrutta"},
    "Olio EVO":                     {"kcal":884,"prot":0.0, "carb":0.0, "fat":100.0,"cat":"Dispensa"},
    "Yogurt greco":                 {"kcal":59, "prot":10.0,"carb":3.6, "fat":0.4, "cat":"Freschi"},
    "Mandorle":                     {"kcal":579,"prot":21.0,"carb":22.0,"fat":50.0,"cat":"Dispensa"},
    "Noci":                         {"kcal":654,"prot":15.0,"carb":14.0,"fat":65.0,"cat":"Dispensa"},
    "Mela":                         {"kcal":52, "prot":0.3, "carb":14.0,"fat":0.2, "cat":"Ortofrutta"},
}

RICETTE_COLAZIONE = [
    {"nome": "Porridge d'avena con frutti di bosco e miele", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio"],
     "ingredienti": [("Fiocchi d'avena", 50), ("Latte parzialmente scremato", 200), ("Mirtilli", 60), ("Miele", 10)],
     "tempo": 8, "nota": "Ricco di fibre solubili (beta-glucani)."},
    {"nome": "Yogurt greco con mandorle e mela", "slot": "colazione", "tipo_colazione": "dolce",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "frutta_a_guscio"],
     "ingredienti": [("Yogurt greco", 200), ("Mandorle", 20), ("Miele", 10), ("Mela", 100)],
     "tempo": 5, "nota": "Ottimo rapporto proteine/grassi buoni."},
    {"nome": "Toast integrale con avocado e uovo", "slot": "colazione", "tipo_colazione": "salata",
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["uova", "glutine"],
     "ingredienti": [("Pane integrale", 60), ("Avocado", 60), ("Uova", 50)],
     "tempo": 10, "nota": "Grassi monoinsaturi per sazietà prolungata."},
]

RICETTE_PRINCIPALI = [
    {"nome": "Petto di pollo con riso basmati e broccoli", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro"], "allergeni": [],
     "ingredienti": [("Petto di pollo", 150), ("Riso basmati (crudo)", 70), ("Broccoli", 200), ("Olio EVO", 10)],
     "tempo": 25, "nota": "Proteine nobili e carboidrati a medio indice glicemico."},
    {"nome": "Salmone al forno con patate e zucchine", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Salmone", 150), ("Patate", 200), ("Zucchine", 150), ("Olio EVO", 10)],
     "tempo": 25, "nota": "Ricco di omega-3 EPA/DHA."},
    {"nome": "Tofu saltato con riso e verdure", "slot": "principale", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
     "ingredienti": [("Tofu", 180), ("Riso basmati (crudo)", 70), ("Zucchine", 100), ("Olio EVO", 10)],
     "tempo": 18, "nota": "Fonte proteica vegetale completa."},
]

RICETTE_SPUNTINO = [
    {"nome": "Yogurt greco con mandorle", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Pescetariano"], "allergeni": ["lattosio", "frutta_a_guscio"],
     "ingredienti": [("Yogurt greco", 150), ("Mandorle", 15)],
     "tempo": 2, "nota": "Spuntino proteico saziante."},
    {"nome": "Mela con noci", "slot": "spuntino", "tipo_colazione": None,
     "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": ["frutta_a_guscio"],
     "ingredienti": [("Mela", 150), ("Noci", 15)],
     "tempo": 2, "nota": "Fibre e grassi sani."},
]

DISTRIBUZIONE = {
    3: {"Colazione": 0.25, "Pranzo": 0.40, "Cena": 0.35},
    4: {"Colazione": 0.20, "Spuntino": 0.10, "Pranzo": 0.35, "Cena": 0.35},
    5: {"Colazione": 0.20, "Spuntino Mattina": 0.10, "Pranzo": 0.30, "Spuntino Pomeriggio": 0.10, "Cena": 0.30},
}
ICONE_SLOT = {"Colazione": "☀️", "Pranzo": "🍽️", "Cena": "🌙", "Spuntino": "🍎", "Spuntino Mattina": "🍎", "Spuntino Pomeriggio": "🍏"}
ATTIVITA = {"Sedentario": 1.20, "Leggero (1-3 gg/sett)": 1.375, "Moderato (3-5 gg/sett)": 1.55, "Intenso (6-7 gg/sett)": 1.725}
OBIETTIVI = ["Mantenimento del peso", "Deficit progressivo (dimagrimento)", "Massa muscolare / Ricomposizione"]

# ============================================================
# 3. LOGICA DI CALCOLO
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
    kcal = tdee * 0.85 if "Deficit" in obiettivo else (tdee * 1.10 if "Massa" in obiettivo else tdee)
    prot_g = peso * (2.2 if "Deficit" in obiettivo else (2.0 if "Massa" in obiettivo else 1.8))
    prot_kcal = prot_g * 4
    fat_kcal = kcal * 0.30
    carb_kcal = max(kcal - prot_kcal - fat_kcal, kcal * 0.20)
    return {"kcal": round(kcal), "prot": round(prot_g), "carb": round(carb_kcal / 4), "fat": round(fat_kcal / 9)}, round(bmr), round(tdee)

def genera_pasto(pool, target_kcal, stile, colazione_pref, max_tempo):
    candidati = [r for r in pool if stile in r["diete"]]
    if not candidati:
        candidati = pool
    ricetta = random.choice(candidati)
    base = totali_ingredienti(ricetta["ingredienti"])
    fattore = target_kcal / base["kcal"] if base["kcal"] > 0 else 1.0
    nuovi_ingr = [(n, max(round(g * fattore), 1)) for n, g in ricetta["ingredienti"]]
    return {"nome": ricetta["nome"], "ingredienti": nuovi_ingr, "totali": totali_ingredienti(nuovi_ingr), "nota": ricetta["nota"], "tempo": ricetta["tempo"]}

def genera_giornata(target_macros, n_pasti, stile, colazione_pref, max_tempo):
    distribuzione = DISTRIBUZIONE[n_pasti]
    day_plan, day_targets = {}, {}
    for slot, perc in distribuzione.items():
        slot_target = {k: v * perc for k, v in target_macros.items()}
        day_targets[slot] = slot_target
        pool = RICETTE_COLAZIONE if "Colazione" in slot else (RICETTE_SPUNTINO if "Spuntino" in slot else RICETTE_PRINCIPALI)
        day_plan[slot] = genera_pasto(pool, slot_target["kcal"], stile, colazione_pref, max_tempo)
    return day_plan, day_targets

# ============================================================
# 4. RIPRISTINO DATI SALVATI ALL'AVVIO
# ============================================================
if "day_plan" not in st.session_state or not st.session_state.day_plan:
    dati_salvati = carica_dati_locali()
    if dati_salvati:
        st.session_state.day_plan = dati_salvati.get("day_plan", {})
        st.session_state.target_macros = dati_salvati.get("target_macros", None)
        st.session_state.day_targets = dati_salvati.get("day_targets", {})
        st.session_state.info_calcolo = dati_salvati.get("info_calcolo", None)

# ============================================================
# 5. INTERFACCIA UTENTE
# ============================================================
col_logo, col_titolo = st.columns([1, 6])
with col_logo:
    st.write("# 🏋️‍♂️")
with col_titolo:
    st.title("MacroMind")

st.caption("Nutrizione Personalizzata & Calcolo Macro")
st.divider()

with st.form("form_piano"):
    st.header("1️⃣ I tuoi dati")
    c1, c2 = st.columns(2)
    with c1:
        età = st.number_input("Età", 14, 100, 25)
        sesso = st.radio("Sesso", ["Donna", "Uomo"], horizontal=True)
        peso = st.number_input("Peso (kg)", 30.0, 200.0, 65.0)
    with c2:
        altezza = st.number_input("Altezza (cm)", 120.0, 230.0, 168.0)
        attività_scelta = st.selectbox("Attività fisica", list(ATTIVITA.keys()))
        obiettivo_scelta = st.selectbox("Obiettivo", OBIETTIVI)

    st.divider()
    st.header("2️⃣ Preferenze")
    stile = st.radio("Stile alimentare", ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], horizontal=True)
    col_a, col_b = st.columns(2)
    with col_a:
        colazione_pref = st.radio("Colazione", ["Dolce", "Salata", "Indifferente"], horizontal=True)
        n_pasti = st.radio("Pasti al giorno", [3, 4, 5], horizontal=True)
    with col_b:
        tempo_scelto = st.select_slider("⏱️ Tempo max preparazione:", ["< 15 min", "15-30 min", "Senza limiti"], value="Senza limiti")

    submitted = st.form_submit_button("🚀 GENERA E SALVA PIANO", use_container_width=True)

if submitted:
    max_tempo_min = 15 if tempo_scelto == "< 15 min" else (30 if tempo_scelto == "15-30 min" else None)
    target, bmr, tdee = calcola_target_automatico(età, sesso, peso, altezza, ATTIVITA[attività_scelta], obiettivo_scelta)
    
    day_plan, day_targets = genera_giornata(target, n_pasti, stile, colazione_pref, max_tempo_min)
    info_calcolo = f"Metabolismo basale: {bmr} kcal | TDEE: {tdee} kcal"

    # Salva in sessione
    st.session_state.day_plan = day_plan
    st.session_state.target_macros = target
    st.session_state.day_targets = day_targets
    st.session_state.info_calcolo = info_calcolo

    # Salva permanentemente su file locale user_data.json
    salva_dati_locali({
        "day_plan": day_plan,
        "target_macros": target,
        "day_targets": day_targets,
        "info_calcolo": info_calcolo,
    })
    st.success("✅ Piano generato e salvato con successo!")

# ============================================================
# 6. VISUALIZZAZIONE RISULTATI
# ============================================================
if "day_plan" in st.session_state and st.session_state.day_plan:
    st.divider()
    if st.session_state.info_calcolo:
        st.info(st.session_state.info_calcolo)

    st.header("🍽️ Il Tuo Piano Alimentare Salvato")
    for slot, meal in st.session_state.day_plan.items():
        icona = ICONE_SLOT.get(slot, "🍴")
        with st.container():
            st.subheader(f"{icona} {slot} — {meal['nome']}")
            st.caption(f"⏱️ Tempo: {meal['tempo']} min")
            for nome, g in meal["ingredienti"]:
                st.write(f"• {nome}: **{g} g**")
            t = meal["totali"]
            st.caption(f"Kcal: {t['kcal']:.0f} | P: {t['prot']:.0f}g | C: {t['carb']:.0f}g | G: {t['fat']:.0f}g")

    st.write("")
    if st.button("🗑️ Rimuovi piano salvato"):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()
