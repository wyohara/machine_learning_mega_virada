import os
import venv
import subprocess
"""
Codo inicial da inicialização do pip

Willian Ohara em 3/11/2024
"""

class CriarAmbienteVirtual:
    def __init__(self, nome_env="venv", requirements_txt="req.txt"):
        """Inicializa a classe com o nome do ambiente virtual e o arquivo de requisitos."""
        self.__nome_env = nome_env
        self.__req_txt = requirements_txt
    
    def existe_ambiente_virtual(self):
        """Verifica se o ambiente virtual existe"""
        if os.path.exists(self.__nome_env): # Verifica se o ambiente virtual já existe
            return True
        else:
            return False


    def cria_virtualenv(self):
        """Cria um ambiente virtual e instala as dependências especificadas."""
        
        if self.existe_ambiente_virtual():
            print(f"O ambiente virtual '{self.__nome_env}' já existe.")
        else:
            try:
                venv.create(self.__nome_env, with_pip=True)
                print(f"Ambiente virtual '{self.__nome_env}' criado com sucesso!")

            except Exception as e:
                print(f"Ocorreu um erro ao criar o ambiente virtual: {e}")

        self.__instalar_dependencias()
        self.__exibir_instrucoes_venv()
    
    def __instalar_dependencias(self):
        """Instala as dependências especificadas no arquivo requirements.txt."""

        req_txt_path = os.path.join(os.getcwd(), self.__req_txt)
        if os.path.isfile(req_txt_path): # Define o caminho para o executável pip dependendo do sistema operacional
            if os.name == "nt":  # Windows
                pip_executable = os.path.join(self.__nome_env, "Scripts", "pip")
            else:  # macOS/Linux
                pip_executable = os.path.join(self.__nome_env, "bin", "pip")

            try: 
                # Comando para instalar dependências
                subprocess.check_call([pip_executable, "install", "-r", ])
                print("Dependências instaladas com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"Ocorreu um erro ao instalar as dependências: {e}")
        else:
            print(f"O arquivo {self.__req_txt} não foi encontrado.")

    def salvar_requirements_pip(self):
        """Executa o comando pip freeze e salva a saída no arquivo req.txt."""
        with open(self.__req_txt, 'w') as req:
            subprocess.run(['pip', 'freeze'], stdout=req)
            print(f"Dependências salvas em {self.__req_txt}.")

    def __exibir_instrucoes_venv(self):
        """Exibe instruções para ativar o ambiente virtual."""
        if os.name == "nt":  # Windows
            #comando = f"{os.getcwd()}\\{self.__nome_env}\\Scripts\\activate"
            comando = f"{self.__nome_env}\\Scripts\\activate"
            
        else:  # macOS/Linux
            comando = f"source {self.__nome_env}/bin/activate"
        
        print(f"Para ativar o ambiente virtual, execute: {comando}")
        print(f"Para acessar o diretório do arquivo: cd {os.getcwd()}")
        print("Para iniciar o shell: python -m idlelib.idle")



if __name__ == "__main__":
    env = CriarAmbienteVirtual()
    print(env.existe_ambiente_virtual())
    env.cria_virtualenv()

    #env.salvar_requirements_pip()
