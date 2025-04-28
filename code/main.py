from github_api import fetch_github_data, fetch_prs_for_repo, load_query
from data_formatter import OUTPUT_DIR, save_to_csv, process_prs, save_prs_to_csv, print_summary
import os
import time
import pandas as pd
import csv
from dotenv import load_dotenv
from analisar_pull_requests import run_research

load_dotenv()

OUTPUT_FILE = f"{OUTPUT_DIR}/repositories.csv"
OUTPUT_PRS_FILE = f"{OUTPUT_DIR}/pull_requests.csv"
GITHUB_API_URL = "api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def menu():
    print("\n==== MENU ====")
    print("1 - Buscar repositórios populares (com +100 PRs) e salvar em CSV")
    print("2 - Buscar PRs dos repositórios salvos")
    print("3 - Analisar PRs salvos")
    print("4 - Sair")
    return input("Escolha uma opção: ")

def load_repos_from_csv(file_path=OUTPUT_FILE):
    """Carrega repositórios do CSV."""
    repos = []
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado.")
        return repos
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader, None)  # Pular cabeçalho
            if not header or len(header) < 6:
                print(f"❌ Cabeçalho inválido em {file_path}.")
                return repos
            for row in reader:
                if len(row) < 6 or not row[1]:  # Verificar nameWithOwner
                    print(f"⚠️ Linha inválida ignorada: {row}")
                    continue
                repos.append({
                    'name': row[0],
                    'nameWithOwner': row[1],
                    'createdAt': row[2],
                    'updatedAt': row[3],
                    'primaryLanguage': {'name': row[4] if row[4] != 'N/A' else None},
                    'totalPRs': int(row[5]) if row[5].isdigit() else 0
                })
        print(f"📂 Carregados {len(repos)} repositórios de {file_path}")
    except Exception as e:
        print(f"❌ Erro ao ler {file_path}: {e}")
    return repos

if __name__ == "__main__":
    while True:
        opcao = menu()

        if opcao == "1":
            print("\n🔍 Buscando repositórios populares com pelo menos 100 PRs...\n")
            repos = fetch_github_data()
            save_to_csv(repos)
            print("\n📁 Repositórios salvos em 'repositories.csv' com sucesso!")

        elif opcao == "2":
            print("\n🧪 Iniciando análise de PRs dos repositórios do CSV...")

            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
                "User-Agent": "Python-Request"
            }
            query_prs = load_query("query_prs.gql")

            all_prs = []
            repos = load_repos_from_csv()

            if not repos:
                print("❌ Nenhum repositório para processar. Verifique o arquivo CSV.")
                continue

            for repo in repos:
                repo_name = repo.get("nameWithOwner")
                if not repo_name:
                    print(f"⚠️ Repositório sem nameWithOwner, ignorando: {repo}")
                    continue

                try:
                    print(f"\n🔄 Buscando PRs para {repo_name}...")
                    prs = fetch_prs_for_repo(repo_name, query_prs, headers)
                    print(f"📥 {len(prs)} PRs brutos retornados por fetch_prs_for_repo")
                    processed = process_prs(repo_name, prs)
                    print(f"   ✅ PRs válidos após filtro: {len(processed)}")

                    all_prs.extend(processed)
                    print(f"📊 Total de PRs acumulados em all_prs: {len(all_prs)}")

                except Exception as e:
                    print(f"❌ Erro ao processar {repo_name}: {e}")
                    continue

                time.sleep(0.4)

            # Salvamento consolidado
            print(f"🏁 Total de PRs para salvar em pull_requests.csv: {len(all_prs)}")
            if all_prs:
                save_prs_to_csv(all_prs)
                print_summary(all_prs)
            else:
                print("❌ Nenhum PR válido para salvar em pull_requests.csv")

        elif opcao == "3":

            df = pd.read_csv(OUTPUT_PRS_FILE, delimiter=';')
    
            # Chamar a função principal para rodar a análise
            run_research(df)

        elif opcao == "4":
            print("👋 Saindo...")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
