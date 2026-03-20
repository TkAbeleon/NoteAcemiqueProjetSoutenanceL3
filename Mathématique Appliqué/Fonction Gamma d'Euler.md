# Définition

La [[Fonction Gamma d'Euler]] est définit par la formule suivante
> [!important]
> 
> $$
> \Gamma (z)= \int_{+ \infty }^{0} x^{z-1}e^{-x} \,dx
> $$
> 
> Avec $\Gamma(z)$ représente la fonction d'Euler où $z \in \mathbb{C}$ et $Re(z)>0$


*Exemple*:

$$
\Gamma(2)= \int_{+\infty}^{0}x^{2-1}e^{-1}\,dx
$$

$$
\Gamma(2)= \int_{+\infty}^{0}x e^{-1}\,dx
$$

$$
U=x \Longrightarrow U'=1
$$

$$
V=-e^{-x}\Longleftarrow  V'=e^{-x}
$$

$$
\Gamma(2)=1
$$

# Propriété:

## Valeur en $1$
> [!note]
> 
> $$
> \Gamma(1)=1
> $$
> 

## Valeur en $\frac{1}{2}$
> [!note]
> 
> $$
> \Gamma(\frac{1}{2})= \sqrt{\pi}
> $$
> 


## Relation de récurrence(prolongement analytique)
> [!note]
> 
> $$
> \Gamma(z+1)=z\Gamma(z)
> $$
> 
> où $z \in \mathbb{C} \setminus \mathbb{Z}^{-}$

*Exemple*
**Calculer**
$\Gamma(10)=9\Gamma(9)$
$\Gamma(9)=8.9\Gamma(8)$
$...$
$\Gamma(1)=9!=362880$
**Calculer**:$\Gamma(\frac{9}{2})$
$\Gamma(\frac{9}{2})=\frac{105}{16}\sqrt{\pi}$
**Calculer** $\Gamma(-\frac{1}{2})$
$-\frac{1}{2}\Gamma(-\frac{1}{2})= \Gamma(-\frac{1}{2} +1)= \Gamma(\frac{1}{2})$
$\Longrightarrow \Gamma($

## Relation avec la factoriel
> [!note]
> 
> $\Gamma(z)= (z-1)!$
> où $z \in \mathbb{N}^*$
> 

**Calculer $\Gamma(13)= 12!= 479001600$**

## Formule de Legendre

> [!info]
> $$\Gamma(z)\Gamma(z+\frac{1}{2})= 2^{1-2z}\sqrt{\pi}\Gamma(2z)$$

où $z \in \mathbb{C}$ tel que $\mathcal{Re}\{ z\} >0$
*Calculer $\Gamma(12)$*
*Calculer $\Gamma(\frac{13}{2})$*
## Formule de duplication de Legendre
> [!note]
> $$
> \Gamma(z+\frac{1}{2})=\frac{(2z)!}{4^z (z!)}\sqrt{\pi}
> $$
> où $z \in$  $\mathbb{N}$

*Calculer $\Gamma(\frac{7}{2})$*
 $\Gamma(\frac{7}{2})=\frac{15}{8}\sqrt{\pi}$



## Formule d'Euler
> [!note]
> 
> $$
> \Gamma(z)\Gamma(1-z)=\frac{1}{\sin(\pi z)}
> $$
> où $z \in \mathbb{R} \setminus \mathbb{Z}$


*Calculer $\Gamma(-\frac{3}{2})$, $\Gamma(\frac{1}{3})\Gamma(\frac{2}{3})$*
# Méthode d'utilisation
## Méthode 1
Soit $I$ une intégral définit par
$$
I= \int_{0}^{+\infty}x^{a}e^{-x}\,dx
$$
où $a \in \mathbb{C}$ tel que $\mathcal{Re}\{ z\} >0$
Pour calculer ce type d'integral il suffit de suivre les étapes suivante
### Effectuer la décomposition suivante $a=z-1$
### Déterminer la valeurs de $z$
### Remplacer $a$ par $z-1$
**Exemple**:
$$I=\int_{0}^{+\infty}x^5 e^{-x}\, dx$$
$5=z-1$
$6=z$
$5=6-1$
$$
I = \int_{0}^{+\infty}
$$
## Méthode
Soit une $I$ une intégrale définit par:
$$
I=\int_{0}^{+\infty} x^ae^{-bx^p}\,dx
$$
Pour calculer ce type d'intégral il suffit de poser $t=bx^p$
**Calculer l'intégral $I$ suivante**
$$
I=\int_{0}^{+\infty} \sqrt{x} e^{-x^3}\, dx

$$
Posons $t=x^3 \Longrightarrow$,$b=-1$,$p=3$
$t=x^3 \Longrightarrow x=t^{-3}$
$dt=3x^2 dx$
$dt=3(t^{-3})^{2}dx$
$dt=3t^{-6}dx$
$\frac{t^6}{3}dt=dx$
$$
I=\int_{0}^{+\infty} \sqrt{t^{-3}} e^{-t}\,dt
$$
$$
I=\int_{0}^{+\infty} t^{9} e^{-t}\,dt
$$
$$I=\frac{1}{3}\sqrt{\pi}$$ 

**Calculer**
$$
I=\int_{0}^{+\infty} x^{\frac{5}{2}}e^{-2x}\,dx
$$
Posons $t=2x \Longrightarrow x=\frac{t}{2}$
$dt=2dx$
$dx=\frac{dt}{2}$
$$
I=\int_{x}^{+\infty} \left( \frac{t}{2} \right)^{\frac{5}{2} }e^{-t} \frac{dt}{2}
$$
$$
I=\frac{1}{2} \left(\frac{1}{2}\right)^{\frac{5}{2}} \int_0^{+\infty}t^{\frac{5}{2}} e^{-t}\,dx
$$
$$
I=\frac{15}{64}\sqrt{\frac{\pi}{2}}
$$
## Méthode 3
Soit l'intégrale 
$$
I = \int_0^1 \left[-\ln(x)\right]^{z-1}\,dx
$$
Pour calculer ce type d'intégral il suffit de poser $x=e^{-t}$
**Calculer $I = \int_0^1 \left[-\ln(x)\right]^{\frac{13}{2}}\,dx$**
Posons $x=e^{-t}$

