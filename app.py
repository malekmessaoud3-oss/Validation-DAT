import streamlit as st
from docx import Document
from openai import OpenAI

st.set_page_config(page_title="Audit DAT IA", layout="centered")

st.title("🛡️ Audit DAT Intelligent")

# 🔑 IA client (Streamlit secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyser_dat(texte):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Tu es un expert en architecture IT et cybersécurité."
            },
            {
                "role": "user",
                "content": f"""
Analyse ce DAT :

Donne :
- résumé
- architecture
- risques sécurité
- flux réseau problématiques
- recommandations

DOCUMENT:
{texte}
"""
            }
        ]
    )

    return response.choices[0].message.content


# 📂 Upload fichier
uploaded_file = st.file_uploader("Uploader un DAT Word", type=["docx"])

if uploaded_file:

    doc = Document(uploaded_file)
    texte = "\n".join([p.text for p in doc.paragraphs])

    st.success("Fichier chargé ✔️")

    with st.spinner("Analyse IA en cours..."):
        resultat = analyser_dat(texte)

    st.subheader("🧠 Résultat IA")
    st.write(resultat)
