import streamlit as st
from accueil import afficher_accueil
from visualisation import afficher_visualisation
from prediction import afficher_prediction
import pandas as pd
import joblib

# Charger le modèle et les données
model = joblib.load('trained_model.pkl')  # Assurez-vous que le modèle est dans le même répertoire
data = pd.read_csv('Final_data.csv')  # Assurez-vous que le fichier CSV est dans le même répertoire
model_columns = joblib.load('model_columns.pkl')  # Charger les colonnes du modèle

# Configuration de la barre latérale
st.sidebar.image("https://cdn.pixabay.com/animation/2023/08/23/15/46/15-46-31-162_512.gif", use_column_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une page", ["Accueil", "Visualisation", "Prédiction"])

# Affichage de la page choisie
if page == "Accueil":
    afficher_accueil()
elif page == "Visualisation":
    afficher_visualisation(data)
elif page == "Prédiction":
    afficher_prediction()

# Ajouter du style CSS pour améliorer l'esthétique
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .stApp {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)
