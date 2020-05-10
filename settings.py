from math import pi

settings = {
    'universe_size': 1000,  # Univers carré de -universe_size / 2 à +universe_size/2
    'nb_blobs': 50,
    # Mouvement circulaire de la source de nourriture
    'food_radius': 250,  # Le cercle est centré en 0,0
    'food_omega': 2 * pi / 440,  # Vitesse de rotation en radian/tick
    # Si food_omega = 2 pi / n, on doit avoir n = 2 pi R / v avec v = vitesse moyenne cible du blob

    # Caractéristiques de la décroissance de la nourriture à partir du centre
    'food_strength': 100,  # Valeur à distance nulle
    'food_depletion_factor': 1,  # Quantité de nourriture = E / (1 + depletion * d)
    'cost_reproduction': 100,
    'nearest_blob_max_dist': 10,

    # Caractéritique des blobs
    'blob_initial_energy': 100,
    'blob_speed': 10,  # Distance parcourue par tick
    'blob_omega': 0.5, # Vitesse angulaire en radians / tick
    'energy_per_move': 1,  # Perte d'energie par déplacement
    'energy_per_rotate': 0.1, # Perte d'énergie par rotation

    # Brain
    'smartbrain_eat_threshold': 1,
    'smartbrain_move_threshold': 0.6,
}