import math
import random
import sys
from statistics import mean
import gurobipy as gp
from Setup import compute_client_overhead, compute_topic_overhead
from gurobipy import GRB, quicksum

def simulation(n_brokers, capacity_per_broker, clients, strategy):
    random.seed(10)
    moved_client = 0
    managed_client = dict()
    execution_times = dict()
    execution_counter = 0
    broker_topic = {}
    for b in range(n_brokers):
        broker_topic[b] = set()
    topic_broker = {}
    topic_client = {}
    remaining_cap = dict(capacity_per_broker)
    cont = 0
    for client in clients:
        topic = client.topic
        # Controlla se il topic ha già un broker assegnato
        if topic_broker.get(topic) is not None:
            broker_number = topic_broker[topic]
            client_overhead = compute_client_overhead(client, topic_client)
            topic_client[topic].append(client)
            remaining_cap[broker_number] = remaining_cap[broker_number] - client_overhead
            # Verifica se la capacità residua è sufficiente per l'overhead richiesto
            if remaining_cap[broker_number] < 0:
                execution_counter += 1
                topics = list(broker_topic[broker_number])
                if strategy == "min_client":
                    # Ordina per numero totale di clients per topic (dal minore al maggiore)
                    topics.sort(key=lambda tp: len(topic_client[tp]))

                elif strategy == "density":
                    # Ordina per densità di clients rispetto all'overhead del topic
                    topics.sort(
                        key=lambda tp: (compute_topic_overhead(topic_client[tp]) / (len(topic_client[tp]))),
                        reverse=True)
                elif strategy == "elasticity":
                    # Ordina per densità di clients rispetto all'elasticity del topic
                    topics_sending_rates = {}
                    for tt in topics:
                        send_rate = 0
                        for c in topic_client[tt]:
                            if c.publisher:
                                send_rate += c.sending_rate
                        topics_sending_rates[tt] = send_rate
                    topics.sort(
                        key=lambda tp: (len(topic_client[tp]) * topics_sending_rates[tp]),
                        reverse=True)

                elif strategy == "max_overhead":
                    # Ordina per overhead in modo decrescente
                    topics.sort(key=lambda tp: compute_topic_overhead(topic_client[tp]), reverse=True)

                elif strategy == "baseline":
                    # Ordina per overhead in modo decrescente
                    random.shuffle(topics)

                else:
                    print("Wrong strategy")

                for t in topics:
                    max_broker = max(remaining_cap, key=lambda br: remaining_cap[br])
                    topic_overhead = compute_topic_overhead(topic_client[t])
                    if remaining_cap[max_broker] < topic_overhead or topic_overhead == 0:
                        continue
                    '''  
                    print(topics)
                    print([compute_topic_overhead(topic_client[tt]) for tt in topics])
                    print([len(topic_client[tt]) for tt in topics])
                    print("topic: " + str(t))
                    return 0,0
                    '''
                    broker_topic[broker_number].remove(t)
                    broker_topic[max_broker].add(t)
                    topic_broker[t] = max_broker
                    remaining_cap[max_broker] = remaining_cap[max_broker] - topic_overhead
                    remaining_cap[broker_number] = remaining_cap[broker_number] + topic_overhead
                    moved_client = moved_client + len(topic_client[t])
                    if remaining_cap[broker_number] >= 0:
                        break
                else:
                    print("END EXECUTION with Strategy:" + strategy)
                    return managed_client, execution_times
        else:
            broker_number = random.randint(0, n_brokers - 1)
            #broker_number = max(remaining_cap, key=lambda br: remaining_cap[br])
            broker_topic[broker_number].add(topic)
            topic_broker[topic] = broker_number
            topic_client[topic] = [client]
        cont += 1
        managed_client[cont] = moved_client
        execution_times[cont] = execution_counter
    print("END COMPLETED EXECUTION with Strategy:" + strategy)

    return managed_client, execution_times


