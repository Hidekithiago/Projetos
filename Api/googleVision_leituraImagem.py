import os, io, sys
from pathlib import Path
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict
from pdf2image import convert_from_path
import json
import re
from PIL import Image


def OcrImagem():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =credenciaisGoogleVision
    client = vision.ImageAnnotatorClient()
    with io.open(diretorioNomeArquivo+'.png', 'rb') as image_file:    
        content = image_file.read()
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    print(texts)
    with open(diretorioNomeArquivo+'.txt', 'a', encoding="utf-8") as file:
            file.write(str(texts))
    for text in texts:
        if(len(text.description) < 200):            
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])            
        print(text.description)
        with open(diretorioNomeArquivo+'.txt', 'a', encoding="utf-8") as file:
            file.write(text.description)
        
def verificaPDF():    
    print(f'Verificando se o arquivo é um PDF')
    path = Path(diretorioPdf)
    arqExtensao = path.suffix    
    if arqExtensao ==".pdf":       
        arqnome = os.path.splitext(os.path.basename(path.name))[0]        
        convertPDF()
    OcrImagem()
        
def convertPDF():
    print(f'Convertendo PDF{diretorioPdf}')
    pages = convert_from_path(diretorioPdf, 100,poppler_path=r'C:\poppler-0.68.0\bin')
    for page in pages:
        page.save(diretorioNomeArquivo+'.jpeg', 'JPEG')
        
        size = 1050, 1490
        im = Image.open(diretorioNomeArquivo+'.jpeg')
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(diretorioNomeArquivo+'.png', "PNG")
        break   
        
if __name__ == "__main__":
    #Para Windows Instalar o Poopler pelo site https://github.com/oschwartz10612/poppler-windows/releases
    #Alterar a linha 43 para o diretorio onde instalou o poopler
    diretorioPasta = f"C:\diretorio\pasta"
    nomeArquivo = f'nomeArquivo'
    extensaoArquivo = '.pdf'
    credenciaisGoogleVision = f'{diretorioPasta}\\credenciaisGoogleVision.json'
    diretorioPdf = f'{diretorioPasta}\\{nomeArquivo}{extensaoArquivo}'
    diretorioNomeArquivo = f'{diretorioPasta}\\{nomeArquivo}'
    verificaPDF()
