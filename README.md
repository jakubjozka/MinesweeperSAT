# Řešení úlohy Minesweeper pomocí SAT solveru

Použitý SAT solver je [Glucose](https://www.labri.fr/perso/lsimon/research/glucose/), konkrétně [Glucose 4.2.1](https://github.com/audemard/glucose/releases/tag/4.2.1). Zdrojový kód je kompilován pomocí

```
cmake .
make
```

Tento projekt obsahuje zkompilovaný UNIX binární soubor Glucose solveru. Solver i Python skript jsou určeny pro UNIX-based systémy.

# Dokumentace
## Popis problému

Minesweeper je logická hra, ve které hráč odkrývá políčka na mřížce, kde některá obsahují miny. Každé odkryté políčko bez miny zobrazuje číslo, které udává, kolik z jeho sousedních políček (až 8 sousedů) obsahuje minu.

### Formální definice:
- Mřížka velikosti $m×n$
- Každé políčko $(r, c)$ může obsahovat minu, nebo ne
- Některá políčka jsou odhalena s číslem $k ∈ {0, 1, ..., 8}$
- Číslo $k$ znamená, že právě $k$ sousedních políček obsahuje minu
- Políčko s číslem nemůže obsahovat minu

Řešený problém: Existuje umístění min, které splňuje všechna zadaná čísla?

### Formát vstupu

Příklad platného vstupního formátu:

```
3 3
1 ? ?
? ? ?
? ? 1
```

kde první řádek obsahuje rozměry mřížky (počet řádků a sloupců). Následujicí řádky obsahují samotnou mřížku, kde:
- $?$ = neznámé políčko (může nebo nemusí obsahovat minu)
- $0-8$ = odkryté políčko s daným počtem sousedních min
- Políčka jsou oddělena mezerami

## Kodování
### Proměnné
Problém koduji pomocí jedné sady proměnných. Proměnná $Mine(r, c)$ reprezentuje, že políčko na řádku $r$ a sloupci $c$ obsahuje minu.

Pro mřížku $m×n$ máme celkem m×n proměnných.

### Omezení

Pro každé políčko $(r, c)$ které je odkryté s číslem $k$:
1. Políčko s číslem není mina: $\neg Mine(r, c)$
2. Přesně $k$ sousedů obsahuje minu: Něchť $N(r, c)$ je množina sousedních políček (až 8 sousedů). Přesně $k$ z nich obsahuje minu. Toto je zakodované jako kombinace dvou podmínek:
    - "Alespoň $k$ min": Pro každou podmnožinu $(n - k + 1)$ sousedů alespoň jeden obsahuje minu: $\bigwedge_{S \subseteq N(r, c), |S| = n - k + 1} \bigvee_{(r', c') \in S} Mine(r', c')$
    - "Nejvýše $k$ min": Pro každou $(k + 1)$ sousedů alespoň jeden neobsahuje minu: $\bigwedge_{S \subseteq N(r,c), |S| = k+1} \bigvee_{(r',c') \in S} \neg Mine(r',c')$

## Uživatelská dokumentace

Základní použití

```
python3 minesweeper.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```