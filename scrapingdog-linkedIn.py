from dotenv import load_dotenv
import requests
import json
import os 
import time 
import re

inicio = time.time()

# Definição do padrão Regex fora das funções para eficiência
pattern = re.compile("(?i)artigo|article")

load_dotenv()

def pesquisar_linkedin(perfil):
    api_key = os.environ.get('SCRAPING_API_KEY')
    print(api_key)
    url = "https://api.scrapingdog.com/profile"
    params = {
        "api_key": api_key,
        "type": "profile",
        "id": perfil,
        "premium": "true"
    }
    print(f"Iniciando busca para: '{perfil}'...")
    try:
        response = requests.get(url, params=params, timeout=45)
        if response.status_code == 200:
            print(f"Busca concluída com sucesso para: {perfil}")
            return response.json()
        else:
            print(f"ERRO: Requisição falhou ({response.status_code}) para {perfil}.")
            print(f"Mensagem da API: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO: Falha ao buscar {perfil}. Detalhe: {e}")
        return None

# Faz o filtro dos dados retornados da API
def filtrar_publicacoes_artigos(dados_brutos_linkedin):
    matches = []

    if not isinstance(dados_brutos_linkedin, list) or not dados_brutos_linkedin or 'publications' not in dados_brutos_linkedin[0]:
        return []

    publicacoes = dados_brutos_linkedin[0]["publications"]
    
    for publicacao in publicacoes:
        for valor in publicacao.values():
            if isinstance(valor, str) and pattern.search(valor):
                matches.append(publicacao)
                break 
    
    return matches

# Deve conter o nome para salvar o resultado e o link do perfil do linkedin que deseja obter os dados
perfis = [
    [
        'nome',
        'link do perfil'
    ]
]

OUTPUT_DIR = "resultados_linkedin"
OUTPUT_DIR_FILTRADO = 'resultados_linkedin_filtrados'

# Criação da pasta de resultados completos
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Pasta '{OUTPUT_DIR}' criada.")
    
# Criação da pasta de resultados filtrados
if not os.path.exists(OUTPUT_DIR_FILTRADO):
    os.makedirs(OUTPUT_DIR_FILTRADO)
    print(f"Pasta '{OUTPUT_DIR_FILTRADO}' criada.")


for perfil in perfis:
    dados_linkedin = pesquisar_linkedin(perfil[1])

    if dados_linkedin:

        nome_arquivo_base = perfil[0].replace(" ", "_").strip()

        #salva resultados completos para fins de teste
        nome_arquivo_completo = f"{nome_arquivo_base}.json"
        caminho_completo = os.path.join(OUTPUT_DIR, nome_arquivo_completo)

        try:
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                json.dump(dados_linkedin, f, indent=4, ensure_ascii=False)
            print(f"Sucesso: Dados de '{perfil[0]}' salvos em '{caminho_completo}'.")
            
        except IOError as e:
            print(f"ERRO DE ARQUIVO: Não foi possível salvar o arquivo completo. Detalhe: {e}")
        # end save

        # Filtra os dados das postagens do linkedin
        print(f"Filtrando dados de '{perfil[0]}'...")
        dados_filtrados = filtrar_publicacoes_artigos(dados_linkedin)
        
        if dados_filtrados:

            nome_arquivo_filtrado = f"{nome_arquivo_base}_filtrado.json"
            caminho_filtrado = os.path.join(OUTPUT_DIR_FILTRADO, nome_arquivo_filtrado)
            
            try:
                with open(caminho_filtrado, 'w', encoding='utf-8') as f:
                    json.dump(dados_filtrados, f, indent=4, ensure_ascii=False)
                print(f"Sucesso: Dados filtrados salvos em '{caminho_filtrado}'.\n")
            
            except IOError as e:
                print(f"ERRO DE ARQUIVO: Não foi possível salvar o arquivo filtrado. Detalhe: {e}")
        else:
            print(f"Aviso: Nenhuma publicação com 'artigo' ou 'article' foi encontrada para '{perfil[0]}'.\n")

    time.sleep(10) 


fim = time.time()
tempo_execucao = fim - inicio
print("Processo de coleta e filtragem concluído.")
print(f"Tempo de execução: {tempo_execucao:.4f} segundos")