import streamlit as st
from docx import Document
import pdfplumber
from openai import OpenAI

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Audit DAT IA", layout="centered")
st.title("🛡️ Audit Document Technique")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

    else:
        return ""

# ==============================
# ANALYSE IA
# ==============================
def analyse_dat(text):

    text = text[:12000]  # éviter dépassement token

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
Tu es un expert en architecture IT et cybersécurité.

Analyse ce document technique et fournis :

1. Résumé
2. Type d’architecture
3. Risques sécurité (critique / warning)
4. Analyse des flux réseau
5. Non conformités
6. Recommandations
7. Score global sur 100

DOCUMENT :
{text}
"""
    )

    return response.output[0].content[0].text


# ==============================
# UI
# ==============================
uploaded_file = st.file_uploader("Uploader un document (Word ou PDF)", type=["docx", "pdf"])

if uploaded_file:

    st.success("Fichier chargé ✔️")

    if st.button("🔍 Lancer l’analyse"):

        with st.spinner("Analyse en cours..."):

            texte = extract_text(uploaded_file)

            if not texte:
                st.error("Impossible de lire le fichier")
            else:
                resultat = analyse_dat(texte)

                st.subheader("📊 Résultat de l’analyse")
                st.write(resultat)