def simulationReal(n_brokers, capacity_per_broker, clients, strategy):
    random.seed(10)
    moved_client = 0
    managed_client = dict()
    execution_times = dict()
    execution_counter = 0
    broker_topic = {}
    for b in range(n_brokers):
        broker_topic[b] = set()
    topic_broker = {}
    topic_client = {}
    remaining_cap = dict(capacity_per_broker)
    cont = 0
    for client in clients:
        topic = client.topic
        # Controlla se il topic ha già un broker assegnato
        if topic_broker.get(topic) is not None:
            broker_number = topic_broker[topic]
            client_overhead = compute_client_overhead(client, topic_client)
            topic_client[topic].append(client)
            remaining_cap[broker_number] = remaining_cap[broker_number] - client_overhead
            # Verifica se la capacità residua è sufficiente per l'overhead richiesto
            if remaining_cap[broker_number] < 0:
                execution_counter += 1
                topics = list(broker_topic[broker_number])
                if strategy == "min_client":
                    # Ordina per numero totale di clients per topic (dal minore al maggiore)
                    topics.sort(key=lambda tp: len(topic_client[tp]))

                elif strategy == "density":
                    # Ordina per densità di clients rispetto all'overhead del topic
                    topics.sort(
                        key=lambda tp: (compute_topic_overhead(topic_client[tp]) / (len(topic_client[tp]))),
                        reverse=True)
                elif strategy == "elasticity":
                    # Ordina per densità di clients rispetto all'elasticity del topic
                    topics_sending_rates = {}
                    for tt in topics:
                        send_rate = 0
                        for c in topic_client[tt]:
                            if c.publisher:
                                send_rate += c.sending_rate
                        topics_sending_rates[tt] = send_rate
                    topics.sort(
                        key=lambda tp: (len(topic_client[tp]) * topics_sending_rates[tp]),
                        reverse=True)

                elif strategy == "max_overhead":
                    # Ordina per overhead in modo decrescente
                    topics.sort(key=lambda tp: compute_topic_overhead(topic_client[tp]), reverse=True)

                elif strategy == "baseline":
                    # Ordina per overhead in modo decrescente
                    random.shuffle(topics)

                else:
                    print("Wrong strategy")

                for t in topics:
                    max_broker = max(remaining_cap, key=lambda br: remaining_cap[br])
                    topic_overhead = compute_topic_overhead(topic_client[t])
                    if remaining_cap[max_broker] < topic_overhead or topic_overhead == 0:
                        continue
                    '''  
                    print(topics)
                    print([compute_topic_overhead(topic_client[tt]) for tt in topics])
                    print([len(topic_client[tt]) for tt in topics])
                    print("topic: " + str(t))
                    return 0,0
                    '''
                    broker_topic[broker_number].remove(t)
                    broker_topic[max_broker].add(t)
                    topic_broker[t] = max_broker
                    remaining_cap[max_broker] = remaining_cap[max_broker] - topic_overhead
                    remaining_cap[broker_number] = remaining_cap[broker_number] + topic_overhead
                    moved_client = moved_client + len(topic_client[t])
                    if remaining_cap[broker_number] >= 0:
                        break
                else:
                    topic_client[topic].remove(client)
                    remaining_cap[broker_number] = remaining_cap[broker_number] + client_overhead

        else:
            broker_number = random.randint(0, n_brokers - 1)
            #broker_number = max(remaining_cap, key=lambda br: remaining_cap[br])
            broker_topic[broker_number].add(topic)
            topic_broker[topic] = broker_number
            topic_client[topic] = [client]
    res = 0
    for b in range(n_brokers):
        for t in broker_topic[b]:
            found_pub = False
            found_sub = False
            for c in topic_client[t]:
                if c.publisher:
                    found_pub = True
                else:
                    found_sub = True
            if found_pub and found_sub:
                res += len(topic_client[t])

    print("END COMPLETED EXECUTION with Strategy:" + strategy)
    return res


