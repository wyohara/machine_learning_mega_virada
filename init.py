from libs.criar_ambiente_virtual import CriarAmbienteVirtual
from libs.machine_learning_mega import MachineLearningMega

resultado = []
tamanho_model = [6,10,16,20,50,60,76,100,150,200,250,500,600,750,1000]
def rodar_rede_neural():
    m = MachineLearningMega()

    for i in tamanho_model:
        if not m.carregar_rede_neural(nome_model=f"model_{i}.keras"):
            m.treinar_e_salvar_modelo(tamanho=i, nome_model=f"model_{i}.keras")
            print(">>>>não existe")
        else:
            resultado.append(m.usar_rede_neural())
    for i in resultado:
        print(i)

if __name__ == "__main__":
   # CriarAmbienteVirtual().salvar_requirements_pip()
    rodar_rede_neural()