import os
import subprocess
import sys
import re

def validate_mysql_user(user):
    if len(user) > 16:
        return "O nome de usuário deve ter no máximo 16 caracteres."
    if not re.match(r'^[a-zA-Z0-9_]+$', user):
        return "O nome de usuário só pode conter letras, números e underscores (_)."
    return None

def validate_mysql_password(password):
    if len(password) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    return None

def validate_mysql_db_name(db_name):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', db_name):
        return "O nome do banco de dados deve começar com uma letra e só pode conter letras, números e underscores (_)."
    return None

def run_command(command):
    """Run a shell command and print its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        exit(1)

def check_root():
    """Check if the script is running as root."""
    if os.geteuid() != 0:
        print("Este script precisa ser executado como root.")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)

def is_mysql_installed():
    """Check if MySQL Server is installed."""
    try:
        subprocess.run("mysql --version", shell=True, check=True, text=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def uninstall_mysql():
    """Uninstall MySQL Server completely."""
    print("Desinstalando o MySQL Server existente...")
    commands = [
        "sudo service mysql stop",
        "sudo apt purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-* -y",
        "sudo rm -rf /etc/mysql /var/lib/mysql",
        "sudo apt autoremove -y",
        "sudo apt autoclean"
    ]
    for command in commands:
        run_command(command)
    print("MySQL Server desinstalado com sucesso.")

def secure_mysql_with_expect(root_password):
    """Automate mysql_secure_installation using expect."""
    print("Configurando a segurança do MySQL com expect...")
    expect_script = f"""
    spawn sudo mysql_secure_installation
    expect "Press y|Y for Yes, any other key for No:"
    send "y\\r"
    expect "There are three levels of password validation policy:"
    send "0\\r"
    expect "New password:"
    send "{root_password}\\r"
    expect "Re-enter new password:"
    send "{root_password}\\r"
    expect "Remove anonymous users?"
    send "y\\r"
    expect "Disallow root login remotely?"
    send "y\\r"
    expect "Remove test database and access to it?"
    send "y\\r"
    expect "Reload privilege tables now?"
    send "y\\r"
    expect eof
    """
    with open("mysql_secure_installation.expect", "w") as f:
        f.write(expect_script)
    run_command("sudo apt install expect -y")
    run_command("expect mysql_secure_installation.expect")
    os.remove("mysql_secure_installation.expect")
    print("Configuração de segurança concluída.")

def main():
    check_root()

    # Verifica se o MySQL Server já está instalado
    if is_mysql_installed():
        print("O MySQL Server já está instalado no sistema.")
        choice = input("Deseja desinstalar o MySQL existente e instalar uma nova versão? (s/n): ").strip().lower()
        if choice == 's':
            uninstall_mysql()
        else:
            print("Encerrando o script.")
            exit(0)

    print("Iniciando a instalação e configuração do MySQL no WSL...")

    # Atualiza o sistema
    print("Atualizando o sistema...")
    run_command("sudo apt update && sudo apt upgrade -y")

    # Instala o MySQL Server
    print("Instalando o MySQL Server...")
    run_command("sudo apt install mysql-server -y")

    # Inicializa o serviço MySQL
    print("Iniciando o serviço MySQL...")
    run_command("sudo service mysql start")

    # Configurações de segurança do MySQL
    # root_password = input("Digite a senha para o usuário root do MySQL: ")
    root_password = 'Senac@123'
    secure_mysql_with_expect(root_password)

    # Solicita informações do usuário
    # db_user = input("Digite o nome do usuário para o banco de dados: ")
    db_user = 'user_app'
    while True:
        # db_user = input("Digite o nome do usuário para o banco de dados: ").strip()
        error = validate_mysql_user(db_user)
        if error:
            print(f"Erro: {error}")
        else:
            break
    # db_password = input("Digite a senha para o usuário: ")
    db_password = 'Senha@123'
    while True:
        # db_password = input("Digite a senha para o usuário: ").strip()
        error = validate_mysql_password(db_password)
        if error:
            print(f"Erro: {error}")
        else:
            break
    # db_name = input("Digite o nome do banco de dados: ")
    db_name = 'db_app'
    while True:
        # db_name = input("Digite o nome do banco de dados: ").strip()
        error = validate_mysql_db_name(db_name)
        if error:
            print(f"Erro: {error}")
        else:
            break

    # Configura o MySQL para permitir conexões externas
    print("Configurando o MySQL para permitir conexões externas...")
    run_command("sudo sed -i 's/bind-address\\s*=\\s*127.0.0.1/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf")
    run_command("sudo service mysql restart")

    # Cria o banco de dados e o usuário, e concede privilégios
    print("Criando banco de dados, usuário e concedendo privilégios...")
    mysql_commands = f"""
    sudo mysql -e "CREATE DATABASE {db_name};"
    sudo mysql -e "CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';"
    sudo mysql -e "GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';"
    sudo mysql -e "FLUSH PRIVILEGES;"
    """
    run_command(mysql_commands)

    print("Configuração concluída com sucesso!")

if __name__ == "__main__":
    main()