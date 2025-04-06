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
        created = pr.get("createdAt")
        merged = pr.get("mergedAt")
        closed = pr.get("closedAt")
        end_time = merged or closed

        reviews = pr.get("reviews", {}).get("nodes", [])
        review_count = len(reviews)
        has_human_review = any(is_human_review(r) for r in reviews)
        hours_to_review = duration_in_hours(created, end_time)

        print(f"🔍 PR: {pr.get('title')[:50]} | Reviews: {review_count} | Human: {has_human_review} | Duração: {hours_to_review:.2f}h")

        if not has_human_review:
            print(f"⚠️ Ignorado (sem revisão humana): {pr.get('title')}")
        elif hours_to_review < 1:
            print(f"⚠️ Ignorado (tempo < 1h): {pr.get('title')} ({hours_to_review:.2f}h)")
        else:
            processed.append([
                repo_name,
                pr.get("title"),
                created,
                end_time,
                hours_to_review,
                review_count
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

def save_prs_to_csv(prs):
    with open(OUTPUT_PRS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Repositório", "Título do PR", "Criado em", "Finalizado em", "Duração (h)", "Qtd Reviews"])
        for pr in prs:
            writer.writerow(pr)
    print(f"\n✅ PRs válidos salvos em: {OUTPUT_PRS_FILE}")

def print_summary(prs):
    print("\n Pull Requests Filtrados \n")
    print(tabulate(
        prs,
        headers=["Repositório", "Título do PR", "Criado em", "Finalizado em", "Duração (h)", "Qtd Reviews"],
        tablefmt="fancy_grid",
        numalign="right"
    ))
