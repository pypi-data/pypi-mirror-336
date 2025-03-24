import os
import requests
import hashlib
import webbrowser
import json

# URLs do servidor
BASE_URL_FLASK = "http://cstore.servehttp.com:8080"  # URL do Flask
BASE_URL_HTTP = "http://cstore.servehttp.com:5060"  # URL do servidor HTTP

# Arquivo para armazenar as credenciais
CREDENTIALS_FILE = "credentials.txt"

# Variáveis globais para armazenar as credenciais
USER_EMAIL = ""
USER_PASSWORD = ""

def load_credentials():
    global USER_EMAIL, USER_PASSWORD
    USER_EMAIL = ""  # Reseta as credenciais
    USER_PASSWORD = ""
    
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                credentials = f.read().strip().split('\n')
                
                # Verifica se há exatamente 2 linhas não vazias
                if len(credentials) == 2 and credentials[0].strip() != "" and credentials[1].strip() != "":
                    USER_EMAIL = credentials[0].strip()
                    USER_PASSWORD = credentials[1].strip()
                    print("✅ Credenciais carregadas com sucesso!")
                else:
                    print("⚠️ Arquivo de credenciais inválido ou incompleto. Ignorando...")
        except Exception as e:
            print(f"⚠️ Erro ao ler arquivo de credenciais: {e}")
    else:
        print("⚠️ Nenhum arquivo de credenciais encontrado.")

def save_credentials():
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f"{USER_EMAIL}\n{USER_PASSWORD}")
    print("✅ Credenciais salvas com sucesso!")

def create_account():
    print("🔍 Abrindo o navegador para criar uma conta...")
    webbrowser.open(f"{BASE_URL_FLASK}/register")
    input("Após criar sua conta, pressione Enter para continuar...")

def login():
    global USER_EMAIL, USER_PASSWORD
    
    # Se já houver credenciais carregadas, tenta usá-las
    if USER_EMAIL and USER_PASSWORD:
        password_hash = hashlib.sha256(USER_PASSWORD.encode("utf-8")).hexdigest()
        try:
            response = requests.post(f"{BASE_URL_HTTP}/login", json={
                "email": USER_EMAIL,
                "password": password_hash
            })
            if response.status_code == 200 and response.json().get("result") == "1":
                print("✅ Login automático realizado com sucesso!")
                return
            else:
                print("❌ Login automático falhou. Por favor, faça login manualmente.")
        except Exception as e:
            print(f"❌ Erro durante o login automático: {e}")

    # Se não houver credenciais válidas, pede ao usuário
    email = input("Digite seu email: ").strip()
    password = input("Digite sua senha: ").strip()
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    try:
        response = requests.post(f"{BASE_URL_HTTP}/login", json={
            "email": email,
            "password": password_hash
        })
        if response.status_code == 200 and response.json().get("result") == "1":
            USER_EMAIL = email
            USER_PASSWORD = password
            save_credentials()
            print("✅ Login realizado com sucesso!")
        else:
            print("❌ Erro no login: Credenciais inválidas.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def download():
    if not USER_EMAIL or not USER_PASSWORD:
        print("❌ Você precisa fazer login primeiro!")
        return

    library_name = input("Digite o nome da biblioteca para baixar: ").strip()
    output_path = os.path.join(os.getcwd(), f"{library_name}.zip")

    if os.path.exists(output_path):
        print(f"⚠️ O arquivo {output_path} já existe. Deseja sobrescrevê-lo? (s/n)")
        overwrite = input().strip().lower()
        if overwrite != 's':
            print("❌ Download cancelado.")
            return

    try:
        response = requests.get(f"{BASE_URL_HTTP}/download/{library_name}", stream=True)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"✅ Download completo! Arquivo salvo em {output_path}")
        else:
            print("❌ Erro no download:", response.json().get("error", "Erro desconhecido"))
    except requests.ConnectionError:
        print("❌ Não foi possível conectar ao servidor.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def search():
    query = input("Digite o termo de pesquisa: ").strip()
    try:
        response = requests.get(f"{BASE_URL_HTTP}/search?q={query}")

        if response.status_code == 200:
            results = response.json()
            if results:
                print("📂 Resultados encontrados:")
                for folder, files in results.items():
                    print(f"\n📁 Pasta: {folder}")
                    for file in files:
                        print(f"  - {file}")
            else:
                print("📂 Nenhum resultado encontrado.")
        else:
            print("❌ Erro na pesquisa:", response.json().get("error", "Erro desconhecido"))
    except requests.ConnectionError:
        print("❌ Não foi possível conectar ao servidor.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def upload():
    print("⚠️ Função de upload ainda não implementada.")

def main():
    load_credentials()
    while True:
        print("\nComandos disponíveis: create_account, login, upload, download, search, exit")
        command = input("Digite o comando: ").strip().lower()

        if command == "create_account":
            create_account()
        elif command == "login":
            login()
        elif command == "upload":
            upload()
        elif command == "download":
            download()
        elif command == "search":
            search()
        elif command == "exit":
            print("Saindo...")
            break
        else:
            print("❌ Comando inválido. Tente novamente.")

if __name__ == "__main__":
    main()