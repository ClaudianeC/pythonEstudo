#Ex031
from time import sleep
import emoji
for c in range(10, -1, -1):
     print(c)
     sleep(0.5)
print('BOMM EXPLOSÂO!!!')
print(emoji.emojize('EXPLOSÂO!!: boom :', use_aliases=True))

#Ex032
somai = 0
media = 0
maiori = 0
nomev = ''
totalm = 0
for p in range(1, 5):
    print('\033[4;36m*******{}ºPESSOA*******\033[m'.format(p))
    nome = str(input('Nome:')).strip()
    idade = int(input('Idade: '))
    sexo = str(input('Sexo [M/F]: ')).strip()
    somai += idade
    if p == 1 and sexo in 'Mm':
        maiori = idade
        nomev = nome
    if sexo 'Mm' and idade > maiori:
        maiori = idade
        nomev = nome
    if sexo 'Ff' and idade < 20:
        totalm += 1
media = somai / 4
print('A soma da idade do grupo e de {} anos.'.format(media))
print('O homem mais velho tem {} anos e se chama {}'.format(maiori, nomev))
print('Ao todo são {} mulheres com menos de 20 anos.'.format(totalm))

#Ex033
from datetime import date
atual = date.today().year
nasc = int(input('Ano de nascimento: '))
idade = atual - nasc
print('Voce nasceu em {} e tem {} anos.'.format(nasc, idade, atual))
if idade == 18:
    print('O dever o chama!! Alisti-se IMEDIATAMENTE!')
elif idade < 18:
    menor = idade - 18
    print('Voce ainda e novo demais, ainda falta {} anos!'.format(menor))
elif idade > 18:
    maior = idade - 18
    print('A obrigatoriedade ja passou, vc ja tem {} anos! Procure uma outra area de interesse!'.format(maior))
    ano = atual - maior
    print('Seu alistamento foi em {}'.format(ano))
