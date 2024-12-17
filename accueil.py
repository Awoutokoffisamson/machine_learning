import streamlit as st
import base64

def afficher_accueil():
    # Charger l'image locale et l'encoder en Base64
    with open("logo6.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    # Appliquer le CSS avec l'image en fond et des styles modernes
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color:#00007F; /* Couleur du texte par défaut */
        }}
        .main-title {{
            font-size: 3.9rem;
            font-weight: bold;
            text-align: center;
            color: #00007F; /* Couleur blanche */
        }}
        .intro-text {{
            font-size: 1.7rem;
            text-align: center;
            font-weight: bold;
            color: #FF0000 ; /* Couleur blanche */
            margin-bottom: 50px;
        }}
        .section-header {{
            font-size: 2.6rem;
            font-weight: bold;
            text-align: left;
            color: #00007F; /* Couleur blanche */
            text-shadow: 1px 1px 3px #00007F; /* Ombre blanche */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenu de la page d'accueil
    st.markdown('<h1 class="main-title">Bienvenue dans l\'application de prédiction de l\'émission du  CO2</h1>', unsafe_allow_html=True)
    st.markdown('<p class="intro-text">Une application intuitive pour explorer et prédire la consommation de CO2.</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">🎯 Commencez dès maintenant !</h2>', unsafe_allow_html=True)
   