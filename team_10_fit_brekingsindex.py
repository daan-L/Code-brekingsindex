import numpy as np
import scipy.optimize as sp
import pandas as pd
import matplotlib.pyplot as plt

#  constanten en de csv inlezen
df = pd.read_csv("team_10_data.csv")
d = 5000000
L = 528
hoek = df["hoek_graden"]
franjes = df["aantal_franjes"]
fout_N = df["onzekerheid_N"]

# hoek naar radialen en de formule voor N
def N(i,n):
    i = np.deg2rad(i)
    return 2*d/L*np.abs(np.sqrt(n**2-np.sin(i)**2)-np.cos(i)+1-n)


# de curve fit maken
curve_1, curve_2 = sp.curve_fit(N, hoek, franjes, sigma=fout_N, absolute_sigma=True)

n_fit = curve_1[0]
fout_n = np.sqrt(curve_2[0, 0])

# de fit lijn gladder maken 
hoek_fit = np.linspace(min(hoek), max(hoek), 500)
franjes_fit = N(hoek_fit, n_fit)


# foutbalken aan de plot toevoegen
plt.errorbar(hoek,franjes,yerr=fout_N,fmt="o",capsize=4,label="Metingen")

# de fit weergeven inde plot
plt.plot(hoek_fit,franjes_fit,label=f"Fit: n = {n_fit:.3f} ± {fout_n:.3f}")

# plot mooier maken met legenda en as titels
plt.xlabel("Hoek (graden)")
plt.ylabel("Aantal franjes")
plt.legend()
plt.grid()

# de grafiek opslaan
plt.savefig("team_10_fit_plot.png", dpi=300)

# de grafiek laten zien
plt.show()

# de waarde van N met de fout printen
print(n_fit, "±", fout_N )