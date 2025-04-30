## Prerequisites:

* ```uv```

* ```python >= 3.12```

## Key Metric:
**Paid conversion rate**, i.e. the probability of a player to purchase the starting offer.

## Modelling alternatives:

| Model                          | Pros                                     | Cons                                         | Best Use Case                        |
|--------------------------------|------------------------------------------|----------------------------------------------|--------------------------------------|
| **Beta-Binomial**              | Simple, fast, intuitive                  | No covariates, no hierarchy                  | Clean binary A/B tests               |
| **Logit-Normal**              | Flexible, realistic                      | Sampling required                            | More complex behavior                |
| **Hierarchical Beta-Binomial**| Partial pooling                          | Slower, needs priors                         | Segment-level comparisons            |
| **Empirical Bayes**           | Fast, uses past data                     | Overconfident, static                        | Large experiment libraries           |
| **Logistic Regression (Bayesian)** | Rich modeling, extensible            | Complex, slow                                | User-level data with covariates      |

