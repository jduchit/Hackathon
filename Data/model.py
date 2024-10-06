import random
import pandas as pd
import pickle

df = pd.read_csv('Data/planets_with_multilingual_descriptions.csv')
df_sample = df[df['Planet'].isin(['TOI-2406 b', 'Qatar-5 b', 'HD 191939 b', 'Kepler-1654 b', 'LTT 1445 A c', 'PH2 b', 'WASP-18 b', 'GPX-1 b', 'NGTS-15 b', 'XO-7 b', 'K2-216 b', 'HAT-P-61 b', 'HATS-70 b', 'KELT-24 b', 'Qatar-4 b'])]

with open('Data/knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)
with open('Data/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

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
    random_idx = random.choice(filtered_indices)
    random_distance = filtered_distances[filtered_indices.index(random_idx)]

    # Display the random closest planet
    print("\nRandom Closest Planet from df_sample:")
    print(f"Planet: {df.iloc[random_idx]['Planet']}")
    print(f"Distance: {random_distance:.2f}")
    print(f"Information: {df.iloc[random_idx]['Information']}\n")
    print(f"Description: {df.iloc[random_idx][f'description_{language}']}\n")
    
    return df.iloc[random_idx]['Planet']