import ftplib
import os
import zipfile

# Função para baixar arquivos de um diretório no FTP
def download_arquivos_ftp(ftp, diretorio, destino_local, extensao='.zip'):
    try:
        # Muda para o diretório desejado no FTP
        ftp.cwd(diretorio)

        # Lista os arquivos no diretório
        arquivos = ftp.nlst()

        # Cria o diretório local se não existir
        if not os.path.exists(destino_local):
            os.makedirs(destino_local)

        # Baixar os arquivos
        for arquivo in arquivos:
            # Verifica se e o arquivo certo
            if arquivo.endswith(extensao):
                local_path = os.path.join(destino_local, arquivo)
                print(f"Baixando {arquivo} para {local_path}...")
                with open(local_path, 'wb') as f:
                    ftp.retrbinary(f"RETR {arquivo}", f.write)
                print(f"Arquivo {arquivo} baixado com sucesso!")

                # Extrair o arquivo ZIP
                if arquivo.endswith('.zip'):
                    extrair_arquivo_zip(local_path, destino_local)

    except Exception as e:
        print(f"Erro ao baixar arquivos de {diretorio}: {e}")

# Função para extrair arquivos ZIP
def extrair_arquivo_zip(caminho_arquivo_zip, destino_local):
    try:
        # Abre o arquivo ZIP
        with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
            # Extrai todos os arquivos no diretório destino
            zip_ref.extractall(destino_local)
            print(f"Arquivo ZIP {caminho_arquivo_zip} extraído com sucesso!")
        # Apaga o arquivo ZIP após extração
        os.remove(caminho_arquivo_zip)
        print(f"Arquivo ZIP {caminho_arquivo_zip} deletado após extração.")
    except Exception as e:
        print(f"Erro ao extrair o arquivo ZIP {caminho_arquivo_zip}: {e}")

# Função para baixar os arquivos de demonstrações contábeis de 2023 e 2024
def baixar_demonstracoes_contabeis(ftp):
    # Diretórios FTP de demonstrações contábeis para 2023 e 2024
    base_demonstracoes_contabeis_2023 = '/FTP/PDA/demonstracoes_contabeis/2023/'
    base_demonstracoes_contabeis_2024 = '/FTP/PDA/demonstracoes_contabeis/2024/'

    # Diretórios locais para armazenar os arquivos
    diretorio_local_2023 = './demonstracoes_contabeis/2023/'
    diretorio_local_2024 = './demonstracoes_contabeis/2024/'

    # Baixar os arquivos de demonstrações contábeis de 2023
    print("\nBaixando os arquivos de demonstrações contábeis de 2023...")
    download_arquivos_ftp(ftp, base_demonstracoes_contabeis_2023, diretorio_local_2023)

    # Baixar os arquivos de demonstrações contábeis de 2024
    print("\nBaixando os arquivos de demonstrações contábeis de 2024...")
    download_arquivos_ftp(ftp, base_demonstracoes_contabeis_2024, diretorio_local_2024)

# Função para baixar os dados cadastrais das operadoras ativas
def baixar_operadoras_ativas(ftp):
    # Diretório FTP de operadoras ativas
    base_operadoras_ativas = '/FTP/PDA/operadoras_de_plano_de_saude_ativas/'

    # Diretório local para armazenar os arquivos
    diretorio_local_operadoras = './operadoras_ativas/'

    # Baixar os arquivos de operadoras ativas (somente CSV)
    print("\nBaixando os arquivos de operadoras ativas...")
    download_arquivos_ftp(ftp, base_operadoras_ativas, diretorio_local_operadoras, extensao='.csv')

# Função principal que executa as tarefas
def main():
    # Conectar ao servidor FTP da ANS
    try:
        ftp = ftplib.FTP('dadosabertos.ans.gov.br')
        ftp.login()
        print("Conectado ao servidor FTP da ANS.")
    except Exception as e:
        print(f"Erro ao conectar ao servidor FTP: {e}")
        return

    # Baixar os arquivos de demonstrações contábeis de 2023 e 2024
    baixar_demonstracoes_contabeis(ftp)

    # Baixar os arquivos de dados cadastrais das operadoras ativas
    baixar_operadoras_ativas(ftp)

    # Fechar a conexão FTP
    ftp.quit()
    print("\nDownload concluído!")

if __name__ == "__main__":
    main()





