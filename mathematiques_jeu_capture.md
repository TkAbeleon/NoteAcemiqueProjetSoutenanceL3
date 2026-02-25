# MATHÉMATIQUES COMPLÈTES POUR JEU DE CAPTURE SUR GRILLE ORTHOGONALE

## TABLE DES MATIÈRES

1. Fondations : Théorie des Graphes
2. Topologie Discrète et Cycles
3. Géométrie Discrète et Polygones Orthogonaux
4. Homologie Algébrique Discrète
5. Analyse Numérique : Équations aux Dérivées Partielles Discrètes
6. Théorie des Jeux et Optimisation
7. Probabilités et Processus de Décision Markoviens

---

# 1. FONDATIONS : THÉORIE DES GRAPHES

## 1.1 Définitions de Base

### 1.1.1 Graphe non orienté

Un graphe G = (V, E) consiste en :
- V : ensemble fini de sommets (vertices)
- $E ⊆ {{u,v} | u,v ∈ V, u ≠ v}$ : ensemble d'arêtes (edges)

**Pour notre jeu :**
- $V = {(x,y) | x,y ∈ {0,1,...,31}}$ (sommets de la grille 32×32)
- |V| = 1024 sommets
- $E = {{{(x,y), (x',y')} | |x-x'| + |y-y'| = 1}}$ (arêtes orthogonales uniquement)

### 1.1.2 Voisinage et degré

Pour un sommet v ∈ V :
- N(v) = {u ∈ V | {u,v} ∈ E} : voisinage de v
- deg(v) = |N(v)| : degré de v

**Dans notre grille :**
- deg(v) ∈ {2, 3, 4}
  - deg(v) = 2 pour les coins
  - deg(v) = 3 pour les bords (non-coins)
  - deg(v) = 4 pour l'intérieur

### 1.1.3 Chemin et cycle

**Chemin :**
Un chemin P de longueur k est une séquence de sommets (v₀, v₁, ..., vₖ) où :
- {vᵢ, vᵢ₊₁} ∈ E pour tout i ∈ {0,...,k-1}
- vᵢ ≠ vⱼ pour i ≠ j (chemin simple)

**Cycle :**
Un cycle C de longueur k ≥ 3 est une séquence (v₀, v₁, ..., vₖ₋₁) où :
- ${vᵢ, vᵢ₊₁ mod k} ∈ E pour tout i ∈ {0,...,k-1}$
- $vᵢ ≠ vⱼ pour i ≠ j$
- Fermeture : ${vₖ₋₁, v₀} ∈ E$

**Propriété fondamentale pour notre jeu :**
Un sommet v appartient à un cycle C si et seulement si deg_C(v) = 2, où deg_C(v) est le nombre de voisins de v dans C.

## 1.2 Connexité et Composantes Connexes

### 1.2.1 Connexité

Un graphe G = (V,E) est connexe si pour tout u,v ∈ V, il existe un chemin de u à v.

**Relation d'équivalence :**
u ~ v ⟺ ∃ chemin de u à v

Cette relation partitionne V en classes d'équivalence appelées composantes connexes.

### 1.2.2 Structure Union-Find (Disjoint Set Union)

**Opérations :**
1. **MakeSet(x)** : Crée un singleton {x}
2. **Find(x)** : Retourne le représentant de la composante contenant x
3. **Union(x,y)** : Fusionne les composantes contenant x et y

**Implémentation optimisée :**

Avec compression de chemin et union par rang :

```
parent : V → V
rank : V → ℕ

Find(x):
    if parent[x] ≠ x:
        parent[x] = Find(parent[x])  // compression de chemin
    return parent[x]

Union(x,y):
    root_x = Find(x)
    root_y = Find(y)
    if root_x = root_y: return
    
    // Union par rang
    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    else if rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1
```

**Complexité :**
- Amortie : O(α(n)) par opération, où α est l'inverse de la fonction d'Ackermann
- Pratiquement : O(1) pour n ≤ 10¹⁸

### 1.2.3 Caractérisation des Cycles dans une Composante

**Théorème (Euler pour graphes planaires) :**
Pour un graphe planaire connexe avec V sommets, E arêtes, F faces :
V - E + F = 2

**Corollaire pour notre jeu :**
Une composante connexe contient un cycle si et seulement si $E_c ≥ V_c$, où :
- V_c : nombre de sommets dans la composante
- E_c : nombre d'arêtes dans la composante

**Démonstration :**
- Un arbre à n sommets a exactement n-1 arêtes
- Toute arête supplémentaire crée un cycle
- Donc : $E_c ≥ V_c ⟹$ au moins $V_c - (V_c - 1) =$ 1 cycle

## 1.3 Détection de Cycles : Algorithmes

### 1.3.1 DFS (Depth-First Search) pour Détection de Cycle

**Algorithme :**

```
DFS-Cycle(G = (V,E), start):
    visited = ∅
    parent = {}
    
    function DFS(v, p):
        visited ← visited ∪ {v}
        parent[v] ← p
        
        for each u ∈ N(v):
            if u ∉ visited:
                if DFS(u, v) returns cycle:
                    return cycle
            else if u ≠ p:
                // Back edge trouvé → cycle détecté
                return ReconstructCycle(u, v, parent)
        
        return None
    
    return DFS(start, None)
```

**ReconstructCycle(u, v, parent) :**

```
cycle = [v]
current = v
while current ≠ u:
    current = parent[current]
    cycle.append(current)
return cycle
```

**Complexité :**
- Temps : $O(V + E)$ pour parcourir la composante
- Espace : $O(V)$ pour visited et parent

