import os

def capturarArquivosPastaSubPasta(diretorio):
    arquivosDicionario = []   

    for diretorio, subpastas, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            arquivosDicionario.append(os.path.join(os.path.realpath(diretorio), arquivo))
            #print(os.path.join(os.path.realpath(diretorio), arquivo))
    return arquivosDicionario
