from datetime import datetime


def dataAtual():
    return datetime.now()

def dataAtualFormatada(formatacao):
    return dataAtual().strftime(formatacao)    
