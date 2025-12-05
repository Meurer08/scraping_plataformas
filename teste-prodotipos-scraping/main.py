from ddgs import DDGS

def buscar_nome(nome, sites, max_results=5):
    """
    Pesquisa um nome em vários sites usando DuckDuckGo.
    Retorna uma lista de snippets ou links públicos.
    """
    resultados = []
    with DDGS() as ddgs:
        for site in sites:
            query = f'"{nome}" site:{site}' if site else f'"{nome}"'
            try:
                resultados_site = list(ddgs.text(query, max_results=max_results))
                if resultados_site:
                    for r in resultados_site:
                        resultados.append(f"[{site}] {r}")
                else:
                    resultados.append(f"[{site}] Nenhum resultado encontrado.")
            except Exception as e:
                resultados.append(f"[{site}] Erro ao buscar: {str(e)}")
    return resultados

def main():
    nome = input("Digite o nome da pessoa: ")
    """
    "lattes.cnpq.br"
    
    """
    sites = ["scholar.google.com"]

    print(f"\nPesquisando '{nome}' nos sites: {', '.join(sites)}...\n")
    resultados = buscar_nome(nome, sites)

    for r in resultados:
        print(r)

if __name__ == "__main__":
    main()
