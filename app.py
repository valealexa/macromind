# -*- coding: utf-8 -*-
"""
MACROMIND — Web App Streamlit
Versione Full: Allergie + Cambio Singolo Piatto + Sostituzione Ingredienti + Salvataggio + PWA
"""

import streamlit as st
import random
import json
import os

# ============================================================
# 0. CONFIGURAZIONE PAGINA E PWA
# ============================================================
st.set_page_config(
    page_title="MacroMind",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <head>
        <title>MacroMind</title>
        <meta name="apple-mobile-web-app-title" content="MacroMind">
        <meta name="application-name" content="MacroMind">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-capable" content="yes">
        <link rel="apple-touch-icon" href="https://img.icons8.com/emoji/192/dumbbell-emoji.png">
        <link rel="icon" type="image/png" sizes="192x192" href="https://img.icons8.com/emoji/192/dumbbell-emoji.png">
    </head>
""", unsafe_allow_html=True)

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
# 1. CSS CUSTOM E STILIZZAZIONE
# ============================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 18px !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #1a5f3f !important;
}

.meal-card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border: 1px solid #eef2f5;
}

.macro-badge {
    background-color: #f4f8f5;
    color: #1a5f3f;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.88rem;
    display: inline-block;
    margin-right: 6px;
    margin-top: 6px;
}

.macro-kcal {
    background-color: #e8f5e9;
    color: #2e7d32;
}

div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #1a5f3f 0%, #2e7d32 100%) !important;
    color: #ffffff !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    padding: 0.9rem !important;
    border-radius: 14px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(26, 95, 63, 0.3) !important;
}

.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. DATABASE ALIMENTI E RICETTE CON ALLERGENI
# ============================================================
FOODS = {
    "Fiocchi d'avena":              {"kcal":389,"prot":16.9,"carb":66.3,"fat":6.9, "cat":"Cereali"},
    "Latte parzialmente scremato":  {"kcal":46, "prot":3.3, "carb":4.8, "fat":1.5, "cat":"Latticini"},
    "Latte di soia":                {"kcal":33, "prot":3.3, "carb":1.8, "fat":1.8, "cat":"Latticini"},
    "Mirtilli":                     {"kcal":57, "prot":0.7, "carb":14.0,"fat":0.3, "cat":"Frutta"},
    "Miele":                        {"kcal":304,"prot":0.3, "carb":82.4,"fat":0.0, "cat":"Dolcificanti"},
    "Uova":                         {"kcal":155,"prot":12.6,"carb":1.1, "fat":10.6,"cat":"Proteine"},
    "Pane integrale":               {"kcal":247,"prot":9.0, "carb":41.0,"fat":3.5, "cat":"Cereali"},
    "Avocado":                      {"kcal":160,"prot":2.0, "carb":8.5, "fat":14.7,"cat":"Grassi"},
    "Petto di pollo":               {"kcal":165,"prot":31.0,"carb":0.0, "fat":3.6, "cat":"Proteine"},
    "Tacchino fette":               {"kcal":104,"prot":22.0,"carb":1.0, "fat":1.0, "cat":"Proteine"},
    "Salmone":                      {"kcal":208,"prot":20.0,"carb":0.0, "fat":13.0,"cat":"Proteine"},
    "Merluzzo":                     {"kcal":82, "prot":18.0,"carb":0.0, "fat":0.7, "cat":"Proteine"},
    "Tofu":                         {"kcal":76, "prot":8.0, "carb":1.9, "fat":4.8, "cat":"Proteine"},
    "Riso basmati (crudo)":         {"kcal":349,"prot":7.5, "carb":77.0,"fat":0.9, "cat":"Cereali"},
    "Farro (crudo)":                {"kcal":335,"prot":15.0,"carb":67.0,"fat":2.5, "cat":"Cereali"},
    "Quinoa (cruda)":               {"kcal":368,"prot":14.0,"carb":64.0,"fat":6.0, "cat":"Cereali"},
    "Patate":                       {"kcal":77, "prot":2.0, "carb":17.0,"fat":0.1, "cat":"Verdura"},
    "Broccoli":                     {"kcal":34, "prot":2.8, "carb":7.0, "fat":0.4, "cat":"Verdura"},
    "Zucchine":                     {"kcal":17, "prot":1.2, "carb":3.1, "fat":0.2, "cat":"Verdura"},
    "Spinaci":                      {"kcal":23, "prot":2.9, "carb":3.6, "fat":0.4, "cat":"Verdura"},
    "Olio EVO":                     {"kcal":884,"prot":0.0, "carb":0.0, "fat":100.0,"cat":"Grassi"},
    "Yogurt greco":                 {"kcal":59, "prot":10.0,"carb":3.6, "fat":0.4, "cat":"Latticini"},
    "Mandorle":                     {"kcal":579,"prot":21.0,"carb":22.0,"fat":50.0,"cat":"Frutta a guscio"},
    "Noci":                         {"kcal":654,"prot":15.0,"carb":14.0,"fat":65.0,"cat":"Frutta a guscio"},
    "Mela":                         {"kcal":52, "prot":0.3, "carb":14.0,"fat":0.2, "cat":"Frutta"},
}

ALLERGENI_DISPONIBILI = ["Lattosio", "Glutine", "Frutta a guscio", "Uova"]

RICETTE_COLAZIONE = [
    {
        "nome": "Porridge d'avena ai frutti di bosco",
        "diete": ["Onnivoro", "Vegetariano", "Pescetariano"],
        "allergeni": ["Lattosio", "Glutine"],
        "ingredienti": [("Fiocchi d'avena", 50), ("Latte parzialmente scremato", 200), ("Mirtilli", 60), ("Miele", 10)],
        "tempo": 8, "nota": "Ricco di fibre e beta-glucani.",
        "istruzioni": "Cuoci i fiocchi d'avena con il latte a fuoco lento per 5 minuti. Versa in ciotola e completa con mirtilli e miele."
    },
    {
        "nome": "Yogurt greco bowls con mela e mandorle",
        "diete": ["Onnivoro", "Vegetariano", "Pescetariano"],
        "allergeni": ["Lattosio", "Frutta a guscio"],
        "ingredienti": [("Yogurt greco", 200), ("Mandorle", 20), ("Miele", 10), ("Mela", 100)],
        "tempo": 5, "nota": "Colazione ad alto contenuto proteico.",
        "istruzioni": "Versa lo yogurt in una ciotola. Aggiungi la mela a cubetti, le mandorle tritate e rifinisci con il miele."
    },
    {
        "nome": "Toast integrale avocado e uovo al tegamino",
        "diete": ["Onnivoro", "Vegetariano", "Pescetariano"],
        "allergeni": ["Glutine", "Uova"],
        "ingredienti": [("Pane integrale", 60), ("Avocado", 60), ("Uova", 50)],
        "tempo": 10, "nota": "Grassi sani a lenta digestione.",
        "istruzioni": "Tosta il pane, schiaccia l'avocado sopra con una forchetta e adagia l'uovo cucinato al tegamino."
    },
]

RICETTE_PRINCIPALI = [
    {
        "nome": "Petto di pollo con riso basmati e broccoli",
        "diete": ["Onnivoro"], "allergeni": [],
        "ingredienti": [("Petto di pollo", 150), ("Riso basmati (crudo)", 70), ("Broccoli", 200), ("Olio EVO", 10)],
        "tempo": 25, "nota": "Pasto classico per la ricomposizione corporea.",
        "istruzioni": "Lessa il riso e i broccoli. Griglia il pollo in padella. Impiatta e condisci con olio EVO a crudo."
    },
    {
        "nome": "Salmone al forno con patate e zucchine",
        "diete": ["Onnivoro", "Pescetariano"], "allergeni": [],
        "ingredienti": [("Salmone", 150), ("Patate", 200), ("Zucchine", 150), ("Olio EVO", 10)],
        "tempo": 25, "nota": "Fonte eccellente di Omega-3.",
        "istruzioni": "Inforna patate e zucchine a 200°C per 15 min. Aggiungi il salmone e cuoci per altri 10-12 min."
    },
    {
        "nome": "Tofu croccante al salto con riso e zucchine",
        "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], "allergeni": [],
        "ingredienti": [("Tofu", 180), ("Riso basmati (crudo)", 70), ("Zucchine", 100), ("Olio EVO", 10)],
        "tempo": 18, "nota": "Proteine vegetali complete.",
        "istruzioni": "Cuoci il riso. Taglia il tofu a cubetti e rosolalo in padella con l'olio. Unisci le zucchine e sfuma a piacere."
    },
    {
        "nome": "Merluzzo al vapore con quinoa e spinaci",
        "diete": ["Onnivoro", "Pescetariano"], "allergeni": [],
        "ingredienti": [("Merluzzo", 180), ("Quinoa (cruda)", 70), ("Spinaci", 150), ("Olio EVO", 10)],
        "tempo": 20, "nota": "Pasto leggerissimo ed estremamente digeribile.",
        "istruzioni": "Cuoci la quinoa per 15 min. Cuoci merluzzo e spinaci al vapore per 10 min. Unisci tutto con l'olio EVO."
    }
]

RICETTE_SPUNTINO = [
    {
        "nome": "Yogurt greco con mandorle tostate",
        "diete": ["Onnivoro", "Vegetariano", "Pescetariano"],
        "allergeni": ["Lattosio", "Frutta a guscio"],
        "ingredienti": [("Yogurt greco", 150), ("Mandorle", 15)],
        "tempo": 2, "nota": "Spuntino veloce a basso indice glicemico.",
        "istruzioni": "Versa lo yogurt in una ciotolina e completa con le mandorle tostate."
    },
    {
        "nome": "Crunchy snack: Mela e noci",
        "diete": ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"],
        "allergeni": ["Frutta a guscio"],
        "ingredienti": [("Mela", 150), ("Noci", 15)],
        "tempo": 2, "nota": "Fibre e grassi buoni per la concentrazione.",
        "istruzioni": "Taglia la mela a fette e consumala insieme ai gherigli di noce."
    },
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
# 3. LOGICA DI CALCOLO E FILTRAGGIO
# ============================================================
def totali_ingredienti(lista_ingr):
    tot = {"kcal": 0.0, "prot": 0.0, "carb": 0.0, "fat": 0.0}
    for nome, grammi in lista_ingr:
        if nome in FOODS:
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

def estrai_ricetta_valida(pool, stile, allergie, usate):
    candidati = []
    for r in pool:
        if stile in r["diete"]:
            # Verifica allergeni
            if not any(a in r["allergeni"] for a in allergie):
                candidati.append(r)
    
    if not candidati:
        candidati = pool # Fallback se nessuna ricetta rispetta i filtri rigidi
        
    non_usate = [r for r in candidati if r["nome"] not in usate]
    return random.choice(non_usate if non_usate else candidati)

def genera_pasto(pool, target_kcal, stile, allergie, ricette_usate):
    ricetta = estrai_ricetta_valida(pool, stile, allergie, ricette_usate)
    ricette_usate.add(ricetta["nome"])
    
    base = totali_ingredienti(ricetta["ingredienti"])
    fattore = target_kcal / base["kcal"] if base["kcal"] > 0 else 1.0
    nuovi_ingr = [(n, max(round(g * fattore), 1)) for n, g in ricetta["ingredienti"]]
    
    return {
        "nome": ricetta["nome"],
        "ingredienti": nuovi_ingr,
        "totali": totali_ingredienti(nuovi_ingr),
        "nota": ricetta["nota"],
        "istruzioni": ricetta["istruzioni"],
        "tempo": ricetta["tempo"]
    }

def genera_giornata(target_macros, n_pasti, stile, allergie):
    distribuzione = DISTRIBUZIONE[n_pasti]
    day_plan, day_targets = {}, {}
    ricette_usate = set()
    
    for slot, perc in distribuzione.items():
        slot_target = {k: v * perc for k, v in target_macros.items()}
        day_targets[slot] = slot_target
        pool = RICETTE_COLAZIONE if "Colazione" in slot else (RICETTE_SPUNTINO if "Spuntino" in slot else RICETTE_PRINCIPALI)
        day_plan[slot] = genera_pasto(pool, slot_target["kcal"], stile, allergie, ricette_usate)
        
    return day_plan, day_targets

# ============================================================
# 4. RIPRISTINO STATO
# ============================================================
if "day_plan" not in st.session_state or not st.session_state.day_plan:
    dati_salvati = carica_dati_locali()
    if dati_salvati:
        st.session_state.day_plan = dati_salvati.get("day_plan", {})
        st.session_state.target_macros = dati_salvati.get("target_macros", None)
        st.session_state.day_targets = dati_salvati.get("day_targets", {})
        st.session_state.info_calcolo = dati_salvati.get("info_calcolo", None)
        st.session_state.stile = dati_salvati.get("stile", "Onnivoro")
        st.session_state.allergie = dati_salvati.get("allergie", [])

# ============================================================
# 5. FORM PARAMETRI
# ============================================================
st.title("🏋️‍♂️ MacroMind")
st.caption("Nutrizione Personalizzata & Calcolo Macro Automagico")
st.divider()

with st.form("form_piano"):
    st.subheader("1️⃣ Dati Fisiologici")
    c1, c2 = st.columns(2)
    with c1:
        età = st.number_input("Età", 14, 100, 22)
        sesso = st.radio("Sesso", ["Donna", "Uomo"], horizontal=True)
        peso = st.number_input("Peso (kg)", 30.0, 200.0, 58.0)
    with c2:
        altezza = st.number_input("Altezza (cm)", 120.0, 230.0, 165.0)
        attività_scelta = st.selectbox("Attività fisica", list(ATTIVITA.keys()), index=2)
        obiettivo_scelta = st.selectbox("Obiettivo", OBIETTIVI)

    st.divider()
    st.subheader("2️⃣ Preferenze & Intolleranze")
    stile = st.radio("Stile alimentare", ["Onnivoro", "Vegetariano", "Vegano", "Pescetariano"], horizontal=True)
    
    allergie = st.multiselect("⚠️ Seleziona le tue allergie/intolleranze:", ALLERGENI_DISPONIBILI)
    
    col_a, col_b = st.columns(2)
    with col_a:
        colazione_pref = st.radio("Preferenza colazione", ["Dolce", "Salata", "Indifferente"], horizontal=True)
        n_pasti = st.radio("Pasti al giorno", [3, 4, 5], index=1, horizontal=True)
    with col_b:
        tempo_scelto = st.select_slider("⏱️ Tempo max preparazione:", ["< 15 min", "15-30 min", "Senza limiti"], value="Senza limiti")

    submitted = st.form_submit_button("🚀 GENERA PIANO PERSONALIZZATO", use_container_width=True)

if submitted:
    target, bmr, tdee = calcola_target_automatico(età, sesso, peso, altezza, ATTIVITA[attività_scelta], obiettivo_scelta)
    day_plan, day_targets = genera_giornata(target, n_pasti, stile, allergie)
    info_calcolo = f"🔥 BMR: {bmr} kcal | TDEE: {tdee} kcal"

    st.session_state.day_plan = day_plan
    st.session_state.target_macros = target
    st.session_state.day_targets = day_targets
    st.session_state.info_calcolo = info_calcolo
    st.session_state.stile = stile
    st.session_state.allergie = allergie

    salva_dati_locali({
        "day_plan": day_plan, "target_macros": target,
        "day_targets": day_targets, "info_calcolo": info_calcolo,
        "stile": stile, "allergie": allergie
    })
    st.success("✅ Piano generato con successo!")

# ============================================================
# 6. BOARD RISULTATI & AZIONI SUI PASTI
# ============================================================
if "day_plan" in st.session_state and st.session_state.day_plan:
    st.divider()
    
    if st.session_state.target_macros:
        tm = st.session_state.target_macros
        st.subheader("📊 Target Giornaliero Calcolato")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Kcal Totali", f"{tm['kcal']} kcal")
        m2.metric("Proteine", f"{tm['prot']} g")
        m3.metric("Carboidrati", f"{tm['carb']} g")
        m4.metric("Grassi", f"{tm['fat']} g")

    st.write("")
    st.subheader("🍽️ Il Tuo Piano Alimentare")
    
    stile_curr = st.session_state.get("stile", "Onnivoro")
    allergie_curr = st.session_state.get("allergie", [])

    for slot, meal in list(st.session_state.day_plan.items()):
        icona = ICONE_SLOT.get(slot, "🍴")
        t = meal["totali"]
        
        # Scheda del pasto
        st.markdown(f"""
        <div class="meal-card">
            <h3 style="margin:0 0 10px 0; color:#1a5f3f;">{icona} {slot} — {meal['nome']}</h3>
            <p style="margin:0 0 10px 0; font-size:0.9rem; color:#666;">⏱️ Tempo: <b>{meal['tempo']} min</b> | <i>{meal['nota']}</i></p>
            <div>
                <span class="macro-badge macro-kcal">🔥 {t['kcal']:.0f} kcal</span>
                <span class="macro-badge">🥩 P: {t['prot']:.0f}g</span>
                <span class="macro-badge">🌾 C: {t['carb']:.0f}g</span>
                <span class="macro-badge">🥑 G: {t['fat']:.0f}g</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_actions1, col_actions2, col_actions3 = st.columns([1, 1, 1])
        
        # Action 1: Cambia Singolo Piatto
        with col_actions1:
            if st.button(f"🔄 Cambia {slot}", key=f"swap_{slot}"):
                pool = RICETTE_COLAZIONE if "Colazione" in slot else (RICETTE_SPUNTINO if "Spuntino" in slot else RICETTE_PRINCIPALI)
                usate = {m["nome"] for m in st.session_state.day_plan.values()}
                target_kcal = st.session_state.day_targets[slot]["kcal"]
                st.session_state.day_plan[slot] = genera_pasto(pool, target_kcal, stile_curr, allergie_curr, usate)
                salva_dati_locali({
                    "day_plan": st.session_state.day_plan, "target_macros": st.session_state.target_macros,
                    "day_targets": st.session_state.day_targets, "info_calcolo": st.session_state.info_calcolo,
                    "stile": stile_curr, "allergie": allergie_curr
                })
                st.rerun()

        # Visualizzazione Espandibile: Ingredienti & Istruzioni
        with st.expander(f"🛒 Ingredienti e Preparazione per {slot}"):
            st.markdown("**Istruzioni:** " + meal["istruzioni"])
            st.divider()
            st.write("**Lista Ingredienti:**")
            
            # Sostituzione singoli ingredienti
            nuova_lista = []
            for idx, (ing_nome, ing_grammi) in enumerate(meal["ingredienti"]):
                c_ing1, c_ing2 = st.columns([2, 2])
                with c_ing1:
                    st.write(f"• **{ing_nome}**: {ing_grammi} g")
                with c_ing2:
                    # Sostituzione dinamica alimento
                    cat_attuale = FOODS.get(ing_nome, {}).get("cat", "")
                    opzioni_simili = [f for f, d in FOODS.items() if d.get("cat") == cat_attuale]
                    if not opzioni_simili:
                        opzioni_simili = list(FOODS.keys())
                    
                    nuovo_ing = st.selectbox(
                        f"Sostituisci {ing_nome}", 
                        opzioni_simili, 
                        index=opzioni_simili.index(ing_nome) if ing_nome in opzioni_simili else 0,
                        key=f"sub_{slot}_{idx}"
                    )
                    
                    if nuovo_ing != ing_nome:
                        # Ricalcola i grammi per mantenere uguali le Kcal dell'ingrediente sostituito
                        kcal_orig = (FOODS[ing_nome]["kcal"] / 100.0) * ing_grammi
                        nuovi_g = max(round((kcal_orig / FOODS[nuovo_ing]["kcal"]) * 100.0), 1)
                        nuova_lista.append((nuovo_ing, nuovi_g))
                    else:
                        nuova_lista.append((ing_nome, ing_grammi))
            
            # Aggiorna se un ingrediente è stato sostituito
            if nuova_lista != meal["ingredienti"]:
                st.session_state.day_plan[slot]["ingredienti"] = nuova_lista
                st.session_state.day_plan[slot]["totali"] = totali_ingredienti(nuova_lista)
                salva_dati_locali({
                    "day_plan": st.session_state.day_plan, "target_macros": st.session_state.target_macros,
                    "day_targets": st.session_state.day_targets, "info_calcolo": st.session_state.info_calcolo,
                    "stile": stile_curr, "allergie": allergie_curr
                })
                st.rerun()

    st.divider()
    if st.button("🗑️ Rimuovi e Ricomincia"):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()
        
