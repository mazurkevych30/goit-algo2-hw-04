from collections import deque
from collections import defaultdict


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [
        [0] * num_nodes for _ in range(num_nodes)
    ]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow, flow_matrix


def add_super_source_sink(
    capacity_matrix_20, terminals=(0, 1), shops=tuple(range(6, 20))
):
    n = len(capacity_matrix_20)  # 20
    super_source = n  # 20
    super_sink = n + 1  # 21
    new_n = n + 2  # 22

    # 22x22 з нулями
    cap = [[0] * new_n for _ in range(new_n)]

    # Копіюємо існуючі ребра
    for i in range(n):
        for j in range(n):
            cap[i][j] = capacity_matrix_20[i][j]

    # Підключаємо суперджерело до терміналів
    # Місткість беремо як суму вихідних ребер термінала (верхня межа його пропускної здатності)
    for t in terminals:
        cap[super_source][t] = sum(capacity_matrix_20[t])

    # Підключаємо магазини до суперстоку
    INF = 10**9
    for s in shops:
        cap[s][super_sink] = INF

    return cap, super_source, super_sink


# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [
    [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Термінал 1
    [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Термінал 2
    [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Склад 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0],  # Склад 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0],  # Склад 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10],  # Склад 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 11
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 12
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 13
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 14
]

# Побудова 22x22
cap22, S, T = add_super_source_sink(capacity_matrix)

max_flow, flow_matrix = edmonds_karp(cap22, S, T)
print("Глобальний максимальний потік:", max_flow)

# Мапінг складів до магазинів
warehouse_to_shops = {
    2: [6, 7, 8],  # Склад 1 -> Магазини 1..3
    3: [9, 10, 11],  # Склад 2 -> Магазини 4..6
    4: [12, 13, 14],  # Склад 3 -> Магазини 7..9
    5: [15, 16, 17, 18, 19],  # Склад 4 -> Магазини 10..14
}

# Які термінали підключені до яких складів
terminal_to_warehouses = {
    0: [2, 3, 4],  # T1 -> W1,W2,W3
    1: [3, 4, 5],  # T2 -> W2,W3,W4
}

# обчислити притік від терміналів у склади
inflow_from_terminal = {w: defaultdict(int) for w in warehouse_to_shops}
for t, warehouses in terminal_to_warehouses.items():
    for w in warehouses:
        inflow_from_terminal[w][t] = flow_matrix[t][w]

# сумарний притік у склад
total_inflow_to_w = {
    w: sum(inflow_from_terminal[w].values()) for w in warehouse_to_shops
}

# розподілити вихідні потоки складу до магазинів пропорційно внеску терміналів
terminal_shop_flow = defaultdict(int)
for w, shops in warehouse_to_shops.items():
    for s in shops:
        w_to_s = flow_matrix[w][s]
        if total_inflow_to_w[w] == 0:
            continue
        for t, t_in in inflow_from_terminal[w].items():
            share = w_to_s * (t_in / total_inflow_to_w[w])
            terminal_shop_flow[(t, s)] += share

# виводимо таблицю
print("Термінал | Магазин | Потік")
for (t, s), val in sorted(terminal_shop_flow.items()):
    print(f"T{t+1:<2} -> M{s-5:<2} : {int(round(val))}")
