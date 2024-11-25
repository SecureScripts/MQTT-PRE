import numpy as np
from matplotlib import pyplot as plt
from Core import simulation, simulationReal, optimalAllocation, optimalAllocationNew
from Setup import client_generation


n_topics = 100
n_brokers = 10
percentage_publisher = 0.5
broker_capacity = 54
max_clients = 1000
sigma = 0

capacity_per_broker = dict()
for b in range(n_brokers):
    capacity_per_broker[b] = broker_capacity

online_skewed = []
optimal_skewed = []
bound_skewed = []
online_not_skewed = []
optimal_not_skewed = []
bound_not_skewed = []
send_per_publisher = np.arange(0.01, 10, 1)


#Non_Skewed_simulation
clients = client_generation(max_clients, percentage_publisher, [0 for _ in range(max_clients)], n_topics, 0)
for send_rate in send_per_publisher:
    print(send_rate)
    for c in clients:
        c.sending_rate = send_rate
    res = simulationReal(n_brokers, capacity_per_broker, clients, "density")
    online_not_skewed.append(res)
    bound, val= optimalAllocationNew(n_brokers, capacity_per_broker, clients)
    optimal_not_skewed.append(val)
    bound_not_skewed.append(bound)

#Skewed_simulation
clients = client_generation(max_clients, percentage_publisher, [0 for _ in range(max_clients)], n_topics, 1)
for send_rate in send_per_publisher:
    print(send_rate)
    for c in clients:
        c.sending_rate = send_rate
    res = simulationReal(n_brokers, capacity_per_broker, clients, "density")
    online_skewed.append(res)
    bound, val = optimalAllocationNew(n_brokers, capacity_per_broker, clients)
    optimal_skewed.append(val)
    bound_skewed.append(bound)

#NOT_SKEWED
plt.figure(figsize=(10, 6))
plt.errorbar(send_per_publisher, online_not_skewed, color="blue", capsize=5, label="Our Algorithm",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density
plt.errorbar(send_per_publisher, optimal_not_skewed, capsize=5, label="Best Gurobi solution", color="orange",linestyle="--",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density

plt.errorbar(send_per_publisher, bound_not_skewed, color="orange", linestyle=":", capsize=5, label="Theoretical Upperbound",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density

plt.xlabel("Messages per second", fontsize=24)
plt.ylabel("Managed clients", fontsize=24)
plt.legend(fontsize=24)
plt.grid(True)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)

#SKEWED

plt.figure(figsize=(10, 6))
plt.errorbar(send_per_publisher, online_skewed, color="blue", capsize=5, label="Our Algorithm",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density
plt.errorbar(send_per_publisher, optimal_skewed, capsize=5, label="Best Gurobi solution", color="orange",linestyle="--",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density

plt.errorbar(send_per_publisher, bound_skewed, color="orange", linestyle=":", capsize=5, label="Theoretical Upperbound",
             linewidth=3)  #yerr=std_devs_min # yerr=std_devs_density

plt.xlabel("Messages per second", fontsize=24)
plt.ylabel("Managed clients", fontsize=24)
plt.legend(fontsize=24)
plt.grid(True)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
plt.show()