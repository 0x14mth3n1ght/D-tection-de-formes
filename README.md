# Detection-de-formes

Il est intéressant qu'un ordinateur puisse reconnaître des formes dans une image : que ce soit en imagerie médicale, en
robotique, en numérisation de textes manuscrits, ou sur des postes de contrôle, on est amené à devoir trouver sur une
image des formes caractéristiques.

Pour cela, Paul Hough développe en 1962 une technique (brevetée par IBM), la « transformée de Hough », qui donne un
moyen efficace de détecter, avec précision, une forme paramétrique dans un échantillon de points. Elle permet notamment
de détecter efficacement les droites ou les cercles de rayon donné.

Alors que certaines techniques commencent par suivre des points de contour afin de les relier par diverses méthodes,
Hough propose d'accumuler des évidences sur la présence d'une forme définie au préalable. Cette méthode va se baser sur
une bijection entre l'espace de l'image et l'espace des paramètres de la forme cherchée.

Pour appliquer la transformée de Hough à une image de largeur l et de hauteur h, il faut d'abord créer un espace de Hough
dans lequel chaque point représentera un accumulateur.

Pour cela il faudra discrétiser l'espace, en abscisse de -π/2 à π/2, en ordonnée de -d à +d où d est la taille de la diagonale de
l'image.

Ainsi on crée un tableau dont chaque case sera un accumulateur. Pour cela, il faut faire un compromis entre :

-La précision de la détection

-La mémoire nécessaire aux accumulateurs

-Le temps de calcul

Pour chaque case (x ; y) repérée au pré-traitement, chaque case du tableau telle que ρ = x.cos(θ) + y.sin(θ) (à
l'approximation près) soit vérifiée.
Pour cela, on peut soit parcourir l'ensemble de l'espace (du tableau) et augmenter
l'accumulateur dans les cases qui vérifient l'égalité (en faisant attention à l'approximation selon la précision du quadrillage
choisi); ou bien on incrémente θ de 1 en 1, on calcule le ρ correspondant, et on augmente l'accumulateur (θ ; ρ).

Cette deuxième méthode peut être plus longue selon la façon d'accéder à la case (θ ; ρ) : si l'accès se fait récursivement
depuis la première case du tableau, il faudra parcourir pour chaque θ le tableau dans une grande partie.
Une fois cette étape terminée pour les points caractéristiques, l'espace de Hough devrait présenter des maxima
d'accumulateurs. On peut au choix chercher un nombre de maxima (un nombre de droites à trouver), ou bien fixer un seuil
que l'accumulateur doit dépasser pour que la droite passant par ce point soit significative.

Ici, les valeurs des accumulateurs sont représentées par une intensité de lumière. Plus la luminosité est élevée, plus la case
en question a reçu de votes de la part des points détectés par l'opérateur de détection de contours.
Un algorithme serait donc le suivant, dans le cas de la détection de droites :

Début

-Quantifier l'espace des paramètres avec un maximum et un minimum pour les 2 paramètres.

-Initialiser un tableau à 2 entrées à 0.

Pour chaque point (x;y) détecté par l'opérateur de détection de contours, pour θ variant entre ses extrema :

-Incrémenter la case ( θ , ρ = arrondi (x.cos(θ)+y.sin(θ)) )

Fin

À la fin de l'exécution, les valeurs des cases du tableau correspondent au nombre de points qui ont « voté » pour cette
droite (sans garantir que cette droite existe réellement dans l'image).

On pourra alors au choix, fixer un seuil de votes pour que la droite soit considérée par le programme, ou bien fixer un
nombre de droites à trouver et les récupérer par ordre décroissant de nombre de votes.
