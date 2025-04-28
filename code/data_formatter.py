import csv
import os
from datetime import datetime
from tabulate import tabulate

OUTPUT_DIR = "../outputs"
OUTPUT_FILE = f"{OUTPUT_DIR}/repositories.csv"
OUTPUT_PRS_FILE = f"{OUTPUT_DIR}/pull_requests.csv"

def duration_in_hours(start, end):
    if not start or not end:
        return 0
    start_dt = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
    end_dt = datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
    return (end_dt - start_dt).total_seconds() / 3600

def is_human_review(review):
    author = review.get("author")
    return author and author.get("__typename") == "User"

def process_prs(repo_name, pr_list):
    processed = []

    for pr in pr_list:
        if not isinstance(pr, dict):
            continue

        state = pr.get("state")
        if state not in {"MERGED", "CLOSED"}:
            continue

        review_count = pr.get("reviews", {}).get("totalCount", 0)
        if review_count < 1:
            continue

        created = pr.get("createdAt")
        merged = pr.get("mergedAt")
        closed = pr.get("closedAt")
        end_time = merged or closed
        hours_to_review = duration_in_hours(created, end_time)

        if hours_to_review is None or hours_to_review < 1:
            continue

        reviews = pr.get("reviews", {}).get("nodes") or []
        comments = pr.get("comments", {}).get("nodes") or []

        review_authors = {r.get('author', {}).get('login') for r in reviews
                          if r.get('author') and r.get('author', {}).get('__typename') != 'Bot'}
        comment_authors = {c.get('author', {}).get('login') for c in comments
                           if c.get('author') and c.get('author', {}).get('__typename') != 'Bot'}
        participants = len(review_authors | comment_authors)

        processed.append([
            repo_name,
            pr.get("number", ""),
            pr.get("title", ""),
            state,
            created,
            end_time,
            hours_to_review,
            pr.get("changedFiles", 0),
            pr.get("additions", 0),
            pr.get("deletions", 0),
            len(pr.get("bodyText") or ""),
            pr.get("comments", {}).get("totalCount", 0),
            review_count,
            participants
        ])

    return processed

def save_to_csv(repos):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Nome", "Nome Completo", "Criado em", "Atualizado em", "Linguagem Principal", "Qtd PRs Válidos"])
        for repo in repos:
            writer.writerow([
                repo.get("name"),
                repo.get("nameWithOwner"),
                repo.get("createdAt"),
                repo.get("updatedAt"),
                repo.get("primaryLanguage", {}).get("name") if repo.get("primaryLanguage") else "N/A",
                repo.get("totalPRs", 0)
            ])
    print(f"\n✅ Repositórios salvos em: {OUTPUT_FILE}")

def save_prs_to_csv(prs, file_path=OUTPUT_PRS_FILE, append=False):
    mode = 'a' if append else 'w'
    fieldnames = [
        "Repositório", "Número", "Título do PR", "Estado", "Criado em", "Finalizado em",
        "Duração (h)", "Arquivos Modificados", "Linhas Adicionadas", "Linhas Removidas",
        "Tamanho Descrição", "Comentários", "Revisões", "Participantes"
    ]
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not append or not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            writer.writerow(fieldnames)
        for pr in prs:
            writer.writerow(pr)
    print(f"\n✅ PRs válidos salvos em: {file_path}")

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

def print_summary(prs):
    print("\n Pull Requests Filtrados \n")
    print(tabulate(
        prs,
        headers=["Repositório", "Número", "Título do PR", "Estado", "Criado em", "Finalizado em",
                 "Duração (h)", "Arquivos Modificados", "Linhas Adicionadas", "Linhas Removidas",
                 "Tamanho Descrição", "Comentários", "Revisões", "Participantes"],
        tablefmt="fancy_grid",
        numalign="right"
    ))