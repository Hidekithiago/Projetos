#pip3 install psutil install pyautogui install pygetwindow
##############################| IMPORTACAO DE BIBLIOTECAS |##############################
import os, io, sys
import time
import pyautogui
import pygetwindow as gw
import psutil as ps
import BancoDados

def IniciaPowerAutomate(atalho):
    print('Finalizando o programa PowerAutomate')
    os.system("taskkill /F /im chrome.exe")
    os.system("taskkill /F /im PAD.Console.Host.exe")
    os.system("taskkill /F /im PAD.Robot.exe")
    time.sleep(2)
    os.startfile("C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe")
    for x in range(60,-1,-1):
        print(f'Iniciando em {x} segundo(s)')
        time.sleep(1)
    
    print(gw.getAllTitles())
    chroWindow = gw.getWindowsWithTitle('Power Automate')[0]
    time.sleep(2)
    chroWindow.restore()    
    time.sleep(1)
    chroWindow.maximize()

    time.sleep(4)
    pyautogui.FAILSAFE = False
    pyautogui.press(atalho)
    
if __name__ == "__main__":
    database = BancoDados.SqlServer()
    database.connect(BancoDados.mysql_homologSqlServer)
    result = database.VerificaUltimaExecucaoRobo()
    if result >= 1:
        print('Aguardando para reinicio do processo')
        IniciaPowerAutomate('F8')