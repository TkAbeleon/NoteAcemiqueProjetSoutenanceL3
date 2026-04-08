# Définition
La Fonction Zêta de Riemann est définit par le formule suivante
$$
\zeta(s) = \sum_{n=1}^{+\infty} \frac{1}{n^s}
$$
avec :
$\zeta(s)$ représente la [[Fonction Zêta de Riemann]]
$s \in \mathbb{C}$ tel que $\mathfrak{Re} \{s\}> 0$
$n \in \mathbb{N}^*$
# Propriété
## Formule d'Euler
### Méthode pour calculer $\zeta(2k)$

Pour calculer $\zeta(2k)$ il suffit d’utiliser la formule suivante
$$
\zeta(2k)=\left[\frac{(-1)^{k+1}}{2}\right]\left[\frac{B_{2k}(2\pi) ^{2k}}{(2k)!}\right]
$$

avec :
- $k \in N$
- $B_n$ sont les nombre de Bernoulli est définit par la formule suivante

$$B_n = \sum_{i=0}^{n-1} C_n^i B_i=0$$
Calculer: $B_1$ $B_2$ $B_3$ $B_4$ $B_5$
- $B_0=1$
- $B_1=\frac{1}{6}$
- $B_3=0$
- $B_4=-\frac{1}{30}$
- $B_5=0$
**Calculer $\zeta(2)$, $\zeta(4)$**
- $\zeta(2)=\frac{\pi^2}{6}$
- $\zeta(4)=\frac{\pi^4}{90}$

### Méthode pour calculer $\zeta(-k)$ (Prolongement)
Pour calculer $\zeta(-k)$ il suffit d'appliquer la formule suivante
$$
\zeta(-k)= \left[\frac{(-1)^k}{k+1}\right]B_{k+1}
$$
Calculer $\zeta(-1)$
$$
\zeta(-1)= \left[\frac{(-1)^1}{1+1}\right]B_{1+1}
$$
$$\zeta(-k)= \left[\frac{-1}{2}\right]\frac{1}{6}$$
$$
\zeta(-1)=-\frac{1}{12}=1+2+3+4+...+\infty
$$
- $\zeta(-2)=0$

## Equation fonctionnel (Prolongement analytique)
$$
\zeta(s)=2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)
$$
Avec
- $s \in \mathbb{C} \setminus \mathbb{N*}$
**Calculer $\zeta(-3)$**
$\zeta(-3)=\frac{1}{120}$
## Relation avec la [[Fonction Gamma d'Euler]] (prolongement analytique)
$$
\zeta(s)=\frac{1}{\Gamma(s)} \int_{0}^{+\infty}\frac{x^{s-1}}{e^x -1}\,dx
$$
où $s \in \mathbb{C} \setminus \mathbb{Z^-}$
**Calculer**
$$
I= \int_{0}^{+\infty}\frac{x^7}{e^x - 1}\,dx=\frac{8}{14}\pi^8
$$
## Zéros de la [[Fonction Zêta de Riemann]]
### Définition
Les zéro de $\zeta(s)$ sont les valeurs $s$ pour lesquels $\zeta(s)=1$
### Zéro triviaux
Les zéro triviaux sont les entier paires négatif. De point de vue mathématique, en peut écrire que:
$$
\zeta(s) =0
$$
si $s = -2k$ où $k \in \mathbb{N^*}$
**Monter que $-2k$ sont zéro de fonction zêta si $n \in \mathbb{N^*}$**
$$
\zeta(s)=2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)
$$
$$
\zeta(-2k)=2^{-2k} \pi^{-2k-1} \sin\left(\frac{\pi (-2k)}{2}\right) \Gamma(1-(-2k)) \zeta(1-s)

$$
$$
\zeta(-2k)=2^{-2K} \pi^{-2K-1} \sin(-k\pi) \Gamma(1-(-2k)) \zeta(1-s)
$$
avec $\sin(-k\pi=0$
$$
\zeta(-2k)=0
$$
### Zéro non triviaux (hypothèse de Riemann)
Les zéro non triviaux de $\zeta(s)$ sont les nombres complexe située dans la bande critique. Du point vue mathématique on peut écrire que:
$$
\zeta(s)=0$$
si $s=a+ib$
Avec:
En 1859, Riemann a formulé l'hypothèse selon laquelle que tous les zéros non triviaux de $\zeta(s)$ se trouve sur la droite critique de la partie réelle $\frac{1}{2}$, ce qui veut dire que $\zeta(s)=0$ ,$b \in \mathbb{R^*}$
Ce problème connu sous le non de l'hypothèse de Riemann demeure non démonter de nos jours. En l'ans 2000, l'institut de mathématique **Clay** a classé cette conjecture permis les 7 problème de millionaire a annoncé un récompense d'un million américain à toutes personne qui parviendrais à fournir une demonstration rigoureuse.
*Exemple*
Montrer que $\frac{1}{2} + ib$  tel que $b \in \mathbb{R^*}$sont les zéro on triviaux de $\zeta(s)$
Résoudre ce problème serait un exploit extraordinaire celui qui y parviendrais un grand mathématiciens reconnus dans le mondes entier en même niveau que des génie que Euler, Gauss, Poincare, Riemann