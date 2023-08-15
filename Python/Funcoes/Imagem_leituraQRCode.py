from PIL import Image
from pyzbar.pyzbar import decode

def ler_qrcode(imagem):
    img = Image.open(imagem)
    qr_codes = decode(img)
    
    if qr_codes:
        for qr_code in qr_codes:
            dados = qr_code.data.decode('utf-8')
            print("QR Code encontrado:", dados)
    else:
        print("Nenhum QR Code encontrado na imagem.")

# Chame a função com o caminho da imagem contendo o QR Code
ler_qrcode(r"frame (3).png")