### 1.3.2 Extraction du Cycle Minimal

**Problème :** Le DFS peut retourner un cycle avec des "branches" (non-simple).

**Solution - Simplification :**

```
SimplifyCycle(C):
    // C est une liste de sommets
    positions = {}
    for i, v in enumerate(C):
        if v in positions:
            // Sommet répété → éliminer la boucle intermédiaire
            return C[:positions[v]+1] + C[i+1:]
        positions[v] = i
    return C
```

**Propriété mathématique :**
Un cycle simple sur grille orthogonale satisfait :
- $∀v ∈ C : deg_C(v) = 2$
- C forme un polygone simple (sans auto-intersection)

---

# 2. TOPOLOGIE DISCRÈTE ET CYCLES

## 2.1 Espaces Topologiques Discrets

### 2.1.1 Topologie sur la Grille

On munit $V = ℤ² ∩ [0,31]²$ de la topologie discrète :
- Tout sous-ensemble est ouvert
- Les composantes connexes sont définies par la relation de voisinage orthogonal

### 2.1.2 Intérieur et Frontière (Définitions Discrètes)

Pour un sous-ensemble S ⊆ V :

**Frontière (boundary) :**
$∂S = {v ∈ S | ∃u ∈ N(v), u ∉ S}$

**Intérieur :**
$Int(S) = S \ ∂S = {v ∈ S | N(v) ⊆ S}$

**Extérieur :**
Ext(S) = V \ (S ∪ ∂S)

## 2.2 Courbe de Jordan Discrète

### 2.2.1 Théorème de Jordan (Version Continue)

**Énoncé classique :**
Toute courbe simple fermée C dans ℝ² partitionne le plan en exactement deux régions connexes : l'intérieur (borné) et l'extérieur (non borné).

### 2.2.2 Version Discrète sur Grille

**Théorème (Jordan Discret) :**
Soit C un cycle simple sur la grille orthogonale. Alors :
1. V \ C se décompose en exactement deux composantes connexes
2. L'une est bornée (intérieur I(C)), l'autre non bornée (extérieur E(C))
3. Tout chemin de I(C) vers E(C) intersecte C

**Démonstration (esquisse) :**
1. Montrer que V\C n'est pas connexe (sinon contradiction avec planarité)
2. Par induction sur |C|, montrer qu'il y a exactement 2 composantes
3. La composante touchant le bord de la grille est non bornée

### 2.2.3 Caractérisation de l'Intérieur

**Méthode 1 - Flood Fill depuis l'Extérieur :**

```
ComputeInterior(C):
    marked = C  // marquer le cycle
    queue = {v ∈ V | v est sur le bord de la grille}
    
    // BFS depuis le bord
    while queue ≠ ∅:
        v = queue.pop()
        if v ∉ marked:
            marked.add(v)
            queue.extend(N(v) \ marked)
    
    return V \ marked  // ce qui reste est l'intérieur
```

**Complexité :** O(|V|) = O(1024) pour notre grille

**Méthode 2 - Point-in-Polygon (Ray Casting) :**

Pour un point p = (x,y), compter les intersections d'un rayon horizontal {(t,y) | t ≥ x} avec les arêtes de C.

**Algorithme :**

```
IsInside(p, C):
    count = 0
    n = |C|
    for i in 0..n-1:
        v_i = C[i]
        v_next = C[(i+1) mod n]
        
        if IsHorizontalEdge(v_i, v_next):
            // Gérer séparément
            if p.y = v_i.y and min(v_i.x, v_next.x) ≤ p.x ≤ max(v_i.x, v_next.x):
                return True  // sur le bord
        else:
            // Arête verticale
            if IntersectsRay(p, v_i, v_next):
                count += 1
    
    return (count mod 2 = 1)
```

**IntersectsRay(p, v_i, v_next) :**

```
// v_i et v_next forment une arête verticale
y_min = min(v_i.y, v_next.y)
y_max = max(v_i.y, v_next.y)
x = v_i.x  // même x pour arête verticale

return (y_min ≤ p.y < y_max) and (x > p.x)
```

**Justification mathématique :**
- Principe de parité : nombre impair d'intersections ⟺ intérieur
- Basé sur le théorème de Jordan

**Complexité :** O(|C|) par point testé

---

# 3. GÉOMÉTRIE DISCRÈTE ET POLYGONES ORTHOGONAUX

## 3.1 Polygones Orthogonaux (Rectilinear Polygons)

### 3.1.1 Définition

Un polygone orthogonal P est un polygone simple dont toutes les arêtes sont parallèles aux axes de coordonnées.

**Propriétés :**
- Sommets à coordonnées entières
- Arêtes horizontales ou verticales
- Pas d'arêtes diagonales

### 3.1.2 Représentation

Un polygone orthogonal avec n sommets peut être représenté comme :
P = (v₀, v₁, ..., v_{n-1})

où chaque arête {vᵢ, vᵢ₊₁} est soit horizontale soit verticale.

## 3.2 Calcul d'Aire : Formule de Shoelace

### 3.2.1 Formule Générale (Polygone Simple)

Pour un polygone P = (v₀, ..., v_{n-1}) avec vᵢ = (xᵢ, yᵢ) :

**Aire signée :**
A_signed = (1/2) Σᵢ₌₀^{n-1} (xᵢ · y_{i+1 mod n} - x_{i+1 mod n} · yᵢ)

**Aire absolue :**
A = |A_signed|

**Démonstration :**
Basée sur le théorème de Green :
∮_C (x dy - y dx) = 2A

où l'intégrale est calculée par somme de Riemann discrète.

