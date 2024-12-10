import csv
from datetime import datetime
import numpy as np
import os
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
from tensorflow.keras.models import load_model  # type: ignore # Importando a função load_model
import random


class Resultado:
    def __init__(self):
        self.concurso = ""
        self.data =""
        self.resultado = []


class MachineLearningMega():
    def __init__(self):
        self.__array_resultados = []
        self.__model = None
        self.__nome_model = "model.keras"
        self.__resultados_sorteio = []

        self.__gerar_array_dados()

    def __gerar_array_dados(self):
        """
        Lê o arquivo CSV e salva como array de resultados
        """
        arquivo = 'dados.csv'
        with open(arquivo, mode='r') as file:
            leitor_csv = csv.reader(file)
            for linha in leitor_csv:
                try:
                    r= Resultado()
                    r.concurso = int(linha[0])
                    r.data = datetime.strptime(linha[1], "%d/%m/%Y").date() 
                    r.resultado = sorted([
                        int(linha[2]),
                        int(linha[3]),
                        int(linha[4]),
                        int(linha[5]),
                        int(linha[6]),
                        int(linha[7]),
                    ])
                    self.__array_resultados.append(r)
                except Exception as e:
                    print(f'>>>>>>> Erro: {e} em {linha[1]}')
        
        # Extraindo os resultados
        self.__resultados_sorteio = [i.resultado for i in self.__array_resultados]  # Cada i.resultado é um array de 6 números
    
    def __definir_tamanho_dados(self, tamanho):
        if tamanho> len(self.__array_resultados):
            print(">>>>> tamanho maior que o conjunto de dados, ajustanto o tamanho.")
            tamanho = len(self.__array_resultados)
        if tamanho%2 == 1:            
            print(">>>>> o conjunto deve ser par, ajustando o tamanho.")
            tamanho = tamanho-1
        return tamanho

    def treinar_e_salvar_modelo(self, tamanho=100, epoch=100, nome_model="model_100.keras", salvar=False):
        """
        Treinamento da rede neural
        tamanho = por padrão só usa os 100 últimos resultados do arquivo CSV
        epoch = número de treinamentos. por padrão é 100
        """
        dados = self.__resultados_sorteio[:self.__definir_tamanho_dados(tamanho)]

        #Dividindo treino e previsão
        treino = int(len(dados)/2)
   
        X_train = np.array(dados[:treino])  # Entradas: primeiras 50% dos dados
        y_train = np.array(dados[treino:])  # Saídas: últimas 50% dos dados

        
        self.__criar_rede_neural()
        self.__nome_model = nome_model

        #Treinando o modelo e salvando uma cópia
        self.__model.fit(X_train, y_train, epochs=epoch, batch_size=1)
        
        if salvar: self.__model.save(self.__nome_model)

    def usar_rede_neural(self, concurso=None, valores=None):
        """
        Utiliza a rede neural para prever o resultado
        valores: valores de entrada para predizer, por padrão é None e carrega o ultimo resultado do arquivo CSV
        concurso: usa valores de um concurso especificado
        """
        entrada = self.__resultados_sorteio[0]
        if valores != None:
            print(f">>>> Testando com os valores: {valores}")
            entrada = valores
        else:
            if concurso == None:
                indice = random.randint(0,len(self.__resultados_sorteio)-1)
                entrada = self.__resultados_sorteio[indice]
                print(f">>>> Testando com o resultado do concurso: {self.__array_resultados[indice].concurso}")

            else:
                for i in self.__array_resultados:
                    if int(i.concurso) == int(concurso):
                        print(f">>>> Testando com o resultado do concurso: {i.concurso}")
                        entrada = i.resultado

        entrada = np.array(entrada).reshape(1, 6)  # Formatação correta para a entrada
    
        previsao = self.__model.predict(entrada)
        for i in range(len(previsao[0])): #converte para inteiro os resultados
            previsao[0][i]=int(previsao[0][i])
        return previsao[0]


    def __criar_rede_neural(self):
        """
        Cria a estrutura da rede neural e salva como self.__model
        """
        model = Sequential()
        model.add(Dense(64, input_dim=6, activation='relu'))  # Camada de entrada
        model.add(Dense(64, activation='relu'))  # Camada oculta
        model.add(Dense(6))  # Saída com 6 números (previsão de 6 números)

        # 4. Compilando o modelo
        model.compile(optimizer='adam', loss='mse')
        self.__model = model

    def carregar_rede_neural(self, nome_model = None):
        """
        Carrega a rede neural se existir
        """
        # Carregando o modelo            
        if os.path.exists(nome_model): # Verifica se o modelo existe
            self.__model = load_model(nome_model)
            return True
        else:
            print (f">>>> Rede neural salva não existe")
            return False
        
if __name__ == "__main__":
    m = MachineLearningMega()
    if not m.carregar_rede_neural(nome_model="model_200.keras"):
        m.treinar_e_salvar_modelo(tamanho=200, epoch=10000, nome_model="model_200.keras", salvar=True)
    print(m.usar_rede_neural())

    
