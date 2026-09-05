# ZFC, material set theory

**Axiom of Empty Set**: $\exists A \forall x (x \in A)$

By Extensionality, there is exactly one such set; we denote it $\emptyset$.

Logic of ZFC: first-order logic with equality. Logical symbols: $\forall$, $\exists$,¬,∧,∨,⇒,⇔,= (if equality is taken as logical), plus variables and punctuation.

Set-theoretic symbol: the single binary relation symbol $\in$.

# **Notation**

Algebraic structure: set equipped with one or more operations and rules.

Relational structure: set equipped with one or more relations and rules.

$|A| \equiv \text{det}A$

`′ &prime;`
Symbol Name: 	Prime
Html Entity: 	`&prime;`
Hex Code: `&#x2032;`
Decimal Code: 	`&#8242`;

## Set Theory

$A$ set, $\emptyset \subseteq A$ is vacuously true. $\emptyset$ can be an element of $A$.

## Real Numbers

Dedekind cut:

$A, B$ disjoint sets, $A\cap B = \mathbb{Q}$, $A$ is the set below, $A$ has no maximal element.
If $B$ has a minimal element the cut is a rational number, otherwise the gap is the irrational number defined by the cut.

The powerset of $\mathbb{Q}$ has the cardinality of $\mathbb{R}$

$a, b, c, x, z \in \mathbb{R}_{>0}$

$$\ln(a)=\int_1^a\frac{1}{x}\mathrm{d}x$$

$a^x := \mathrm{e}^{x\ln(a)}$ 

$\ln(a^x)=x\ln(a)$

$$\log_a b = \frac{\log_c b}{\log_c a}$$

## Complex Numbers

$\mathbb{C} = \mathbb{R} \times \mathbb{R}$ $\quad$ $(x, y) \equiv x + \mathrm{i}y$ $\quad$ $\mathrm{e}$ Euler number

With the natural identification of any real number $r$ with the complex number $(r, 0) = r + \mathrm{i} * 0 = r$,
we can think of $\mathbb{R}$ as a subset of $\mathbb{C}$.

$z \in \mathbb{C}$ $\quad \mathrm{i}^2 = -1 = \mathrm{e}^{\mathrm{i}\pi}$

$$\mathrm{e}^{z}=\sum _{n=0}^{\infty }{\frac {z^{n}}{n!}}$$

$$\cos x ={\frac {\mathrm{e}^{\mathrm{i}x}+\mathrm{e}^{-\mathrm{i}x}}{2}}$$
$$\sin x ={\frac {\mathrm{e}^{\mathrm{i}x}-\mathrm{e}^{-\mathrm{i}x}}{2\mathrm{i}}}$$

$$\sin z =\sin x\cosh y+\mathrm{i}\cos x\sinh y$$ $$\cos z =\cos x\cosh y-\mathrm{i}\sin x\sinh y$$

$$\cosh(x)=\frac{1}{2}(\mathrm{e}^x+\mathrm{e}^{-x})$$

$$\sinh(x)=\frac{1}{2}(\mathrm{e}^x-\mathrm{e}^{-x})$$

$\mathrm{e}^{\mathrm{i}x}=\cos x+\mathrm{i}\sin x $

$|\mathrm{e}^{z}|=\mathrm{e}^{\Re (z)}$

$ z = \big| z \big| \cdot
\big( \cos\theta + \mathrm{i}\sin\theta \big) $

$\big| z \big| = \sqrt{x^2 + y^2}$

$\cos n \theta + \mathrm{i} \sin n \theta =
\big( \cos \theta + \mathrm{i} \sin \theta \big) ^n$

boundedness

$A \subseteq \mathbb{C}$, $a\in A$ limit point of $A$.

$f: A \to \mathbb{C}$ is **differentiable at** if
$$\lim_{x\to a} \frac{f(x)-f(a)}{x-a}$$ exists. **the derivative of f at a**

Newton notation: $f'(a) = (f(x))'|_{x=a}$

Leibniz notation: $\frac{df}{dx}(a) = \frac{df(x)}{dx}|_{x=a}$

A function is **differentiable** if it is differentiable at all points in its domain.

$$\zeta_n:=e^{2π\mathrm{i}/n}=\cos\frac{⁡2π}{n}+\mathrm{i}\sin\frac{⁡2π}{n}$$
It is a **primitive n-th root of unity**

**unitary**: $U^* U=UU^* =I$

Complex Exponential $\mathrm{e}^{\mathrm{i} 2 \pi f_0 t}$, reverse Fourier transform of the Dirac delta function.

