import numpy as np
import random
from matplotlib import pyplot as plt


def NaSch(N, L, P, Vmax, Time, density):
    V = np.zeros((Time, N))
    slots = np.arange(1, L + 1)
    pos = np.zeros(N, dtype=int)
    Lvector = L * np.ones(N, dtype=int)
    headway = np.zeros(N, dtype=int)
    Velocity = np.zeros(N, dtype=int)
    O = np.zeros(L, dtype=int)
    mean_velocity = np.ones(Time)

    for i in range(N):  # assign a distinct position to each car
        u = random.randint(0, len(slots) - 1)
        pos[i] = slots[u]
        slots = np.delete(slots, u)

    pos = np.sort(pos)

    for i in range(Time):  # start the simulation
        headway[:-1] = np.diff(pos)  # find the distance with respect to slots(L)
        ToTail = L - pos[-1]
        headway[-1] = ToTail + pos[0] - 1

        #headway = np.concatenate([pos[1:] - pos[:-1], [pos[0] + L - pos[-1]]])
        #headway = pos[1:] - pos[:-1]
        #headway = np.append(headway, pos[0] + L - pos[-1])


        # heuristics
        V1 = np.where(Velocity < Vmax)[0]
        Velocity[V1] = np.minimum(Velocity[V1] + 1, Vmax)

        V2 = np.where((headway - 1) < Velocity)[0]
        Velocity[V2] = np.maximum(headway[V2] - 1, 0)

        u = np.random.rand(N)
        V3 = np.where(u < P)[0]
        Velocity[V3] = np.maximum(Velocity[V3] - 1, 0)

        k4 = np.where(pos + Velocity > L)[0]
        pos = pos + Velocity  # update
        pos[k4] = pos[k4] - L

        # to make sure the boundry rules are followed
        if not np.all(np.diff(pos) >= 0):
            ss = np.argsort(pos)
            pos = np.sort(pos)
            Velocity = Velocity[ss]

        mean_velocity[i] = np.mean(Velocity)

    flux = density * np.mean(mean_velocity)

    return flux


vmax = 5
p = 0  # 0 or 0.2
time = 20000  # was 20000
N = 20
L = 40000  # was 1000
densities = np.linspace(0, 1, num=200)
fluxes = np.zeros(len(densities))
flux = []

for i, density in enumerate(densities):

    n = int(density * L)
    if n != 0:
        flux = []
        for _ in range(2):
            mean_velocity = NaSch(n, L, p, vmax, time, density)
            flux.append(mean_velocity)

        fluxes[i] = np.mean(flux)
    else:
        continue

# Plot Flux VS Densities
plt.plot(densities, fluxes)
plt.xlabel('Density')
plt.ylabel('Flux')
plt.show()
