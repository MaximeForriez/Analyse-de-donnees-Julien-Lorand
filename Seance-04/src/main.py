#coding:utf8

import numpy as np
import pandas as pd
import scipy
import scipy.stats  
from scipy.stats import poisson, binom, randint, zipf, norm, lognorm, uniform, chi2, pareto

import matplotlib.pyplot as plt   # ← LIGNE AJOUTÉE

#https://docs.scipy.org/doc/scipy/reference/stats.html

dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)

# -----------------------------------------
# FONCTIONS D’AFFICHAGE
# -----------------------------------------

def plot_discrete_pmf(x, pmf, title):
    plt.stem(x, pmf, use_line_collection=True)
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("Probabilité")
    plt.grid(True)
    plt.show()

def plot_continuous_pdf(x, pdf, title):
    plt.plot(x, pdf)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("densité")
    plt.grid(True)
    plt.show()

# -----------------------------------------
# DISTRIBUTIONS DISCRÈTES
# -----------------------------------------

# 1) Loi de Dirac (delta de Dirac)
def dirac(k0=0):
    x = np.arange(k0 - 2, k0 + 3)
    pmf = np.zeros_like(x, dtype=float)
    pmf[x == k0] = 1.0
    plot_discrete_pmf(x, pmf, f"Loi de Dirac en {k0}")

# 2) Loi uniforme discrète
def uniforme_discrete(a=0, b=10):
    x = np.arange(a, b + 1)
    pmf = randint(a, b + 1).pmf(x)
    plot_discrete_pmf(x, pmf, "Loi uniforme discrète")

# 3) Loi binomiale
def binomiale(n=20, p=0.4):
    x = np.arange(0, n + 1)
    pmf = binom(n, p).pmf(x)
    plot_discrete_pmf(x, pmf, "Loi binomiale")

# 4) Loi de Poisson
def poisson_discrete(l=5):
    x = np.arange(0, 20)
    pmf = poisson(l).pmf(x)
    plot_discrete_pmf(x, pmf, "Loi de Poisson")

# 5) Loi de Zipf–Mandelbrot (approximation Zipf)
def zipf_mandelbrot(s=2.0, N=20):
    x = np.arange(1, N+1)
    pmf = zipf(s).pmf(x)
    plot_discrete_pmf(x, pmf, "Loi de Zipf–Mandelbrot (approx Zipf)")

# -----------------------------------------
# DISTRIBUTIONS CONTINUES
# -----------------------------------------

# Poisson continue : NON DÉFINIE → approximation Gamma
def poisson_continue(l=5):
    x = np.linspace(0, 20, 500)
    pdf = poisson(l).pmf(np.round(x))
    plot_continuous_pdf(x, pdf, "Approx Poisson continue")

def normale(mu=0, sigma=1):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
    pdf = norm(mu, sigma).pdf(x)
    plot_continuous_pdf(x, pdf, "Loi normale")

def log_normale(s=0.5):
    x = np.linspace(0.001, 5, 500)
    pdf = lognorm(s).pdf(x)
    plot_continuous_pdf(x, pdf, "Loi log-normale")

def uniforme_continue(a=0, b=1):
    x = np.linspace(a, b, 500)
    pdf = uniform(a, b-a).pdf(x)
    plot_continuous_pdf(x, pdf, "Loi uniforme continue")

def chi_deux(k=4):
    x = np.linspace(0, 20, 500)
    pdf = chi2(k).pdf(x)
    plot_continuous_pdf(x, pdf, f"Loi du Chi-2 (df={k})")

def pareto_cont(a=2):
    x = np.linspace(1, 10, 500)
    pdf = pareto(a).pdf(x)
    plot_continuous_pdf(x, pdf, "Loi de Pareto")

# -----------------------------------------
# TEST DES FONCTIONS
# -----------------------------------------

if __name__ == "__main__":
    dirac()
    uniforme_discrete()
    binomiale()
    poisson_discrete()
    zipf_mandelbrot()

    poisson_continue()
    normale()
    log_normale()
    uniforme_continue()
    chi_deux()
    pareto_cont()