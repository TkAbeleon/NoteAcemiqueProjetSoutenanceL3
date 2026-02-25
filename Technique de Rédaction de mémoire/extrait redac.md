
# Plateforme intelligente de suivi des feux de brousse et de la déforestation à Madagascar
---
# ***Jery Motro**

---
1. Problématique:
On sait tous que Madagascar s'appelle *"Nosy Maitso"*  auparavant mais aujourd’hui on l'appelle *"Nosy Mena"* . Madagascar fait face depuis plusieurs décennies à une **dégradation environnementales accélérée**, causé principalement par des feux de brousse, le *"tavy"* et l'exploitation abusive de la forêt. Ces phénomène ont des conséquences directes sur la biodiversité ubique de l'île, la fertilité de sols, la sécurité alimentaire, climat local et l'avenir des génération à venir.

Selon les données issues de programmes satellitaire internationaux **MODIS** et **VIIRS**, plusieurs milliers de point de feux sont détecté chaque année sur le territoire malgache. Malgré cette donnée à l’échelle mondiale, **l'exploitation local est presque inexistant**. Les principales causes sont:
- l'absence de plateforme adaptée au contexte local,
- le manque d'outils d'analyse automatisé accessibles,
- la difficulté pour les non spécialiste de comprendre les donnée
Ainsi, le problème centrale est comme suit:
> **Comment concevoir une plateforme intelligente capable de transformer des données satellitaires brutes en informations pertinentes, exploitables et compréhensibles pour le suivi des feux de brousse et de la déforestation à Madagascar ?**
> La solutions consiste à concevoir une plateforme intelligent ***Jery Motro*** intégrés, capable d'automatiser la collecte, le traitement, analyse et visualisation de données satellitaires brutes afin de produire des informations fiables, compréhensibles et exploitables pour tous les mondes. Les analyse peut être ensuite utiliser pour la détection des feux de brousses et les suivi de la déforestions à Madagascar.

- Description de la solution proposé:
	***Jery Motro*** repose sur une **plateforme intélligent modulaire**, en combinant:
	- Collecte autoamtiques des données satellitaires
		- Données ouvetes (NASA FIRMS, MODIS, VIIRS, Sentinel)
		- Image brutes et les données géospatilaes
		- Mise à jour péridiques des données
- Traitement intelligent et analyse par IA:
	- Nettoyage et normalisations des données
	- Détection automatique:des feux actifs, des zones brûlées, des zones de déforestations
	- Utilisations de machine learning pur la classifications, Deep
-  Transformations des résultats en information exploitables:
	- L'IA génératives analyse le résultats et donne un rapport et aide à la prise de décision et pour faire des alertes automatique


1. Méthodologie:
	Le projet repose d’abord sur la **collecte de données factuelles issues des satellites**, sans intervention de l’intelligence artificielle. Des APIs ouvertes telles que NASA FIRMS, NASA Earthdata, Copernicus Sentinel Hub et Hansen Global Forest Change permettent de récupérer des informations fiables sur les feux de brousse et l’évolution du couvert forestier à Madagascar. Ces données fournissent des éléments objectifs comme les coordonnées GPS, les dates, l’intensité thermique et les changements forestiers, constituant ainsi une base scientifique solide.
	
	Dans un second temps, ces données sont **prétraitées et analysées à l’aide du Machine Learning et du Deep Learning**. Les modèles de Machine Learning (Random Forest, SVM, régression) permettent de classifier les zones, détecter les changements temporels et établir des corrélations entre feux et déforestation. Le Deep Learning, utilisé comme axe d’évolution, affine cette analyse par la segmentation d’images satellites et la prédiction des zones à risque. L’ensemble du processus est automatisé grâce à n8n, qui orchestre la collecte, l’analyse et la mise à jour continue des résultats.
	
	Enfin, les résultats techniques sont **interprétés par une IA générative**, dont le rôle n’est pas d’analyser les données brutes mais de transformer les sorties des modèles en informations compréhensibles. Cette couche permet de produire des rapports, des synthèses régionales et des alertes intelligentes destinées aux décideurs. Ainsi, le projet agit comme un pont entre données scientifiques complexes et aide à la décision, en fournissant une vision claire et exploitable de la situation des feux de brousse à Madagascar.


[[think_tonk]]
 

2. Résultats:
3. Référence:

