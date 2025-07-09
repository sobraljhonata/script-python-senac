import os
import subprocess
import shutil
import sys

def run_command(command):
    """Executa um comando no terminal e exibe a saída."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {command}\nCódigo de saída: {e.returncode}\nMensagem: {e}")
        sys.exit(1)  # Encerra o script em caso de erro crítico

def is_command_available(command):
    """Verifica se um comando está disponível no sistema."""
    return shutil.which(command) is not None

def get_node_version():
    """Obtém a versão do Node.js instalada."""
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True, check=True)
        return result.stdout.strip().lstrip("v")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar a versão do Node.js: {e}")
        return None

def main():
    try:
        # Atualizar todos os pacotes do Linux
        print("Atualizando pacotes do sistema...")
        run_command("sudo apt-get update -y && sudo apt-get upgrade -y")

        # Verificar se o Python 3 está instalado
        print("Verificando se o Python 3 está instalado...")
        if not is_command_available("python3"):
            print("Python 3 não encontrado. Instalando...")
            run_command("sudo apt-get install -y python3")
        else:
            print("Python 3 já está instalado.")

        # Verificar se o arquivo .bash_aliases existe, caso contrário, criar
        bash_aliases_path = os.path.expanduser("~/.bash_aliases")
        if not os.path.isfile(bash_aliases_path):
            print("Arquivo .bash_aliases não encontrado. Criando...")
            with open(bash_aliases_path, "w") as f:
                pass
        else:
            print("Arquivo .bash_aliases já existe.")

        # Criar um alias para python3 com o nome python
        with open(bash_aliases_path, "r") as f:
            aliases = f.read()
        if "alias python=" not in aliases:
            print("Criando alias para python3...")
            with open(bash_aliases_path, "a") as f:
                f.write("alias python='python3'\n")
            print("Alias criado. Execute 'source ~/.bash_aliases' para aplicar.")
        else:
            print("Alias para python3 já existe.")

        # Verificar se o Node.js está instalado e com versão >= 22
        print("Verificando se o Node.js está instalado...")
        if is_command_available("node"):
            node_version = get_node_version()
            if node_version:
                try:
                    major_version = int(node_version.split(".")[0])
                    if major_version < 22:
                        print(f"Node.js versão {node_version} encontrada. Atualizando para a versão 22 ou superior...")
                        run_command("sudo apt-get remove -y nodejs")
                        run_command("curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -")
                        run_command("sudo apt-get install -y nodejs")
                    else:
                        print(f"Node.js já está na versão {node_version}.")
                except ValueError:
                    print(f"Erro ao interpretar a versão do Node.js: {node_version}")
                    sys.exit(1)
        else:
            print("Node.js não encontrado. Instalando a versão 22 ou superior...")
            run_command("curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -")
            run_command("sudo apt-get install -y nodejs")

        print("Setup concluído!")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()