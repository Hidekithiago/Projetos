import cv2
from pyzbar import pyzbar
import re
import tkinter as tk
from tkinter import filedialog

# Inicializa a câmera
cap = cv2.VideoCapture(0)

def ler_qrcode_imagem(caminho_imagem):
    """Lê um QR Code de uma imagem e retorna os dados."""
    imagem = cv2.imread(caminho_imagem)
    decoded_objects = pyzbar.decode(imagem)

    if not decoded_objects:
        return None  # QR Code não encontrado

    data = decoded_objects[0].data.decode()
    print(data)
    # Aplica a expressão regular para extrair NF e preço (se necessário)
    match = re.search(r'(.+?)\|(.+?)\|(.+)', data)
    print(match)
    if match:
        nf = match.group(1)
        data = match.group(2)
        preco = match.group(3)
        return nf, data, preco
    else:
        return data  # Retorna os dados brutos se não houver correspondência

def selecionar_imagem():
    """Abre uma janela de diálogo para selecionar a imagem."""
    root = tk.Tk()
    root.withdraw()

    caminho_imagem = filedialog.askopenfilename(
        initialdir="/",
        title="Selecione uma imagem",
        filetypes=(("Arquivos de imagem", "*.jpg *.jpeg *.png *.gif"), ("todos os arquivos", "*.*"))
    )

    if caminho_imagem:
        resultado = ler_qrcode_imagem(caminho_imagem)
        if resultado:
            if isinstance(resultado, tuple):
                nf, data, preco = resultado
                print("NF:", nf)
                print("Data:", data)
                print("Preço:", preco)
            else:
                print("Dados do QR Code:", resultado)
        else:
            print("QR Code não encontrado na imagem.")

while True:
    # Captura o frame da câmera
    _, frame = cap.read()

    # Decodifica os QR Codes no frame
    decoded_objects = pyzbar.decode(frame)

    # Processa os QR Codes decodificados
    for obj in decoded_objects:
        data = obj.data.decode()
        print(data)
        # Aplica a expressão regular para extrair NF, data e preço
        match = re.search(r'(.+?)\|(.+?)\|(.+)', data)
        print(match)
        if match:
            nf = match.group(1)
            data = match.group(2)
            preco = match.group(3)
            print("NF:", nf)
            print("Preço:", preco)
            print("Data:", data)
        else:
            print("Formato de dados do QR Code não reconhecido.")

    # Exibe o frame com os QR Codes detectados (opcional)
    cv2.imshow("QR Code Scanner", frame)

    # Sai do loop ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Verifica se a tecla 'i' foi pressionada para ler QR Code de uma imagem
    if cv2.waitKey(1) & 0xFF == ord('i'):
        selecionar_imagem()

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
