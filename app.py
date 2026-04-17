import streamlit as st
from docx import Document
import pdfplumber
from openai import OpenAI, RateLimitError
import time

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Audit DAT IA", layout="centered")
st.title("🛡️ Audit Document Technique")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# SESSION (anti double clic)
# ==============================
if "running" not in st.session_state:
    st.session_state.running = False

# ==============================
# EXTRACTION TEXTE
# ==============================
def extract_text(file):

    if file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    elif file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    return ""

# ==============================
# DECOUPAGE TEXTE (anti limite)
# ==============================
def split_text(text, chunk_size=5000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ==============================
# APPEL IA AVEC RETRY
# ==============================
def call_ai(prompt):

    for i in range(3):
        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            return response.output[0].content[0].text

        except RateLimitError:
            time.sleep(3)

    return "⚠️ Limite API atteinte après plusieurs tentatives."

# ==============================
# ANALYSE COMPLETE
# ==============================
def analyse_dat(text):

    chunks = split_text(text, 5000)

    results = []

    for chunk in chunks:
        prompt = f"""
Tu es un expert en architecture IT et cybersécurité.

Analyse cette partie de document et donne :
- résumé
- risques
- problèmes
- recommandations

DOCUMENT:
{chunk}
"""
        result = call_ai(prompt)
        results.append(result)

    # 🔥 Synthèse finale
    final_prompt = f"""
Voici plusieurs analyses de parties d’un document technique.

Fais une synthèse globale avec :
- résumé global
- architecture
- risques majeurs
- non conformités
- recommandations
- score global sur 100

ANALYSES:
{''.join(results)}
"""

    return call_ai(final_prompt)

# ==============================
# UI
# ==============================
uploaded_file = st.file_uploader("Uploader un document (Word ou PDF)", type=["docx", "pdf"])

if uploaded_file:

    st.success("Fichier chargé ✔️")

    if st.button("🔍 Lancer l’analyse") and not st.session_state.running:

        st.session_state.running = True

        with st.spinner("Analyse IA en cours..."):

            texte = extract_text(uploaded_file)

            if not texte:
                st.error("Impossible de lire le fichier")
            else:
                resultat = analyse_dat(texte)

                st.subheader("📊 Résultat de l’analyse")
                st.write(resultat)

        st.session_state.running = False
