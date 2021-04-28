
#EX05
n1 = int(input('Digite um numero: '))
s = n1 * 3
a = n1 * 2
print('O dobro e {} vale {}'.format(n1, a))

#Ex06
n = int(input('Digite um numero: '))
d = n * 2 
t = n * 3
r = n ** (1/2)
print('O dobro e {} e o tripo e {}'.format(d, t))
print('A raiz quadrada e {:.2f}'.format(r))

#Ex07
n1 = float(input('Digite a primeira nota: '))
n2 = float(input('Digite a segunda nota: '))
n = (n1 + n2) / 2
print(' A media {} da primeira nota e {} e a da segunda e {}'.format(n, n1, n2))

#Ex08
medida = float(input('Uma distancia em metros: '))
cm = medida * 100
mm = medida * 1000
print('A medida {} corresponde a {:.0f}cm e {:.0f}mm'.format(medida, cm, mm))

#Ex09
num = int(input('Digite um numero para a tabuada: '))
print('{} x {} = {}'.format(num, 1, num*1))
print('{} x {} = {}'.format(num, 2, num*2))
print('{} x {} = {}'.format(num, 3, num*3))
print('{} x {} = {}'.format(num, 4, num*4))
print('{} x {} = {}'.format(num, 5, num*5))
print('{} x {} = {}'.format(num, 6, num*6))
print('{} x {} = {}'.format(num, 7, num*7))
print('{} x {} = {}'.format(num, 8, num*8))
print('{} x {} = {}'.format(num, 9, num*9))
print('{} x {} = {}'.format(num, 10, num*10))

#Ex010
real = float(input(' Digite quanto vc tem na carteira: '))
dolar = real / 3.27
print('O que vc tem de R${:.2f} fica U${:.2f} convertidos.'.format(real, dolar))

#Ex011
larg = float(input(' DIgite a largura da parede: '))
alt = float(input('Digite a altura da parede: '))
area = larg * alt
print('A dimensão da párede e {}x{} e sua area e de {}m2'.format(larg, alt, area))
tinta = area / 2
print('Que ira gastar {} de tinta'.format(tinta))

#Ex012
preço = float(input('Digite o valor do produto:R$ '))
novo = preço - (preço * 5 / 100)
print('O seu valor atual e {} com desconto de 5% ira ficar {}'.format(preço, novo))

print('Reajuste salarial Ex013')

salario = float(input('O valor atual do salario do funcionaro e:R$ '))
reajuste = salario + (salario * 15 / 100)
print('O novo valor de {:.3f} passa a ser {}'.format(salario, reajuste))


