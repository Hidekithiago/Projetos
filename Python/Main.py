#pip3 install PyMuPDF install opencv-python
import Pasta
import Pdf
import Data
import cv2
import Arquivo
import BancoDados as bd
import re
from ClasseFuncionario import Funcionario


#Pdf.capturaPaginaPdf(r'C:/GitHub/Grs/Exemplos/rtc.pdf', 0, zoom = 1.5)

database = bd.Mysql()
database.connect(bd.mysql_homolog)
diretorioArquivoOriginalPdf = r"Z:\Digitalização prontuários físicos - GRS"
listaArquivosPasta = Pasta.capturarArquivosPastaSubPasta(diretorioArquivoOriginalPdf)
#Pdf.ExcluirPaginaPdf(r'C:\GitHub\Grs\Exemplos\aa.pdf', [17-1]) #Gera um novo arquivo sem algumas páginas
querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId) VALUES (2, 1)"
idLogRobos = database.InsertMysql(querySql)

for listaArquivos in listaArquivosPasta:
    #listaArquivos = r'C:\GitHub\Grs\Exemplos\kit_demo.pdf'
    contador = 0
    diretorioPdfGerado = ""
    dataAtual = Data.dataAtualFormatada('%Y-%m-%d_%H%M%S')
    jsonQRCodeInsert = ''
    print(listaArquivos)
    nome, extensao = Arquivo.capturaNomeArquivo(listaArquivos)
    Arquivo.copiaArquivo(listaArquivos, f'Z:\Backup - Robo\{nome}_{dataAtual}{extensao}')
    while True:
        dataAtual = Data.dataAtualFormatada('%Y-%m-%d_%H%M%S')
        quantidadePaginas = Pdf.quantidadePaginasPdf(listaArquivos)
        print(f'Contador {contador} Quantidade de Páginas {quantidadePaginas}')
        if quantidadePaginas == (contador+1) and contador != 0: # Verifica se é a ultima página do arquivo PDF caso arquivo original tenha mais que 1 pagina            
            Pdf.copiaPdf(listaArquivos, diretorioPdfGerado, contador)
            listaArq = listaArquivos.replace('\\','\\\\')
            dirPdfGerado = diretorioPdfGerado.replace('\\','\\\\')
            try:
                querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId, json, ArquivoOriginal, ArquivoCortado) VALUES (3, 1, '{jsonQRCodeInsert}', '{listaArq}', '{dirPdfGerado}')"
            except:
                querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId, json, ArquivoOriginal, ArquivoCortado) VALUES (3, 1, '', '{listaArq}', '{dirPdfGerado}')"
            database.InsertMysql(querySql)
            Arquivo.excluiArquivo(listaArquivos)
            break
        
        jsonQRCode = Pdf.capturaPaginaPdf(listaArquivos, contador, 1.5)
        if len(jsonQRCode) == 0:
            jsonQRCode = Pdf.capturaPaginaPdf(listaArquivos, contador, 0.5)

        if len(jsonQRCode) != 0:
            jsonQRCodeInsert = jsonQRCode[0]
        
        '''''Resultado do QRCode
        ('{"0":"1261614","1":"952","7":"233134633","99":"6"}',)
        0 = Código da Empresa
        1 = Código do Funcionário
        7 = Código Sequencial da Ficha
        99 = Código do Tipo de Ficha
            6 = ASO - Atestado de Saúde Ocupacional
        '''''

        try:
            f1 = Funcionario(jsonQRCode)        
            if contador > 0: 
                Pdf.excluirPaginaPdf(listaArquivos, [contador-1])
                contador = 0
                listaArq = listaArquivos.replace('\\','\\\\')
                dirPdfGerado = diretorioPdfGerado.replace('\\','\\\\')
                querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId, json, ArquivoOriginal, ArquivoCortado) VALUES (3, 1, '{jsonQRCode[0]}', '{listaArq}', '{dirPdfGerado}')"
                database.InsertMysql(querySql)
                diretorioPdfGerado = ""
                
            if diretorioPdfGerado == "":
                nome, extensao = Arquivo.capturaNomeArquivo(listaArquivos)
                diretorioPdfGerado = f"Z:\Importacao - Robo\{f1.tipoArquivo}_{f1.codFuncionario}_{f1.codSequencialFicha}{dataAtual}{extensao}"
                #tipoFicha_codSequencial_data.pdf
            diretorioPdfGerado = Pdf.copiaPdf(listaArquivos, diretorioPdfGerado, contador)
            
            if quantidadePaginas == 1: #Verifica se e a ultima pagina do arquivo PDF
                Arquivo.copiaArquivo(listaArquivos, f'Z:\Importacao - Robo\{nome}_{dataAtual}{extensao}')
                listaArq = listaArquivos.replace('\\','\\\\')
                dirPdfGerado = diretorioPdfGerado.replace('\\','\\\\')
                querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId, json, ArquivoOriginal, ArquivoCortado) VALUES (3, 1, '{jsonQRCode[0]}', '{listaArq}', '{dirPdfGerado}')"
                database.InsertMysql(querySql)
                Arquivo.excluiArquivo(listaArquivos)
                break
            
            contador += 1

        except Exception as descricaoErro:
            if quantidadePaginas == 1:
                Arquivo.copiaArquivo(listaArquivos, f'Z:\Falha - Robo\{nome}_{dataAtual}{extensao}')
                listaArq = listaArquivos.replace('\\','\\\\')
                dirPdfGerado = diretorioPdfGerado.replace('\\','\\\\')
                querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId, json, ArquivoOriginal, ArquivoCortado) VALUES (4, 1, '', '{listaArq}', '{dirPdfGerado}')"
                logRoboId = database.InsertMysql(querySql)
                querySql = f"INSERT INTO logroboerros (DescricaoErro, LogRoboId) VALUES ('Arquivo sem QRCode', '{logRoboId}')"
                database.InsertMysql(querySql)
                Arquivo.excluiArquivo(listaArquivos)
                break
            if contador == 0:
                Arquivo.copiaArquivo(listaArquivos, f'Z:\Falha - Robo\{nome}_{dataAtual}{extensao}')
                listaArq = listaArquivos.replace('\\','\\\\')
                dirPdfGerado = diretorioPdfGerado.replace('\\','\\\\')
                querySql = f"INSERT INTO logRobos (StatusRoboId, RoboId, json, ArquivoOriginal, ArquivoCortado) VALUES (4, 1, '', '{listaArq}', '{dirPdfGerado}')"
                logRoboId = database.InsertMysql(querySql)
                querySql = f"INSERT INTO logroboerros (DescricaoErro, LogRoboId) VALUES ('Arquivo sem QRCode', '{logRoboId}')"
                database.InsertMysql(querySql)
                Arquivo.excluiArquivo(listaArquivos)
                break
            print(descricaoErro)            
            diretorioPdfGerado = Pdf.copiaPdf(listaArquivos, diretorioPdfGerado, contador)
            contador += 1
            continue