from math import pi

settings = {
    'universe_size': 1000,  # Univers carré de -universe_size / 2 à +universe_size/2
    'nb_blobs': 200,
    # Mouvement circulaire de la source de nourriture
    'food_radius': 250,  # Le cercle est centré en 0,0
    'food_omega': 2 * pi / 700,  # Vitesse de rotation en radian/tick
    # Si food_omega = 2 pi / n, on doit avoir n = 2 pi R / v avec v = vitesse moyenne cible du blob

    # Caractéristiques de la décroissance de la nourriture à partir du centre
    'food_strength': 110,  # Valeur à distance nulle
    'food_depletion_factor': 1,  # Quantité de nourriture = E / (1 + depletion * d)
    'cost_reproduction': 0.5,  # Pourcentage d'énergie transférée à l'enfant
    'nearest_blob_max_dist': 10,

    # Caractéritique des blobs
    'blob_initial_energy': 200,
    'blob_speed': 10,  # Distance parcourue par tick
    'blob_omega': 0.5, # Vitesse angulaire en radians / tick
    'energy_per_move': 5,  # Perte d'energie par déplacement
    'energy_per_rotate': 2, # Perte d'énergie par rotation
    'energy_when_idle': 1, # Perte d'énergie dans le cas contraire (manger)
    'reproduction_maturity': 30,  # Age en ticks avant de pouvoir se reproduire

    # Brain
    'smartbrain_eat_threshold': 1,
    'smartbrain_move_threshold': 0.6,
    'smartbrain_reproduce_distance_threshold': 5,

    # RandomSmartBrain
    'randomsmartbrain_eat_threshold': 10,
    'randomsmartbrain_move_threshold': 4,
    'randomsmartbrain_reproduce_distance_threshold': 10,
}