$\mathcal{F}\{\sin(2\pi f_0 t)\} = \frac{1}{2\mathrm{i}}\delta(f-f_0)-\frac{1}{2\mathrm{i}}\delta(f+f_0)$
$=\frac{\mathrm{i}}{2}\delta(f+f_0)-\frac{\mathrm{i}}{2}\delta(f-f_0)$

$\mathcal{F}\{\cos(2\pi f_0 t)\} = \frac{1}{2}\delta(f-f_0)+\frac{1}{2}\delta(f+f_0)$

Hopf oscillator:

dz/dt = (μ + iω)z - α|z|²z

---

$M$ topological space

$D$ manifold

https://en.wikipedia.org/wiki/Physical_system

https://en.wikipedia.org/wiki/Configuration_space_(physics)

***

Quantum Mechanics is based on the Hamiltonian formalism. For a closed system the **Hamiltonian** is the sum of the kinetic (T) and potential (V) energy in the system. $\mathcal{H}(q,p,t) = T + V$, $p = (p_1,...,p_n)$, momentum $p_i$ is conjugate to $q_i$.

$p_i \equiv \frac{\partial \mathcal{L}}{\partial \dot q_i}$

General Relativity is a based on the Lagrangian formalism. $\mathcal{L}(q,\dot q, t) = T - V$, $q = (q_i,...,q_n)$ generalized coordinates.

$\frac{\mathrm{d}}{\mathrm{d}t}\frac{\partial \mathcal{L}}{\partial \dot q} - \frac{\partial \mathcal{L}}{\partial q} = 0$

$S = \int_{t1}^{t2}\mathcal{L}(q,\dot q, t)\mathrm{d}t$, action

---

https://en.wikipedia.org/wiki/Self-oscillation

https://ncatlab.org/nlab/show/state

## Cauchy-Riemann Equations

The Cauchy–Riemann equations on a pair of real-valued functions of two real
variables $u(x,y)$ and $v(x,y)$ are the two equations:

$$\tag{1a} \quad \frac{\partial u}{\partial x}=\frac {\partial v}{\partial y}$$
$$\tag{1b} \quad \frac{\partial u}{\partial y}=-\frac {\partial v}{\partial x}$$

Typically $u$ and $v$ are taken to be the real and imaginary parts respectively of
a complex-valued function of a single complex variable, $f(x + \mathrm{i}y) =
u(x,y) + \mathrm{i}v(x,y)$. Suppose that $u$ and $v$ are $\color{green}\text{real-differentiable}$ at a point in an open subset of $\mathbb{C}$, which can be considered as
functions from $\mathbb{R}^2$ to $\mathbb{R}$. This implies that the $\color{green}\text{partial derivatives}$ of $u$ and $v$
exist (although they need not be $\color{red}\text{continuous}$) and we can approximate small
variations of $f$ linearly. Then $f = u + \mathrm{i}v$ is **complex-differentiable** at that
point if and only if the partial derivatives of $u$ and $v$ satisfy the
Cauchy–Riemann equations (1a) and (1b) at that point. The sole existence of
partial derivatives satisfying the Cauchy–Riemann equations is not enough to
ensure complex differentiability at that point. It is necessary that $u$ and $v$ be
real differentiable, which is a stronger condition than the existence of the
partial derivatives, but it is not necessary that these partial derivatives be
continuous.

**Holomorphy** is the property of a complex function of being differentiable at
every point of an $\color{green}\text{open}$ and $\color{green}\text{connected}$ subset of $\mathbb{C}$ (this is called a **domain** in
$\mathbb{C}$). Consequently, we can assert that a complex function $f$, whose real and
imaginary parts $u$ and $v$ are real-differentiable functions, is **holomorphic** iff equations (1a) and (1b) are satisfied throughout their domain. Holomorphic functions are $\color{green}\text{analytic}$ and vice versa. This means
that, in complex analysis, a function that is complex-differentiable in a whole
domain (holomorphic) is the same as an analytic function. This is not true for
real differentiable functions.

## Topology

shapes

A **space** is a $\color{green}\text{set}$ (sometimes called a $\color{green}\text{universe}$) with some
added $\color{green}\text{structure}$ ($\color{gree}\text{objects}$ in the set are $\color{green}\text{related}$ to each other).

A set with a topology is called a **topological space**.

An open set generalizes the
idea of an open interval in the real line.

https://pi.math.cornell.edu/~hatcher/

-> "Introductory Point-Set Topology"

let $X$ be a set and let $τ$ be a family of subsets of $X$. Then
$τ$ is called a topology on $X$ if:

