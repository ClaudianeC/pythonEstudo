#Ex016
import math
num = float(input('Digite um numero: '))
print('A parte inteira de {} e {}'.format(num, math.trunc(num)))

#Ex017
ca = float(input('Digite o cateto adjacente: '))
co = float(input('Digite o cateto oposto: '))
hi = math.hypot(ca, co)
print('O valor da hipotenusa do ca {} e do ca {} e {:.2f}'.format(ca, co, hi))

#Ex018
a = float(input('Digite um angulo: '))
seno = math.sin(math.radians(a))
cos = math.cos(math.radians(a))
tan = math.tan(math.radians(a))
print('O SENO do angulo e :{}º '.format(seno))
print('O COSSENO do angulo e :{}º '.format(cos))
print('O TANGENTE do angulo e :{}º '.format(tan))

#Ex019
import random
a1 = str(input('Digite um nome: '))
a2 = str(input('Digite um nome: '))
a3 = str(input('Digite um nome: '))
a4 = str(input('Digite um nome: '))
lista = [a1, a2, a3, a4]
sorteio = random.choice(lista)
print('O nome sorteado foi {} '.format(sorteio))


