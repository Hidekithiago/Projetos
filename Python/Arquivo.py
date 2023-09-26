import shutil
import os

def copiaArquivo(original, destino):
    shutil.copy2(original, destino)
    
def capturaNomeArquivo(caminhoArquivo):
    file_name = os.path.basename(caminhoArquivo)
    file = os.path.splitext(file_name)
    return file[0], file[1]

def criarArquivo(diretorio, texto):
    arquivo = open(diretorio, "w")
    arquivo.write(texto)
    arquivo.close()
    
def excluiArquivo(diretorio):
    os.remove(diretorio)