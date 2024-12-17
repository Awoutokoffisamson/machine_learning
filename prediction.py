
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from multi_prediction import afficher_multi_prediction

import base64

# Charger le modèle et les colonnes sauvegardées
model = joblib.load('trained_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Charger les données pour les sélecteurs
data = pd.read_csv('Final_data.csv')

def afficher_prediction():
    # Charger l'image locale et l'encoder en Base64
    with open("logo4.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    # Appliquer le CSS pour le fond d'écran et les styles de texte
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: #FFFFFF; /* Couleur de texte par défaut */
        }}
        .stApp::before {{
            content: "";
            background: rgba(0, 0, 0, 0.5); /* Fond semi-transparent */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}
        .main-title {{
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: #000000; /* Couleur noire pour le titre */
            margin-top: 20px;
        }}
        .sub-text {{
            font-size: 1.2rem;
            text-align: center;
            color: #FFD700; /* Couleur blanche pour le sous-titre */
        }}
        .stNumberInput, .stSelectbox, .stTextInput {{
            color: #FFFFFF; /* Couleur blanche pour les entrées de texte */
            background-color: #333333; /* Couleur de fond pour les entrées de texte */
            border: 1px solid #FFFFFF; /* Bordure pour les entrées de texte */
            padding: 10px; /* Espacement pour les entrées de texte */
        }}
        .stNumberInput label, .stSelectbox label, .stTextInput label {{
            color: #FFFFFF; /* Couleur blanche pour les labels */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titre principal avec styles
    st.markdown('<h1 class="main-title">🔮 Prédiction de la consommation de CO2</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Veuillez entrer les informations ci-dessous pour générer une prédiction.</p>', unsafe_allow_html=True)

    # Formulaire pour entrer les valeurs
    st.markdown('<h3 style="color: #000000;">🏢 Informations sur le bâtiment</h3>', unsafe_allow_html=True)
    number_of_floors = st.number_input('Nombre d\'étages', min_value=1, max_value=100, value=10)
    number_of_buildings = st.number_input('Nombre de bâtiments', min_value=1, max_value=100, value=5)
    property_gfa_building = st.number_input('Surface totale du bâtiment (GFA)', min_value=1, max_value=100000, value=5000)
    property_gfa_parking = st.number_input('Surface du parking (GFA)', min_value=1, max_value=100000, value=1000)
    energystar_score = st.number_input('Score ENERGY STAR', min_value=0, max_value=100, value=50)
    site_eui = st.number_input('Site EUI (kBtu/sf)', min_value=0, max_value=1000, value=200)
    largest_property_use_type_gfa = st.number_input('Plus grande utilisation du bâtiment (GFA)', min_value=1, max_value=100000, value=10000)
    electricity_kbtu = st.number_input('Consommation d\'électricité (kBtu)', min_value=0, max_value=1000000, value=100000)
    natural_gas_kbtu = st.number_input('Consommation de gaz naturel (kBtu)', min_value=0, max_value=1000000, value=50000)
    ghg_emissions_intensity = st.number_input('Intensité des émissions GES', min_value=0.0, max_value=1000.0, value=200.0)
    building_type = st.selectbox('Type de bâtiment', data['BuildingType'].unique())
    neighborhood = st.selectbox('Quartier', data['Neighborhood'].unique())
    largest_use_type_encode = st.number_input('Encodage de l\'utilisation principale', min_value=0, max_value=100, value=10)
    building_age = st.number_input('Âge du bâtiment', min_value=0, max_value=100, value=30)

    # Préparer les données pour la prédiction
    input_data = {
        'NumberofFloors': number_of_floors,
        'NumberofBuildings': number_of_buildings,
        'PropertyGFABuilding(s)': property_gfa_building,
        'PropertyGFAParking': property_gfa_parking,
        'ENERGYSTARScore': energystar_score,
        'SiteEUIWN(kBtu/sf)': site_eui,
        'LargestPropertyUseTypeGFA': largest_property_use_type_gfa,
        'Electricity(kBtu)': electricity_kbtu,
        'NaturalGas(kBtu)': natural_gas_kbtu,
        'GHGEmissionsIntensity': ghg_emissions_intensity,
        'BuildingType': building_type,
        'Neighborhood': neighborhood,
        'largestUseType_encode': largest_use_type_encode,
        'BuildingAge': building_age
    }

    # Convertir les données en DataFrame
    input_df = pd.DataFrame(input_data, index=[0])
    input_df = pd.get_dummies(input_df, drop_first=True)

    # Ajouter les colonnes manquantes avec des zéros
    missing_cols = set(model_columns) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0

    # Réorganiser les colonnes
    input_df = input_df[model_columns]

    # Prédiction
    predicted_log_y = model.predict(input_df)
    predicted_co2 = np.exp(predicted_log_y)

    # Résultat
    print(predicted_co2)  # Ajoutez cette ligne pour déboguer
    st.markdown(f'<h2 style="color: #000000;">🌍 La consommation de CO2 prédite est : <strong>{predicted_co2[0]:.2f} kg CO2</strong></h2>', unsafe_allow_html=True)


# Ajouter la sous-section de prédiction multiple à la fin du formulaire existant
    afficher_multi_prediction()  # Appel de la fonction pour la prédiction multiple
# Assurez-vous d'appeler la fonction afficher_prediction() dans votre fichier main.py
if __name__ == "__main__":
    afficher_prediction()