### 3.2.2 Application aux Polygones Orthogonaux

Pour un polygone orthogonal, la formule se simplifie :

**Contribution d'une arête horizontale (y constant) :**
- De (x₁, y) à (x₂, y) : contribution = y · (x₂ - x₁)

**Contribution d'une arête verticale (x constant) :**
- De (x, y₁) à (x, y₂) : contribution = 0

**Formule simplifiée :**
A = Σ_{arêtes horizontales} |y · Δx|

où Δx = x_{fin} - x_{début}, en tenant compte de l'orientation.

### 3.2.3 Implémentation

```
PolygonArea(C):
    // C = liste ordonnée de sommets
    n = |C|
    area = 0
    
    for i in 0..n-1:
        x_i, y_i = C[i]
        x_next, y_next = C[(i+1) mod n]
        area += x_i * y_next - x_next * y_i
    
    return abs(area) / 2
```

**Complexité :** O(n) où n = |C|

## 3.3 Théorème de Pick

### 3.3.1 Énoncé

**Théorème (Georg Pick, 1899) :**
Pour un polygone simple P dont les sommets sont sur le réseau ℤ² :

A = I + B/2 - 1

où :
- A : aire du polygone (en unités carrées)
- I : nombre de points du réseau strictement à l'intérieur de P
- B : nombre de points du réseau sur le bord de P

### 3.3.2 Démonstration (Esquisse)

**Cas de base :** Triangle rectangle minimal
- Sommets : (0,0), (1,0), (0,1)
- A = 1/2, B = 3, I = 0
- Vérification : 1/2 = 0 + 3/2 - 1 ✓

**Décomposition :**
1. Tout polygone peut être triangulé
2. Pick est additif sous union de polygones adjacents
3. Par induction sur le nombre de triangles

**Démonstration additive :**
Soient P₁, P₂ deux polygones partageant une arête commune e.

A(P₁ ∪ P₂) = A(P₁) + A(P₂)
I(P₁ ∪ P₂) = I(P₁) + I(P₂) + (points de e \ extrémités)
B(P₁ ∪ P₂) = B(P₁) + B(P₂) - 2·(points de e)

On vérifie que la formule est préservée.

### 3.3.3 Application à Notre Jeu

**Calcul du nombre de points intérieurs :**

```
ComputeInteriorPoints(C):
    A = PolygonArea(C)  // Shoelace
    B = |C|             // nombre de sommets du cycle
    I = A - B/2 + 1
    return I
```

**Interprétation :**
- Si I > 0, il y a potentiellement des captures
- I donne le nombre total de points strictement intérieurs
- Pour identifier quels adversaires sont capturés, il faut tester individuellement (ray casting)

**Exemple :**
Rectangle 3×3 :
- Sommets : (0,0), (3,0), (3,3), (0,3)
- A = 9, B = 4
- I = 9 - 4/2 + 1 = 9 - 2 + 1 = 8 ✓
- En effet, 8 points intérieurs : {(1,1), (1,2), (2,1), (2,2), ...}

### 3.3.4 Généralisation : Formule d'Euler

Pour un polygone orthogonal avec h trous (composantes intérieures) :

A = I + B/2 - 1 + h

Cette généralisation nécessite l'homologie pour compter h.

---

# 4. HOMOLOGIE ALGÉBRIQUE DISCRÈTE

## 4.1 Complexes Simpliciaux et Cubiques

### 4.1.1 Définitions

**Complexe simplicial :**
Un complexe simplicial K est un ensemble de simplexes (points, arêtes, triangles, ...) tel que :
1. Toute face d'un simplexe dans K est aussi dans K
2. L'intersection de deux simplexes est soit vide soit une face commune

**Complexe cubique (pour grilles) :**
On représente la grille comme un complexe cubique :
- 0-cells : sommets (vertices)
- 1-cells : arêtes orthogonales
- 2-cells : carrés unitaires (faces)

### 4.1.2 Construction pour Notre Grille

**Ensemble de cellules :**

C₀ = {(x,y) | 0 ≤ x,y ≤ 31} (1024 sommets)

C₁ = {arêtes horizontales} ∪ {arêtes verticales}
    = {[(x,y), (x+1,y)] | 0 ≤ x < 31, 0 ≤ y ≤ 31} 
      ∪ {[(x,y), (x,y+1)] | 0 ≤ x ≤ 31, 0 ≤ y < 31}
    ≈ 2·31·32 = 1984 arêtes

C₂ = {carrés [(x,y), (x+1,y), (x+1,y+1), (x,y+1)] | 0 ≤ x,y < 31}
    = 961 faces

## 4.2 Groupes de Chaînes et Opérateur Bord

### 4.2.1 Groupes de Chaînes

**Définition :**
Le groupe de k-chaînes Cₖ est le groupe abélien libre engendré par les k-cells :

Cₖ = ℤ^{|Cₖ|} ou Cₖ = (ℤ/2ℤ)^{|Cₖ|} (coefficients mod 2)

**Interprétation :**
Une k-chaîne c ∈ Cₖ est une combinaison linéaire formelle de k-cells :

c = Σᵢ aᵢ σᵢ, où aᵢ ∈ ℤ (ou ℤ/2ℤ) et σᵢ est une k-cell

### 4.2.2 Opérateur Bord

**Définition :**
L'opérateur bord ∂ₖ : Cₖ → Cₖ₋₁ est un homomorphisme de groupes défini sur les générateurs :

**Pour une arête e = [v₀, v₁] (1-cell) :**
∂₁(e) = v₁ - v₀

