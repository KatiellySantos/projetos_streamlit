# ============================================================
# IMPORTAÇÕES
# ============================================================

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# ============================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================

base_folder = "populacao"
os.makedirs(base_folder, exist_ok=True)

anos = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009,
        2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991,
        1990, 1989]

base_url = "https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_{ano}/"

arquivos_baixados = 0

# ============================================================
# DOWNLOAD DOS ARQUIVOS POR ANO
# ============================================================

for ano in anos:

    # --------------------------------------------------------
    # PREPARAÇÃO DA PASTA E URL DO ANO
    # --------------------------------------------------------

    url_ano = base_url.format(ano=ano)
    pasta_ano = os.path.join(base_folder, f"Estimativas_{ano}")
    os.makedirs(pasta_ano, exist_ok=True)

    print(f"\n🔎 Acessando: {url_ano}")

    # --------------------------------------------------------
    # ACESSO À PÁGINA DO IBGE
    # --------------------------------------------------------

    try:
        response = requests.get(url_ano)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao acessar {ano}: {e}")
        continue

    # --------------------------------------------------------
    # COLETA DOS LINKS DISPONÍVEIS
    # --------------------------------------------------------

    soup = BeautifulSoup(response.text, "html.parser")

    links = [a["href"] for a in soup.find_all("a", href=True)]

    if not links:
        print(f"⚠ Nenhum arquivo encontrado para {ano}")
        continue

    # --------------------------------------------------------
    # DOWNLOAD DOS ARQUIVOS
    # --------------------------------------------------------

    for link in links:

        if not link.endswith((".zip", ".xls", ".xlsx", ".csv", ".ods", ".pdf")):
            continue

        file_url = urljoin(url_ano, link)
        file_path = os.path.join(pasta_ano, link)

        # ----------------------------------------------------
        # VERIFICA SE O ARQUIVO JÁ EXISTE
        # ----------------------------------------------------

        if os.path.exists(file_path):
            print(f"Já existe: {link}")
            continue

        print(f"⬇ Baixando: {link}")

        # ----------------------------------------------------
        # DOWNLOAD DO ARQUIVO
        # ----------------------------------------------------

        try:
            r = requests.get(file_url)
            r.raise_for_status()

            with open(file_path, "wb") as f:
                f.write(r.content)

            arquivos_baixados += 1

        except Exception as e:
            print(f"Erro ao baixar {link}: {e}")

# ============================================================
# RESUMO FINAL
# ============================================================

print(f"\n✅ Total de arquivos baixados: {arquivos_baixados}")