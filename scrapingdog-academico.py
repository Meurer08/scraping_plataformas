from dotenv import load_dotenv
import requests
import json
import os 
import time # Adicionar um delay - muitas requisições podem travar a API

load_dotenv()

inicio = time.time()

def pesquisar_google_academico(termo_pesquisa):
    """
    Realiza uma pesquisa no Google Acadêmico usando a API Scraping Dog.
    """
    
    # Chave e URL da API
    api_key = os.environ.get('SCRAPING_API_KEY')
    # Link para a API referente ao google scholar
    url = "https://api.scrapingdog.com/google_scholar"

    # Parâmetros da Requisição
    params = {
        "api_key": api_key,
        "query": termo_pesquisa,  
        "language": "PT-BR",
        "page": 0,
        "results": 30
    }
    
    print(f"Iniciando busca para: '{termo_pesquisa}'...")
    
    try:
        # Adiciona um timeout para evitar que a requisição trave indefinidamente
        response = requests.get(url, params=params, timeout=45) 
        
        if response.status_code == 200:
            print(f"Busca concluída com sucesso para: {termo_pesquisa}")
            return response.json()
        else:
            print(f"ERRO: Requisição falhou ({response.status_code}) para {termo_pesquisa}.")
            print(f"Mensagem da API: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO: Falha ao buscar {termo_pesquisa}. Detalhe: {e}")
        return None

# Uso de aspas simples ('') para envolver a string, 
# permitindo que as aspas duplas ("") internas sejam usadas de forma Literal 
# Não pode ter espaços na configuração do termo de pesquisa seguir o formato:
# 'author:\"Nome completo do autor\"'
termos_de_pesquisa = [
    'author:\"\"',
]

# 2. Pasta onde os resultados serão salvos
OUTPUT_DIR = "resultados_academico"

# Cria a pasta se ela não existir
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Pasta '{OUTPUT_DIR}' criada.")


# 3. Itera sobre a lista de termos
for termo in termos_de_pesquisa:
    
    # Chama a função para buscar os dados
    dados_egresso = pesquisar_google_academico(termo)
    
    if dados_egresso:
        
        # Cria um nome de arquivo seguro a partir do termo de pesquisa
        # Remove caracteres problemáticos (aspas) e substitui espaços por underscores
        nome_arquivo_base = termo.replace('"', '').replace(':', '').replace(" ", "_").strip() 
        nome_arquivo = f"{nome_arquivo_base}.json"
        caminho_completo = os.path.join(OUTPUT_DIR, nome_arquivo)
        
        # Salva os dados no arquivo JSON
        try:
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                json.dump(dados_egresso, f, indent=4, ensure_ascii=False)
            print(f"Sucesso: Dados de '{termo}' salvos em '{caminho_completo}'.\n")
            
        except IOError as e:
            print(f"ERRO DE ARQUIVO: Não foi possível salvar o arquivo {caminho_completo}. Detalhe: {e}")

    # Pausa de 5 segundos entre as requisições (boa prática para APIs de terceiros)
    time.sleep(5) 

# Para calcular o tempo de execução
fim = time.time()
tempo_execucao = fim - inicio

print("Processo de coleta concluído.")
print(f"Tempo de execução: {tempo_execucao:.4f} segundos")