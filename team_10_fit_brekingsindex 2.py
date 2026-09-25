import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# importeren van de data (csv-bestand)
df = pd.read_csv("data.csv")

# meetdata
i = df.hoek_graden.to_numpy()  # invalshoek (i) in graden
N = df.aantal_franjes.to_numpy()  # aantal franjes (N) bij de hoeken
oN = df.onzekerheid_N.to_numpy()  # de onzekerheid van het aantal franjes
d = 0.003  # dikte van het materiaal
l = 0.000000528  # golflengte van het de laserstraal (licht)


# functie N(i,n) waarmee de data gefit wordt
def f(i, n):
    i_rad = np.radians(i)  # wordt omgezet van graden naar radialen voor Numpy
    return (2 * d) / l * (np.sqrt(n**2 - np.sin(i_rad) ** 2) - np.cos(i_rad) + (1 - n))


# fit het model op de meetdata
popt, pcov = curve_fit(f, i, N, sigma=oN, absolute_sigma=True)
n = popt[0]

# de onzekerheid van de brekingsindex (n)
perr = np.sqrt(np.diag(pcov))

plt.figure(figsize=(8, 5))  # grootte van het plot
plt.plot(
    i, f(i, *popt), label=f"Fit: n={n:.3f} ± {perr[0]:.3f}", color="tab:red"
)  # plot van de fit op de meetdata
plt.errorbar(
    i, N, yerr=oN, fmt="o", label="Data", color="tab:blue", capsize=3
)  # errorbars gebasseerd op de onzekerheid van N

# opmaak van de grafiek
plt.grid(linewidth=0.5, alpha=0.5)
plt.ylabel("Aantal Franjes N")
plt.xlabel("Hoek i (Graden)")
plt.title("Aantal franjes als een functie van de invalshoek")
plt.legend()

# opslaan van de grafiek als png
plt.savefig("team_10_fit_plot.png", dpi=300, bbox_inches="tight")
plt.show()