'''
def optimalAllocation(n_broker, capacity_per_brokers, clients):
    overall_Cap = 0
    for b in range(n_broker):
        overall_Cap += capacity_per_brokers[b]
    topic_clients = dict()
    for cl in clients:
        topic = cl.topic
        if topic_clients.get(topic) is None:
            topic_clients[topic] = []
        topic_clients[topic].append(cl)
    topic_overhead = dict()
    for t in topic_clients.keys():
        topic_overhead[t] = compute_topic_overhead(topic_clients[t])
    topic_list = list(topic_clients.keys())
    topic_list.sort(
        key=lambda tp: (topic_overhead[tp] / len(topic_clients[tp])))

    res = 0
    for t in topic_list:
        res += len(topic_clients[t])
        overall_Cap = overall_Cap - topic_overhead[t]
        if overall_Cap < 0:
            return res
    return res




def optimalAllocation(n_broker, capacity_per_brokers, clients):
    topic_clients = dict()
    for cl in clients:
        topic = cl.topic
        if topic_clients.get(topic) is None:
            topic_clients[topic] = []
        topic_clients[topic].append(cl)

    topic_overhead = dict()
    for t in topic_clients.keys():
        topic_overhead[t] = compute_topic_overhead(topic_clients[t])
    topic_list = list(topic_clients.keys())
    topic_list.sort(
        key=lambda tp: (topic_overhead[tp] / len(topic_clients[tp])))

    res = 0
    for b in range(n_broker):
        overall_Cap = capacity_per_brokers[b]
        taken_topic = []
        for t in topic_list:
            res += len(topic_clients[t])
            overall_Cap = overall_Cap - topic_overhead[t]
            taken_topic.append(t)
            if overall_Cap < 0:
                break
        for t in taken_topic:
            topic_list.remove(t)
    return res

'''
def optimalAllocation(n_broker, capacity_per_brokers, clients):
    topic_clients = dict()
    for cl in clients:
        topic = cl.topic
        if topic_clients.get(topic) is None:
            topic_clients[topic] = []
        topic_clients[topic].append(cl)
    topic_list=list(topic_clients.keys())
    topic_list.sort()

    # Dati del problema
    T = len(topic_list)  # Numero di topic
    K = n_broker  # Numero di broker
    P=[]
    S=[]
    for t in topic_list:
        cont_pub=0
        cont_sub=0
        for c in topic_clients[t]:
            if c.publisher:
                cont_pub+=1
            else:
                cont_sub+=1
        P.append(cont_pub)
        S.append(cont_sub)
    R = clients[0].sending_rate # Tasso di carico per interazione
    C = capacity_per_brokers[0]  # Capacità di ciascun broker

    API_key = "c77214af-dd4f-4da2-9d73-47e18b018476"
    params = {
        "WLSACCESSID": 'c77214af-dd4f-4da2-9d73-47e18b018476',
        "WLSSECRET": '399b4cdb-3f4f-45c9-a2a7-52ae2e24716f',
        "LICENSEID": 2585840,
    }
    env = gp.Env(params=params)

    # Creazione del modello
    model = gp.Model(env=env)
    # model = Model("Broker_Allocation")

    # Variabili
    # x = model.addVars(T, K, vtype=GRB.BINARY, name="x")  # x[t, b]
    # change1
    x = model.addVars(T, K, vtype=GRB.BINARY, name="x")
    p = model.addVars(T, K, vtype=GRB.INTEGER, name="p")  # p[t, b]
    s = model.addVars(T, K, vtype=GRB.INTEGER, name="s")  # s[t, b]

    # Funzione obiettivo: massimizzare i client allocati
    model.setObjective(
        quicksum(p[t, b] + s[t, b] for t in range(T) for b in range(K)), GRB.MAXIMIZE
    )

    # Vincoli
    # 1. Capacità del broker
    for b in range(K):
        model.addConstr(
            quicksum(p[t, b] * s[t, b] * R for t in range(T)) <= C,
            name=f"capacity_broker_{b}"
        )

    # 2. Allocazione unica per topic
    for t in range(T):
        model.addConstr(
            quicksum(x[t, b] for b in range(K)) <= 1,
            name=f"unique_allocation_topic_{t}"
        )

    # 3. Relazione tra variabili x, p e s
    for t in range(T):
        for b in range(K):
            model.addConstr(p[t, b] <= P[t] * x[t, b], name=f"limit_p_{t}_{b}")
            model.addConstr(s[t, b] <= S[t] * x[t, b], name=f"limit_s_{t}_{b}")

    # 4. Allocazione parziale valida: almeno un publisher e un subscriber se il topic è allocato

    for t in range(T):
        for b in range(K):
            model.addConstr(p[t, b] >= x[t, b], name=f"min_publisher_{t}_{b}")
            model.addConstr(s[t, b] >= x[t, b], name=f"min_subscriber_{t}_{b}")

    model.setParam("TimeLimit", 60)
    model.setParam("MIPGap", 0.15)
    # Risolvi il modello
    model.optimize()
    return model.ObjBound, model.objVal