-    Both the empty set and $X$ are elements of $τ$.
-    Any union of elements of $τ$ is an element of $τ$.
-    Any intersection of finitely many elements of $τ$ is an element of $τ$.

The members of $τ$ are called open sets in $X$. A subset of $X$
is said to be closed if its complement is in $τ$ (i.e., its
complement is open). A subset of $X$ may be open, closed, both
(clopen set), or neither. The empty set and $X$ itself are
always both closed and open. A subset of $X$ including an open
set containing a point $x$ is called a 'neighborhood' of $x$.

Every *metric space* is, in a natural way, a topological space. There are, however, topological spaces that are not metric spaces.

A **surface** is a two-dimensional manifold, 2-manifold. It can be a sphere (locally it is flat 2d euclidean).

A vector bundle assigns a vector space to each point of a topological space, varying continuously across 

$T$, tangent bundle

The finest topology on $X$ is the discrete topology; this
topology makes all subsets open. The coarsest topology on $X$
is the trivial topology; this topology only admits the empty
set and the whole space as open sets.

Given topological spaces $X$ and $Y$, a function $f$ from $X$ to $Y$
is **continuous** if the $\color{red}\text{preimage}$ of every open set in $Y$ is open
in $X$. The function $f$ is called **open** if the 
$\color{red}\text{image}$ of every
open set in $X$ is open in $Y$.

Two coninuous functions from one topological space to
another are called **homotopic** if one can be "continuously
deformed" into the other, such a deformation being called a
**homotopy** between the two functions.

***

https://www.youtube.com/watch?v=1BhSQiHTNbg

https://mathworld.wolfram.com/Measure.html

https://en.wikipedia.org/wiki/Function_space

Measurable Space. A set considered together with the $\sigma$-algebra on the set. 

A measure space is a measurable space possessing a nonnegative $\color{red} \text{measure}$.

The Lebesgue measure is an extension of the classical notions of length and area to more complicated sets. 

On a measure space $X$, the set of square integrable L2-functions is an $L^2$-space.

Taken together with the L2-inner product with respect to a measure $\mu$,
$\langle f,g \rangle =\int_X f g \mathrm{d}\mu$ the $L^2$-space forms a Hilbert space. 

## 3D Euklidean Space

All three-dimensional Euclidean spaces
are mutually $\color{green}\text{isomorphic}$. In this sense we have "the" three-dimensional
Euclidean space. In terms of Bourbaki, the corresponding theory is univalent

A $\color{green}\text{vector space}$ with a scalar product.

Topological notions (continuity, convergence, open sets,
closed sets etc.) are defined naturally in every Euclidean
space. Every Euclidean space is also a
topological space.

## Inner Product Space

$(L_2, \langle-,-\rangle_2)$ inner product space, $L_2$ (set of square inegrable functions).

**square integrable** function:
$f$ $\color{red}\text{measurable}$ function, $\int_{-\infty}^\infty |f(x)|^2 \mathrm{d}x < \infty$ (on the real line)

***

**Inner product** $⟨-,-⟩:V×V→k$, $\color{green}\text{sesquilinear}$ and $\color{green}\text{conjugate-symmetric}$.

$f$, $g$ square integrable functions.
$⟨f,g⟩ = \int_A \overline{f(x)}g(x)\mathrm{d}x$, $A$ set over which one $\color{green}\text{integrates}$ ($-\infty$,$+\infty$) real line).

$⟨f,f⟩ < \infty$, since $|a|^2 = a\bar{a}$

https://en.wikipedia.org/wiki/Hermitian_adjoint

## Hilbert Space

Vector space with $\color{red}\text{positive definite Hermitian}$ inner product. Complete (as a topological space) with respect to the induced $\color{red}\text{metric}$.

Any general property of $\color{red}\text{Banach spaces}$ continues to hold for Hilbert spaces.

$H^*$, dual space of $H$

## Fixed Point

$f(x)=x$

https://en.wikipedia.org/wiki/Hyperbolic_equilibrium_point

## Quantum Mechanics

average: $$\langle A \rangle_\varphi = \frac{\int \varphi^* \hat A \varphi \mathrm{d}\tau}{\int \varphi^* \varphi \mathrm{d} \tau}$$

$\hat A$ is an operator acting on the wavefunction $\varphi$

(measurement)

$\triangle x = \sqrt{\langle x^2 \rangle - \langle x \rangle^2}$ $\quad$ $\triangle p = \sqrt{\langle p^2 \rangle - \langle p \rangle^2}$

