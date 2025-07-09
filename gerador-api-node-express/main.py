from pathlib import Path
import os
import subprocess

# INSTALA O NODE VERSÃO 20 NA MÁQUINA
subprocess.run(f'''curl -sL https://deb.nodesource.com/setup_20.x -o /tmp/nodesource_setup.sh''', shell=True, check=True, executable='/bin/bash')
subprocess.run(f'''sudo bash /tmp/nodesource_setup.sh''', shell=True, check=True, executable='/bin/bash')
subprocess.run(f'''sudo apt install nodejs -y''', shell=True, check=True, executable='/bin/bash')

# INSTALA O NPM E O YARN
subprocess.run(f'''sudo npm install -g yarn''', shell=True, check=True, executable='/bin/bash')

# BUSCAR NOME DA PASTA DE USUÁRIO
diretorio_home = Path.home()
# ENTRAR NA PASTA DE USUÁRIO
os.chdir(diretorio_home)

# VARIAVÉL PARA DIRETÓRIO PADRÃO DOS PROJETOS
diretorio_projetos = f'{diretorio_home}/Projetos'

# VERIFICA SE EXISTE O DIRETÓRIO PADRÃO CASO NÃO ELE O CRIA
if os.path.exists(diretorio_projetos) == False:
    os.mkdir(diretorio_projetos)

# ENTRA NO DIRETÓRIO PADRÃO
os.chdir(diretorio_projetos)
dir_novo_projeto = 'api-alunos'
# VARIÁVEL COM O CAMINHO COMPLETO DO PROJETO A SER CRIADO
path_full_novo_projeto = f'{diretorio_projetos}/{dir_novo_projeto}'

# CASO NÃO EXISTA O DIRETÓRIO CRIA
if os.path.exists(path_full_novo_projeto) == False:
    os.mkdir(path_full_novo_projeto)
os.chdir(path_full_novo_projeto)

# CRIA O ARQUIVO package.json
subprocess.run(f'''yarn init -y''', shell=True, check=True, executable='/bin/bash')
subprocess.run(f'''yarn add express''', shell=True, check=True, executable='/bin/bash')
subprocess.run(f'''yarn add cors''', shell=True, check=True, executable='/bin/bash')
subprocess.run(f'''yarn add nodemon -D''', shell=True, check=True, executable='/bin/bash')