**Pour un carré σ = [v₀, v₁, v₂, v₃] (2-cell) :**
∂₂(σ) = [v₀,v₁] + [v₁,v₂] + [v₂,v₃] + [v₃,v₀]

avec orientation cohérente (mod 2, les signes disparaissent).

### 4.2.3 Propriété Fondamentale

**Théorème :**
∂ₖ₋₁ ∘ ∂ₖ = 0

**Démonstration (pour k=2) :**
$∂₁(∂₂(σ)) = ∂₁([v₀,v₁] + [v₁,v₂] + [v₂,v₃] + [v₃,v₀])$
           $= (v₁-v₀) + (v₂-v₁) + (v₃-v₂) + (v₀-v₃)$
           $= 0$

**Conséquence :**
Im(∂ₖ₊₁) ⊆ Ker(∂ₖ)

Cela permet de définir l'homologie.

## 4.3 Groupes d'Homologie

### 4.3.1 Définition

**k-ième groupe d'homologie :**
$Hₖ = Ker(∂ₖ) / Im(∂ₖ₊₁)$

**Interprétation :**
- Ker(∂ₖ) : k-chaînes qui sont des "cycles" (pas de bord)
- Im(∂ₖ₊₁) : k-chaînes qui sont des "bords" (frontières de (k+1)-chaînes)
- Hₖ : cycles qui ne sont pas des bords (classes d'équivalence)

### 4.3.2 Homologie H₁ (Cycles)

**Pour notre jeu, H₁ détecte les "trous" :**

Un élément de H₁ correspond à un cycle qui n'est pas la frontière d'une région remplie.

**Dimension de H₁ :**
β₁ = dim(H₁) = nombre de Betti (nombre de trous indépendants)

### 4.3.3 Calcul Pratique

**Représentation matricielle (mod 2) :**

Soient :
- M₁ : matrice d'incidence ∂₁ (arêtes → sommets)
  - $M₁ ∈ (ℤ/2ℤ)^{|C₀| × |C₁|}$
  - M₁[v,e] = 1 si v est une extrémité de e

- M₂ : matrice d'incidence ∂₂ (faces → arêtes)
  - M₂ ∈ (ℤ/2ℤ)^{|C₁| × |C₂|}
  - M₂[e,σ] = 1 si e est une arête de σ

**Calcul de H₁ :**

1. **Réduction de M₁ par élimination de Gauss (mod 2) :**
   - rank(M₁) = r₁
   - dim(Ker(∂₁)) = |C₁| - r₁

2. **Réduction de M₂ par élimination de Gauss (mod 2) :**
   - rank(M₂) = r₂
   - dim(Im(∂₂)) = r₂

3. **Nombre de Betti :**
   β₁ = dim(Ker(∂₁)) - dim(Im(∂₂))
      = (|C₁| - r₁) - r₂

### 4.3.4 Algorithme d'Élimination de Gauss sur GF(2)

```
GaussianEliminationGF2(M):
    // M est une matrice binaire
    rows, cols = M.shape
    rank = 0
    
    for col in 0..cols-1:
        // Trouver pivot
        pivot_row = -1
        for row in rank..rows-1:
            if M[row, col] = 1:
                pivot_row = row
                break
        
        if pivot_row = -1:
            continue  // pas de pivot, passer à la colonne suivante
        
        // Échanger lignes
        swap(M[rank], M[pivot_row])
        
        // Éliminer
        for row in 0..rows-1:
            if row ≠ rank and M[row, col] = 1:
                M[row] ^= M[rank]  // XOR sur GF(2)
        
        rank += 1
    
    return rank
```

**Complexité :** O(min(rows, cols) · rows · cols)

Pour notre grille : O(1984³) ≈ O(10¹⁰) opérations bit, mais très rapide en pratique.

### 4.3.5 Extraction de Cycles Représentants

Une fois M₁ réduite, les vecteurs du noyau donnent des cycles.

**Algorithme :**

```
ExtractCycleBasis(M₁):
    // Après élimination de Gauss
    kernel_basis = []
    
    for col in free_columns(M₁):
        // Construire vecteur du noyau
        cycle_vector = [0] * |C₁|
        cycle_vector[col] = 1
        
        // Back-substitution pour trouver les autres composantes
        for pivot_col in pivot_columns(M₁):
            if M₁[pivot_row(pivot_col), col] = 1:
                cycle_vector[pivot_col] = 1
        
        kernel_basis.append(cycle_vector)
    
    return kernel_basis
```

Chaque `cycle_vector` encode un ensemble d'arêtes formant un cycle.

## 4.4 Application au Jeu : Détection de Trous Multiples

**Scénario :**
Le joueur a créé plusieurs cycles imbriqués ou adjacents.

**Problème :**
Déterminer combien de régions distinctes peuvent capturer.

**Solution via Homologie :**

1. Construire le complexe cubique sur les points du joueur
2. Calculer β₁ = nombre de trous
3. Interpréter : β₁ = nombre de cycles indépendants capturant potentiellement

**Exemple :**

```
Configuration avec deux cycles concentriques :

Cycle extérieur : C_ext
Cycle intérieur : C_int

β₁ = 2 ⟹ deux trous indépendants
```

**Formule généralisée de Pick :**
A = I + B/2 - 1 + h

où h = β₁ (nombre de trous).

---

# 5. ANALYSE NUMÉRIQUE : ÉQUATIONS AUX DÉRIVÉES PARTIELLES DISCRÈTES

## 5.1 Équation de Laplace/Poisson Discrète

### 5.1.1 Laplacien Discret

**Définition (grille orthogonale) :**
Pour une fonction φ : V → ℝ, le Laplacien discret est :

$∇²φ(x,y) = φ(x+1,y) + φ(x-1,y) + φ(x,y+1) + φ(x,y-1) - 4φ(x,y)$

**Forme compacte :**
$∇²φ(v) = Σ_{u ∈ N(v)} φ(u) - deg(v)·φ(v)$

### 5.1.2 Équation de Poisson Discrète

**Problème :**
Trouver φ : V → ℝ tel que :

∇²φ = f

où f : V → ℝ est une fonction source donnée.

**Conditions aux limites :**
- **Dirichlet :** φ(v) = g(v) pour v ∈ ∂V (bord)
- **Neumann :** ∂φ/∂n = h sur ∂V (dérivée normale)

### 5.1.3 Formulation Matricielle

**Matrice Laplacienne L :**

$L ∈ ℝ^{|V| × |V|}$, définie par :

$L[i,j] = {$
    $-deg(vᵢ)     si i = j$
    $1            si {vᵢ, vⱼ} ∈ E$
    $0            sinon$
$}$

**Système linéaire :**
Lφ = f

où φ, f ∈ ℝ^{|V|} sont des vecteurs.

**Propriétés de L :**
- Symétrique : L^T = L
- Semi-définie positive : x^T L x ≥ 0 pour tout x
- Singulière si pas de conditions Dirichlet (nullspace = constantes)

### 5.1.4 Application au Jeu : Champ de Potentiel Territorial

**Idée :**
Modéliser l'influence territoriale comme un champ de potentiel.

**Configuration de la source f :**

$f(v) = {$
    $+α      si v occupé par le bot$
    $-β      si v occupé par l'adversaire$
    $0       sinon$
$}$

où α, β > 0 sont des poids d'influence.

**Interprétation de φ :**
- φ(v) > 0 : zone sous influence du bot
- φ(v) < 0 : zone sous influence adversaire
- |φ(v)| grand : forte influence
- Gradient ∇φ : direction d'expansion optimale

## 5.2 Méthodes de Résolution Itératives

### 5.2.1 Méthode de Jacobi

**Algorithme :**

```
Jacobi(L, f, φ₀, tol, max_iter):
    φ = φ₀
    
    for k in 1..max_iter:
        φ_new = [0] * |V|
        
        for each vertex v:
            sum_neighbors = Σ_{u ∈ N(v)} φ[u]
            φ_new[v] = (f[v] + sum_neighbors) / deg(v)
        
        if ||φ_new - φ|| < tol:
            return φ_new
        
        φ = φ_new
    
    return φ
```

**Convergence :**
- Converge si L est diagonale dominante (vrai pour Laplacien)
- Taux de convergence : O((1 - c/n)^k) pour grille n×n

**Complexité par itération :** O(|E|) ≈ O(|V|)

### 5.2.2 Méthode de Gauss-Seidel

**Algorithme :**

```
GaussSeidel(L, f, φ₀, tol, max_iter):
    φ = φ₀
    
    for k in 1..max_iter:
        for each vertex v (dans un ordre fixe):
            sum_neighbors = Σ_{u ∈ N(v)} φ[u]  // utilise valeurs déjà mises à jour
            φ[v] = (f[v] + sum_neighbors) / deg(v)
        
        if converged:
            return φ
    
    return φ
```

**Avantage :** Converge ~2× plus vite que Jacobi.

### 5.2.3 Méthode SOR (Successive Over-Relaxation)

**Algorithme :**

```
SOR(L, f, φ₀, ω, tol, max_iter):
    // ω ∈ (0, 2) : paramètre de relaxation
    φ = φ₀
    
    for k in 1..max_iter:
        for each vertex v:
            sum_neighbors = Σ_{u ∈ N(v)} φ[u]
            φ_new = (f[v] + sum_neighbors) / deg(v)
            
            // Relaxation
            φ[v] = (1 - ω)·φ[v] + ω·φ_new
        
        if converged:
            return φ
    
    return φ
```

**Choix optimal de ω :**
Pour grille n×n, ω_optimal ≈ 2/(1 + π/n)

**Convergence :** Jusqu'à n fois plus rapide que Gauss-Seidel.

### 5.2.4 Gradient Conjugué (CG)

**Algorithme (pour système Ax = b avec A symétrique définie positive) :**

```
ConjugateGradient(A, b, x₀, tol):
    x = x₀
    r = b - A·x     // résidu
    p = r           // direction
    
    for k in 1..max_iter:
        α = (r^T · r) / (p^T · A·p)
        x = x + α·p
        r_new = r - α·A·p
        
        if ||r_new|| < tol:
            return x
        
        β = (r_new^T · r_new) / (r^T · r)
        p = r_new + β·p
        r = r_new
    
    return x
```

**Convergence :**
- Converge en au plus |V| itérations (théoriquement)
- En pratique : O(√κ · log(1/tol)) itérations, où κ = cond(A)
- Pour Laplacien de grille : κ ≈ O(n²), donc O(n·log(1/tol)) itérations

**Complexité totale :** O(|V|^{1.5} · log(1/tol)) pour grille

**Avantage :** Très rapide pour systèmes creux de grande taille.

## 5.3 Mise à Jour Incrémentale

**Problème :**
Après chaque coup, recalculer φ complètement est coûteux.

**Solution - Perturbation Locale :**

Si on ajoute un point en position v₀, la source devient :
f_new = f_old + Δf

où Δf est nulle partout sauf en v₀.

**Résolution :**
φ_new = φ_old + Δφ

où Δφ satisfait :
L·Δφ = Δf

**Approximation :** Utiliser quelques itérations de solveur itératif à partir de Δφ₀ = 0.

**Complexité :** O(k·|V|) où k ≪ nombre d'itérations pour convergence complète.

---

# 6. THÉORIE DES JEUX ET OPTIMISATION

## 6.1 Jeux à Somme Nulle et Stratégies Optimales

### 6.1.1 Définition

**Jeu à deux joueurs :**
- Joueurs : {1, 2} (Bot, Adversaire)
- États : S (configurations du plateau)
- Actions : A(s) (coups légaux depuis s)
- Fonction de transition : T: S × A → S
- Fonction d'utilité : u: S → ℝ (score terminal)

**Somme nulle :**
u₁(s) = -u₂(s)

### 6.1.2 Théorème Minimax

**Théorème (von Neumann) :**
Pour un jeu à somme nulle fini, il existe une valeur v* et des stratégies optimales σ₁*, σ₂* telles que :

max_{σ₁} min_{σ₂} 𝔼[u₁ | σ₁, σ₂] = v* = min_{σ₂} max_{σ₁} 𝔼[u₁ | σ₁, σ₂]

**Interprétation :**
- Le bot peut garantir un score ≥ v*
- L'adversaire peut limiter le bot à ≤ v*

### 6.1.3 Recherche Minimax (Arbre de Jeu)

**Algorithme :**

```
Minimax(s, depth, isMaximizingPlayer):
    if depth = 0 or s est terminal:
        return Evaluate(s)
    
    if isMaximizingPlayer:
        max_eval = -∞
        for each action a ∈ A(s):
            s' = T(s, a)
            eval = Minimax(s', depth-1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = +∞
        for each action a ∈ A(s):
            s' = T(s, a)
            eval = Minimax(s', depth-1, True)
            min_eval = min(min_eval, eval)
        return min_eval
```

**Complexité :** O(b^d) où b = branching factor, d = profondeur.

Pour notre jeu : b ≈ 100-500 (nombre de cases vides adjacentes), d ≈ 10-20 → infaisable.

### 6.1.4 Élagage Alpha-Beta

**Amélioration :** Couper les branches qui ne peuvent pas influencer le résultat.

**Algorithme :**

```
AlphaBeta(s, depth, α, β, isMaximizingPlayer):
    if depth = 0 or s est terminal:
        return Evaluate(s)
    
    if isMaximizingPlayer:
        max_eval = -∞
        for each action a ∈ A(s):
            s' = T(s, a)
            eval = AlphaBeta(s', depth-1, α, β, False)
            max_eval = max(max_eval, eval)
            α = max(α, eval)
            if β ≤ α:
                break  // β cut-off
        return max_eval
    else:
        min_eval = +∞
        for each action a ∈ A(s):
            s' = T(s, a)
            eval = AlphaBeta(s', depth-1, α, β, True)
            min_eval = min(min_eval, eval)
            β = min(β, eval)
            if β ≤ α:
                break  // α cut-off
        return min_eval
```

**Complexité (moyenne) :** O(b^{d/2}) avec bon ordonnancement.

## 6.2 Monte Carlo Tree Search (MCTS)

### 6.2.1 Principe

**Idée :**
Construire un arbre de recherche asymétrique guidé par des simulations aléatoires (rollouts).

**Phases (par itération) :**

1. **Selection :** Descendre dans l'arbre selon une politique (UCT)
2. **Expansion :** Ajouter un nœud enfant
3. **Simulation :** Jouer aléatoirement jusqu'à la fin (rollout)
4. **Backpropagation :** Remonter le résultat dans l'arbre

### 6.2.2 UCT (Upper Confidence Bounds for Trees)

**Formule UCB1 :**

Pour choisir l'action a depuis un nœud avec N visites totales :

UCB(a) = Q(a)/N(a) + C·√(ln N / N(a))

où :
- Q(a) : somme des récompenses pour l'action a
- N(a) : nombre de visites de a
- C : constante d'exploration (typiquement √2)

**Justification mathématique :**
- Premier terme : exploitation (moyenne empirique)
- Deuxième terme : exploration (intervalle de confiance)
- Théorème (Kocsis & Szepesvári, 2006) : UCT converge vers la valeur minimax avec probabilité 1

### 6.2.3 Algorithme MCTS Complet

```
MCTS(root, num_simulations):
    for i in 1..num_simulations:
        node = root
        
        // 1. Selection
        while node.isFullyExpanded() and not node.isTerminal():
            node = node.selectChildUCT()
        
        // 2. Expansion
        if not node.isTerminal():
            node = node.expand()  // ajouter un enfant aléatoire
        
        // 3. Simulation (Rollout)
        reward = rollout(node.state)
        
        // 4. Backpropagation
        while node ≠ None:
            node.visits += 1
            node.totalReward += reward
            reward = -reward  // inverser pour l'adversaire
            node = node.parent
    
    return root.bestChild()  // selon N(a) ou Q(a)/N(a)
```

### 6.2.4 Politique de Rollout Informée

**Problème :** Rollout complètement aléatoire est inefficace.

**Solution :** Utiliser une heuristique pour guider les simulations.

**Exemples de politiques :**

1. **ε-greedy avec champ de potentiel :**
   - Avec probabilité ε : action aléatoire
   - Avec probabilité 1-ε : action maximisant φ(v)

2. **Softmax avec température :**
   P(a) ∝ exp(φ(a)/T)

3. **Heuristique topologique :**
   - Priorité aux coups fermant un cycle capturant
   - Éviter les coups suicidaires

**Implémentation :**

```
GuidedRollout(state):
    while not state.isTerminal():
        actions = state.getLegalActions()
        
        // Calculer scores heuristiques
        scores = [Evaluate(state, a) for a in actions]
        
        // Échantillonner selon softmax
        probabilities = softmax(scores, T=0.5)
        action = sample(actions, probabilities)
        
        state = state.applyAction(action)
    
    return state.getReward()
```

## 6.3 Évaluation Heuristique

### 6.3.1 Fonction d'Évaluation Composite

**Forme générale :**

Eval(s) = Σᵢ wᵢ · fᵢ(s)

où fᵢ sont des features et wᵢ leurs poids.

### 6.3.2 Features Importantes

**1. Potentiel de Capture :**

f₁(s) = Σ_{cycles C du bot} |adversaires dans I(C)|

**2. Potentiel Territorial :**

f₂(s) = Σ_{v} φ(v) · 𝟙{v vide}

où φ est le champ de potentiel.

**3. Risque de Capture :**

f₃(s) = -Σ_{cycles C adverses} |points du bot dans I(C)|

**4. Mobilité :**

f₄(s) = |{v voisin d'un point du bot et vide}|

**5. Connexité :**

f₅(s) = -nombre_de_composantes_du_bot

**6. Avantage Matériel :**

f₆(s) = |points du bot| - |points adverses|

### 6.3.3 Apprentissage des Poids

**Méthodes :**

1. **Réglage manuel :** Expertise humaine
2. **Régression linéaire :** Minimiser erreur sur positions étiquetées
3. **Temporal Difference Learning (TD) :**

Δwᵢ = α · (r + γ·Eval(s_{t+1}) - Eval(s_t)) · ∂Eval/∂wᵢ

où α = learning rate, γ = discount factor

4. **Apprentissage par renforcement (REINFORCE, PPO, etc.) :**

Optimiser directement le win rate via gradient policy.

---

# 7. PROBABILITÉS ET PROCESSUS DE DÉCISION MARKOVIENS

## 7.1 Modélisation comme MDP

### 7.1.1 Définition d'un MDP

Un Processus de Décision Markovien est un tuple (S, A, P, R, γ) :
- S : ensemble d'états
- A : ensemble d'actions
- P : S × A × S → [0,1] : fonction de transition
  P(s' | s, a) = probabilité de passer de s à s' en prenant a
- R : S × A → ℝ : fonction de récompense
- γ ∈ [0,1] : facteur de discount

### 7.1.2 Application au Jeu

**États :** S = configurations du plateau

**Actions :** A(s) = cases vides légales

**Transition :** Déterministe pour le bot, stochastique si on modélise l'adversaire :
- P(s' | s, a) = 1 si s' résulte de l'action a du bot
- P(s'' | s', a') modélise la distribution de l'action adversaire

**Récompense :**
- R(s, a) = 0 pour actions intermédiaires
- R(s_terminal, ·) = +1 si victoire, -1 si défaite, 0 si nul

### 7.1.3 Politique et Fonction de Valeur

**Politique :** π : S → A (ou S → Dist(A) si stochastique)

**Fonction de valeur d'état :**
$V^π(s) = 𝔼[Σₜ γ^t R(sₜ, aₜ) | s₀=s, π]$

**Fonction de valeur action-état (Q-function) :**
Q^π(s, a) = 𝔼[Σₜ γ^t R(sₜ, aₜ) | s₀=s, a₀=a, π]

### 7.1.4 Équations de Bellman

**Optimalité :**

V*(s) = max_a 𝔼[R(s,a) + γ·V*(s') | a]
$Q*(s,a) = 𝔼[R(s,a) + γ·max_{a'} Q*(s',a')]$


**Politique optimale :**
π*(s) = argmax_a Q*(s,a)

## 7.2 Apprentissage par Renforcement

### 7.2.1 Q-Learning

**Algorithme (off-policy TD) :**

```
Q-Learning(α, γ, ε):
    Initialize Q(s,a) arbitrairement
    
    for each episode:
        s = s₀
        while s not terminal:
            // ε-greedy action selection
            a = {
                random action         with prob ε
                argmax_a' Q(s,a')    with prob 1-ε
            }
            
            s', r = environment.step(a)
            
            // Q-learning update
            Q(s,a) ← Q(s,a) + α·(r + γ·max_{a'} Q(s',a') - Q(s,a))
            
            s = s'
```

**Convergence :** Q converge vers Q* sous conditions (visites infinies, α décroissant).

### 7.2.2 Deep Q-Networks (DQN)

**Idée :** Approximer Q par un réseau de neurones θ.

**Réseau :**
Q(s,a; θ) ≈ Q*(s,a)

**Loss :**
L(θ) = 𝔼[(y - Q(s,a; θ))²]

où y = r + γ·max_{a'} Q(s',a'; θ⁻)

et θ⁻ = paramètres cibles (mis à jour périodiquement).

**Innovations (Mnih et al., 2015) :**
- Experience replay : stocker transitions (s,a,r,s') dans un buffer, échantillonner mini-batches
- Target network : stabilise l'apprentissage

### 7.2.3 Policy Gradient

**Objectif :**
Maximiser J(θ) = 𝔼_{τ~π_θ}[R(τ)]

où τ = (s₀, a₀, s₁, ...) est une trajectoire.

**Théorème du Gradient de Politique :**

∇_θ J(θ) = 𝔼_{τ~π_θ}[Σₜ ∇_θ log π_θ(aₜ|sₜ) · Gₜ]

où Gₜ = Σ_{t'≥t} γ^{t'-t} rₜ' (retour cumulé).

**Algorithme REINFORCE :**

```
REINFORCE(θ, α):
    for each episode:
        Generate trajectory τ = (s₀,a₀,r₀, s₁,a₁,r₁, ...)
        
        for t in 0..T-1:
            Gₜ = Σ_{k=t}^{T-1} γ^{k-t} rₖ
            θ ← θ + α·∇_θ log π_θ(aₜ|sₜ)·Gₜ
```

### 7.2.4 Actor-Critic

**Architecture :**
- Actor : π_θ(a|s) (politique)
- Critic : V_φ(s) (fonction de valeur)

**Avantage :**
A(s,a) = Q(s,a) - V(s) ≈ r + γ·V(s') - V(s)

**Update :**
- Critic : φ ← φ + α_φ·δ·∇_φ V_φ(s), où δ = r + γ·V_φ(s') - V_φ(s)
- Actor : θ ← θ + α_θ·∇_θ log π_θ(a|s)·A(s,a)

## 7.3 Exploration vs Exploitation

### 7.3.1 Multi-Armed Bandit

**Problème :**
K bras (actions), chacun avec distribution de récompense inconnue.
But : maximiser récompense totale.

**Stratégies :**

1. **ε-greedy :**
   - Avec prob ε : exploration (action aléatoire)
   - Avec prob 1-ε : exploitation (meilleure action connue)

2. **UCB1 (Upper Confidence Bound) :**
   Choisir action a maximisant :
   
   μ̂_a + √(2 ln t / n_a)
   
   où μ̂_a = moyenne empirique, n_a = nombre d'essais, t = temps total.

3. **Thompson Sampling :**
   Maintenir distribution bayésienne sur paramètres, échantillonner et choisir meilleure action.

### 7.3.2 Régret et Bornes

**Régret cumulé :**
Regret(T) = T·μ* - Σₜ rₜ

où μ* = meilleure récompense moyenne.

**Théorème (Lai & Robbins) :**
Pour toute stratégie, Regret(T) = Ω(log T).

**UCB1 atteint :**
Regret(T) = O(K log T / Δ)

où Δ = gap entre meilleures/pires actions.

---

# SYNTHÈSE ET INTÉGRATION

## Pipeline Complet du Bot Intelligent

### 1. Représentation (Structures de Données)
- Bitboards pour états
- Union-Find pour composantes
- Cache topologique (cycles détectés)
- Index spatial pour adversaires

### 2. Détection Topologique
- Incrémenter E_c, V_c après chaque coup
- Si E_c ≥ V_c : extraction DFS du cycle
- Validation simplicité
- Homologie (si cas complexe)

### 3. Calcul d'Intérieur
- Pick's theorem pour comptage rapide
- Ray casting pour identification précise
- Ou flood fill (coût O(N))

### 4. Champ de Potentiel
- Résoudre ∇²φ = f via SOR/CG
- Update incrémental après chaque coup
- Utiliser φ comme prior dans MCTS

### 5. Recherche MCTS
- Selection via UCT avec prior φ
- Expansion guidée par heuristiques
- Simulation avec rollout informé
- Backpropagation

### 6. Évaluation
- Features : capture potentielle, territorial, risque, mobilité
- Poids appris ou manuels
- Intégration dans fonction de valeur

### 7. Décision
- Choisir action avec meilleur Q ou N après MCTS
- Ou politique directe via neural network

---

# COMPLEXITÉS RÉCAPITULATIVES

| Opération | Complexité | Note |
|-----------|------------|------|
| Union-Find (amortie) | O(α(n)) ≈ O(1) | Quasi-constant |
| Détection cycle DFS | O(V_c + E_c) | Local à composante |
| Ray casting | O(\|C\|) | Par point testé |
| Flood fill | O(N) = O(1024) | Acceptable |
| Pick's theorem | O(\|C\|) | Très rapide |
| Homologie (Gauss GF2) | O(m³) | m ≈ 2000, faisable |
| SOR (100 iter) | O(100·N) | ~100k ops |
| CG (convergence) | O(√N · N) | ~30k ops |
| MCTS (T simulations) | O(T · depth · b_eff) | Paramétrable |

---

# CONCLUSION MATHÉMATIQUE

Ce jeu combine de manière élégante :
- **Théorie des graphes** (cycles, connexité)
- **Topologie discrète** (Jordan, intérieur/extérieur)
- **Géométrie combinatoire** (Pick, polygones orthogonaux)
- **Homologie algébrique** (trous, classes d'équivalence)
- **Analyse numérique** (EDP discrètes, solveurs itératifs)
- **Théorie des jeux** (minimax, équilibres)
- **Recherche stochastique** (MCTS, bandits)
- **Apprentissage** (RL, approximation de fonction)

Chaque concept mathématique a une justification rigoureuse et une application pratique directe dans l'implémentation d'un bot compétitif.

La beauté réside dans l'interaction entre ces domaines : l'homologie garantit la détection correcte des trous, Pick accélère le comptage, le champ de potentiel guide la recherche, et MCTS équilibre exploration/exploitation de manière optimale.

**Recommandation finale :**
Pour un prototype rapide mais solide :
1. Bitboards + Union-Find
2. DFS cycle + Pick
3. Champ φ via SOR
4. MCTS avec rollout guidé par φ
5. Heuristique composite simple

Pour un bot état-de-l'art :
Ajouter homologie, deep RL, et optimisations avancées (parallel MCTS, neural network priors, etc.).

---

**FIN DU DOCUMENT MATHÉMATIQUE**
