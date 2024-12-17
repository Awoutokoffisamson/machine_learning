import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st

def afficher_carte(fichier_coordonnees):
    """
    Affiche une carte Folium interactive avec des marqueurs pour chaque point
    défini par les colonnes 'Latitude' et 'Longitude' dans le fichier Excel fourni.
    """
    # Titre en rouge
    st.markdown("<h2 style='color: red;'>Carte Interactive des Emplacements</h2>", unsafe_allow_html=True)

    # Charger le fichier Excel
    try:
        coord_data = pd.read_excel(fichier_coordonnees)
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}", key='load_error')
        return

    # Vérification que les colonnes nécessaires existent
    if 'Latitude' in coord_data.columns and 'Longitude' in coord_data.columns:
        # Centrer la carte sur la moyenne des coordonnées
        centre_lat = coord_data['Latitude'].mean()
        centre_lon = coord_data['Longitude'].mean()
        carte = folium.Map(location=[centre_lat, centre_lon], zoom_start=6)

        # Ajouter les marqueurs avec clustering pour une meilleure lisibilité
        marker_cluster = MarkerCluster().add_to(carte)
        for lat, lon in zip(coord_data['Latitude'], coord_data['Longitude']):
            folium.Marker(location=[lat, lon]).add_to(marker_cluster)

        # Afficher la carte dans Streamlit
        folium_static(carte)  # Sans le paramètre key
    else:
        st.error("Les colonnes 'Latitude' et 'Longitude' sont manquantes dans le fichier.", key='columns_error')
