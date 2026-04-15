import streamlit as st
from docx import Document
from openai import OpenAI, RateLimitError

st.set_page_config(page_title="Audit DAT IA", layout="centered")

st.title("🛡️ Audit DAT Intelligent")

# 🔑 IA client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ✅ Cache pour éviter appels multiples
@st.cache_data(show_spinner=False)
def analyser_dat(texte):

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"""
Tu es un expert en architecture IT et cybersécurité.

Analyse ce DAT et donne :
- résumé
- architecture
- risques sécurité
- flux réseau problématiques
- recommandations

DOCUMENT:
{texte}
"""
        )

        return response.output[0].content[0].text

    except RateLimitError:
        return "⚠️ Limite API atteinte. Réessaye dans quelques secondes."


# 📂 Upload fichier
uploaded_file = st.file_uploader("Uploader un DAT Word", type=["docx"])

if uploaded_file:

    doc = Document(uploaded_file)
    texte = "\n".join([p.text for p in doc.paragraphs])

    st.success("Fichier chargé ✔️")

    # ✅ Bouton pour éviter spam API
    if st.button("🔍 Lancer l’analyse"):

        with st.spinner("Analyse IA en cours..."):
            resultat = analyser_dat(texte)

        st.subheader("🧠 Résultat IA")
        st.write(resultat)
