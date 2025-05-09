import json
import random
import time

# fisier JSON
with open('date.json') as f:
    data = json.load(f)

bancnote_initiale = data['bancnote']
produse = data['produse']

def bancnote_to_dict(bancnote):
    return {b['valoare']: b['stoc'] for b in bancnote}

# Programare dinamica pt rest
def calculeaza_rest(rest, bancnote_stoc):
    valori = sorted(bancnote_stoc.keys(), reverse=True)
    dp = [None] * (rest + 1)
    dp[0] = {}

    for suma in range(1, rest + 1):
        min_comb = None
        for val in valori:
            if val > suma or dp[suma - val] is None:
                continue
            prev = dp[suma - val]
            if prev.get(val, 0) < bancnote_stoc[val]:
                comb = prev.copy()
                comb[val] = comb.get(val, 0) + 1
                if min_comb is None or sum(comb.values()) < sum(min_comb.values()):
                    min_comb = comb
        dp[suma] = min_comb
    return dp[rest]

# Simulare clienti
bancnote_stoc = bancnote_to_dict(bancnote_initiale)
client_id = 1

while True:
    produs = random.choice(produse)
    pret = produs['pret']
    suma_platita = pret + random.randint(1, 20)
    rest = suma_platita - pret

    print(f"\nClient #{client_id}")
    print(f"Produs cumparat: {produs['nume']}")
    print(f"Pret: {pret}")
    print(f"Suma platita: {suma_platita}")
    print(f"Rest de dat: {rest}")

    rest_bancnote = calculeaza_rest(rest, bancnote_stoc)

    if rest_bancnote is None:
        print("Nu se poate da restul cu bancnotele disponibile. Simularea se opreste.")
        print("Stoc curent bancnote:", bancnote_stoc)
        break

    print("Rest oferit:")
    for val in sorted(rest_bancnote.keys(), reverse=True):
        print(f"{val} x {rest_bancnote[val]}")
        bancnote_stoc[val] -= rest_bancnote[val]
    time.sleep(2)
    client_id += 1