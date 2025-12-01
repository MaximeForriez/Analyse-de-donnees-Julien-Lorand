#coding:utf8

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, binom, randint, zipf, norm, lognorm, uniform, chi2, pareto

os.makedirs("images", exist_ok=True)


# Code sauvegarde des graphiques


def save_discrete(x, pmf, title, filename):
    plt.figure()
    plt.stem(x, pmf, use_line_collection=True)
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("Probabilité")
    plt.grid(True)
    plt.savefig(f"images/{filename}")
    plt.close()

def save_continuous(x, pdf, title, filename):
    plt.figure()
    plt.plot(x, pdf)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("Densité")
    plt.grid(True)
    plt.savefig(f"images/{filename}")
    plt.close()


# DISTRIBUTIONS DISCRÈTES

def dirac(k0=0):
    x = np.arange(k0 - 2, k0 + 3)
    pmf = np.zeros_like(x, dtype=float)
    pmf[x == k0] = 1.0
    save_discrete(x, pmf, f"Loi de Dirac (k0={k0})", "dirac.png")

def uniforme_discrete(a=0, b=10):
    x = np.arange(a, b + 1)
    pmf = randint(a, b + 1).pmf(x)
    save_discrete(x, pmf, "Loi uniforme discrète", "uniforme_discrete.png")

def binomiale(n=20, p=0.4):
    x = np.arange(0, n + 1)
    pmf = binom(n, p).pmf(x)
    save_discrete(x, pmf, "Loi binomiale", "binomiale.png")

def poisson_discrete(l=5):
    x = np.arange(0, 20)
    pmf = poisson(l).pmf(x)
    save_discrete(x, pmf, "Loi de Poisson", "poisson.png")

def zipf_mandelbrot(s=2.0, N=20):
    x = np.arange(1, N+1)
    pmf = zipf(s).pmf(x)
    save_discrete(x, pmf, "Loi de Zipf-Mandelbrot", "zipf.png")


# DISTRIBUTIONS CONTINUES


def poisson_continue(l=5):
    x = np.linspace(0, 20, 500)
    pdf = poisson(l).pmf(np.round(x))
    save_continuous(x, pdf, "Approximation Poisson continue", "poisson_continue.png")

def normale(mu=0, sigma=1):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
    pdf = norm(mu, sigma).pdf(x)
    save_continuous(x, pdf, "Loi normale", "normale.png")

def log_normale(s=0.5):
    x = np.linspace(0.001, 5, 500)
    pdf = lognorm(s).pdf(x)
    save_continuous(x, pdf, "Loi log-normale", "log_normale.png")

def uniforme_continue(a=0, b=1):
    x = np.linspace(a, b, 500)
    pdf = uniform(a, b-a).pdf(x)
    save_continuous(x, pdf, "Loi uniforme continue", "uniforme_continue.png")

def chi_deux(k=4):
    x = np.linspace(0, 20, 500)
    pdf = chi2(k).pdf(x)
    save_continuous(x, pdf, f"Loi du Chi-2 (k={k})", "chi2.png")

def pareto_cont(a=2):
    x = np.linspace(1, 10, 500)
    pdf = pareto(a).pdf(x)
    save_continuous(x, pdf, "Loi de Pareto", "pareto.png")


# MAIN

# TEST DES FONCTIONS

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
