# -*- coding: utf-8 -*-
#pip3 install mysql-connector-python==8.0.21

import os, io, sys, time
from datetime import datetime, timedelta
#################### MYSQL ####################
import socket
import mysql.connector as mysql
from mysql.connector import errorcode


def limpaArquivos():#################### Exclui os arquivos com mais de 90 dias ####################        
    path = "/home/quaestum/atestados_storage/temp"
    files = os.listdir(path)    

    for filename in files:            
        try: 
            fullPatch = path+"/"+filename
            modification_time = os.path.getmtime(fullPatch)#Verifica a ultima data de que teve alteracao
            modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modification_time))#Converte o resultado em segundos para data no formato selecionado
            date_time_obj = datetime.strptime(modificationTime, '%Y-%m-%d %H:%M:%S')#Converte o resultado em string para data

            today = datetime.today()#Verifica a data atual
            #print(date_time_obj,  today - timedelta(days=90)) #Subtrai 90 dias da data


            if(date_time_obj < today - timedelta(days=90)): #Subtrai 90 dias da data e compara com a data da ultima modificacao
                print(fullPatch)
                if os.path.exists(fullPatch):
                    os.remove(fullPatch)
            else:
                pass
        except OSError: 
            print("Path '%s' does not exists or is inaccessible" %fullPatch) 
            sys.exit()
    print("Limpou a pasta /home/quaestum/atestados_storage/temp")
    
if __name__ == "__main__":
    try: 
        limpaArquivos()
    except:
        print(str(sys.exc_info()))
        pass