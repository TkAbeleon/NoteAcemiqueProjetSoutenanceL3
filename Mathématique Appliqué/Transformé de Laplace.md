# Définition
La [[Transformé de Laplace]] d'un signal continu $f(t)$, définit pour $t\leq0$ *fonction causale*, et définie par la formule suivante:
$$
\mathcal{L}\{f(t)\}=F(s)=\int_{-\infty}^{+\infty}f(t)e^{-st}\,dx
$$
avec:
- $f(t)$ est la fonction temporel à transfomé
- $F(s)$ est la [[Transformé de Laplace]] du signal $f(t)$
- $s$ est une varible complexe ($s=a+ib$ ,$a,b \in \mathbb{R}$)
- $i^2=-1$
Pour que la [[Transformé de Laplace]] existe, il esy nécéssaire que l'intégrale converge. Cela implique généralement que, $f(t)$ soit une fonction de croissence exponentielement borné, c'est à dire qu'il exite des constante $M$ et $\alpha$ 
$\left\lvert f(t) \right\rvert \leq Me^{at}$ $\forall t \geq 0$
# Propriété
## Unicité:
Cette p^ropiété stipule qu'à chaque fonction temporel $f(t)$ correspond de maniére unique [[Transformé de Laplace]] et vis-versa
## Linéarité
$$
\mathcal{L}\{af(t)+bg(t)\}= aF(s)+bG(s)
$$
$a$ et $b \in \mathbb{R}$
## Dérivation par rapport au temps
$$
\mathcal{L}\{f^{(n)}(t)\}=s^{n}F(s)-s^{n-1}f(0)-s^{n-2}f^{'}(0).. sf^{n-2}(0)-f^{n-1}(0)
$$
$n \in \mathbb{N}$
## Intégration par rapport au temps
$$
\mathcal{L}\{\int_{0}^{t}f(\alpha)\,d\alpha\}=\frac{F(s)}{s}
$$
## Décalage par rapport dans le temps
$$
\mathcal{L}\{f(t-a)\}=e^{-as}F(s)
$$
## Mutliplication par $t^n$
$$
\mathcal{L}\{t^nf(t)\}=(-1)^{n} \frac{d^n}{ds^n}
$$
## Mutliplication par $e^{at}$
$$
\mathcal{L}\{e^{at}f(t)\}=F(s-a)
$$
## Changement d'échélle
$$
\mathcal{L}\{f(at)\}= \frac{1}{a} F(\frac{s}{a})
$$
## Produit de convolution
$$
\mathcal{L}\{f(t)*g(t)\}=\int_{0}^{t}f(\alpha)g(t-\alpha)\,d\alpha
$$
## Fontion périodique
$$
\mathcal{L}\{f(t)\}=\frac{1}{1-e^{-sT}}  \int_{0}^{T} f_0(t)e^{-st}\,dt
$$
![[Fonction périodique]]
## Valeur final
$$
\lim_{t \to 0^+}f(t)=\lim_{s \to +\infty }sF(s)
$$

# [[Transformé de Laplace]] inverse
La transofré de Laplace invece de récuper la fonction temporelle $f(t)$ à paritr da ça trnsfomré $F(s)$. Elle est définie par la formule suivante
$$
\mathcal{L^{-1}}\{f(t)\}=f(t)=\frac{1}{2\pi i}\int_{\alpha -i\omega}^{\alpha+i\alpha} F(s)e^{st}\,ds
$$
où $\alpha$ est constante Réél, la ligne de contour d'intégration est situé dans la région de convergence de $F(s)$.
Mais pour claculer la transofrmé de la Laplce inverse, pmusisuer méthode est courament utlisé
- Utlisation de table de transforé
- Décompostion en élément simple
- Théreme des résidu

| $f(t)$                                                                          | $F(s)$                                         |
| ------------------------------------------------------------------------------- | ---------------------------------------------- |
| $1$                                                                             | $\frac{1}{s}$                                  |
| $e^{at}$                                                                        | $\frac{1}{s-a}$                                |
| $t^n$                                                                           | $\frac{n!}{s^{n-1}}$                           |
| $\cos(\omega t)$                                                                | $\frac{s}{s^2+\omega ^2}$                      |
| $\sin(\omega t)$                                                                | $\frac{\omega}{s^2+\omega^2}$                  |
| $e^{at}\cos(\omega t)$                                                          | $\frac{s-a}{(s-a)^2+\omega ^{2}}$              |
| $e^{at}\sin(\omega t)$                                                          | $\frac{\omega}{(s-1)^2+\omega^2}$              |
| $\delta(t)$                                                                     | $1$                                            |
| $\delta(t-a)$                                                                   | $e^{-as}$                                      |
| $\cosh(kt)$                                                                     | $\frac{k}{s^2-k^2}$                            |
| $\sinh(kt)$                                                                     | $\frac{s}{s^2+k^2}$                            |
| $t^n e^{at}$                                                                    | $\frac{n!}{(s-a)^{n+1}}$                       |
| $u(t-a)$                                                                        | $\frac{e^{-as}}{s}$                            |
| $\frac{1}{2\omega} \sin(\omega t)$                                              | $\frac{s}{\left(s^2+\omega^2\right)^2}$        |
| $\frac{1}{2\omega}\left[ \sin(\omega t) + \omega t \cos(\omega t)   \right]$    | $\frac{s^2}{\left( s^2 +\omega ^ 2 \right)^2}$ |
| $\frac{1}{2\omega ^3}\left[ \sin(\omega t) - \omega t \cos(\omega t)   \right]$ | $\frac{1}{\left( s^2 +\omega ^ 2 \right)^2}$   |
# Fonction de transfert des circuit électrique et électronique

![[Fonction de transfert des circuit électrique et électronique.excalidraw]]
$$
s(t)=f(t)*e(t) 
$$

$$
\mathcal{L} \{s(t)\}=\mathcal{L} \{f(t)*e(t)\}
$$
$$
S(p)=F(p)E(p)
$$
$$
F(p)=\frac{S(p)}{E(p)}
$$
**Exemple:**
![[RL_transfer.excalidraw]]
- $$
e(t)+U_R+U_C=0
$$
$$
e(t)-R.i(t)-L\frac{di(t)}{dt}=0
$$
$$
e(t)-R.i(t)\frac{di(t)}{dt}=0(1)
$$
$$
L\frac{di(t)}{dt}-s(t)=0
$$
$$
s(t)=L\frac{di(t)}{dt}(2)
$$
D'après $(1)$
$$
e(t)=R.i(t)+L\frac{di(t)}{dt}
$$
$$
\mathcal{L}\{e(t)\}=R.\mathcal{L}\{i(t)\}+L.\mathcal{L}\{\frac{di(t)}{dt}\}
$$
$$
E(p)=J(p)(R+p.L)
$$
D'après $(2)$
$$
S(p)=L.p.I(p)
$$
$\Rightarrow$ $F(p)=\frac{S(p)}{E(p)}$
$$
F(p)=\frac{L.p.I(p)}{(R+L.p).I(p)}
$$
$$
F(p)=\frac{L.p}{R+L.p}
$$

> [!hint] Formule
> - **Bobine**:
> $$
> v(t)=L\frac{di(t)}{dt}
> $$
> - **Condensateur**:
> $$
> i(t)=C\frac{dv(t)}{dt}
> $$
> - **Résistance**:
> $$
> v(t)=R.i(t)
> $$
