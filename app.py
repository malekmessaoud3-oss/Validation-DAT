import streamlit as st
import pandas as pd

st.title("🛡️ Validateur de DAT")
st.write("Uploadez votre document pour une analyse technique automatique.")

uploaded_file = st.file_uploader("Choisir un fichier DAT (PDF)", type="pdf")

if uploaded_file is not None:
    st.success("Fichier reçu ! Analyse en cours...")

    data = {
        "Point de Contrôle": ["Sécurité Réseau", "Stockage Données", "Scalabilité"],
        "Statut": ["Conforme", "À vérifier", "Conforme"],
        "Commentaire": ["DMZ bien isolée", "Absence de précision sur le chiffrement", "Auto-scaling activé"]
    }

    df = pd.DataFrame(data)
    st.table(df)

    import io
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    st.download_button(
        "📥 Télécharger l'analyse Excel",
        data=output,
        file_name="Analyse_Architecture.xlsx"
    )
