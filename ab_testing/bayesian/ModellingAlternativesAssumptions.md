# Bayesian Modeling Options for Paid Conversion Experiment in "Total Battle":

This document evaluates Bayesian modeling options for analyzing a two-group A/B experiment comparing paid conversions from different price/offer combinations in the game *Total Battle* by Scorewarrior.

## 1. Beta-Binomial Model (Standard Conjugate Prior)

**Model**:

Let  $X_i \sim \text{Binomial}(n_i, p_i)$ where:

- $X_i$ is the number of conversions in variant $i$
- $n_i$ is the number of exposures (users shown variant $i$)
- $p_i$ is the true conversion rate for variant $i$

**Prior**:

$p_i \sim \text{Beta}(\alpha, \beta)$


**Posterior**:

$p_i \mid X_i \sim \text{Beta}(\alpha + X_i, \beta + n_i - X_i)$


**Pros**:

- Closed-form posterior update
- Simple and interpretable
- Computationally efficient
- Well-suited for low conversion rates

**Cons**:

- Assumes a fixed, independent $ p_i$ per variant
- No support for covariates (e.g., device, locale etc)
- No built-in shrinkage or hierarchy

**Recommended if**:

- We want a lightweight, interpretable model
- Conversion rates are low, and segments are not needed
- The experiment is isolated, with limited historical data

The conditions above match the context I am presented with the closest, however this would not necessarily be the case in prod.

## 2. Logit-Normal Model

**Model**:

Let $\theta_i = \log \left( \frac{p_i}{1 - p_i} \right)$, the log-odds of conversion.

$$
\theta_i \sim \mathcal{N}(\mu, \sigma^2) \quad
p_i = \frac{1}{1 + e^{-\theta_i}} \quad
X_i \sim \text{Binomial}(n_i, p_i)
$$

**Pros**:

- More flexible than Beta-Binomial
- Can model correlation between groups (better captures real-world limitations)
- Natural in logistic regression context; extensible

**Cons**:

- Requires sampling (e.g., MCMC or variational inference)
- Slightly harder to interpret (log-odds)

**Recommended if**:

- We plan to include covariates or want more modeling flexibility
- We suspect correlations or tail behavior (e.g., very low/high conversion extremes)
- We're open to modelling in PyMC or Stan in order to handle sampling computationally

This is potentially a good match as well, though with the current limited scope we probably don't care about predictor variables and there seem to be no reasons to suspect correlation.

## 3. Hierarchical Beta-Binomial Model

**Model**:

Useful when modeling cohorts (e.g., device type, geo) or smoothing across segments.

$$
p_i \sim \text{Beta}(\alpha, \beta) \quad
\alpha, \beta \sim \text{Hyperpriors} \quad
X_i \sim \text{Binomial}(n_i, p_i)
$$

Reparameterized version:

$$
\mu \sim \text{Beta}(a, b), \quad \kappa \sim \text{Gamma}(c, d) \quad
\alpha = \mu \kappa, \quad \beta = (1 - \mu) \kappa
$$

**Pros**:

- Partial "pooling" across groups
- More robust estimates for small segments

In practice, this means sharing information between different groups in a smart way. In our specific context, let's imagine we’re testing the conversion rate of two offers for a starter pack, and we have results split by user segment — say, players on mobile vs. PC. If we analyze each segment completely separately (called "no pooling"), we treat each one as totally independent, which could lead to noisy estimates - especially if one segment has very few users. On the flip side, if we fully pool all the data, we treat all users the same and ignore any segment differences, which could mean oversimplifying things. Partial pooling is kinda the middle ground. It essentially means that each segment is of course different but probably not by "that much", so we should let the data itself decide how much to, in a sense, borrow strength from the remaining segments.

Mathematically, this is often executed via hierarchical models that estimate a global prior (shared belief across groups), but allow group-level adjustments.

- Interpretability of the beta distribution retained

**Cons**:

- Requires MCMC or variational inference
- Slower and way more complex (so running at scale should be exercised with a lot of caution)
- *Hyperprior tuning* is required

**Recommended if**:

- There is segment-wise data (e.g., platform, locale etc)
- We want to "borrow strength" across groups
- We're concerned about overfitting small groups

Since I don't have access to segment data, this is skipped, though potentially useful given access to real data.

## 4. Empirical Bayes

**Approach**:

Estimate prior parameters $\alpha, \beta$ from historical A/B test data. Treat those as fixed priors for future experiments.

**Pros**:

- Quite fast to compute
- Leverages previous experiments
- Simple implementation

**Cons**:

- Does not model prior uncertainty
- May lead to overconfidence if prior estimates are poor or outdated

**Recommended if**:

- We have access to historical A/B test outcomes
- We need very fast and, more importantly, scalable inference
- Our organization runs frequent experiments

The above doesn't at all match the scope of the task and the data provided with it but is typically something to keep closely in mind.

## 5. Fully Bayesian Logistic Regression (with Covariates)

**Model**:

If I had individual-level data:

$$
y_j \sim \text{Bernoulli}(p_j), \quad \log \left( \frac{p_j}{1 - p_j} \right) = \beta_0 + \beta_1 \cdot \text{variant}_j + \beta_2 \cdot \text{device}_j + \ldots
$$

(which I don't, not to the extent required)

Priors:

$
\beta_k \sim \mathcal{N}(0, \tau^2)
$

**Pros**:

- Most flexible and expressive
- Can model contextual effects and heterogeneity
- Fully Bayesian uncertainty on treatment effects

**Cons**:

- Requires user-level data
- Really computationally expensive
- Harder to communicate results

**Recommended if**:

- We want to model user behavior in depth
- We want to assess variant impact across user types
- We are doing causal inference with rich data

Again, this doesn't match the context of the task at all.

---

## Strategic Considerations

In Scorewarrior's context:

- If this was an **isolated test** with no historical priors or segments, even in 
prod" we'd go with **Beta-Binomial** for simplicity.
- If **future tests** are expected and logs are retained, we would try and build towards **Empirical Bayes** or **Hierarchical Beta-Binomial**.
- If we're interested in **behavioral drivers** (e.g., pricing sensitivity by platform or region),which I imagine business stakeholders very much would be, we need to prepare for **Fully Bayesian Logistic Regression**.

## Decision:
I will be doing a sensitivity analysis using the simplest modelling alternative - Beta-Binomial model - as it matches the context of the task the closest.

## Prior Choice

Given a large sample size and ~15% base conversion, I could use **weakly informative** prior: $\alpha = 15, \beta = 85$ → centers prior at 15% with moderate weight (acts like prior of 100 users). If extremely skeptical, I can use something like $\alpha = 3, \beta = 17$ (lower weight).

Since the business risk from a "wrong" call could be pretty high given the conversion rate I would prefer to execute a sensitivity analysis with the following priors.

| Prior | Parameters              | Rationale                          |
|-------|--------------------------|------------------------------------|
| **Neutral** | $\text{Beta}(1, 1)$       | Easy to explain, uninformative     |
| **Skeptical** | $\text{Beta}(3, 17)$     | Encodes prior belief that CVRs are likely ~15% |
| **Weak** | $\text{Beta}(15, 85)$     | Centers prior at ~15%, "reasonable" weight |
| **Historical** | $\text{Beta}(150, 850)$ | Shrinks to 15% but allows for learning |

## Stopping rule:

The zero uplift is in 95% HDI.
