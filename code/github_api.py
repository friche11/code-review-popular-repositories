from datetime import datetime
import http.client
import json
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

GITHUB_API_URL = "api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def load_query(file_name):
    """Carrega a query GraphQL a partir de um arquivo .gql"""
    path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado em: {path}")
    with open(path, "r") as file:
        return file.read()

def fetch_github_data(limit=200):
    """Busca os repositórios populares com base nos critérios definidos"""
    if not TOKEN:
        raise ValueError("❌ GITHUB_TOKEN não está definido.")

    conn = http.client.HTTPSConnection(GITHUB_API_URL)

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Python-Request"
    }

    QUERY_REPOS = load_query("query_repos.gql")

    repos = []
    after_cursor = None
    page = 1

    print(f"\n🚀 Iniciando busca dos {limit} repositórios mais populares...")

    while len(repos) < limit:
        print(f"\n📄 Página {page} | Cursor atual: {after_cursor}")
        variables = {"after": after_cursor}
        request_body = json.dumps({"query": QUERY_REPOS, "variables": variables})

        conn.request("POST", "/graphql", body=request_body, headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        if "errors" in data:
            print(f"❌ Erro na requisição: {data['errors']}")
            break

        search = data.get("data", {}).get("search", {})
        new_repos = [edge["node"] for edge in search.get("edges", [])]
        print(f"🔎 {len(new_repos)} repositórios encontrados nesta página")

        for repo in new_repos:
            repos.append(repo)

            if len(repos) % 20 == 0:
                print(f"📦 {len(repos)} repositórios acumulados até agora")

            if len(repos) >= limit:
                break

        if not search.get("pageInfo", {}).get("hasNextPage"):
            print("✅ Fim da paginação: não há mais páginas.")
            break

        after_cursor = search.get("pageInfo", {}).get("endCursor")
        page += 1

    conn.close()
    print(f"\n🏁 Busca finalizada. Total de repositórios coletados: {len(repos)}")
    return repos[:limit]


def fetch_prs_for_repo(conn, headers, query, repo_name):
    """Busca PRs com pelo menos 1 revisão e mais de 1h de vida"""
    print(f"  🔍 Começando busca de PRs para {repo_name}...")  # NOVO LOG
    owner, name = repo_name.split("/")
    after_cursor = None
    valid_prs = []
    page = 1

    while True:
        variables = {
            "owner": owner,
            "name": name,
            "after": after_cursor
        }
        body = json.dumps({"query": query, "variables": variables})
        conn.request("POST", "/graphql", body=body, headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        if "errors" in data:
            print(f"⚠️ Erro ao buscar PRs para {repo_name}: {data['errors']}")
            break

        pr_nodes = data.get("data", {}).get("repository", {}).get("pullRequests", {}).get("nodes", [])
        for pr in pr_nodes:
            review_count = len(pr.get("reviews", {}).get("nodes", []))
            created = pr.get("createdAt")
            closed = pr.get("closedAt") or pr.get("mergedAt")
            if review_count >= 1 and created and closed:
                created_dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
                closed_dt = datetime.strptime(closed, "%Y-%m-%dT%H:%M:%SZ")
                if (closed_dt - created_dt).total_seconds() >= 3600:
                    valid_prs.append(pr)

        page_info = data.get("data", {}).get("repository", {}).get("pullRequests", {}).get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break

        after_cursor = page_info.get("endCursor")
        page += 1

    print(f"🔁 {repo_name}: {len(valid_prs)} PRs válidos encontrados")
    return valid_prs
