from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def varrer_lattes_com_selenium(link):
    """
    Função para varrer um currículo Lattes usando Selenium para simular
    um navegador real e BeautifulSoup para análise do HTML.
    """
    driver = None
    try:
        # Configura o serviço do Chrome
        service = Service(ChromeDriverManager().install())
        
        # Configura as opções do navegador (como o User-Agent)
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Remova a linha abaixo para ver o navegaInicializa o navegador em modo "invisídor em ação
        # options.add_argument("--headless")

        driver = webdriver.Chrome(service=service, options=options)
        
        # Acessa o link
        driver.get(link)

        # --- ADIÇÃO DA ESPERA EXPLÍCITA ---
        # Espera até que o elemento com o ID "identificacao" (que contém o nome) esteja visível
        # Isso garante que a página do currículo, e não a do captcha, foi carregada
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.NAME, "identificacao"))
        )
        # O script só continuará a partir daqui quando o elemento for encontrado ou após 20 segundos
        
        # Pega o conteúdo HTML completo da página já renderizada
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        dados = {}

        # Exemplo: extrair o nome do pesquisador
        nome_h2 = soup.find("h2")
        if nome_h2:
            dados["nome"] = nome_h2.text.strip()
            
        # Exemplo: pegar os títulos de seção
        secoes = [h3.text.strip() for h3 in soup.find_all("h3")]
        dados["secoes"] = secoes
        
        return dados
        
    except Exception as e:
        return f"Ocorreu um erro: {e}"
        
    finally:
        # Fecha o navegador
        if driver:
            driver.quit()

# Teste com um link real 
link_lattes = ""
resultado = varrer_lattes_com_selenium(link_lattes)
print(resultado)