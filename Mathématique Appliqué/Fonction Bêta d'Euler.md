# Definition
La fonction Bête d'Euler est définit par la formule suivant
$$
\beta(m,n)=\int_{0}^{1} x^{m-1}\left(1-x\right)^{n-1}\,dx
$$
avec 
$\beta(m,n)$ représente la [[Fonction Bêta d'Euler]] 
$m \in \mathcal{Re}\{m\}>0$
$n \in \mathcal{Re}\{n\}>0$
**Calculer**
$\beta(m,n)=\frac{1}{12}$
$\beta(4,\frac{1}{2})=\frac{32}{35}$
# Propriété:
## Si $m=1$
$$
\beta(1,n)=\frac{1}{n}
$$
où $n \in \mathbb{C}$ tel que $\mathcal{Re}\{n\}>0$
## Si $n=1$
$$\beta(m,1)=\frac{1}{m}$$



## Si $n=m=\frac{1}{2}$
$$\beta(\frac{1}{2},\frac{1}{2})=\pi$$
## Symétrie:
$$\beta(m,n)=\beta(n,m)$$


## Valeur spécial
$$\beta(m,1-m)=\frac{\pi}{\sin(\pi m)}$$
**Exemple**
$$\beta(\frac{1}{3},\frac{2}{3})=\frac{2\sqrt{3}\pi}{3}$$
## Relation avec la [[Fonction Gamma d'Euler]]
$$\beta(m,n)=\frac{\Gamma(m)\Gamma(n)}{\Gamma(m+n)}$$
**Exemple:
$\beta(4,13)=\frac{1}{7280}$
$\beta(7,\frac{3}{2})=\frac{2048}{45045}$
$\beta(\frac{5}{12},\frac{15}{2})=\frac{143\pi}{65536}$
# Méthode d'utilisation

## Méthode 1

Soit $I$ une integral définit par
$$
I=\int_{0}^{1} x^{a}(1-x)^{b}\,dx
$$
- Effectuer les décomposition suivante $a=m-1$ et $b=n-1$
- Déterminer les valeurs de $m$ et $n$
- Remplacer $a$ par $m-1$ et par $b$ par $n-1$
**Exemple**
$I=\int_{0}^{1} x^{-\frac{1}{3}}(1-x)^{-\frac{2}{3}}\,dx=\frac{2\sqrt{3}\pi}{3}$
$I=\int_{0}^{1} x^{2}(1-x)^{\frac{3}{2}}\}\,dx=\beta(3,\frac{5}{2})=\frac{16}{315}$
## Méthode 2
Soit $I$ un integral définit par
$$I=\int_{0}^{a}x^{m-1}(a-x)^{n-1}\, dx$$
Pour calculer ce type d'intégral il suffit de poser $t=\frac{x}{a}$

**Exemple**
$$I=\int_{0}^{3}x^{\frac{7}{2}}(3-x)^{\frac{1}{2}}\, dx=\beta(\frac{9}{2},\frac{3}{2})=\frac{1701}{256}\pi$$
## Méthode 3
Soit $I$ une intégral définit par
$$I=\int_{0}^{1}x^{m-1}\left(a-ax^k\right)^{n-1}\,dx$$
où $k$, $a>0$

Pour calculer il suffit de suivre les étapes suivant
- Factoriser $a$
- Poser $t=x^k$
**Exemple**
$$
I= \int_{0}^{1}x^{5}(3-3x^4)^{\frac{7}{2}}\,dx=\frac{3^{\frac{7}{2}}}{4}\beta\left(\frac{3}{2},\frac{9}{2}\right)=\frac{189}{1024}\sqrt{3}\pi
$$

## Méthode 4
$$
\beta(m,n)=2\int_{0}^{\frac{\pi}{2}} \sin^{2m-1}{(\theta)\cos^{2n-1}{(\theta)}}\,d\theta
$$
**Exemple**
$$
I=\int_{0}^{\frac{\pi}{2}} \sin^{4}{(\theta)\cos^{3}{(\theta)}}\,d\theta=
\frac{1}{2}\beta\left(\frac{5}{2},2\right)
=\frac{2}{35}
$$
## Méthode 5
$$
\beta(m,n)=\int_{0}^{+\infty}\frac{x^{m-1}}{(1+x)^{m+n}}\,dx
$$
$$
I=\int_{0}^{+\infty}\frac{x^{3}}{(1+x)^{6}}\,dx=\beta(2,4)=\frac{1}{20}
$$


