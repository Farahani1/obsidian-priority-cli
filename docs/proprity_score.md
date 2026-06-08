# Task Prioritization Framework

This document explains how a **decision function for task prioritization** under cognitive and temporal constraints, is implimented. It functions more like a sophisticated scheduling heuristic than a simple priority score.

A basic linear weighted sum often fails here because variables interact in asymmetric, nonlinear ways—particularly around deadline pressure, necessity, and cognitive load. This system is designed to behave correctly under edge cases and align with effective human prioritization principles.

## First Principles

Before defining equations, the framework is built on these core dominance rules:

### A. Deadline Pressure
A task due tomorrow is not "slightly more important" than one due in a week—it must be **orders of magnitude** more urgent. Urgency grows nonlinearly.

### B. Necessity as Survival Constraint
Critical tasks (e.g., paying bills, addressing health/safety issues) should override value-based optimization.

### C. Value as Long-Term Optimization
Important but non-urgent tasks should surface naturally when no urgent or necessary tasks dominate.

### D. Load and Force as Friction
These act as penalties on execution probability rather than direct priority drivers:
- **Load**: Time/energy cost
- **Force**: Psychological or mental resistance

## Input Normalization

All inputs are assumed to be scaled to the range `[0, 1]`:

- `L` = Load (higher = longer/more demanding)
- `F` = Force (higher = more mentally taxing)
- `N` = Necessity
- `V` = Value
- `D` = Days left until deadline (non-negative real number)

## Core Formula

Priority is computed as a product of three components:

$$
\text{Priority} = U(D, N) \cdot S(N, V) \cdot E(L, F)
$$

### 1. Urgency Function `U(D, N)`

$$
U = \left(\frac{1}{(D + 1)^\alpha}\right) \cdot (1 + \beta N)
$$

- Exponential decay models sharp deadline pressure.
- Necessity amplifies urgency.
- Recommended: $\alpha \approx 1.5 - 2.5$

### 2. Strategic Importance `S(N, V)`

$$
S = N^\gamma + (1 - N) \cdot V^\delta
$$

- When necessity is high, value is largely ignored.
- When necessity is low, it becomes value-driven.
- Recommended: $\gamma > \delta$ (necessity is weighted more heavily)

### 3. Execution Penalty `E(L, F)`

$$
E = e^{- (w_L L + w_F F)}
$$

- Smooth exponential damping prevents large or mentally costly tasks from dominating unfairly.
- Recommended: $w_F > w_L$ (mental friction typically matters more)

## Final Formula

$$
\boxed{
\text{Priority} =
\left(\frac{1}{(D + 1)^\alpha}\right)
\cdot (1 + \beta N)
\cdot \left[N^\gamma + (1 - N) V^\delta\right]
\cdot e^{- (w_L L + w_F F)}
}
$$

## Doability Gate (Optional but Recommended)

Add a soft threshold to model psychological resistance:

$$
G = \frac{1}{1 + e^{k(F - \theta)}}
$$

$$
\text{Priority}_{final} = \text{Priority} \cdot G
$$

This temporarily suppresses tasks with excessively high force.

## Behavior Analysis

### Case 1: Urgent + Necessary
Small `D`, high `N` → priority explodes (correct).

### Case 2: High Value, No Deadline
Large `D`, low `N`, high `V` → moderate priority that surfaces when urgent tasks are cleared (correct).

### Case 3: High Force Task
Large `F` → heavily penalized, helping avoid burnout (correct).

### Case 4: Trivial but Urgent
Small `D`, low `N`, low `V` → still receives some priority for quick wins (correct).

## Suggested Default Parameters

```python
alpha = 2.0   # deadline sharpness
beta = 2.0    # necessity amplification
gamma = 2.5   # necessity dominance
delta = 1.5   # value influence
w_L = 0.8     # load penalty
w_F = 1.5     # force penalty (higher emphasis)
k = 10        # gate steepness
theta = 0.6   # force threshold