import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


EMPRESAS_PARA_MONITORAR = [
    "govbr",
    "fcamara",
    "unisinos",
    "sabiumcarreiras",
    "editoradobrasil",
    "sidi"
]
PALAVRAS_CHAVE = [
    "junior", 
    "jr", 
    "estagio", 
    "estagiario", 
    "estagiária"
]

DRIVER_PATH = 'chromedriver.exe'
BRAVE_BROWSER_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""


def buscar_vagas():
    print(">>> Iniciando busca por vagas v2.1 (Paginação Corrigida)...")
    
    try:
        service = Service(executable_path=DRIVER_PATH)
        options = Options()
        options.binary_location = BRAVE_BROWSER_PATH
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(service=service, options=options)
        print("✔️ Driver e navegador iniciados com sucesso!")

    except Exception as e:
        print(f"!!! ERRO AO INICIAR O SELENIUM !!!")
        print(f"Detalhe do erro: {e}")
        return

    vagas_encontradas_total = []
    for empresa_id in EMPRESAS_PARA_MONITORAR:
        url_pagina = f"https://{empresa_id}.gupy.io/"
        print(f"\n--- Buscando vagas em: {empresa_id} ---")
        driver.get(url_pagina)
        time.sleep(3)

        pagina_atual = 1
        while True:
            print(f"   Analisando página {pagina_atual}...")
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')

            container_vagas = soup.find(attrs={'data-testid': 'job-list'})
            if not container_vagas:
                print("       Nenhum container de vagas encontrado nesta página.")
                break

            itens_vagas = []
            # Tenta encontrar por data-testid primeiro (mais específico)
            itens_vagas_testid = container_vagas.find_all(attrs={'data-testid': 'job-list__list-item'})
            if itens_vagas_testid:
                itens_vagas = itens_vagas_testid
            else:
                # Se não achar, tenta pela tag 'a' que contém o link da vaga. É mais genérico mas funciona.
                itens_vagas_links = container_vagas.find_all('a', href=True)
                # Filtra apenas os links que realmente são de vagas
                itens_vagas = [link for link in itens_vagas_links if 'job' in link.get('href', '')]

            if not itens_vagas:
                print("       Nenhum item de vaga encontrado com os seletores conhecidos.")
                break

            print(f"       Encontrados {len(itens_vagas)} itens de vagas nesta página.")
            for item in itens_vagas:
                link_tag = item 

                titulo = link_tag.get_text(strip=True)
                link_parcial = link_tag['href']

                if not PALAVRAS_CHAVE or any(p.lower() in titulo.lower() for p in PALAVRAS_CHAVE):
                    link_completo = link_parcial
                    if link_parcial.startswith('/'):
                        link_completo = f"https://{empresa_id}.gupy.io{link_parcial}"

                    # Para pegar o local, buscamos o elemento pai e depois os spans dentro dele
                    elemento_pai = link_tag.find_parent('li') or link_tag.find_parent('tr')
                    local_texto = "N/A"
                    if elemento_pai:
                        spans = elemento_pai.find_all('span')
                        if len(spans) > 1:
                            local_texto = spans[1].get_text(strip=True)

                    info_vaga = {"empresa": empresa_id, "titulo": titulo, "local": local_texto, "link": link_completo}

                    # Evita adicionar vagas duplicadas se elas já estiverem na lista
                    if info_vaga not in vagas_encontradas_total:
                        vagas_encontradas_total.append(info_vaga)
                        print(f"  [VAGA ENCONTRADA!] {info_vaga['titulo']}")
                        mensagem = f"<b>{info_vaga['empresa'].upper()}</b>\n<b>{info_vaga['titulo']}</b>\nLocal: {info_vaga['local']}\n<a href='{info_vaga['link']}'>Ver vaga</a>"
                        enviar_mensagem_telegram(mensagem)

            # --- Lógica de Paginação ---
            try:
                botao_proxima = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Próxima página']")
                parent_li = botao_proxima.find_element(By.XPATH, "..")
                parent_class = parent_li.get_attribute('class')
                if parent_class and 'disabled' in parent_class:
                    print("   Fim da paginação (botão desabilitado).")
                    break

                botao_proxima.click()
                pagina_atual += 1
                time.sleep(3)

            except NoSuchElementException:
                print("   Fim da paginação (botão não encontrado).")
                break

    driver.quit()
    print(f"\n>>> Busca finalizada! Total de vagas encontradas: {len(vagas_encontradas_total)}")
    
def enviar_mensagem_telegram(mensagem):
    """Envia uma mensagem formatada para o chat no Telegram."""
    url_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem, 'parse_mode': 'HTML'}
    try:
        requests.post(url_api, data=payload)
        print("   ✔️ Notificação enviada com sucesso!")
    except Exception as e:
        print(f"   ❌ Falha ao enviar notificação para o Telegram: {e}")
# --- Fim da Função ---

# --- Execução Principal ---
if __name__ == "__main__":
    buscar_vagas()