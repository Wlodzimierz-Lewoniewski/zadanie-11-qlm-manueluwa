import math
from collections import Counter
import re

lambda_wartosc = 0.5

def tokenizuj(tekst):
    return [slowo.strip() for slowo in re.split(r'[,\.\?!: ]+', tekst.lower()) if slowo]

def oblicz_czestosci(dokumenty):
    czestosci_w_dokumentach = [Counter(tokenizuj(dok)) for dok in dokumenty]
    czestosci_korpusu = Counter(slowo for czestosci in czestosci_w_dokumentach for slowo in czestosci)
    return czestosci_w_dokumentach, czestosci_korpusu

def policz_prawdopodobienstwo(dokumenty, zapytanie, czestosci_w_dokumentach, czestosci_korpusu):
    terminy_zapytania = tokenizuj(zapytanie)
    dlugosc_korpusu = sum(czestosci_korpusu.values())
    wyniki = []

    for indeks, czestosci_dokumentu in enumerate(czestosci_w_dokumentach):
        dlugosc_dokumentu = sum(czestosci_dokumentu.values())
        log_prawdopodobienstwo = 0

        for termin in terminy_zapytania:
            p_td = czestosci_dokumentu[termin] / dlugosc_dokumentu if dlugosc_dokumentu > 0 else 0
            p_tc = czestosci_korpusu[termin] / dlugosc_korpusu if dlugosc_korpusu > 0 else 0
            p_t = lambda_wartosc * p_td + (1 - lambda_wartosc) * p_tc

            if p_t > 0:
                log_prawdopodobienstwo += math.log(p_t)
            else:
                log_prawdopodobienstwo = float('-inf')
                break

        wyniki.append((indeks, log_prawdopodobienstwo))

    wyniki.sort(key=lambda x: (-x[1], x[0]))
    return wyniki

def model_prawdopodobienstwa(zapytanie, dokumenty):
    czestosci_w_dokumentach, czestosci_korpusu = oblicz_czestosci(dokumenty)
    wyniki = policz_prawdopodobienstwo(dokumenty, zapytanie, czestosci_w_dokumentach, czestosci_korpusu)
    indeksy = [indeks for indeks, _ in wyniki]
    print(indeksy)

def main():
    liczba_dokumentow = int(input())
    dokumenty = [input() for _ in range(liczba_dokumentow)]
    zapytanie = input()

    model_prawdopodobienstwa(zapytanie, dokumenty)

main()
