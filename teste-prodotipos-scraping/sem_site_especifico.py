from ddgs import DDGS

def buscar_nome(nome, max_results=5):
    """
    Pesquisa um nome no DuckDuckGo sem restringir a sites específicos.
    Retorna os primeiros links relacionados.
    """
    resultados = []
    with DDGS() as ddgs:
        try:
            resultados_busca = list(ddgs.text(nome, max_results=max_results))
            if resultados_busca:
                for r in resultados_busca:
                    # r contém dict com 'title', 'href' e 'body'
                    titulo = r.get("title", "Sem título")
                    link = r.get("href", "Sem link")
                    snippet = r.get("body", "Sem descrição")
                    resultados.append(f"{titulo}\n{link}\n{snippet}\n")
            else:
                resultados.append("Nenhum resultado encontrado.")
        except Exception as e:
            resultados.append(f"Erro ao buscar: {str(e)}")
    return resultados

def main():
    nome = input("Digite o termo de pesquisa: ")
    print(f"\nPesquisando '{nome}' no DuckDuckGo...\n")
    resultados = buscar_nome(nome)

    for i, r in enumerate(resultados, start=1):
        print(f"--- Resultado {i} ---")
        print(r)

if __name__ == "__main__":
    main()