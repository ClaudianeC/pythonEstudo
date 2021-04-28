#Ex022
nome = str(input('Digite seu nome completo: ')).strip()
separa = nome.split()
print('___ANALISANDO O SEU NOME___')
print('Seu nome em letras maiusculas e {} '.format(nome.upper()))
print('Seu nome em letras minusculas e {} '.format(nome.lower())) 
print('O seu primeiro nome e {}, e ele tem {} letras'.format(separa[0], len(separa[0])))
print('O Seu nome tem {} letras'.format(len(nome) - nome.count(' ')))

#Ex023
num = int(input('Digite um numero: '))
n = str(num)
u = num // 1 % 10
d = num // 10 % 10
c = num // 100 % 10
m = num // 1000 % 10
print('Analisando o numero {}'.format(num))
print('Unidade {}'.format(u))
print('Dezena {}'.format(d))
print('Centena {}'.format(c))
print('Milhar {}'.format(m))

