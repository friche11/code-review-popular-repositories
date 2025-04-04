from github_api import fetch_github_data
from data_formatter import save_to_csv

def menu():
    print("\n==== MENU ====")
    print("1 - Buscar repositórios populares (com +100 PRs) e salvar em CSV")
    print("2 - (Reservado) Analisar PRs dos repositórios salvos")
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
            print("\n🧪 (Em breve) Esta opção permitirá analisar os PRs dos repositórios salvos.")
            

        elif opcao == "3":
            print("👋 Saindo...")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
