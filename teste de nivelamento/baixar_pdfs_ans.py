import requests
from bs4 import BeautifulSoup
import os
import zipfile
import pdfplumber
import pandas as pd

# Baixar os PDFs 
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

headers = {
    "User-Agent": "Mozilla/5.0"
}

pdf_links = {
    "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf": "Anexo_I.pdf",
    "Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf": "Anexo_II.pdf"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
links = soup.find_all("a", href=True)

# Pastas
pasta_pdfs = "pdfs_ans"
pasta_saida = "saida"
os.makedirs(pasta_pdfs, exist_ok=True)
os.makedirs(pasta_saida, exist_ok=True)

# Baixa os arquivos
for link in links:
    href = link["href"]
    for trecho_pdf, nome_simples in pdf_links.items():
        if trecho_pdf in href:
            pdf_url = href if href.startswith("http") else "https://www.gov.br" + href
            print(f"Baixando: {nome_simples}")
            pdf_response = requests.get(pdf_url)
            with open(os.path.join(pasta_pdfs, nome_simples), "wb") as f:
                f.write(pdf_response.content)

print("Download dos PDFs concluído.")

# Compactar os PDFs
zip_pdfs = os.path.join(pasta_saida, "pdfs_ans.zip")
with zipfile.ZipFile(zip_pdfs, "w") as zipf:
    for root, _, files in os.walk(pasta_pdfs):
        for file in files:
            caminho_completo = os.path.join(root, file)
            caminho_relativo = os.path.relpath(caminho_completo, pasta_pdfs)
            zipf.write(caminho_completo, arcname=caminho_relativo)

print(f"PDFs compactados em: {zip_pdfs}")

# Extrair tabelas do Anexo I
pdf_anexo_i = os.path.join(pasta_pdfs, "Anexo_I.pdf")
tabelas = []

with pdfplumber.open(pdf_anexo_i) as pdf:
    for pagina in pdf.pages:
        tabela = pagina.extract_table()
        if tabela:
            df = pd.DataFrame(tabela[1:], columns=tabela[0])
            tabelas.append(df)

df_rol = pd.concat(tabelas, ignore_index=True)

# Ssubstituição
df_rol.replace({
    "OD": "Consulta realizada por cirurgião-dentista",
    "AMB": "Consulta realizada por profissional de outra categoria"
}, inplace=True)

# salvar csv e compactar
csv_nome = "rol_procedimentos.csv"
df_rol.to_csv(csv_nome, index=False)
print(f"Tabela salva como {csv_nome}")

zip_csv = os.path.join(pasta_saida, "Teste_Allan_Dias.zip")
with zipfile.ZipFile(zip_csv, "w") as zipf:
    zipf.write(csv_nome)

os.remove(csv_nome)
print(f"CSV compactado em: {zip_csv} (e removido depois de zipar)")
