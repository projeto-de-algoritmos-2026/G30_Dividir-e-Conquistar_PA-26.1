def _merge_count(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left
    inversions = 0

    while i <= mid and j <= right:
        if arr[i][1] <= arr[j][1]:
            temp[k] = arr[i]
            i += 1
        else:
            inversions += (mid - i + 1)
            temp[k] = arr[j]
            j += 1
        k += 1

    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1

    for idx in range(left, right + 1):
        arr[idx] = temp[idx]

    return inversions


def _merge_sort_count(arr, temp, left, right):
    inversions = 0
    if left < right:
        mid = (left + right) // 2
        inversions += _merge_sort_count(arr, temp, left, mid)
        inversions += _merge_sort_count(arr, temp, mid + 1, right)
        inversions += _merge_count(arr, temp, left, mid, right)
    return inversions


def contar_inversoes(ranking_a: list[float], ranking_b: list[float]) -> tuple[int, list[tuple]]:
    if len(ranking_a) != len(ranking_b):
        raise ValueError("Os rankings devem ter o mesmo tamanho.")

    n = len(ranking_a)
    if n == 0:
        return 0, []

    pares = sorted(
        enumerate(zip(ranking_a, ranking_b)),
        key=lambda x: x[1][0],  
        reverse=True
    )

    sequencia_b = [(pares[i][0], pares[i][1][1]) for i in range(n)]
    temp = [None] * n

    total_inversoes = _merge_sort_count(sequencia_b, temp, 0, n - 1)

    pares_invertidos = _encontrar_pares_invertidos(ranking_a, ranking_b)

    return total_inversoes, pares_invertidos


def _encontrar_pares_invertidos(ranking_a, ranking_b):
    n = len(ranking_a)
    pares = []
    for i in range(n):
        for j in range(i + 1, n):
            if (ranking_a[i] > ranking_a[j]) != (ranking_b[i] > ranking_b[j]):
                pares.append((i, j))
    return pares


def total_inversoes_grupo(rankings: dict[str, list[float]]) -> dict[tuple[str, str], tuple[int, list]]:
    resultado = {}
    pessoas = list(rankings.keys())
    for i in range(len(pessoas)):
        for j in range(i + 1, len(pessoas)):
            pa, pb = pessoas[i], pessoas[j]
            inv, pares = contar_inversoes(rankings[pa], rankings[pb])
            resultado[(pa, pb)] = (inv, pares)
    return resultado


def ranking_mais_discordante(resultado_grupo: dict) -> tuple[str, str] | None:
    if not resultado_grupo:
        return None
    return max(resultado_grupo, key=lambda k: resultado_grupo[k][0])


def similaridade(num_inversoes: int, n_filmes: int) -> float:
    max_inv = n_filmes * (n_filmes - 1) / 2
    if max_inv == 0:
        return 100.0
    return round((1 - num_inversoes / max_inv) * 100, 1)
