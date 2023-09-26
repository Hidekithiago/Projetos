import BancoDados as bd
import Arquivo
import json
import os
import re

database = bd.Mysql()
database.connect(bd.mysql_homolog)

querySql = f"Select json, ArquivoCortado, logroboId from logRobos where StatusRoboId <> 4 and Json <>'' and integracao = 0" #60 107
arquivos = database.selectMysql(querySql)
for row in arquivos:
    if re.findall(r'"0"', row[0]): 
        dict = row[0].replace('"0"','"codEmpresa"').replace('"1"','"codFuncionario"').replace('"7"','"codSequencialFicha"').replace('}',f', "nomeArquivo":"{row[1]}"'+"}")
    else:
        dict = row[0].replace('"tipo_doc"','"tipoFicha"').replace('"seq_ficha"','"codTipoFicha"').replace('"cod_empresa"','"codEmpresa"').replace('"cod_funcionario"','"codFuncionario"').replace('}',f', "nomeArquivo":"{row[1]}"'+"}")
        dict = re.sub(r'":\s(?=\w)', '":"', dict)
        dict = re.sub(r'(?<=\w),\s', '", ', dict)
    Arquivo.criarArquivo(r'C:\GitHub\Grs\Script\Importacao\json.txt', dict)
    execucaoJava = os.popen(f'java -jar "C:\GitHub\Grs\SocGed\SocGed_UploadArquivos\dist\JavaApplication1.jar"').read()
    print(execucaoJava)
    if r'Upload n?o realizado' in execucaoJava or r'An error occurred.' in execucaoJava or r'ERRO DE WS SECURITY' in execucaoJava:
        database.updateTable('logRobos', row[2], 'StatusRoboId', '4', 'Integracao', '1')
        execucaoJava = execucaoJava.replace('\'', '')
        querySql = f"INSERT INTO logroboerros (DescricaoErro, LogRoboId) VALUES ('{execucaoJava}', '{row[2]}')"
        database.InsertMysql(querySql)
    else:
        database.updateTable('logRobos', row[2], 'StatusRoboId', '3', 'Integracao', '1')