import streamlit as st
import pandas as pd
from docx import Document
import io

# ================================
# CONFIG UI
# ================================
st.set_page_config(page_title="Audit DAT", layout="centered")

st.title("🛡️ Audit Automatique de DAT")
st.write("Analyse technique et conformité des documents d'architecture")

# ================================
# UPLOAD
# ================================
uploaded_file = st.file_uploader(
    "Uploader un DAT (Word ou PDF)",
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

        with st.spinner("Lecture du document Word..."):
            doc = Document(uploaded_file)
            texte = "\n".join([p.text for p in doc.paragraphs])

    elif uploaded_file.name.endswith(".pdf"):
        st.warning("Lecture PDF non encore implémentée")

    texte_min = texte.lower()

    # ================================
    # 🔎 RESUME STRUCTURE DU DAT
    # ================================
    st.subheader("📄 Analyse complète du DAT")

    resume_points = []

    with st.spinner("Analyse du contenu en cours..."):

        # INFRA
        if "serveur" in texte_min or "server" in texte_min:
            resume_points.append(("✔ Architecture serveur identifiée", "success"))
        else:
            resume_points.append(("❌ Aucune architecture serveur clairement décrite", "error"))

        # RESEAU
        if "dmz" in texte_min:
            resume_points.append(("✔ Zone DMZ mentionnée", "success"))
        else:
            resume_points.append(("❌ DMZ non définie", "error"))

        if "firewall" in texte_min or "pare-feu" in texte_min:
            resume_points.append(("✔ Firewall présent", "success"))
        else:
            resume_points.append(("❌ Firewall absent", "error"))

        # DONNEES
        if "base de données" in texte_min or "database" in texte_min:
            resume_points.append(("✔ Base de données identifiée", "success"))
        else:
            resume_points.append(("❌ Base de données non décrite", "error"))

        # BACKUP
        if "backup" in texte_min or "sauvegarde" in texte_min:
            resume_points.append(("✔ Sauvegarde mentionnée", "success"))
        else:
            resume_points.append(("❌ Sauvegarde absente", "error"))

        # SECURITE
        if "tls" in texte_min or "ssl" in texte_min or "chiffrement" in texte_min:
            resume_points.append(("✔ Chiffrement des échanges présent", "success"))
        else:
            resume_points.append(("❌ Chiffrement non mentionné", "error"))

        # FLUX RISQUE
        if "internet" in texte_min and "database" in texte_min:
            resume_points.append(("⚠️ Flux Internet direct vers base de données détecté", "warning"))

    # AFFICHAGE
    for msg, level in resume_points:
        if level == "success":
            st.success(msg)
        elif level == "warning":
            st.warning(msg)
        else:
            st.error(msg)

    # ================================
    # SCORE GLOBAL
    # ================================
    score = 100

    for msg, level in resume_points:
        if level == "error":
            score -= 15
        elif level == "warning":
            score -= 25

    score = max(score, 0)

    st.metric("📊 Score de conformité DAT", f"{score}/100")

    # ================================
    # TABLEAU SYNTHÈSE
    # ================================
    df = pd.DataFrame({
        "Check": [p[0] for p in resume_points],
        "Statut": [p[1] for p in resume_points]
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
        "📥 Télécharger rapport Excel",
        data=output,
        file_name="Audit_DAT.xlsx"
    )
