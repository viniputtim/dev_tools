import random
import time

banca_inicial = 1000
aposta_inicial = 10
limite_aposta = 5000.0
pausar = False

banca = banca_inicial
aposta = aposta_inicial
rodada = 0
vitorias = 0
derrotas = 0

def jogar_roleta():
    return random.random() < 0.47

for i in range(1000):
    rodada += 1
    banca -= aposta
    ganhou = jogar_roleta()

    if ganhou:
        banca += aposta * 2
        aposta = aposta_inicial
        vitorias += 1
        resultado = "✅ Vitória"
    else:
        aposta *= 2
        derrotas += 1
        resultado = "❌ Derrota"

    if aposta > limite_aposta or aposta > banca:
        print(f"\n💥 FALÊNCIA na rodada {rodada}!")
        print(f"Banca final: R$ {banca:.2f}")
        break

    print(f"Rodada {rodada:4} | Aposta: R$ {aposta:7.2f} | Banca: R$ {banca:8.2f} | {resultado}")

    if pausar:
        time.sleep(0.2)

print(f"\n📊 Estatísticas:")
print(f"  Rodadas:     {rodada}")
print(f"  Vitórias:    {vitorias}")
print(f"  Derrotas:    {derrotas}")
print(f"Banca final: R$ {banca:.2f}")
