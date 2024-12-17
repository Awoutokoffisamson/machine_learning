import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV  # Importer GridSearchCV
from sklearn.ensemble import RandomForestRegressor  # Modèle de régression RandomForest
import joblib  # Pour sauvegarder le modèle
import os
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score  # Pour évaluer le modèle

# Définir le répertoire de travail
working_directory = r'C:\Users\SAMSON\Documents\ENSAE\co2_prediction_app'
os.chdir(working_directory)  # Changer le répertoire de travail

# Charger les données
data = pd.read_csv('Final_data.csv')  # Assurez-vous que le fichier est dans le répertoire de travail

# Sélectionner les variables explicatives et la variable cible
X = data[['NumberofFloors', 'NumberofBuildings', 'PropertyGFABuilding(s)',
           'PropertyGFAParking', 'ENERGYSTARScore', 'SiteEUIWN(kBtu/sf)',
           'LargestPropertyUseTypeGFA', 'NaturalGas(kBtu)',
           'GHGEmissionsIntensity', 'BuildingType',
           'Neighborhood', 'largestUseType_encode', 'BuildingAge']]  # Ajoutez ou modifiez les variables selon vos besoins

log_y = np.log(data['TotalGHGEmissions'])  # Variable cible

# Convertir les variables catégorielles en variables numériques
X_dummies = pd.get_dummies(X, drop_first=True)

# Sauvegarder les colonnes pour les futures prédictions
model_columns = X_dummies.columns.tolist()
with open('model_columns.pkl', 'wb') as f:
    joblib.dump(model_columns, f)

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_dummies, log_y, test_size=0.3, random_state=42)

# Définir les paramètres pour la recherche par grille
param_grid = {
    'n_estimators': [10, 50, 100, 300],
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10, 15],
    'min_samples_leaf': [1, 2, 4, 6]
}

# Créer le modèle RandomForest
model = RandomForestRegressor(random_state=42)

# Créer le GridSearchCV pour optimiser les hyperparamètres
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# Entraîner le modèle avec GridSearchCV
grid_search.fit(X_train, y_train)

# Meilleur modèle trouvé
best_model = grid_search.best_estimator_

# Prédictions sur l'ensemble de test
y_pred = best_model.predict(X_test)

# Évaluation du modèle
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred))
r2_test = r2_score(y_test, y_pred)

# Affichage des résultats
print("RMSE sur l'ensemble de test: ", np.round(rmse_test, 2))
print("Score R² sur l'ensemble de test: ", np.round(r2_test, 2))

# Sauvegarder le modèle avec joblib
joblib.dump(best_model, 'trained_model.pkl')

# Encapsuler les résultats dans un dictionnaire
results = {
    'rmse_test': rmse_test,
    'r2_test': r2_test,
    'best_params': grid_search.best_params_
}

# Sauvegarder les résultats avec joblib
joblib.dump(results, 'model_results.pkl')