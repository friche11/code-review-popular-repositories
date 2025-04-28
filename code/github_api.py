from datetime import datetime
from http.client import IncompleteRead
import http.client
import json
import os
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
import time

# Carregar variáveis do .env
load_dotenv()


GITHUB_API_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def load_query(file_name):
    """Carrega a query GraphQL a partir de um arquivo .gql"""
    path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado em: {path}")
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def fetch_with_retry(url, json_data, headers, max_retries=10, backoff_factor=3):
    """Faz uma requisição com retry em caso de falha."""
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=json_data, headers=headers, timeout=90)
            remaining = response.headers.get('X-RateLimit-Remaining', 'N/A')
            limit = response.headers.get('X-RateLimit-Limit', 'N/A')
            used = response.headers.get('X-RateLimit-Used', 'N/A')
            reset = response.headers.get('X-RateLimit-Reset', 'N/A')
            print(f"📋 Status HTTP: {response.status_code}, Rate Limit: {remaining}/{limit} restantes, Usado: {used}, Reset em: {reset}")
            if remaining != 'N/A' and int(remaining) < 100:
                print(f"⚠️ Rate limit baixo ({remaining} pontos). Pausando por 300s...")
                time.sleep(300)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            if attempt == max_retries - 1:
                print(f"❌ Falha após {max_retries} tentativas: {e}")
                raise
            wait_time = backoff_factor * (2 ** attempt)
            print(f"⚠️ Tentativa {attempt + 1} falhou: {e}. Aguardando {wait_time}s...")
            time.sleep(wait_time)
    return None

def fetch_github_data(limit=200):
    """Busca os repositórios populares com pelo menos 100 PRs (MERGED + CLOSED)"""
    if not TOKEN:
        raise ValueError("❌ GITHUB_TOKEN não está definido.")

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Python-Request",
        "Accept": "application/vnd.github+json",
        "Accept-Encoding": "gzip"
    }

    QUERY_REPOS = load_query("query_repos.gql")

    repos = []
    after_cursor = None
    page = 1

    print(f"\n🚀 Iniciando busca dos {limit} repositórios mais populares com >= 100 PRs...")

    while len(repos) < limit:
        print(f"\n📄 Página {page} | Cursor atual: {after_cursor}")
        variables = {"after": after_cursor}
        request_body = {"query": QUERY_REPOS, "variables": variables}

        raw_response = fetch_with_retry(
            f"{GITHUB_API_URL}/graphql",
            request_body,
            headers,
            max_retries=10,
            backoff_factor=3
        )

        if not raw_response:
            print("❌ Resposta vazia ou falha após retries.")
            break

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON da resposta dos repositórios: {e}")
            print(f"Resposta bruta: {raw_response}")
            break

        if "errors" in data:
            print(f"❌ Erro na requisição: {data['errors']}")
            break

        search = data.get("data", {}).get("search", {})
        new_repos = [edge["node"] for edge in search.get("edges", [])]
        print(f"🔎 {len(new_repos)} repositórios encontrados nesta página")

        for repo in new_repos:
            pr_count = repo.get("pullRequests", {}).get("totalCount", 0)
            if pr_count >= 100:  # Filtrar repositórios com >= 100 PRs
                repos.append(repo)
                print(f"✅ {repo['nameWithOwner']} adicionado ({pr_count} PRs)")

                if len(repos) % 20 == 0:
                    print(f"📦 {len(repos)} repositórios acumulados até agora")

                if len(repos) >= limit:
                    break

        if not search.get("pageInfo", {}).get("hasNextPage"):
            print("✅ Fim da paginação: não há mais páginas.")
            break

        after_cursor = search.get("pageInfo", {}).get("endCursor")
        page += 1
        time.sleep(2)  # Aumentado para 1s para reduzir pressão

    print(f"\n🏁 Busca finalizada. Total de repositórios coletados: {len(repos)}")
    return repos[:limit]

def fetch_prs_for_repo(repo_name, query, headers):
    """Busca até 100 PRs MERGED ou CLOSED, com ao menos uma revisão e duração > 1h."""
    print(f"  🔍 Começando busca de PRs para {repo_name}...")
    owner, name = repo_name.split("/")
    after_cursor = None
    valid_prs = []
    page = 1

    MAX_PRS = 100

    while True:
        variables = {
            "owner": owner,
            "name": name,
            "cursor": after_cursor
        }
        body = {"query": query, "variables": variables}

        raw_response = fetch_with_retry(
            f"{GITHUB_API_URL}/graphql",
            body,
            headers,
            max_retries=10,
            backoff_factor=3
        )

        if not raw_response:
            print(f"❌ Resposta vazia recebida para o repositório: {repo_name}")
            return valid_prs

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON para {repo_name}: {e}")
            print(f"Resposta bruta: {raw_response}")
            return valid_prs

        if "errors" in data:
            print(f"⚠️ Erro ao buscar PRs para {repo_name}: {data['errors']}")
            for error in data['errors']:
                if 'extensions' in error and 'trackingId' in error['extensions']:
                    print(f"📌 ID de rastreamento: {error['extensions']['trackingId']}")

        pr_nodes = data.get("data", {}).get("repository", {}).get("pullRequests", {}).get("nodes", [])
        print(f"  🧪 {repo_name} → PRs brutos recebidos: {len(pr_nodes)}")

        for pr in pr_nodes:
            review_count = pr.get("reviews", {}).get("totalCount", 0)
            created = pr.get("createdAt")
            closed = pr.get("closedAt") or pr.get("mergedAt")

            if review_count < 1:
                print(f"⚠️ PR {pr.get('number')} ignorado: sem revisões")
                continue
            if not created or not closed:
                print(f"⚠️ PR {pr.get('number')} ignorado: datas inválidas")
                continue
            try:
                created_dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
                closed_dt = datetime.strptime(closed, "%Y-%m-%dT%H:%M:%SZ")
                duration = (closed_dt - created_dt).total_seconds() / 3600
                if duration < 1:
                    print(f"⚠️ PR {pr.get('number')} ignorado: duração {duration:.2f}h < 1h")
                    continue
            except ValueError as e:
                print(f"⚠️ PR {pr.get('number')} ignorado: erro nas datas ({e})")
                continue

            valid_prs.append(pr)
            print(f"✅ PR {pr.get('number')} adicionado: {review_count} revisões, {duration:.2f}h")

            if len(valid_prs) >= MAX_PRS:
                print(f"🚀 Limite de {MAX_PRS} PRs atingido para {repo_name}")
                return valid_prs

        page_info = data.get("data", {}).get("repository", {}).get("pullRequests", {}).get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break

        after_cursor = page_info.get("endCursor")
        page += 1
        time.sleep(2)

    print(f"🔁 {repo_name}: {len(valid_prs)} PRs válidos encontrados")
    return valid_prs
