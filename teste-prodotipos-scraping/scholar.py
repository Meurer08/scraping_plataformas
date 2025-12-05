from scholarly import scholarly

termo_pesquisa = 'author:"Vitor Meurer"' 
# O comando AND deve ser usado com cuidado;

# Buscar publicações
search_query_pubs = scholarly.search_pubs(termo_pesquisa)

print(f"--- Publicações filtradas por: {termo_pesquisa} ---")
for i in range(5): # Limita a 5 resultados para teste
    try:
        pub = next(search_query_pubs)
        print(f"Título: {pub['bib']['title']}")
        print("-" * 20)
    except StopIteration:
        break