def optimalAllocationNew(n_broker, capacity_per_brokers, clients):
    topic_clients = dict()
    for cl in clients:
        topic = cl.topic
        if topic_clients.get(topic) is None:
            topic_clients[topic] = []
        topic_clients[topic].append(cl)
    topic_list=list(topic_clients.keys())
    topic_list.sort()

    # Dati del problema
    T = len(topic_list)  # Numero di topic
    K = n_broker  # Numero di broker
    P=[]
    S=[]
    for t in topic_list:
        cont_pub=0
        cont_sub=0
        for c in topic_clients[t]:
            if c.publisher:
                cont_pub+=1
            else:
                cont_sub+=1
        P.append(cont_pub)
        S.append(cont_sub)
    R = clients[0].sending_rate # Tasso di carico per interazione
    C = capacity_per_brokers[0]  # Capacità di ciascun broker


    params = {
        "WLSACCESSID": '#################################',
        "WLSSECRET": '#################################',
        "LICENSEID": 00000000,
    }
    env = gp.Env(params=params)

    # Creazione del modello
    model = gp.Model(env=env)
    # model = Model("Broker_Allocation")

    # Variabili
    # x = model.addVars(T, K, vtype=GRB.BINARY, name="x")  # x[t, b]
    # change1
    x = model.addVars(T, K, vtype=GRB.BINARY, name="x")
    p = model.addVars(T, vtype=GRB.INTEGER, name="p")  # p[t, b]
    s = model.addVars(T, vtype=GRB.INTEGER, name="s")  # s[t, b]
    ps = model.addVars(T, vtype=GRB.INTEGER, name="ps")

    # Funzione obiettivo: massimizzare i client allocati
    model.setObjective(
        quicksum(p[t] + s[t] for t in range(T)), GRB.MAXIMIZE
    )

    # Vincoli
    # 1. Capacità del broker
    for b in range(K):
        model.addConstr(
            quicksum(ps[t] * R * x[t, b] for t in range(T)) <= C,
            name=f"capacity_broker_{b}"
        )

    for t in range(T):
        model.addConstr(ps[t] == p[t] * s[t], name=f"product_ps_{t}")

    # 2. Allocazione unica per topic
    for t in range(T):
        model.addConstr(
            quicksum(x[t, b] for b in range(K)) <= 1,
            name=f"unique_allocation_topic_{t}"
        )

    # 3. Relazione tra variabili x, p e s
    for t in range(T):
        model.addConstr(p[t] <= P[t] * quicksum(x[t, b] for b in range(K)), name=f"limit_p_{t}")
        model.addConstr(s[t] <= S[t] * quicksum(x[t, b] for b in range(K)), name=f"limit_s_{t}")

    # 4. Allocazione parziale valida: almeno un publisher e un subscriber se il topic è allocato

    for t in range(T):
        for b in range(K):
            model.addConstr(p[t] >= x[t, b], name=f"min_publisher_{t}_{b}")
            model.addConstr(s[t] >= x[t, b], name=f"min_subscriber_{t}_{b}")

    model.setParam("TimeLimit", 1400)
    # Risolvi il modello
    model.optimize()
    return model.ObjBound, model.objVal