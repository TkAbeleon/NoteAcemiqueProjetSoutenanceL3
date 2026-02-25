# BOT INTELLIGENT - IMPLÉMENTATION AVEC MATHÉMATIQUES AVANCÉES

## ARCHITECTURE COMPLÈTE DU SYSTÈME

---

# PARTIE I : FONDATIONS MATHÉMATIQUES DU BOT

## 1. MODÉLISATION PROBABILISTE DE L'ÉTAT DU JEU

### 1.1 Espace d'États comme Variété Discrète

**Définition formelle :**

L'espace d'états S peut être vu comme un graphe orienté (S, T) où :
- S = {(A, B) | A, B ⊂ V, A ∩ B = ∅} : configurations possibles
- T : S × Actions → S : fonction de transition
- |S| ≈ 3^1024 (chaque cellule peut être : vide, joueur A, joueur B)

**Métrique sur S :**

On définit une distance de Hamming généralisée :

d(s₁, s₂) = |{v ∈ V | state₁(v) ≠ state₂(v)}|

Cette métrique induit une topologie sur S permettant de définir :
- Voisinages d'états
- Continuité des fonctions d'évaluation
- Convergence des algorithmes d'apprentissage

### 1.2 Distribution de Probabilité sur les États Futurs

**Modèle de transition stochastique :**

