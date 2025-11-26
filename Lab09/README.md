### b)

### 1. The Effect of $Y$ (Observed Buyers)

* **The Constraint Upon n:**
    The most immediate effect is that **$n$ cannot be less than $Y$**. If you observed 10 buyers, there must have been at least 10 visitors.
    * *Visual Effect:* In the plots where $Y=10$, the posterior probability should be 0 for all $n < 10$.
* **The Rightward Shift:**
    As $Y$ increases, the likelihood function pushes the estimated $n$ higher.
    * *Low $Y$ (e.g., 0):* The data provides little evidence to contradict the Prior. The posterior remains close to $\text{Poisson}(10)$.
    * *High $Y$ (e.g., 10):* The data suggests $n$ is large. This pulls the posterior mean to the right, moving it away from the prior mean of 10.

### 2. The Effect of $\theta$ (Purchase Probability)

* **The Scaling Effect (The Multiplier):**
    The data suggests that the total visitors are roughly $n \approx \frac{Y}{\theta}$.
    * **High $\theta$ (0.5):** The multiplier is small ($1/0.5 = 2$). If $Y=10$, the data suggests $n \approx 20$. This is relatively close to the Prior (10), so the posterior settles comfortably between 10 and 20.
    * **Low $\theta$ (0.2):** The multiplier is large ($1/0.2 = 5$). If $Y=10$, the data suggests $n \approx 50$. This creates a massive conflict with the Prior (which prefers 10). The posterior is dragged significantly to the right.

* **The Uncertainty Effect (Variance):**
    * **High $\theta$:** We have observed a large percentage of the population. We are "sure" about the count. The posterior is **narrow/sharp** (low variance).
    * **Low $\theta$:** We have only observed a tiny fraction of the population. The "unseen" visitors ($n-Y$) could be few or very many. The posterior becomes **flat/wide** (high variance), spreading out over a large range of values.

### Summary Table

| Combination | Conflict Level | Posterior Shape | Location of Peak ($n$) |
| :--- | :--- | :--- | :--- |
| **$Y=0, \theta=0.5$** | Low | Similar to Prior | $\approx 10$ |
| **$Y=0, \theta=0.2$** | Low | Similar to Prior | $\approx 10$ |
| **$Y=10, \theta=0.5$** | Medium | Sharp (Confident) | $\approx 18-20$ |
| **$Y=10, \theta=0.2$** | **High** | **Wide (Uncertain)** | $\approx 25-35$ (Long tail) |

### d)

The Posterior Predictive distribution is always wider than the Posterior, because it accounts for the noise in the data generation process itself, not just the uncertainty in the parameter.

**1. Posterior Distribution for $n$ ($P(n \mid Y)$)**
* **What it is:** The probability distribution of the *unknown parameter* (total visitors).
* **The Question it Answers:** "Based on the sales we observed, how many people *actually* visited the store today?"
* **Uncertainty Source:** It reflects our uncertainty about the true value of $n$ after seeing the data.

**2. Posterior Predictive Distribution ($P(Y^* \mid Y)$)**
* **What it is:** The probability distribution of *future observable data* (future buyers).
* **The Question it Answers:** "If we opened the store tomorrow, how many sales ($Y^*$) should we expect?"
* **Uncertainty Source:** It incorporates **two** layers of uncertainty:
    1.  **Parameter Uncertainty:** We don't know the true $n$ (from the Posterior above).
    2.  **Sampling Variability:** Even if we knew $n$ perfectly, the Binomial process is random.
