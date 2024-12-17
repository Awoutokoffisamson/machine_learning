import pandas as pd
from io import BytesIO
import joblib
import streamlit as st

# Charger le modèle et les colonnes sauvegardées
model = joblib.load('trained_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Fonction pour traiter le fichier Excel téléchargé
def traiter_fichier_excel(uploaded_file):
    try:
        # Lire les données du fichier Excel
        data = pd.read_excel(uploaded_file)
        st.write("Fichier chargé avec succès!")

        # Vérifier si les colonnes nécessaires sont présentes
        if not set(model_columns).issubset(data.columns):
            st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(model_columns)}")
            return None

        # Sélectionner les colonnes nécessaires à la prédiction
        X = data[model_columns]
        return X
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier : {e}")
        return None

# Fonction pour effectuer des prédictions et créer un fichier Excel avec les résultats
def effectuer_predictions(X):
    # Effectuer les prédictions de CO2 pour chaque ligne du DataFrame
    predictions = model.predict(X)
    # Ajouter les prédictions au DataFrame
    X['Predicted_CO2_Emissions'] = predictions

    # Créer un fichier Excel avec les résultats (utilisation de openpyxl comme moteur)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:  # Utilisation de openpyxl
        X.to_excel(writer, index=False, sheet_name='Predictions')
    
    output.seek(0)  # Réinitialiser la position du curseur dans le flux mémoire
    return output

# Fonction pour afficher l'interface et gérer la soumission du fichier
def afficher_multi_prediction():
    st.markdown("<h3 style='color: red;'>Prédictions multiples pour plusieurs bâtiments</h3>", unsafe_allow_html=True)
    
    # Chargement du fichier Excel par l'utilisateur
    uploaded_file = st.file_uploader("Téléchargez un fichier Excel avec les données des bâtiments", type="xlsx")

    if uploaded_file:
        # Traiter le fichier et effectuer les prédictions
        X = traiter_fichier_excel(uploaded_file)
        if X is not None:
            if st.button("Effectuer les prédictions de CO2"):
                # Effectuer les prédictions
                output = effectuer_predictions(X)
                st.write("Les prédictions ont été effectuées avec succès !")

                # Télécharger le fichier avec les prédictions
                st.download_button(
                    label="Télécharger le fichier avec les prédictions",
                    data=output,
                    file_name="predictions_batiments.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
