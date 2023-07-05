#Exemplo de codigo python para identificar as colunas de uma tabela em uma imagem
import cv2
import numpy as np

# Carrega a imagem da tabela
img = cv2.imread(r'diretorioDaImagem')

# Converte a imagem para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplica a detecção de bordas Canny
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Aplica a transformada de Hough para encontrar linhas
lines = cv2.HoughLinesP(edges, 1, cv2.PI/180, threshold=100, minLineLength=100, maxLineGap=10)

# Encontra as linhas verticais (correspondentes às colunas)
vertical_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    if abs(x2 - x1) < 10 and abs(y2 - y1) > 50:
        vertical_lines.append((x1, y1, x2, y2))

# Ordena as linhas verticais da esquerda para a direita
vertical_lines.sort()

# Imprime as coordenadas x dos pontos iniciais das colunas
for line in vertical_lines:
    x1, y1, x2, y2 = line
    print(x1)

# Desenha as linhas na imagem original
for line in vertical_lines:
    x1, y1, x2, y2 = line
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Exibe a imagem com as linhas desenhadas
cv2.imshow('Imagem com linhas detectadas', img)
cv2.waitKey(0)
cv2.destroyAllWindows()