import numpy as np
from scipy import stats


def generate_thickness_permeability_transmissivity_for_pvalue(thickness_mean, thickness_sd, ln_permeability_mean, ln_permeability_sd, Pvalue, nSamples=10000):
    if Pvalue > 1.0:
        Pvalue /= 100

    thickness_dist = stats.norm(loc=thickness_mean, scale=thickness_sd)
    thickness_pvalue = thickness_dist.ppf(1 - Pvalue)

    ln_permeability_dist = stats.norm(loc=ln_permeability_mean, scale=ln_permeability_sd)
    permeability_pvalue = np.exp(ln_permeability_dist.ppf(1 - Pvalue))

    # Sampling method for transmissivity
    transmissivity_samples = np.sort(np.exp(ln_permeability_dist.rvs(nSamples) + np.log(thickness_dist.rvs(nSamples))))
    transmissivity_pvalue_sampled = transmissivity_samples[int((1 - Pvalue) * nSamples)]

    return thickness_pvalue, permeability_pvalue, transmissivity_pvalue_sampled
