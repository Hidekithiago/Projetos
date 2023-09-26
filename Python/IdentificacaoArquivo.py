import os, io, sys
import re
import json
from unidecode import unidecode
import pdfplumber
import mysql.connector
from pdf2image import convert_from_path
from google.cloud import vision
from google.cloud.vision_v1 import types
from pathlib import Path
from PIL import Image
import cv2
import numpy as np

'''mydb = mysql.connector.connect(
        host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com",
        user="sys.perdcompdev",
        password="nS8454s@$a",
        database="perdcompdev"
)
mycursor = mydb.cursor()'''



def convertPDF(dirPDF, dirPastaPDF):
    global quantidadePaginasPdf;
    pages = convert_from_path(dirPDF,100,poppler_path=r'C:\quaestum\poppler\bin')
    quantidadePaginasPdf = len(pages)
    for c in range(quantidadePaginasPdf):
        pages[c].save(diretorioPngArquivoSemExtensao+str(f'{c}.png'), 'PNG')
   
    size = 1050, 1490
    for c in range(quantidadePaginasPdf):
        im = Image.open(diretorioPngArquivoSemExtensao+str(f'{c}.png'))
    
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(diretorioPngArquivo, "PNG")
    
def OCR_Imagem():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\quaestum\robos\visionapi-manserv-681136a258f6.json'
    client = vision.ImageAnnotatorClient()
    
    for c in range(quantidadePaginasPdf):
        diretorioPngArquivo = diretorioPngArquivoSemExtensao+str(f'{c}.png')
        diretorioTxtArquivo = diretorioPngArquivoSemExtensao+str(f'{c}.txt')
        '''
        with io.open(diretorioPngArquivo, 'rb') as image_file:
            
            content = image_file.read()

        image = types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        for text in texts:
            print(text)
        with open(diretorioTxtArquivo, 'w', encoding='ascii') as file:        
            file.write(str(texts))
        '''
        
        
        with open(diretorioTxtArquivo, 'r') as file:
            data = file.read()
            text = data
        pattern = r'description: "(.*)"\nbounding_poly \{\n\s\svertices\s\{\n\s{4}x:\s(\d+)\n\s{4}y:\s(\d+)\n\s\s\}\n\s\svertices\s\{\n\s{4}x:\s(\d+)\n\s{4}y:\s(\d+)\n\s\s\}\n\s\svertices\s\{\n\s{4}x:\s(\d+)\n\s{4}y:\s(\d+)\n\s\s\}\n\s\svertices\s\{\n\s{4}x:\s(\d+)\n\s{4}y:\s(\d+)'

        verticesBL = re.findall(pattern, text)


        palavras = []

        for item in verticesBL:
            palavras.append({"text": item[0], "x1": int(item[1]), "y1": int(item[2]), "x2": int(item[5]), "y2": int(item[6])})
        
        palavraAso = ['ASO - ATESTADO DE SA', 'ASO ATESTADO DE SA']
        for x in palavraAso:
            fonteArquivo = re.findall(x.lower(), text.lower())    
        
            if (len(fonteArquivo) > 0):
                del palavras[0]
                BuscaAso(palavras)


def BuscaAso(palavras):
    nomeFuncionario = ''
    for palavra in palavras:
        if 'Funcion\\303\\241rio'.lower() in palavra["text"].lower():
            x1Funcionario = palavra["x1"]
            y1Funcionario = palavra["y1"]
            for palavra in palavras:                
                if palavra["y1"] > (y1Funcionario + 10) and palavra["y1"] < (y1Funcionario + 28) and palavra["x1"] > 100 and palavra["x1"] < 410:
                    nomeFuncionario = nomeFuncionario + " " +palavra["text"]
                    x1CodigoRetencao = palavra["x1"]
                    y1CodigoRetencao = palavra["y1"]
                
                
            break
                
    desnivelCodigoRetencao = y1Funcionario - (y1CodigoRetencao - desnivelDefault) #A palavra Retenção está abaixo do mês
    desnivelRendimento = y1Funcionario - (y1Rendimento + desnivelDefault)
    desnivelImposto = y1Funcionario - (y1Imposto + desnivelDefault)
                
    print(f'\n\n\nPosicao encontrada da palavra mes {x1Funcionario} {y1Funcionario}')
    valores = texto_da_regiao({"x1":0, "y1":y1Funcionario, "x2":x1Funcionario+1000, "y2":y1Funcionario+400})
    print(valores)
            
if __name__ == "__main__":    
    quantidadePaginasPdf = 0
    diretorioPdfArquivo = r"C:\quaestum\capturaGrs\PAULO CESAR DE JESUS.pdf"
    
    local = 'C:\\quaestum\\capturaGrs'
    path = Path(diretorioPdfArquivo)
    nomeArquivo = os.path.splitext(os.path.basename(path.name))[0]
    diretorioPngArquivoSemExtensao = local + '\\' + str(nomeArquivo)
    diretorioPngArquivo = local + '\\' + str(nomeArquivo) + '.png'
    diretorioTxtArquivo = local + '\\' + str(nomeArquivo) + '.txt'
    
    path = Path(diretorioPdfArquivo)
    convertPDF(path, local)
    OCR_Imagem()
    