P(s_{t+1} | s_t, a_t) = {
    1                           si déterministe
    π_adversaire(a' | s_t)      si on modélise l'adversaire
}

**Modèle d'adversaire bayésien :**

On maintient une distribution de croyance sur les stratégies adverses :

β(θ_adv) = P(θ_adv | historique)

mise à jour via règle de Bayes :

β'(θ) ∝ P(a_adv | θ) · β(θ)

où θ paramétrise la stratégie adverse (ex : vecteur de poids pour heuristique).

### 1.3 Fonction de Partition et Entropie

**Entropie de Shannon de l'état :**

H(s) = -Σ_a P(a|s) log P(a|s)

où P(a|s) est la distribution de politique actuelle.

**Interprétation :**
- H élevé → grande incertitude, exploration nécessaire
- H faible → politique convergée, exploitation

**Régularisation par entropie maximale :**

Dans l'apprentissage, on ajoute un terme :

J_reg(π) = J(π) + α·H(π)

favorisant l'exploration.

---

## 2. THÉORIE SPECTRALE DES GRAPHES APPLIQUÉE

### 2.1 Matrice d'Adjacence et Spectre

**Matrice d'adjacence A :**

Pour la grille complète :
A[i,j] = 1 si {v_i, v_j} ∈ E (voisins orthogonaux)

**Propriétés spectrales :**

Valeurs propres λ₁ ≥ λ₂ ≥ ... ≥ λ_n :
- λ₁ = 4 (grille infinie, ≈ 4 pour grande grille finie)
- λ_n ≈ -4
- Gap spectral : λ₁ - λ₂ mesure la connexité

### 2.2 Matrice Laplacienne et ses Propriétés

**Laplacien normalisé :**

L_norm = I - D^(-1/2) A D^(-1/2)

où D est la matrice de degrés.

**Valeurs propres du Laplacien :**

0 = μ₁ ≤ μ₂ ≤ ... ≤ μ_n ≤ 2

**Connectivité algébrique (Fiedler value) :**

μ₂ > 0 ⟺ graphe connexe

**Vecteur de Fiedler :**

Le vecteur propre v₂ associé à μ₂ donne une partition optimale du graphe :
- v₂[i] > 0 : nœud dans partition A
- v₂[i] < 0 : nœud dans partition B

**Application au jeu :**

On utilise le vecteur de Fiedler pour :
1. Détecter les "frontières naturelles" du territoire
2. Identifier les zones à défendre en priorité
3. Trouver les points de connexion critiques

### 2.3 Diffusion sur Graphe et Random Walks

**Matrice de transition d'une marche aléatoire :**

P = D^(-1) A

**Distribution stationnaire π :**

π^T P = π^T, avec π[i] ∝ deg(v_i)

**Temps de mélange :**

t_mix = inf{t : ||P^t(i,·) - π||_TV ≤ 1/4 pour tout i}

Lié aux valeurs propres : t_mix ≈ 1/(1 - λ₂)

**Commute time (temps de retour) :**

C(i,j) = temps moyen pour aller de i à j et revenir

Formule : C(i,j) = 2|E| · (L⁺[i,i] + L⁺[j,j] - 2L⁺[i,j])

où L⁺ est la pseudo-inverse de L.

**Application :**
- Mesurer la "distance effective" entre positions
- Évaluer l'accessibilité territoriale
- Prioriser les coups selon la centralité du graphe

### 2.4 Centralité et Mesures d'Importance

**Centralité de degré :**
C_deg(v) = deg(v)

**Centralité de proximité (closeness) :**
C_close(v) = 1 / Σ_u d(v,u)

**Centralité d'intermédiarité (betweenness) :**
C_bet(v) = Σ_{s≠v≠t} σ_st(v) / σ_st

où σ_st = nombre de plus courts chemins de s à t,
σ_st(v) = nombre passant par v.

**PageRank (centralité d'eigen) :**

PR(v) = (1-d)/N + d · Σ_{u→v} PR(u)/deg_out(u)

**Application au bot :**
- Évaluer l'importance stratégique de chaque position
- Pondérer les coups selon leur centralité
- Détecter les "hubs" territoriaux

---

## 3. GÉOMÉTRIE COMPUTATIONNELLE AVANCÉE

### 3.1 Diagramme de Voronoï Discret

**Définition :**

Pour des sites S = {s₁, ..., s_k} (points des joueurs), la cellule de Voronoï de s_i est :

Vor(s_i) = {v ∈ V | d(v, s_i) ≤ d(v, s_j) pour tout j}

où d est la distance Manhattan.

**Calcul par inondation (flood fill) :**

```
ComputeVoronoi(sites):
    voronoi = {}
    queue = PriorityQueue()
    
    for s_i in sites:
        queue.push((s_i, s_i, 0))  // (position, site_origine, distance)
    
    while queue:
        v, site, dist = queue.pop()
        
        if v in voronoi:
            continue
        
        voronoi[v] = site
        
        for u in neighbors(v):
            queue.push((u, site, dist+1))
    
    return voronoi
```

**Complexité :** O(|V| log |V|)

**Application :**
- Partitionnement territorial
- Estimation de l'influence de chaque joueur
- Détection des frontières contestées

### 3.2 Triangulation de Delaunay Discrète

**Dual du Voronoï :**

Le graphe de Delaunay D relie deux sites s_i, s_j si Vor(s_i) et Vor(s_j) sont adjacents.

**Propriétés :**
- Maximise l'angle minimum (évite triangles "étirés")
- Utile pour interpolation et maillage

**Application au jeu :**
- Détecter les "alliances naturelles" entre points
- Identifier zones vulnérables (grands triangles)
- Planifier extensions territoriales

### 3.3 Enveloppe Convexe et α-shapes

**Enveloppe convexe des points du joueur :**

Graham scan en O(n log n) :

```
ConvexHull(points):
    // Trier par angle polaire depuis point le plus bas
    p₀ = min(points, key=lambda p: (p.y, p.x))
    sorted_points = sort(points \ {p₀}, by=polar_angle(p₀))
    
    hull = [p₀, sorted_points[0]]
    
    for p in sorted_points[1:]:
        while len(hull) ≥ 2 and cross(hull[-2], hull[-1], p) ≤ 0:
            hull.pop()
        hull.append(p)
    
    return hull
```

**α-shapes (généralisation) :**

Pour α > 0, l'α-shape capture la "forme" des points avec résolution α :
- α = 0 : points individuels
- α = ∞ : enveloppe convexe
- α intermédiaire : forme "naturelle"

**Application :**
- Estimer le périmètre effectif du territoire
- Détecter les concavités (zones de faiblesse)
- Mesurer la "compacité" de la position

### 3.4 Médial Axis et Squelette

**Définition :**

Le medial axis (axe médian) d'une forme est l'ensemble des centres des cercles maximaux inscrits.

**Calcul via distance transform :**

```
MedialAxis(shape):
    // Distance transform : distance au bord
    dist = DistanceTransform(shape)
    
    // Maxima locaux = points de l'axe médian
    medial = {v | dist[v] ≥ dist[u] for all u in neighbors(v)}
    
    return medial
```

**Application :**
- Trouver les "routes principales" à l'intérieur du territoire
- Identifier les points stratégiques centraux
- Planifier défense/attaque le long de l'axe

---

## 4. TOPOLOGIE ALGÉBRIQUE APPROFONDIE

### 4.1 Homologie Persistante

**Motivation :**

L'homologie classique donne une information binaire (trou / pas trou).
L'homologie persistante suit l'évolution des trous à travers une filtration.

**Filtration :**

Une suite de sous-complexes K₀ ⊆ K₁ ⊆ ... ⊆ K_n

**Exemple - Filtration par distance :**

K_r = {cells σ | diam(σ) ≤ r}

**Persistance :**

Un trou né à K_r et mort à K_s a une persistance pers = s - r.

**Barcode et diagramme de persistance :**

Visualise les intervalles [r, s) pour chaque feature homologique.

**Application au jeu :**

1. Filtration par temps : K_t = points posés jusqu'au tour t
2. Détecte quand un cycle se forme (naissance)
3. Détecte quand il se ferme/remplit (mort)
4. Persistance = robustesse du trou

**Algorithme simplifié :**

```
PersistentHomology(filtration):
    barcodes = []
    boundary_matrix = []
    
    for t, sigma in enumerate(filtration):
        # Ajouter sigma à la matrice
        col = BoundaryColumn(sigma)
        
        # Réduction
        for i in range(len(boundary_matrix)):
            if low(col) == low(boundary_matrix[i]):
                col = col + boundary_matrix[i]  # mod 2
        
        if low(col) == -1:
            # Créateur de cycle
            barcodes.append((t, ∞))
        else:
            # Destructeur de cycle
            barcodes[low(col)] = (barcodes[low(col)][0], t)
        
        boundary_matrix.append(col)
    
    return barcodes
```

**Complexité :** O(n³) dans le pire cas, O(n²) en moyenne.

### 4.2 Homologie Relative et Exacte Sequences

**Homologie relative H_k(X, A) :**

Mesure les k-cycles dans X qui ne sont pas des cycles dans A.

**Suite exacte longue :**

... → H_k(A) → H_k(X) → H_k(X,A) → H_{k-1}(A) → ...

**Application :**
- X = territoire total
- A = bord du territoire
- H_k(X,A) détecte cycles intérieurs indépendants du bord

### 4.3 Cup Product et Ring Structure

**Cup product :**

$∪ : H^p × H^q → H^{p+q}$

donne une structure d'anneau à la cohomologie.

**Application (avancée) :**
- Détecter interactions entre cycles
- Mesurer "entrelacement" de structures topologiques

---

## 5. ANALYSE HARMONIQUE SUR GRAPHE

### 5.1 Transformée de Fourier sur Graphe

**Base orthonormée des vecteurs propres :**

Le Laplacien L a une décomposition spectrale :

L = Σᵢ λᵢ uᵢ uᵢ^T

où (λᵢ, uᵢ) sont valeurs/vecteurs propres.

**Transformée de Fourier sur graphe :**

Pour un signal f : V → ℝ,

f̂(λᵢ) = ⟨f, uᵢ⟩ = Σ_v f(v) uᵢ(v)

**Inverse :**

f(v) = Σᵢ f̂(λᵢ) uᵢ(v)

**Fréquences :**
- λᵢ petit : basses fréquences (variation lente)
- λᵢ grand : hautes fréquences (variation rapide)

### 5.2 Filtrage Spectral

**Filtre passe-bas :**

f_lp(v) = Σ_{λᵢ < λ_c} f̂(λᵢ) uᵢ(v)

lisse le signal.

**Filtre passe-haut :**

$f_hp(v) = Σ_{λᵢ > λ_c} f̂(λᵢ) uᵢ(v)$

extrait les détails.

**Application au potentiel φ :**

1. Calculer φ (champ d'influence)
2. Décomposer en fréquences : φ̂
3. Filtrer basses fréquences → tendances territoriales globales
4. Filtrer hautes fréquences → tactiques locales, frontières

### 5.3 Diffusion de Chaleur sur Graphe

**Équation de diffusion :**

∂φ/∂t = -L φ

**Solution :**

$φ(t) = e^{-tL} φ(0) = Σᵢ e^{-t λᵢ} ⟨φ(0), uᵢ⟩ uᵢ$

**Heat kernel :**

K_t(i,j) = Σ_k e^{-t λ_k} u_k(i) u_k(j)

**Application :**
- Propager influence avec décroissance naturelle
- Estimer accessibilité à temps t
- Lisser fonctions d'évaluation

---

## 6. THÉORIE DES JEUX AVANCÉE

### 6.1 Équilibre de Nash et Stratégies Mixtes

**Jeu bimatriciel (forme normale) :**

Joueurs : {1, 2}
Stratégies : A₁, A₂ (ensembles finis)
Payoffs : u₁(a₁, a₂), u₂(a₁, a₂)

**Stratégie mixte :**

σᵢ ∈ Δ(Aᵢ) : distribution de probabilité sur Aᵢ

**Équilibre de Nash :**

(σ₁*, σ₂*) tel que :
- u₁(σ₁*, σ₂*) ≥ u₁(σ₁, σ₂*) pour tout σ₁
- u₂(σ₁*, σ₂*) ≥ u₂(σ₁*, σ₂) pour tout σ₂

**Théorème (Nash, 1950) :**
Tout jeu fini possède au moins un équilibre en stratégies mixtes.

**Calcul via support enumeration ou Lemke-Howson.**

**Application :**
- Modéliser situations répétées
- Équilibrer exploration/exploitation
- Anticiper réponses adverses

### 6.2 Backward Induction et Sous-Jeux Parfaits

**Jeu extensif (arbre de jeu) :**

Ensemble de nœuds N, arêtes (actions), fonction de payoff terminale.

**Équilibre de sous-jeu parfait (SPE) :**

Stratégie qui forme un équilibre de Nash dans chaque sous-jeu.

**Backward induction (induction à rebours) :**

```
BackwardInduction(node):
    if node.is_terminal():
        return node.payoff
    
    if node.player == MAX:
        return max(BackwardInduction(child) for child in node.children)
    else:
        return min(BackwardInduction(child) for child in node.children)
```

Retourne valeur minimax et stratégie optimale.

### 6.3 Regret Minimization et No-Regret Learning

**Regret externe :**

R_T(a) = Σ_{t=1}^T (u(a, o_t) - u(a_t, o_t))

où a_t = action jouée, o_t = action adverse.

**Algorithme Regret Matching :**

```
RegretMatching(T):
    regrets = [0] * |A|
    strategy_sum = [0] * |A|
    
    for t in 1..T:
        # Stratégie proportionnelle au regret positif
        strategy = normalize(max(regrets, 0))
        strategy_sum += strategy
        
        # Jouer selon strategy
        a_t = sample(strategy)
        
        # Observer payoffs
        for a in A:
            regrets[a] += u(a, o_t) - u(a_t, o_t)
    
    return normalize(strategy_sum)  # stratégie moyenne
```

**Théorème :**
Regret moyen → 0 quand T → ∞.

Si les deux joueurs utilisent RM, convergence vers équilibre de Nash.

### 6.4 Counterfactual Regret Minimization (CFR)

**Extension pour jeux d'information imparfaite :**

CFR minimise le regret contrefactuel :

R_T(I, a) = Σ_{t | I_t = I} π^{-i}(I_t) · (u^i(σ_{I→a}, σ^{-i}) - u^i(σ))

où :
- I = information set
- π^{-i} = probabilité de reach par l'adversaire
- σ_{I→a} = jouer a à I, sinon suivre σ

**Application à notre jeu :**

Bien que jeu à information parfaite, CFR est utile si :
- On ne connaît pas parfaitement la stratégie adverse
- On modélise l'incertitude sur les coups futurs

---

## 7. OPTIMISATION CONVEXE ET NON-CONVEXE

### 7.1 Programmation Linéaire pour Stratégies Optimales

**Formulation LP pour jeu à somme nulle :**

Max joueur veut :
max v
s.t. Σ_j A[i,j] x_j ≥ v  pour tout i
     Σ_j x_j = 1
     x_j ≥ 0

Min joueur résout le dual.

**Algorithme du simplexe / points intérieurs.**

### 7.2 Descente de Gradient Stochastique

**Objectif :** Minimiser J(θ) = 𝔼[L(θ, data)]

**Algorithme SGD :**

```
SGD(θ₀, α, epochs):
    θ = θ₀
    
    for epoch in 1..epochs:
        for batch in shuffle(data):
            g = ∇_θ L(θ, batch)  # gradient stochastique
            θ = θ - α · g
    
    return θ
```

**Variantes :**
- **Momentum :** v_{t+1} = β·v_t + g_t, θ_{t+1} = θ_t - α·v_t
- **Adam :** Moments adaptatifs (m_t, v_t) pour chaque paramètre
- **RMSprop, AdaGrad, etc.**

### 7.3 Méthode du Lagrangien et KKT

**Problème avec contraintes :**

min f(x)
s.t. g_i(x) ≤ 0, i=1..m
     h_j(x) = 0, j=1..p

**Lagrangien :**

ℒ(x, λ, ν) = f(x) + Σᵢ λᵢ g_i(x) + Σⱼ νⱼ h_j(x)

**Conditions KKT (Karush-Kuhn-Tucker) :**

1. ∇f(x*) + Σᵢ λᵢ ∇g_i(x*) + Σⱼ νⱼ ∇h_j(x*) = 0
2. g_i(x*) ≤ 0
3. λᵢ ≥ 0
4. λᵢ g_i(x*) = 0 (complémentarité)

**Application :**
- Optimiser placement sous contraintes (ex : budget de coups)
- Trouver équilibres avec contraintes territoriales

### 7.4 Optimisation Combinatoire et Relaxations

**Problème du sac à dos (analogue) :**

Choisir k coups parmi n maximisant valeur totale.

**Relaxation LP :**
Autoriser fractions x_i ∈ [0,1] au lieu de {0,1}.

**Arrondi randomisé :**
Après résolution LP, arrondir probabilistiquement.

**Application au jeu :**
- Planification multi-coups
- Allocation de ressources (temps de calcul par zone)

---

# PARTIE II : ARCHITECTURE DU BOT

## 8. SYSTÈME MULTI-AGENTS ET DÉCOMPOSITION

### 8.1 Agents Spécialisés

**Architecture modulaire :**

```
Bot
├── TopologicalAgent       # Détection cycles, captures
├── TerritorialAgent       # Contrôle territorial, Voronoï
├── TacticalAgent          # Coups locaux, défense
├── StrategicAgent         # Planification long-terme
└── MetaAgent              # Arbitrage entre agents
```

**Communication inter-agents :**

Blackboard partagé :
- État global du jeu
- Évaluations partielles
- Recommandations de chaque agent

**Fusion des décisions :**

Vote pondéré :
action* = argmax_a Σᵢ wᵢ · score_i(a)

ou négociation via enchères.

### 8.2 Apprentissage Hiérarchique

**Hierarchical Reinforcement Learning :**

Politique de haut niveau : π_high : S → Goals
Politique de bas niveau : π_low : S × Goal → Actions

**Options framework (Sutton et al.) :**

Une option ω = (I_ω, π_ω, β_ω) :
- I_ω : ensemble d'initialisation
- π_ω : politique interne
- β_ω : condition de terminaison

**Application :**
- Options = "construire cycle", "défendre zone", "étendre territoire"
- Haut niveau choisit option
- Bas niveau exécute

---

## 9. REPRÉSENTATION PAR RÉSEAUX DE NEURONES

### 9.1 Architecture CNN pour Grille

**Entrée :** Grille 32×32 avec 3 canaux :
- Canal 0 : positions du bot (0/1)
- Canal 1 : positions adverses (0/1)
- Canal 2 : cases vides (0/1)

**Couches :**

```
Input: (32, 32, 3)
  ↓
Conv2D(64 filters, 3×3, ReLU)
  ↓
Conv2D(128 filters, 3×3, ReLU)
  ↓
Residual Blocks × N
  ↓
Conv2D(256 filters, 3×3, ReLU)
  ↓
Policy Head         Value Head
  ↓                    ↓
Conv2D(2, 1×1)      Conv2D(1, 1×1)
  ↓                    ↓
Flatten             GlobalAvgPool
  ↓                    ↓
Softmax(1024)       Tanh (scalar)
```

**Policy head :** Distribution π(a|s) sur actions
**Value head :** Évaluation V(s) de l'état

### 9.2 Residual Blocks (ResNet)

```
ResidualBlock(x):
    shortcut = x
    x = Conv2D(filters, 3×3, padding='same')(x)
    x = BatchNorm()(x)
    x = ReLU()(x)
    x = Conv2D(filters, 3×3, padding='same')(x)
    x = BatchNorm()(x)
    x = x + shortcut  # skip connection
    x = ReLU()(x)
    return x
```

**Avantage :** Entraînement profond sans gradient vanishing.

### 9.3 Attention Mechanism

**Self-attention pour grille :**

```
Attention(Q, K, V):
    scores = (Q · K^T) / √d_k
    weights = softmax(scores)
    return weights · V
```

**Multi-head attention :**

Parallélise h têtes d'attention avec projections différentes.

**Application :**
- Détecter relations long-range entre positions
- Identifier zones critiques
- Pondérer importance de chaque région

### 9.4 Graph Neural Networks (GNN)

**Représentation alternative :**

Au lieu de grille 2D, utiliser graphe explicite.

**Message passing :**

```
h_v^{(l+1)} = σ(W^{(l)} h_v^{(l)} + Σ_{u ∈ N(v)} M^{(l)}(h_u^{(l)}, e_{uv}))
```

où :
- h_v : représentation du nœud v
- e_{uv} : features de l'arête
- M : fonction de message

**Architectures :**
- Graph Convolutional Networks (GCN)
- GraphSAGE
- Graph Attention Networks (GAT)

**Avantage :**
- Exploite structure de graphe naturellement
- Invariant aux permutations des nœuds
- Généralise à grilles de tailles différentes

---

## 10. ALGORITHMES DE RECHERCHE AVANCÉS

### 10.1 MCTS avec RAVE et AMAF

**RAVE (Rapid Action Value Estimation) :**

Partage information entre mouvements similaires joués à différents moments.

**AMAF (All Moves As First) :**

Crédite un mouvement même s'il n'est pas joué immédiatement.

**Valeur combinée :**

Q_combined(s,a) = β(n) · Q_RAVE(s,a) + (1 - β(n)) · Q_MC(s,a)

où β(n) = √(k/(3n + k)), k constante.

### 10.2 Parallelization Strategies

**Root parallelization :**

Plusieurs threads indépendants font MCTS depuis la racine, puis fusionnent résultats.

**Tree parallelization :**

Threads partagent le même arbre avec verrous (locks).

**Leaf parallelization :**

Paralléliser les rollouts depuis feuilles.

**Virtual Loss :**

Pendant qu'un thread explore un nœud, ajouter temporairement une pénalité pour dissuader autres threads → réduire redondance.

### 10.3 Progressive Widening

**Problème :** Trop de branches possibles.

**Solution :** Limiter nombre d'enfants explorés à :

n_children ≈ k · N(s)^α

où N(s) = visites du nœud, α ∈ (0,1), k constante.

**Effet :** Concentration sur coups prometteurs.

### 10.4 Transposition Tables

**Problème :** États identiques atteignables par ordre différent.

**Solution :** Hash table état → évaluation.

**Zobrist hashing :**

```
hash(state) = ⊕_{v occupied} ZobristTable[v][player(v)]
```

où ⊕ = XOR, ZobristTable contient valeurs aléatoires pré-générées.

**Complexité hash :** O(1) incrémental (update = XOR).

---

## 11. APPRENTISSAGE PAR RENFORCEMENT PROFOND

### 11.1 AlphaZero Framework

**Architecture :**

Réseau de neurones f_θ : s → (p, v)
- p : vecteur de politique (probabilités sur actions)
- v : valeur scalaire estimée

**Entraînement par self-play :**

1. Générer partie via MCTS guidé par f_θ
2. À chaque état s_t, stocker (s_t, π_t, z_t) où :
   - π_t = distribution MCTS améliorée
   - z_t = résultat final ∈ {-1, 0, +1}
3. Optimiser loss :

L(θ) = (z - v)² - π^T log p + c·||θ||²

où premier terme = value loss, deuxième = policy loss, troisième = régularisation L2.

**Algorithme complet :**

```
AlphaZero():
    θ = InitializeNetwork()
    replay_buffer = []
    
    for iteration in 1..N:
        # Self-play
        for game in 1..M:
            trajectory = SelfPlay(θ)
            replay_buffer.extend(trajectory)
        
        # Training
        for epoch in 1..E:
            batch = sample(replay_buffer, batch_size)
            θ = θ - α · ∇_θ L(θ, batch)
        
        # Evaluation
        if WinRate(θ, θ_old) > threshold:
            θ_best = θ
    
    return θ_best
```

### 11.2 MuZero Extension

**Différence avec AlphaZero :**

Ne nécessite pas connaissance exacte du modèle de transition.

**Composants :**
- Representation function : h_θ(o₁, ..., o_t) → s
- Dynamics function : g_θ(s, a) → (r, s')
- Prediction function : f_θ(s) → (p, v)

**Apprentissage bout-en-bout :**

À partir d'observations brutes, apprendre représentation latente s et dynamique.

**Application :** Utile si on veut généraliser à variantes de règles.

### 11.3 Policy Gradient with Baseline

**REINFORCE with baseline :**

$∇_θ J(θ) = 𝔼_τ[Σ_t ∇_θ log π_θ(a_t|s_t) · (G_t - b(s_t))]$

où b(s_t) = baseline (réduit variance).

**Choix optimal de baseline :**

b*(s) = V^π(s) (fonction de valeur)

### 11.4 Proximal Policy Optimization (PPO)

**Objectif :**

L^{CLIP}(θ) = 𝔼_t[min(r_t(θ)Â_t, clip(r_t(θ), 1-ε, 1+ε)Â_t)]

où :
- r_t(θ) = π_θ(a_t|s_t) / π_θ_old(a_t|s_t)
- Â_t = avantage estimé
- ε ≈ 0.2

**Avantage :** Limite ampleur des mises à jour, stabilise apprentissage.

---

## 12. ÉVALUATION HEURISTIQUE SOPHISTIQUÉE

### 12.1 Features Géométriques

**Compacité (isopérimétrie) :**

C = 4π · Area / Perimeter²

Plus C est proche de 1, plus la forme est compacte (cercle = optimal).

**Moments géométriques :**

M₀₀ = Σ_v 𝟙{v occupé}  (masse)
M₁₀ = Σ_v x_v · 𝟙{v occupé}  (moment x)
M₀₁ = Σ_v y_v · 𝟙{v occupé}  (moment y)

Centre de masse : (x̄, ȳ) = (M₁₀/M₀₀, M₀₁/M₀₀)

**Moments centrés :**

μ₂₀ = Σ_v (x_v - x̄)² · 𝟙{v occupé}
μ₀₂ = Σ_v (y_v - ȳ)² · 𝟙{v occupé}
μ₁₁ = Σ_v (x_v - x̄)(y_v - ȳ) · 𝟙{v occupé}

**Axes principaux (via diagonalisation) :**

Matrice d'inertie $I = [μ₂₀  μ₁₁]$
                       $[μ₁₁  μ₀₂]$

Valeurs propres λ₁, λ₂ donnent élongation.
Ratio λ₁/λ₂ mesure anisotropie.

### 12.2 Features Topologiques

**Nombre de composantes connexes :**

Χ₀ = |{composantes du joueur}|

**Nombre de Betti :**

β₀ = nombre de composantes
β₁ = nombre de trous (cycles indépendants)

**Euler characteristic :**

χ = β₀ - β₁ + β₂

Pour graphe planaire : χ = V - E + F (formule d'Euler).

### 12.3 Features Spectrales

**Énergies spectrales du Laplacien :**

E_k = Σ_{i=1}^k λᵢ

mesure "énergie" concentrée dans k premières fréquences.

**Trace du heat kernel :**

Tr(K_t) = Σᵢ e^{-t λᵢ}

décroît exponentiellement, taux lié à la géométrie.

### 12.4 Features Probabilistes

**Probabilité de capture Monte Carlo :**

Estimer P(capture dans k coups) via simulations.

**Entropie positionnelle :**

H = -Σ_v P(occupation de v) log P(occupation de v)

où P est estimée par simulations.

---

## 13. META-STRATÉGIES ET ADAPTATION

### 13.1 Opponent Modeling

**Bayesian opponent model :**

Hypothèses H = {h₁, ..., h_n} sur stratégie adverse.

Prior : P(h_i)

Mise à jour après observation a_obs :

P(h_i | a_obs) ∝ P(a_obs | h_i) · P(h_i)

**Exploitation du modèle :**

Jouer best response contre la stratégie adverse estimée.

### 13.2 Portfolio of Algorithms

**Ensemble de bots :**

Bot_1 : agressif (maximise captures)
Bot_2 : défensif (minimise pertes)
Bot_3 : territorial (maximise aire Voronoï)
...

**Meta-learning :**

Apprendre quel bot utiliser contre quel type d'adversaire.

**Contextual bandits :**

Contexte = features de l'adversaire
Actions = choix de bot
Récompense = win rate

### 13.3 Online Learning and Adaptation

**Gradient descent on the fly :**

Après chaque partie :
θ ← θ + α · ∇_θ log π_θ(game) · (result - baseline)

**Experience replay :**

Buffer des N dernières parties, ré-entraîner périodiquement.

---

# PARTIE III : IMPLÉMENTATION SYSTÈME

## 14. ARCHITECTURE LOGICIELLE

### 14.1 Design Patterns

**State Pattern :**

```python
class GameState:
    def __init__(self, grid, current_player):
        self.grid = grid
        self.current_player = current_player
    
    def apply_action(self, action):
        new_grid = self.grid.copy()
        new_grid[action] = self.current_player
        return GameState(new_grid, 3 - self.current_player)
    
    def get_legal_actions(self):
        return [v for v in self.grid if self.grid[v] == 0]
```

**Strategy Pattern :**

```python
class EvaluationStrategy:
    def evaluate(self, state): pass

class TerritorialEvaluation(EvaluationStrategy):
    def evaluate(self, state):
        return compute_voronoi_advantage(state)

class TopologicalEvaluation(EvaluationStrategy):
    def evaluate(self, state):
        return count_potential_captures(state)
```

**Observer Pattern :**

Agents s'abonnent aux changements d'état.

### 14.2 Data Structures Optimales

**Bitboard representation :**

```python
class Bitboard:
    def __init__(self):
        self.player_A = 0  # 1024 bits
        self.player_B = 0
    
    def set_bit(self, pos, player):
        if player == 'A':
            self.player_A |= (1 << pos)
        else:
            self.player_B |= (1 << pos)
    
    def get_neighbors(self, pos):
        # Bit shifts pour voisins orthogonaux
        x, y = pos % 32, pos // 32
        neighbors = []
        if x > 0: neighbors.append(pos - 1)
        if x < 31: neighbors.append(pos + 1)
        if y > 0: neighbors.append(pos - 32)
        if y < 31: neighbors.append(pos + 32)
        return neighbors
```

**Union-Find avec compression :**

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.component_size = [1] * n
        self.component_edges = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            self.component_edges[root_x] += 1
            return
        
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.component_size[root_x] += self.component_size[root_y]
        self.component_edges[root_x] += self.component_edges[root_y] + 1
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
    
    def has_cycle(self, component_root):
        return self.component_edges[component_root] >= self.component_size[component_root]
```

### 14.3 Caching et Memoization

**LRU Cache pour évaluations :**

```python
from functools import lru_cache

@lru_cache(maxsize=100000)
def evaluate_state(state_hash):
    # Calculs coûteux
    return score
```

**Zobrist hashing :**

```python
import random

class ZobristHasher:
    def __init__(self, size=1024, players=2):
        self.table = [[random.getrandbits(64) for _ in range(players)] 
                      for _ in range(size)]
        self.hash_value = 0
    
    def toggle(self, pos, player):
        self.hash_value ^= self.table[pos][player]
    
    def get_hash(self):
        return self.hash_value
```

---

## 15. OPTIMISATIONS NUMÉRIQUES

### 15.1 Calcul Parallèle

**Numba JIT compilation :**

```python
from numba import jit, prange

@jit(nopython=True, parallel=True)
def compute_potential_field(grid, sources, alpha):
    n = len(grid)
    phi = np.zeros(n)
    
    for iteration in range(100):
        phi_new = phi.copy()
        for i in prange(n):
            if grid[i] == 0:  # case vide
                neighbor_sum = 0
                count = 0
                for j in neighbors[i]:
                    neighbor_sum += phi[j]
                    count += 1
                phi_new[i] = (sources[i] + neighbor_sum) / count
        
        phi = phi_new
    
    return phi
```

**Vectorisation avec NumPy :**

```python
# Au lieu de boucles
for i in range(n):
    result[i] = expensive_op(data[i])

# Utiliser
result = np.vectorize(expensive_op)(data)
# ou mieux, opérations natives NumPy
result = np.sum(data, axis=1)
```

### 15.2 Approximations et Heuristiques

**Early termination :**

Dans MCTS, arrêter rollout si :
- État clairement gagnant/perdant
- Profondeur max atteinte
- Temps épuisé

**Lazy evaluation :**

Ne calculer features coûteuses que si nécessaire.

**Approximation de distance :**

Distance Manhattan au lieu de Dijkstra quand acceptable.

### 15.3 Sparse Matrix Operations

**Pour Laplacien :**

```python
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

# Construire L en format sparse
L = csr_matrix((data, (row, col)), shape=(n, n))

# Résolution rapide
phi = spsolve(L, f)
```

---

## 16. TESTING ET VALIDATION

### 16.1 Unit Tests

**Tests de détection de cycle :**

```python
def test_cycle_detection():
    # Créer configuration avec cycle rectangulaire
    state = create_rectangle_cycle(top_left=(5,5), size=(3,3))
    
    cycle = detect_cycle(state)
    assert cycle is not None
    assert len(cycle) == 8  # périmètre 2*(3-1) + 2*(3-1)
    assert is_simple_cycle(cycle)
```

**Tests de Pick's theorem :**

```python
def test_picks_theorem():
    cycle = [(0,0), (4,0), (4,3), (0,3)]
    area = polygon_area(cycle)
    B = len(cycle)
    I = area - B/2 + 1
    
    # Rectangle 4×3 : aire = 12, B = 4, I = 12 - 2 + 1 = 11
    # Mais sommets intérieurs : (1,1), (1,2), (2,1), (2,2), (3,1), (3,2) = 6
    # Erreur : Pick compte points entiers, pas sommets grille
    # Correction nécessaire selon définition
```

### 16.2 Integration Tests

**Simulation de partie complète :**

```python
def test_full_game():
    bot1 = AlphaBot(model_path="model_v1.h5")
    bot2 = RandomBot()
    
    wins = 0
    for _ in range(100):
        result = play_game(bot1, bot2)
        if result == 1: wins += 1
    
    assert wins >= 80  # Bot devrait gagner au moins 80%
```

### 16.3 Performance Profiling

**Profiling Python :**

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code à profiler
for _ in range(1000):
    bot.choose_action(state)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**Identifier bottlenecks :**
- Cycle detection trop fréquent ?
- Calcul potentiel non optimisé ?
- MCTS insuffisamment parallélisé ?

---

## 17. DÉPLOIEMENT ET INTERFACE

### 17.1 API REST

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
bot = load_trained_bot()

@app.route('/move', methods=['POST'])
def get_move():
    state = request.json['state']
    action = bot.choose_action(state)
    return jsonify({'action': action})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    state = request.json['state']
    score = bot.evaluate(state)
    return jsonify({'score': score})
```

### 17.2 WebSocket pour Temps Réel

```python
import asyncio
import websockets

async def bot_handler(websocket, path):
    async for message in websocket:
        state = json.loads(message)
        action = await asyncio.to_thread(bot.choose_action, state)
        await websocket.send(json.dumps({'action': action}))

start_server = websockets.serve(bot_handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

### 17.3 Interface Graphique (Pygame)

```python
import pygame

class GameGUI:
    def __init__(self, size=32, cell_size=20):
        self.size = size
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((size*cell_size, size*cell_size))
        self.bot = AlphaBot()
    
    def draw_grid(self, state):
        for x in range(self.size):
            for y in range(self.size):
                color = {
                    0: (255, 255, 255),  # vide
                    1: (0, 0, 255),      # joueur 1
                    2: (255, 0, 0)       # joueur 2
                }[state.grid[x,y]]
                pygame.draw.rect(self.screen, color, 
                               (x*self.cell_size, y*self.cell_size, 
                                self.cell_size, self.cell_size))
    
    def run(self):
        running = True
        state = GameState.initial()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    action = (x // self.cell_size, y // self.cell_size)
                    if action in state.get_legal_actions():
                        state = state.apply_action(action)
                        # Bot joue
                        bot_action = self.bot.choose_action(state)
                        state = state.apply_action(bot_action)
            
            self.draw_grid(state)
            pygame.display.flip()
```

---

# PARTIE IV : RÉSULTATS ET ANALYSES

## 18. MÉTRIQUES D'ÉVALUATION

### 18.1 ELO Rating

**Système ELO pour classement :**

Après partie entre A (rating R_A) et B (rating R_B) :

E_A = 1 / (1 + 10^{(R_B - R_A)/400})

Si A gagne (S_A = 1) :
R_A' = R_A + K(S_A - E_A)

K = 32 typiquement (facteur d'apprentissage).

**Application :**
Suivre évolution du bot à travers versions/entraînements.

### 18.2 Analyse de Variabilité

**Win rate avec intervalle de confiance :**

p̂ ± z_{α/2} · √(p̂(1-p̂)/n)

où p̂ = taux de victoire empirique, n = nombre de parties.

Pour IC à 95% : z_{0.025} ≈ 1.96.

### 18.3 Courbes d'Apprentissage

**Plots à surveiller :**
- Win rate vs itérations
- Loss (policy + value) vs epochs
- Temps moyen par coup
- Profondeur moyenne de l'arbre MCTS
- Distribution des types de victoire (capture / territoire / timeout)

---

## 19. CONCLUSION ET PERSPECTIVES

### 19.1 Récapitulatif des Concepts Mathématiques Utilisés

1. **Théorie des graphes** : cycles, composantes, centralité
2. **Topologie algébrique** : homologie, persistance
3. **Géométrie computationnelle** : Voronoï, convexe, α-shapes
4. **Analyse spectrale** : Laplacien, Fourier sur graphe
5. **Théorie des jeux** : Nash, minimax, regret
6. **Optimisation** : convexe, combinatoire, gradient
7. **Apprentissage** : RL, deep learning, MCTS
8. **Probabilités** : MDP, bandits, bayésien

### 19.2 Extensions Possibles

**Multi-joueurs (>2) :**
- Coalition formation
- Shapley value pour attribution de gains

**Grilles non-régulières :**
- Graphes arbitraires
- Géométrie hyperbolique

**Information imparfaite :**
- Fog of war
- CFR adapté

**Apprentissage continu :**
- Meta-learning (apprendre à apprendre)
- Transfer learning vers variantes

### 19.3 Recherche Future

**Théorème de complexité :**

Prouver NP-complétude du problème :
"Étant donné état s, existe-t-il coup gagnant ?"

**Bornes théoriques :**

Trouver stratégie optimale avec complexité prouvée.

**Analogie avec Go :**

Notre jeu partage :
- Capture territoriale
- Topologie (cycles vs chaînes)
- Complexité combinatoire

Mais diffère par :
- Cycles explicites vs territoires émergents
- Captures binaires vs attrition graduelle

**Open problems :**
- Valeur du jeu depuis position vide ?
- Premier joueur a-t-il avantage forcé ?
- Existe-t-il stratégie gagnante polynomiale ?

---

# ANNEXES

## A. Pseudocode Complet du Bot
`py`
```py
class AdvancedBot:
    def __init__(self):
        self.neural_net = load_pretrained_network()
        self.union_find = UnionFind(1024)
        self.zobrist = ZobristHasher()
        self.transposition_table = {}
        self.potential_field_cache = {}
    
    def choose_action(self, state):
        # 1. Génération de candidats
        candidates = self.generate_candidate_moves(state)
        
        # 2. Filtrage rapide
        candidates = self.filter_suicidal_moves(candidates, state)
        
        # 3. Évaluation heuristique
        scores = []
        for action in candidates:
            score = self.quick_evaluate(state, action)
            scores.append((action, score))
        
        # 4. Sélection top-K
        top_k = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
        
        # 5. MCTS sur top-K
        best_action = None
        best_value = -inf
        
        for action, _ in top_k:
            value = self.mcts(state, action, simulations=1000)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    
    def mcts(self, state, root_action, simulations):
        # Implémentation MCTS complète
        root = MCTSNode(state.apply_action(root_action))
        
        for _ in range(simulations):
            node = root
            
            # Selection
            while node.is_fully_expanded() and not node.is_terminal():
                node = node.select_child_uct()
            
            # Expansion
            if not node.is_terminal():
                node = node.expand()
            
            # Simulation
            reward = self.guided_rollout(node.state)
            
            # Backpropagation
            while node is not None:
                node.update(reward)
                reward = -reward
                node = node.parent
        
        return root.value()
    
    def guided_rollout(self, state):
        depth = 0
        max_depth = 50
        
        while not state.is_terminal() and depth < max_depth:
            # Politique guidée par potentiel + réseau
            actions = state.get_legal_actions()
            policy, value = self.neural_net.predict(state)
            
            # Softmax sur subset
            probs = softmax([policy[a] for a in actions])
            action = np.random.choice(actions, p=probs)
            
            state = state.apply_action(action)
            depth += 1
        
        return state.get_reward()
    
    def quick_evaluate(self, state, action):
        # Features rapides
        phi = self.get_potential_field(state)
        
        features = {
            'potential': phi[action],
            'centrality': self.centrality[action],
            'capture_threat': self.count_capture_threats(state, action),
            'mobility': len(state.get_legal_actions())
        }
        
        # Combinaison linéaire
        weights = [2.0, 1.5, 3.0, 0.5]
        return sum(w * f for w, f in zip(weights, features.values()))
    
    def get_potential_field(self, state):
        hash_val = self.zobrist.get_hash()
        
        if hash_val in self.potential_field_cache:
            return self.potential_field_cache[hash_val]
        
        phi = self.solve_poisson(state)
        self.potential_field_cache[hash_val] = phi
        
        return phi
    
    def solve_poisson(self, state):
        # SOR solver
        n = 1024
        phi = np.zeros(n)
        f = np.zeros(n)
        
        # Sources
        for v in range(n):
            if state.grid[v] == MY_PLAYER:
                f[v] = +1.0
            elif state.grid[v] == OPPONENT:
                f[v] = -1.0
        
        # Itérations SOR
        omega = 1.8
        for iteration in range(100):
            for v in range(n):
                if state.grid[v] == 0:
                    neighbor_sum = sum(phi[u] for u in neighbors[v])
                    phi_new = (f[v] + neighbor_sum) / len(neighbors[v])
                    phi[v] = (1 - omega) * phi[v] + omega * phi_new
        
        return phi
```

## B. Ressources et Références

**Livres :**
- "Artificial Intelligence: A Modern Approach" - Russell & Norvig
- "Reinforcement Learning" - Sutton & Barto
- "Computational Topology" - Edelsbrunner & Harer

**Papers clés :**
- Silver et al. (2016) - "Mastering the game of Go with deep neural networks"
- Coulom (2006) - "Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search"
- Edelsbrunner & Harer (2008) - "Persistent Homology - A Survey"

**Implémentations :**
- AlphaZero : https://github.com/suragnair/alpha-zero-general
- MCTS : https://github.com/pbsinclair42/MCTS
- Gudhi (topologie) : https://gudhi.inria.fr/

---

**FIN DU DOCUMENT**
