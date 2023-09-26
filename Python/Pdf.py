#pip3 install PyMuPDF install opencv-python

import fitz 
import cv2
import os

from PyPDF2 import PdfReader, PdfWriter
from copy import copy

def capturaPaginaPdf(diretorioPdf, numeroPagina, zoom = 1.5):
    reader = PdfReader(diretorioPdf)
    page = reader.pages[numeroPagina]
    count = 0
    nomeArquivo = ""
    for image_file_object in page.images:
        nomeArquivo = str(count) + image_file_object.name
        with open(nomeArquivo, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1
    img = cv2.imread(nomeArquivo)
    img = cv2.resize(img, (0,0), fx=zoom, fy=zoom)    
    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
    os.remove(nomeArquivo)
    return decoded_info

def excluirPaginaPdf(diretorioPdf, paginasDeletar = []):
    for x in range(paginasDeletar[0],-1,-1):
        paginasDeletar.append(x)
    infile = PdfReader(diretorioPdf)
    output = PdfWriter()

    for i in range(0,len(infile.pages),1):
        if i not in paginasDeletar:
            p = infile.pages[i]
            output.add_page(p)

    with open(diretorioPdf, 'wb') as f:
        output.write(f)

def quantidadePaginasPdf(diretorioPdf):
    reader = PdfReader(diretorioPdf)
    return len(reader.pages)


def copiaPdf(diretorioPdfOriginal, diretorioPdfGerado, quantidadePaginas = 1):
    try:
        output = PdfWriter(open(diretorioPdfGerado, "rb"))
    except:
        output = PdfWriter()
    reader = PdfReader(open(diretorioPdfOriginal, "rb"))
    with open(diretorioPdfGerado, "wb") as outputStream:    
        for x in range(quantidadePaginas+1):
            page = reader.pages[x]
            x = copy(page)
            output.add_page(x)
        output.write(outputStream)
        outputStream.close()
        output.close()
        reader.stream.close()
    return diretorioPdfGerado