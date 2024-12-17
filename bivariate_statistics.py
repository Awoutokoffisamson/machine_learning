import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

def afficher_statistiques_bivariees(data):
    # Titre principal en rouge
    st.markdown("<h1 style='color: red;'>Statistiques Bivariées</h1>", unsafe_allow_html=True)

    # Sélection des variables
    quantitative_columns = data.select_dtypes(include=['float64', 'int']).columns.tolist()
    qualitative_columns = data.select_dtypes(include=['object']).columns.tolist()

    # Titres de sélection de variables en rouge
    st.markdown("<h3 style='color: red;'>Choisissez la première variable</h3>", unsafe_allow_html=True)
    var1 = st.selectbox('', quantitative_columns + qualitative_columns, key='selectbox1')

    st.markdown("<h3 style='color: red;'>Choisissez la deuxième variable</h3>", unsafe_allow_html=True)
    var2 = st.selectbox('', quantitative_columns + qualitative_columns, key='selectbox2')

    # Vérification des types de variables
    if var1 in quantitative_columns and var2 in quantitative_columns:
        # Nuage de points
        st.markdown(f"<h3 style='color: red;'>Nuage de points entre {var1} et {var2}</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.scatter(data[var1], data[var2])
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        st.pyplot(fig)

        # Calcul et affichage de la corrélation
        correlation = data[[var1, var2]].corr().iloc[0, 1]
        st.write(f"Coefficient de corrélation : {correlation:.2f}")

    elif (var1 in qualitative_columns and var2 in quantitative_columns) or (var1 in quantitative_columns and var2 in qualitative_columns):
        # Diagramme en barres empilées
        st.markdown(f"<h3 style='color: red;'>Diagramme en barres entre {var1} et {var2}</h3>", unsafe_allow_html=True)
        if var1 in qualitative_columns:
            sns.countplot(data=data, x=var1, hue=var2)
        else:
            sns.countplot(data=data, x=var2, hue=var1)
        st.pyplot()

        # Tableau croisé
        st.markdown("<h3 style='color: red;'>Tableau croisé</h3>", unsafe_allow_html=True)
        cross_tab = pd.crosstab(data[var1], data[var2])
        st.write(cross_tab)

    elif var1 in qualitative_columns and var2 in qualitative_columns:
        # Tableau croisé et test du chi-deux
        st.markdown(f"<h3 style='color: red;'>Tableau croisé entre {var1} et {var2}</h3>", unsafe_allow_html=True)
        cross_tab = pd.crosstab(data[var1], data[var2])
        st.write(cross_tab)

        chi2, p, dof, expected = chi2_contingency(cross_tab)
        st.write(f"Valeur du test de Chi-deux : {chi2:.2f}, p-value : {p:.4f}")
