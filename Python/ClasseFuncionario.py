import json

class Funcionario():
    def __init__(self, list) -> None:        
        jsonQRCode = json.loads(list[0])
        print(jsonQRCode)
        try:
            self.codEmpresa = jsonQRCode['0']
            self.codFuncionario = jsonQRCode['1']
            self.codSequencialFicha = jsonQRCode['7']
            self.tipoArquivo = jsonQRCode['99']
        except:
            self.codEmpresa = jsonQRCode['cod_empresa']
            self.codFuncionario = jsonQRCode['cod_funcionario']
            self.codSequencialFicha = jsonQRCode['seq_ficha']
            self.tipoArquivo = jsonQRCode['tipo_doc']
        
        if self.tipoArquivo == '6':
            self.tipoArquivo = 'ASO'
        elif self.tipoArquivo == '9':
            self.tipoArquivo = 'FC'
            
    def mostraDadosObjeto(self):
        print(f'Codigo Empresa {self.codEmpresa}')
        
        print(f'Codigo Empresa {self.codFuncionario}')
        print(f'Codigo Empresa {self.codSequencialFicha}')
        print(f'Codigo Empresa {self.tipoArquivo}')