> [!NOTE]
> 
> Alliot, J.-M., Schiex, T., Garcia, F., & Brisset, P. (2002). Intelligence artificielle et informatique théorique. Cépaduès éditions.
> 
> Géron, A. (2019). Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems. O'Reilly.
> 
> Géron, A. (2022). Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems. O'Reilly.
> 
> Jakobowicz, E. (2018). Python pour le data scientist: Des bases du langage au machine learning. Dunod.
> 
> scikit-learn: machine learning in Python — scikit-learn 1.8.0 documentation. https://scikit-learn.org/stable/. Consulté le 6 février 2026
> 
> NumPy. https://numpy.org/. Consulté le 6 février 2026.
> 
> Numpy and Scipy Documentation — Numpy and Scipy documentation. https://docs.scipy.org/doc/. Consulté le 6 février 2026.
> 
> Matplotlib documentation — Matplotlib 3.10.8 documentation. https://matplotlib.org/stable/. Consulté le 6 février 2026.
> 
> pandas documentation — pandas 3.0.0 documentation. https://pandas.pydata.org/docs/. Consulté le 6 février 2026.
> 
> NASA-FIRMS. https://firms.modaps.eosdis.nasa.gov/map/. Consulté le 6 février 2026.
> 
> CSIR AFIS Map Viewer. https://viewer.afis.co.za/map. Consulté le 6 février 2026.
> 
> Fire Alarms, Security Systems Concord | Security System Company. https://www.rfscanada.ca/. Consulté le 6 février 2026


## 1️⃣ **NASA FIRMS (Fire Information for Resource Management System)**

🔹 **Organisme** : NASA  
🔹 **Sujet** : Détection des feux de végétation  
🔹 **Données** : MODIS, VIIRS  
🔹 **Fonction** : Feux quasi temps réel, cartes, CSV, API

👉 **Ton projet est une version académique locale de FIRMS**, focalisée sur Madagascar + ML.

---

## 2️⃣ **Global Forest Watch – Fires**

🔹 **Organisme** : World Resources Institute (WRI)  
🔹 **Sujet** : Feux + déforestation  
🔹 **Fonction** :

- Suivi des feux
    
- Impact sur les forêts
    
- Alertes environnementales
    

👉 Très proche de ton projet si tu ajoutes la déforestation après.

---

## 3️⃣ **Global Forest Watch – Deforestation Monitoring**

🔹 **Organisme** : WRI  
🔹 **Sujet** : Perte de couverture forestière  
🔹 **Données** : Landsat, Sentinel  
🔹 **Indicateurs** : Tree cover loss

👉 C’est l’équivalent **déforestation** de ton projet.

---

## 4️⃣ **GFED – Global Fire Emissions Database**

🔹 **Organisme** : NASA / Universités  
🔹 **Sujet** : Feux de végétation et émissions  
🔹 **Fonction** :

- Analyse historique des feux
    
- Intensité, superficie brûlée
    

👉 Projet scientifique très proche (mais plus avancé).

---

## 5️⃣ **Copernicus Emergency Management Service (EMS)**

🔹 **Organisme** : Union Européenne  
🔹 **Sujet** : Feux, catastrophes naturelles  
🔹 **Données** : Sentinel  
🔹 **Fonction** :

- Cartes des zones brûlées
    
- Analyse post-incendie
    

👉 Ton projet = version étudiante de ce service.

---

## 6️⃣ **MAAP – Monitoring of the Andean Amazon Project**

🔹 **Organisme** : Amazon Conservation  
🔹 **Sujet** : Déforestation + feux  
🔹 **Fonction** :

- Détection automatique
    
- Cartes interactives
    
- Analyses locales
    

👉 Très proche dans la **philosophie** (analyse locale).

---

## 7️⃣ **Burned Area Products (MODIS MCD64A1)**

🔹 **Organisme** : NASA  
🔹 **Sujet** : Zones brûlées après incendie  
🔹 **Fonction** :

- Cartographie des surfaces brûlées
    
- Analyse environnementale
    

👉 Complément naturel à ton projet feux de brousse.

---

## 8️⃣ **African Wildfire Information System**

🔹 **Sujet** : Feux de végétation en Afrique  
🔹 **Fonction** :

- Surveillance continentale
    
- Statistiques régionales
    

👉 Ton projet = focus Madagascar (beaucoup plus précis).