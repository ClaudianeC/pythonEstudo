#Ex028
import random
num = int(input('\033[0;34mEscreva um numero de 0 a 5: \033[m'))
computador = random.randint(0, 5)
print('#' * 25)
print('\033[0;35m ADVINHANDO..\033[m')
print("True" if computador == num else "False")
print("---FIM---")

#Ex029
velocidade = float(input('Qual e a velocidade do seu carro:'))
if velocidade > 80:
    print('\033[0;31m MULTADO! Voce execedeu o limite de velocidade. O limite e de 80KM/h\033[m')
    multa = (velocidade - 80) * 7
    print('Voce vai pagar uma multa de R${:.2f}!'.format(multa))
print('\033[0;32m Tenha um bom dia, dirija com cuidado!\033[m')

#Ex030
distancia = float(input('A distancia da sua viagem e de: '))
print('Voce esta em uma viagem de {}Km'.format(distancia))
if distancia <= 200:
    preço = distancia * 0.45
else
    preço = distancia * 0.50
print('Sua viagem custara R${}'.format(preço))
print('BOA VIAGEM!!')
    

