import numpy as np
from matplotlib import pyplot as plt
from Core import simulation
from Plot import plot_info
from Setup import client_generation, get_initial_topics, broker_capacity, compute_client_overhead

n_simulations = 100
n_clients = 100000
n_topics = 1000
n_brokers = 100
percentage_publisher = 0.5
mean_rate = 1000  # Media del sending rate in bytes/s (valore ipotetico)
sigma = 0
s = 0
min_client_res = []
density_res = []
max_overhead_res = []
base_res = []
elast_res = []

exec_min = []
exec_dens = []
exec_max = []
exec_base = []
exec_elast = []

for _ in range(n_simulations):
    print(_)
    # Generazione dei sending rate usando una distribuzione lognormale (per variazioni ampie)
    sending_rates = [s.item() for s in np.random.lognormal(mean=np.log(mean_rate), sigma=sigma, size=n_clients)]
    clients = client_generation(n_clients, percentage_publisher, sending_rates, n_topics, s)

    capacity_per_broker = broker_capacity(clients, n_topics, n_brokers)

    res, ex_min = simulation(n_brokers, capacity_per_broker, clients, "min_client")
    min_client_res.append(res)
    exec_min.append(ex_min)

    res, ex_dens = simulation(n_brokers, capacity_per_broker, clients, "density")
    density_res.append(res)
    exec_dens.append(ex_dens)

    res, ex_max = simulation(n_brokers, capacity_per_broker, clients, "max_overhead")
    max_overhead_res.append(res)
    exec_max.append(ex_max)

    res, ex_base = simulation(n_brokers, capacity_per_broker, clients, "baseline")
    base_res.append(res)
    exec_base.append(ex_max)

    #res, ex_elast = simulation(n_brokers, capacity_per_broker, clients, "elasticity")
    #elast_res.append(res)
    #exec_elast.append(ex_elast)

means_min, std_devs_min, x_values_min = plot_info(n_simulations, min_client_res)  #min_client_res
means_density, std_devs_density, x_values_density = plot_info(n_simulations, density_res)  #density_res
means_max, std_devs_max, x_values_max = plot_info(n_simulations, max_overhead_res)  #max_overhead_res
means_base, std_devs_base, x_values_base = plot_info(n_simulations, base_res)  #max_overhead_res
#means_elast, std_devs_elast, x_values_elast = plot_info(n_simulations, elast_res) #max_overhead_res


# Plot delle medie e delle deviazioni standard
plt.figure(figsize=(10, 6))
plt.errorbar(x_values_min, means_min, capsize=5, label="Min_client",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density
plt.errorbar(x_values_max, means_max, capsize=5, label="Max_overhead", linewidth=3)
plt.errorbar(x_values_density, means_density, capsize=5, label="Max_Density", linewidth=3)  #yerr=std_devs_max
plt.errorbar(x_values_base, means_base, capsize=5, label="Baseline", linewidth=3)  #yerr=std_devs_max
#plt.errorbar(x_values_elast, means_elast, capsize=5, label="Elasticity")  #yerr=std_devs_max


plt.xlabel("Cumulative number of clients", fontsize=24)
plt.ylabel("Moved clients", fontsize=24)
plt.legend(fontsize=24)
plt.grid(True)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
plt.show()

