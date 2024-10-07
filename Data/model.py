import random
import pandas as pd
import pickle
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(f"Using PyInstaller base path: {base_path}")
    except Exception:
        base_path = os.path.abspath(".")
        print(f"Using default base path: {base_path}")

    full_path = os.path.join(base_path, relative_path)
    print(f"Attempting to load CSV from: {full_path}")
    return full_path

# List all files in the Data directory (debugging)
def list_data_files():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    data_path = os.path.join(base_path, 'Data')
    print(f"Checking Data directory: {data_path}")
    if os.path.exists(data_path):
        print("Files in Data directory:")
        for file in os.listdir(data_path):
            print(f"  - {file}")
    else:
        print("Data directory not found!")

# Call this before trying to load the CSV
list_data_files()

# Use this function when loading the CSV file
csv_path = resource_path('Data/planets_with_multilingual_descriptions.csv')
try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded CSV with {len(df)} rows")
except Exception as e:
    print(f"Error loading CSV: {str(e)}")
    sys.exit(1)

df_sample = df[df['Planet'].isin(['TOI-2406 b', 'Qatar-5 b', 'HD 191939 b', 'Kepler-1654 b', 'LTT 1445 A c', 'PH2 b', 'WASP-18 b', 'GPX-1 b', 'NGTS-15 b', 'XO-7 b', 'K2-216 b', 'HAT-P-61 b', 'HATS-70 b', 'KELT-24 b', 'Qatar-4 b'])]



# Load pickle file
model_path = resource_path('Data/knn_model.pkl')
try:
    with open(model_path, 'rb') as f:
        knn_model = pickle.load(f)
    print("Successfully loaded KNN model")
except Exception as e:
    print(f"Error loading KNN model: {str(e)}")
    sys.exit(1)

# Load pickle file
scaler_path = resource_path('Data/scaler.pkl')
try:
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    print("Successfully loaded scaler")
except Exception as e:
    print(f"Error loading scaler: {str(e)}")
    sys.exit(1)




def getPlanet(radious, density, temp, language):

    # New data for which we want to find neighbors
    new_data = {
        'Planet Size (Earths)': radious,
        'Planet Density': density,
        'Planet Temp (C)': temp
    }
    new_data_scaled = scaler.transform([list(new_data.values())])

    # Find the nearest neighbors from the full dataset
    distances, indices = knn_model.kneighbors(new_data_scaled)

    # Indices of sample planets
    sample_indices = df_sample.index.values

    # Filter the neighbors to include only those in df_sample
    filtered_indices = [idx for idx in indices[0] if idx in sample_indices]
    filtered_distances = [distances[0][i] for i, idx in enumerate(indices[0]) if idx in sample_indices]
    neigh = 15
    while not filtered_indices:
        # Find the closest planet in df_sample manually
        distances, indices = knn_model.kneighbors(new_data_scaled, n_neighbors=neigh)
        
        filtered_indices = [idx for idx in indices[0] if idx in sample_indices]
        filtered_distances = [distances[0][i] for i, idx in enumerate(indices[0]) if idx in sample_indices]
        if (neigh < 218):
            neigh += 5
        else :
            break

    # Select a random planet from the filtered list
    index = filtered_indices[0]
    distance = filtered_distances[filtered_indices.index(index)]

    # Display the random closest planet
    print("\nRandom Closest Planet from df_sample:")
    print(f"Planet: {df.iloc[index]['Planet']}")
    print(f"Distance: {distance:.2f}")
    print(f"Information: {df.iloc[index]['Information']}\n")
    print(f"Description: {df.iloc[index][f'description_{language}']}\n")
    
    return df.iloc[index][f'description_{language}'], df.iloc[index]['Planet']