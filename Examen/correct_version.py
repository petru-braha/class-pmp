import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm
import pandas as pd

df = pd.read_csv("bike_daily.csv")

temp_c = df["temp_c"].values
humidity = df["humidity"].values
wind_kph = df["wind_kph"].values
is_holiday = df["is_holiday"].values
# fix mistake of pm.Categorical().codes
season = pd.Categorical(df["season"].values).codes
rentals = df["rentals"].values

# fix plots
fig, axs = plt.subplots(2, 3, figsize=(15, 8))
axs[0, 0].scatter(temp_c, rentals)
axs[0, 1].scatter(humidity, rentals)
axs[0, 2].scatter(wind_kph, rentals)
axs[1, 0].scatter(is_holiday, rentals)
axs[1, 1].scatter(season, rentals)
plt.tight_layout()
plt.show()

# fix coller way of make them standard
def standardize(x):
    return (x - x.mean()) / x.std()

temp_s = standardize(temp_c)
humidity_s = standardize(humidity)
wind_s = standardize(wind_kph)
rentals_s = standardize(rentals)

X = np.column_stack([temp_s, humidity_s, wind_s, is_holiday, season])

with pm.Model() as model_linear:
    # fix of the given paremeters. 100 and 1000 bad values.
    alpha = pm.Normal("alpha", 0, 1)
    beta = pm.Normal("beta", 0, 1, shape=X.shape[1])
    sigma = pm.HalfNormal("sigma", 1)

    mu = alpha + pm.math.dot(X, beta)

    y = pm.Normal("y", mu=mu, sigma=sigma, observed=rentals_s)
    trace_linear = pm.sample(2000, chains=2, target_accept=0.9, return_inferencedata=True)

with pm.Model() as model_quadratic:
    alpha = pm.Normal("alpha", 0, 1)
    beta = pm.Normal("beta", 0, 1, shape=X.shape[1] + 1)
    sigma = pm.HalfNormal("sigma", 1)

    mu = (
        alpha
        + pm.math.dot(X, beta[:-1])
        + beta[-1] * temp_s**2
    )

    y = pm.Normal("y", mu=mu, sigma=sigma, observed=rentals_s)
    trace_quadratic = pm.sample(2000, chains=2, target_accept=0.9, return_inferencedata=True)

az.summary(trace_linear)
az.summary(trace_quadratic)

waic_linear = az.waic(trace_linear)
print(waic_linear)
waic_quadratic = az.waic(trace_quadratic)
print(waic_quadratic)

pm.sample_posterior_predictive(trace_linear, model=model_linear, extend_inferencedata=True)
az.plot_ppc(trace_linear, mean=True)

pm.sample_posterior_predictive(trace_quadratic, model=model_quadratic, extend_inferencedata=True)
az.plot_ppc(trace_quadratic, mean=True)



# second part, the logistic regression
threshold = np.percentile(rentals, 75)
is_high_demand = (rentals > threshold).astype(int)

# fix of the model, i was confuzed while taking the test
with pm.Model() as model_logistic:
    alpha = pm.Normal("alpha", 0, 1)
    beta = pm.Normal("beta", 0, 1, shape=X.shape[1])

    logits = alpha + pm.math.dot(X, beta)
    p = pm.Deterministic("p", pm.math.sigmoid(logits))

    y = pm.Bernoulli("y", p=p, observed=is_high_demand)

    trace_logistic = pm.sample(2000, chains=2, target_accept=0.9, return_inferencedata=True)

az.summary(trace_logistic, var_names=["alpha", "beta"])
az.hdi(trace_logistic, var_names=["p"], hdi_prob=0.95)
