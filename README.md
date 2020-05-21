# Blob Eating

Introduction
============

Nous avons décidé de faire un projet en deux parties, pour explorer les
deux aspects qui nous intéressaient dans ces simulations : le
machine-learning et l'effet de l'altruisme dans un environnement
compétitif.

En effet, la première partie se déroule dans un environnement plus
simple et petit qui permet de simuler des échanges et des relations
personnelles entre les blobs.

La seconde partie se déroule dans un environnement plus large qui permet
de brasser d'importantes générations et de raffiner leur intelligences.

Inspiré de [cette vidéo](https://www.youtube.com/watch?v=lFEgohhfxOA).


L'apprentissage sur trois critères de survie
============================================

Ici, nous étudions des blobs qui ont plusieures actions possibles : 

* avancer
* tourner sur eux même
* manger
* se reproduire

dans un univers continu dans lequel une source de nourriture se déplace en cercle de façon régulière, avec une intensité qui diminue à mesure qu'on s'en éloigne. L'univers donne aux blobs à chaque tic des informations minimales :

* la quantité de nourriture là où ils se trouvent
* leur angle par rapport au gradient de la nourriture
* un couple avec le blob le plus proche et sa distance (s'il y en a un assez proche)
* leur propre niveau d'énergie

Et les blobs y réagissent à l'aide de leur cerveau qui renvoie une action à l'univers. Il existe deux types de cerveaux : le SmartBrain et le RandomBrain. Ils ont comme caractérisitiques trois paramêtres : 

* eat_threshold: a partir de quelle quantité de nourriture ils mangent
* move_threshold: a partir de quelle quantité de nourriture ils se reproduisent
* reprod_energy_threshold: a partir de quel niveau d'énergie ils se reproduisent

Le Smart Brain permet de trouver 'à la main' des paramètres qui permettent au blob de survivre et ainsi de calibrer l'univers de façon à ce qu'une population stable
puisse se former. Sinon, on a soit des populations qui se multiplient exponentiellement sans s'améliorer, soit des populations qui meurent en quelques secondes.

Le Random Brain quand à lui permet de simuler l'apprentissage des 'blobs'. Le principe est que chaque blob est d'abord généré avec une valeur aléatoire pour chacun de ses paramètres et une variance associée. A ses descendants il transmet une valeur uniformément tirée autour de sa valeur, dans un intervalle de sa variance. L'idée donc est d'améliorer génétiquement ces paramêtres de génération en génération, par 'sélection naturelle' des blobs.

On introduit ensuite une notion d'époque : chaque simulation a une longueur limitée après laquelle le paramètre moyen des survivants estrécupéré et passé aux blobs de l'époque suivante, mais avec une variance moindre. Ainsi, époque après époque, les blobs convergent vers une population homogène et efficace.


Simulation d'interactions dans un jeu de captation de ressources 
================================================================

Dans [la première partie du projet](https://github.com/Ellana42/BlobEating), nous simulons des interactions entre
des blobs sur un plateau sur lequel on dispose aléatoirement de la
nourriture. L'objectif de départ était d'étudier les décisions et
stratégies des blobs, et en particulier d'observer le rôle de
l'altruisme. Nous avons donc mis en place un jeu de captation des
ressources, qui se joue en un certain nombre de tours prédéfini, au
cours desquels les blobs agissent de la manière suivante : les blobs se
déplacent vers la nourriture la plus proche, et lorsqu'un blob arrive
sur une case avec de la nourriture, il la stocke. A la fin du tour, le
sort de chaque blob dépend de son stock de nourriture. S'il n'a plus de
nourriture, il meurt ; s'il en a au moins deux unités, il se reproduit ;
s'il lui en reste encore après, il peut en donner à d'autres blobs ayant
survécu. Ce jeu avec survie permet d'observer l'évolution de la
population de manière dynamique.

Le point central de ce jeu est néanmoins la modélisation de l'altruisme
ou de l'égoïsme. Pour ce faire, nous avons créé une matrice de
connectivité (baptisée 'generosity matrix') dans laquelle le coefficient
i,j représente la probabilité que le blob i donne une unité de
nourriture au blob j s'il peut le faire. Celle-ci est construite à
partir de \"vecteurs de générosité\" attribués à chaque créature. Les
coefficients de la matrice sont initialisés, puis évoluent entre chaque
tour de manière à prendre en compte les tours précédents. Les blobs qui
ont reçu de la nourriture de la part d'un de leur compère au tour
précédent deviennent reconnaissants envers lui (ce qui augmente la
probabilité de don d'un certain coefficient aléatoire).

Enfin, la reproduction a lieu sous forme de duplication. Le nouveau blob
généré hérite des caractéristiques de son parent en ce qui concerne la
reconnaissance ('gratefulness'), mais son vecteur de générosité est
réinitialisé, et il y a une probabilité que ces caractéristiques mutent
('mutation probability'), c'est-à-dire qu'elles soient multipliées par
un coefficient appelé 'mutation intensity'.

Nous avons finalement créé des statistiques permettant d'évaluer et de
visualiser notamment l'ampleur de l'altruisme dans ce jeu. Nous
reviendrons plus en détail sur ce point lors de la soutenance.

Tout le code pour cette partie du projet est accessible sur Github à [cette adresse](https://github.com/Ellana42/BlobEating).