$\triangle x \triangle p \ge \frac{\hbar}{2}$ $\quad$ **Heisenberg uncertenty** principle

Original quantum mechanics (1920s) was non-relativistic.

Many systems are non-relativistic: Electrons in atoms move at ~1% of light speed—relativistic effects are small corrections

1930s-40s: Quantum Field Theory (fully relativistic)

A **stationary state** does not change in time.

**degenerate state**: same Energy, different quantum states.

Niels Bohr's **correspondence principle** states that quantum mechanics must reproduce classical results in the limit of large quantum numbers or large actions.

$\ket{\psi} = \sum_i c_i\ket{\phi_i}$, $c_i \in \mathbb{C}$. The $\phi$s are the chosen basis. There is no preferred basis.
$\braket{\phi_i|\phi_j} = \delta_{ij}$

$|c_i|^2 = c_i^* c_i$, probability of measuring the system to be in the state $\ket{\phi_i}$ after measurement, which means $\ket{\psi}$ colapses into $\ket{\psi_i}$.

$\braket{\varphi|\psi}$ probablility amplitude for the state $\psi$ to collapse into the state $\varphi$

$\psi(r) = \braket{r|\psi}$
    
$A\psi(r) = \braket{r|A|\psi}$

physically $\ket{\psi} \sim c\ket{\psi}$, $c \neq 0$

***

**phase shift**: When two objects are oscillating and are not perfectly in sync, i.e., they don't reach the maximum of their oscillations at the same time, they are said to be "out of phase". The phase shift is a measure of how far apart the two oscillations are.

**Phase** in sinusoidal functions or in waves has two different, but closely related, meanings. One is the initial angle of a sinusoidal function at its origin and is sometimes called phase offset or phase difference. Another usage is the fraction of the wave cycle that has elapsed relative to the origin.

***

## Manifold

A **manifold** is a lower-dimensional subspace of some parent space that is locally similar to a linear (Euclidean) space.

Variety vs Manifold (2 Major Differences): https://www.youtube.com/watch?v=5XrvrU2SR5A

A **chart** for a topological space (also called local frame)
is a homeomorphism $\rho$ from an open subspace $U$ of $M$ to an
open subspace of Euclidean space.

An **atlas** for a *topological space* is a collection ${(U_{\alpha},\rho_\alpha)}$
of *charts* on $M$ such that $\bigcup U_\alpha=M$. If the codomain
of each chart is the $n$-dimensional Euclidean Space and the atlas is connected,
then $M$ is said to be a **n-dimensional manifold**.

A smooth function is a function that has derivates
of all orders everywhere in its domain. If each $\color{red}\text{transition function}$ is a $\color{red}\text{smooth map}$, then the atlas is called
a smooth altlas, and the manifold itself is called **smooth**.


All the $\color{red}\text{tangent spaces}$ can be "glued together" to form a new
differentiable manifold of twice the dimension of the original
manifold, called the **tangent bundle** of the manifold.

A **symplectic manifold** is a smooth manifold
equipped with a $\color{red}\text{closed nondegenerate differential 2-form}$,
called the symplectic form.

Symplectic manifolds serve as the phase spaces in the
Hamiltonian formalism of classical mechanics, while
four-dimensional Lorentzian manifolds model spacetime in
general relativity.

Minkowski space is a flat (the simplest) Lorentzian manifold.

Any smooth real-valued function $H$ on a *symplectic
manifold* can be used to define a Hamiltonian system.
The function $H$ is known as the *Hamiltonian* or energy
function.

#### Complex Manifold

A **Riemann surface** is a connected one-dimensional *complex manifold*.

The transition maps are "holomorphic" (complex-differentiable). When you switch from one complex coordinate chart to another, the function that does the switching must be not just smooth, but complex smooth. This is a much stricter condition than regular smoothness.

### Lie Group

A **Lie group** is a $\color{green}\text{group}$ that is also a $\color{red}\text{differentiable manifold}$, with the
property that the group operations are compatible with the smooth structure.

Euclidean space $\mathbb{R}^n$ with ordinary vector addition as the
group operation becomes an n-dimensional noncompact abelian
Lie group.

## Tensor

A **Tensor** is a $n$-dimensional array of numbers.
($n=1$: vector; $n=2$: matrix).

**Tensor**: a element of the tensor product. Type $(m,n)$ tensor.
$\underbrace{V\otimes\dots\otimes V}_m$ $\otimes$ $\underbrace{V^\star \otimes \dots \otimes V^\star}_n$


---

"Operator" vs "Function"

When both terms are available, mathematicians often distinguish:

