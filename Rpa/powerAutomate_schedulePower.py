#pip3 install psutil install pyautogui
##############################| IMPORTACAO DE BIBLIOTECAS |##############################

import os, io, sys
import time
import pyautogui
import pygetwindow as gw
import psutil as ps

def startPower(nomeRobo, contaPremium):
    premium = 0
    if contaPremium == 'nao': premium = 1        
    time.sleep(5)
    print('Finalizando o programa PowerAutomate')
    os.system("taskkill /F /im chrome.exe")
    os.system("taskkill /F /im PAD.Console.Host.exe")
    os.system("taskkill /F /im PAD.Robot.exe")
    time.sleep(2)
    print('Iniciando o Power Automate')
    os.startfile("C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe")
    time.sleep(20)
    
    print(gw.getAllTitles())
    chroWindow = gw.getWindowsWithTitle('Power Automate')[0]
    time.sleep(1)
    chroWindow.minimize()
    time.sleep(1)
    chroWindow.maximize()    

    time.sleep(4)
    #Caso não exista a opção "Go Premium" no PowerAutomate, utilizar 11 "TABs", caso contrario utilizar 12 
    for x in range(11+int(premium)):        
        pyautogui.press("tab")
    time.sleep(2)    
    for x in range(6):
        pyautogui.press("pagedown")
    time.sleep(3)
    for x in range(10+int(premium)):
        pyautogui.press("tab")
    time.sleep(2)
    pyautogui.write(nomeRobo)
    for x in range(6):
        pyautogui.press("tab")
    pyautogui.press("right")
    pyautogui.press("up")
    for x in range(3):
        pyautogui.press("tab")
    pyautogui.press("enter")

    time.sleep(30)
    for proc in ps.process_iter():
        info = proc.as_dict(attrs=['pid', 'name'])        
        if info['name'] == 'PAD.Robot.exe':            
            sys.exit()
    startPower(nomeRobo)

if __name__ == "__main__":
    print('Aguardando para reinicio do processo')
    #time.sleep(3600) #Tempo definido com o cliente e de 10800(3 horas) 3600(1 Hora)
    #Caso for uma conta do powerAutomate paga mensalmente digitar "sim" caso contrario digite "nao"
    startPower("NotasDespesas", "nao")    
    
