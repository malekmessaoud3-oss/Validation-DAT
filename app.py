import streamlit as st
import pandas as pd
from docx import Document
import io

# ================================
# CONFIG UI
# ================================
st.set_page_config(page_title="Audit DAT", layout="centered")

st.title("🛡️ Audit Automatique de DAT")
st.write("Analyse technique automatique des documents d'architecture")

# ================================
# UPLOAD
# ================================
uploaded_file = st.file_uploader(
    "Uploader un DAT (Word ou PDF)",
    type=["docx", "pdf"]
)

# ================================
# ANALYSE
# ================================
if uploaded_file is not None:

    st.success("Fichier reçu ✔️")

    texte = ""

    # ============================
    # LECTURE WORD
    # ============================
    if uploaded_file.name.endswith(".docx"):

        with st.spinner("Lecture du document Word..."):
            doc = Document(uploaded_file)
            texte = "\n".join([p.text for p in doc.paragraphs])

        st.subheader("📄 Contenu extrait")
        st.text_area("", texte, height=250)

    # ============================
    # PDF (placeholder)
    # ============================
    elif uploaded_file.name.endswith(".pdf"):
        st.warning("Lecture PDF non encore implémentée")

    # ============================
    # ANALYSE INTELLIGENTE
    # ============================
    with st.spinner("Analyse du DAT en cours..."):

        score = 100
        risques = []
        commentaires = []

        t = texte.lower()

        # ============================
        # RÈGLES DE CONTRÔLE
        # ============================

        # Sécurité
        if "dmz" in t:
            commentaires.append("DMZ détectée ✔️")
        else:
            risques.append("DMZ non mentionnée")
            score -= 15

        if "firewall" not in t and "pare-feu" not in t:
            risques.append("Absence de firewall")
            score -= 15

        # Base de données
        if "database" in t or "base de données" in t:
            commentaires.append("Base de données identifiée ✔️")

        # Chiffrement
        if "chiffrement" not in t and "tls" not in t:
            risques.append("Chiffrement non mentionné")
            score -= 10

        # Backup
        if "backup" not in t and "sauvegarde" not in t:
            risques.append("Sauvegarde non documentée")
            score -= 10

        # Flux réseau dangereux (simple détection)
        if "internet" in t and "database" in t:
            risques.append("⚠️ Flux Internet direct vers base de données")
            score -= 25

    # ================================
    # RESULTATS
    # ================================
    st.success("Analyse terminée ✔️")

    st.metric("📊 Score de conformité DAT", f"{score}/100")

    # Risques
    st.subheader("⚠️ Risques détectés")

    if risques:
        for r in risques:
            st.error(r)
    else:
        st.success("Aucun risque majeur détecté")

    # Commentaires positifs
    st.subheader("✅ Éléments conformes")

    for c in commentaires:
        st.info(c)

    # ================================
    # TABLEAU RÉSUMÉ
    # ================================
    df = pd.DataFrame({
        "Indicateur": ["Score", "Risques", "Commentaires"],
        "Valeur": [score, len(risques), len(commentaires)]
    })

    st.subheader("📊 Synthèse")
    st.table(df)

    # ================================
    # EXPORT EXCEL
    # ================================
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.download_button(
        "📥 Télécharger le rapport Excel",
        data=output,
        file_name="Audit_DAT.xlsx"
    )