-    Function: usually maps numbers to numbers (f:R→R)

-    Functional: maps functions to numbers (F:V→R)

-    Operator: maps functions to functions (T:V→V) — typically linear

Examples:

$f(x)=x^2$ → function

$F[f]=∫_0^1f(x)$ → functional

$Tf=\frac{df}{dx}$ → (differential) operator

***

# Multilinear Algebra

$
\begin{matrix}
\text{linear algebra} & \text{function} \\\\
\text{linear transformation} & \text{linear operator} \\\\
\text{dot product} & \text{inner product} \\\\
\text{Eigenvector} & \text{Eigenfunction} \\\\
\end{matrix}
$

space: all ploynomials

basis functions:  
$b_0(x)=1$  
$b_1(x)=x$  
$b_2(x)=x^2$  
...

linear operator / linear function:  
$\frac{d}{dx}(1x^3 + 5x^2 + 4x + 5)$

$\displaystyle
\begin{pmatrix} 0 & 1 & 0 & 0 & \ldots
\\ 0 & 0 & 2 & 0 & \ldots
\\ 0 & 0 & 0 & 3 & \ldots
\\ 0 & 0 & 0 & 0 & \ldots
\\ \vdots & \vdots & \vdots & \vdots & \ddots
\\ \end{pmatrix}
\begin{pmatrix} 5 \\ 4 \\ 5 \\ 1 \\ \vdots \\ \end{pmatrix} =
\begin{pmatrix} 1\cdot 4 \\ 2\cdot 5 \\ 3\cdot 1 \\ \vdots \\ \end{pmatrix} =
3x^2+10x+4
$



## Metric space

Pair $(X,d)$ where $X$ is a set and $d$ a metric
on $X$

$d: X\times X \rightarrow \mathbb{R}^0$, set of nonnegative real numbers, such
that $\forall x,y,z \in X$ we have

(1) $d$ is real valued, finite and nonnegative. $d(x,y)\geq 0$  
(2) $d(x,y)=0 \Leftrightarrow x=y$  
(3) $d(x,y)=d(y,x)$  
(4) $d(x,y)\leq d(x,z) + d(z,y)$  


---

# Special Functions

Most special functions are considered as a function of a complex variable.

## Gamma

A function that interpolates factorials.

$
\Gamma(t)=\int_0^\infty x^{t-1}e^{-x}\,dx
$
,$ℜt>0$

$n$, nonnegative integer.
$
\Gamma(\frac{1}{2}+n)=\frac{(2n)!}{4^nn!}\sqrt{\pi}
$
$
\Gamma(\frac{1}{2}-n)=\frac{(-4)^nn!}{(2n)!}\sqrt{\pi}
$

$m$ positive integer.
$\gamma$ Euler-Mascheroni constant.
$
\Gamma^{′}(m+1)=m!(-\gamma +\sum_{k=1}^m\frac{1}{k})
$

$n$ positive integer
$
\Gamma(n)=(n-1)!
$

## digamma, polygamma

The logarithmic derivate of the gamma function
is called the digamma function, $\psi$; higher derivates
are polygamma functions.

$
\psi(x)=\frac{d}{dx}\ln\Gamma(x)=
\frac{\Gamma\text{'}(x)}{\Gamma(x)}
=\psi^{(0)}(x)
$
$
\psi^{(m)}(x)=\frac{d^m}{dx^m}\psi(x)
=\frac{d^{m+1}}{dx^{m+1}}\ln\Gamma(x)
$

$$\psi (n) = H_{n-1} - \gamma$$



# Ordinary Differential Equation

The order is the highest derivate that appears in the equatio.

Higher-order equations can be converted into systems of first-order equations.

state phase model:

$\dot x = Ax + Bu$  
$y = Cx + Du$

# Partial Differential Equation (PDE)

$u_{xx} := \frac{\partial^2u}{\partial x^2}$,
$u_x := \frac{\partial u}{\partial x}$,
$u_{xy} := \frac{\partial^2 u}{\partial y\partial x} = \frac{\partial}{\partial y}(\frac{\partial u}{\partial x})$

Any second order linear PDE in two variables can be written in the form
$Au_{xx} + 2Bu_{xy} + Cu_{yy} + Du_x + Eu_y + Fu + G = 0$
Where $A,B,C,D,E,F,G$ are functions of $x$ and $y$.

A PDE written in this form is elliptic if $B^2-AC<0$

Laplace equation $\triangle u = u_{xx} + u_{yy} = 0$
Poisson equation $\triangle u = u_{xx} + u_{yy} = f(x,y)$
