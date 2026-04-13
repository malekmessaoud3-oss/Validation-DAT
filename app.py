import streamlit as st
import pandas as pd
from docx import Document
import io

# ================================
# UI
# ================================
st.set_page_config(page_title="Validateur DAT", layout="centered")

st.title("🛡️ Validateur de DAT")
st.write("Uploadez votre document (Word ou PDF) pour analyse technique.")

# ================================
# UPLOAD
# ================================
uploaded_file = st.file_uploader(
    "Choisir un fichier DAT",
    type=["docx", "pdf"]
)

# ================================
# TRAITEMENT
# ================================
if uploaded_file is not None:

    st.success("Fichier reçu ✔️")

    texte = ""

    # ================================
    # LECTURE WORD
    # ================================
    if uploaded_file.name.endswith(".docx"):

        with st.spinner("Lecture du document Word en cours..."):
            doc = Document(uploaded_file)
            texte = "\n".join([para.text for para in doc.paragraphs])

        st.subheader("📄 Contenu du document")
        st.text_area("", texte, height=300)

    # ================================
    # PDF (non traité ici)
    # ================================
    elif uploaded_file.name.endswith(".pdf"):
        st.warning("Lecture PDF non implémentée pour le moment")

    # ================================
    # SIMULATION ANALYSE DAT
    # ================================
    with st.spinner("Analyse technique du DAT en cours..."):

        data = {
            "Point de Contrôle": [
                "Sécurité Réseau",
                "Stockage Données",
                "Scalabilité",
                "Sauvegarde",
                "Accès Applicatif"
            ],
            "Statut": [
                "Conforme",
                "À vérifier",
                "Conforme",
                "Conforme",
                "À vérifier"
            ],
            "Commentaire": [
                "DMZ bien isolée",
                "Chiffrement non précisé",
                "Auto-scaling activé",
                "Backup quotidien OK",
                "Contrôle d’accès partiel"
            ]
        }

        df = pd.DataFrame(data)

    st.success("Analyse terminée ✔️")

    st.subheader("📊 Résultat de l'analyse")
    st.table(df)

    # ================================
    # EXPORT EXCEL
    # ================================
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.download_button(
        "📥 Télécharger l'analyse Excel",
        data=output,
        file_name="Analyse_DAT.xlsx"
    )
