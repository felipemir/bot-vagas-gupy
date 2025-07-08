# 🤖 Bot de Vagas Gupy

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green?style=for-the-badge&logo=selenium)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

## 📖 Sobre o Projeto

Este é um bot desenvolvido em Python para automatizar a busca por vagas de emprego na plataforma Gupy. O objetivo principal deste projeto é poupar tempo no processo de busca manual, centralizando as vagas de diversas empresas e notificando sobre novas oportunidades que correspondam a filtros pré-definidos.

O projeto foi construído como parte do meu aprendizado em automação web e desenvolvimento de software, demonstrando habilidades em web scraping.

---

## ✨ Funcionalidades Principais

-   **Busca Multi-Empresa:** Monitora uma lista customizável de empresas na Gupy.
-   **Paginação Automática:** Navega por todas as páginas de resultados de cada empresa.
-   **Filtros Inteligentes:** Filtra vagas por palavras-chave no título (ex: "Júnior", "Estágio").
-   **Notificações no Telegram:** Envia alertas instantâneos para um chat do Telegram quando uma nova vaga que passa nos filtros é encontrada.
-   **Memória Persistente:** Salva as vagas já notificadas em um arquivo local para evitar notificações repetidas.

---

## 🚀 Tecnologias Utilizadas

-   **Python:** Linguagem principal do projeto.
-   **Selenium:** Para automação do navegador e web scraping de páginas dinâmicas.
-   **Beautiful Soup:** Para parsing do HTML das páginas.
-   **Requests:** Para comunicação com a API do Telegram.
-   **Git & GitHub:** Para versionamento e hospedagem do código.

---

## 🛠️ Instalação e Configuração

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clone o Repositório:**
```bash
git clone [https://github.com/Felipemir/bot-vagas-gupy.git](https://github.com/Felipemir/bot-vagas-gupy.git)
cd bot-vagas-gupy
```

**2. Instale as Dependências:**
Certifique-se de ter o Python 3.9+ instalado. Em seguida, instale as bibliotecas necessárias a partir do arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

**3. Configure o WebDriver:**
Este projeto utiliza o [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/).
-   Verifique a versão do seu navegador (Google Chrome ou Brave).
-   Baixe a versão correspondente do ChromeDriver.
-   Coloque o arquivo `chromedriver.exe` na raiz do projeto.

**4. Crie o arquivo de Configuração:**
-   Crie um arquivo chamado `config.py` na raiz do projeto.
-   Dentro dele, adicione suas credenciais do Telegram:
```python
# config.py
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"
```

---

## ▶️ Como Usar

Após a configuração, basta executar o script principal no seu terminal:

```bash
python vagas_bot.py
```

O bot iniciará a busca, e qualquer nova vaga que corresponda aos filtros definidos no topo do script será enviada para o seu Telegram.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

_Desenvolvido por [Robson Felipe](https://github.com/Felipemir)_