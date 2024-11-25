# MQTT-PRE

This repository is for reproducibility of the experiments presented in the paper: TODO

## Reproducing the Figures

### Figures 2, 3, 4, and 5

To generate Figures 2, 3, 4, and 5, use the script `SimulationCriteria.py`. This script allows you to simulate the required scenarios by setting the following variables:

- **sigma**: Experimental condition, set to `0` or `10`.
- **s**: Scenario setting, set to `0` or `1`.

By running the script with these combinations of `sigma` and `s`, you will obtain the respective figures:
- **(sigma=0, s=0)**: Figure 2
- **(sigma=0, s=1)**: Figure 3
- **(sigma=10, s=0)**: Figure 4
- **(sigma=10, s=1)**: Figure 5

#### Default settings
The default values are:
- `sigma=0`
- `s=1`

#### Speeding up the simulation
To reduce the simulation time, you can lower the value of the `n_simulations` variable in the script. The default value is `n_simulations=100`. Reducing it will speed up the process but may slightly decrease the accuracy of the results.

---

### Figures 6 and 7

To generate Figures 6 and 7, use the script `SimulationRealScenario.py`. This requires installing the **Gurobi** optimization library and activating a valid license.
To reduce computation time, adjust the time limit in the Core.py file. Modify the following line in the class Core.py:
```python
   model.setParam("TimeLimit", 1400)
```
#### Setting up Gurobi
1. **Install the Gurobi Python library:**
   ```bash
   pip install gurobipy
   ```
2. **Obtain and activate a Gurobi license:**
   Obtain a license from Gurobi's official website.
   Configure your license as required by Gurobi's installation instructions.
3. **Obtain and activate a Gurobi license:**
   Update the params dictionary in the Core.py file with your Gurobi license details:
```python
   params = {
    "WLSACCESSID": '#################################',  # Replace with your WLSACCESSID
    "WLSSECRET": '#################################',   # Replace with your WLSSECRET
    "LICENSEID": 00000000,                              # Replace with your LICENSEID
}
