from github_api import fetch_github_data, fetch_prs_for_repo, load_query
from data_formatter import save_to_csv, process_prs, save_prs_to_csv, print_summary
import http.client
import os
import time
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def menu():
    print("\n==== MENU ====")
    print("1 - Buscar repositórios populares (com +100 PRs) e salvar em CSV")
    print("2 - Analisar PRs dos repositórios salvos")
    print("3 - Sair")
    return input("Escolha uma opção: ")

if __name__ == "__main__":
    while True:
        opcao = menu()

        if opcao == "1":
            print("\n🔍 Buscando repositórios populares com pelo menos 100 PRs...\n")
            repos = fetch_github_data()
            save_to_csv(repos)
            print("\n📁 Repositórios salvos em 'popular_repos.csv' com sucesso!")

        elif opcao == "2":
            print("\n🧪 Iniciando análise de PRs dos repositórios...")

            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
                "User-Agent": "Python-Request"
            }
            query_prs = load_query("query_prs.gql")

            all_prs = []
            repos = fetch_github_data()

            for repo in repos:
                repo_name = repo.get("nameWithOwner")
                if not repo_name:
                    continue

                print(f"\n🔄 Buscando PRs para {repo_name}...")

                # ✅ Abre nova conexão para cada repo
                conn = http.client.HTTPSConnection(GITHUB_API_URL)
                prs = fetch_prs_for_repo(conn, headers, query_prs, repo_name)
                conn.close()

                processed = process_prs(repo_name, prs)
                print(f"   ✅ PRs válidos após filtro: {len(processed)}")
                all_prs.extend(processed)

                # 💤 Espera 200ms entre repositórios
                time.sleep(0.1)

            save_prs_to_csv(all_prs)
            print_summary(all_prs)

        elif opcao == "3":
            print("👋 Saindo...")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
