from datetime import datetime
DIAS = [
    'Domingo',
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado'
]
#data = datetime.strptime('2023-05-29', "%'%'%Y-%'%'%m-%'%'%d") #PowerAutomate
data = datetime.strptime('2023-05-29', "%Y-%m-%d")

print(data)
print(DIAS[data.isoweekday()])
print(data.isoweekday())
