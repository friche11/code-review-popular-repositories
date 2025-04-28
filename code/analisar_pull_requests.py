import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import matplotlib.pyplot as plt

def run_research(df):
    # Garante que a pasta '../docs/graficos' exista
    output_dir = os.path.join('..', 'docs', 'graficos')
    output_dir_correlacao = os.path.join('..', 'docs')
    os.makedirs(output_dir, exist_ok=True)

    """Executa todas as questões de pesquisa, gera gráficos e imprime os dados no console de forma organizada."""
    print("Analisando as questões de pesquisa e gerando gráficos...\n")
    
    # --------- RQ 01 ---------
    feedback_status = df.groupby('Estado')[['Arquivos Modificados', 'Linhas Adicionadas', 'Linhas Removidas']].median()
    print("\nRQ01 - Tamanho dos PRs vs Feedback")
    print(feedback_status)
    feedback_status.plot(kind='bar')
    plt.title('RQ01 - Tamanho dos PRs vs Feedback')
    plt.ylabel('Mediana')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq01.png'))
    plt.close()

    # --------- RQ 02 ---------
    feedback_time_analysis = df.groupby('Estado')['Duração (h)'].median()
    print("\nRQ02 - Tempo de Análise vs Feedback")
    print(feedback_time_analysis)
    feedback_time_analysis.plot(kind='bar', color='orange')
    plt.title('RQ02 - Tempo de Análise vs Feedback')
    plt.ylabel('Duração (h)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq02.png'))
    plt.close()

    # --------- RQ 03 ---------
    feedback_description = df.groupby('Estado')['Tamanho Descrição'].median()
    print("\nRQ03 - Descrição vs Feedback")
    print(feedback_description)
    feedback_description.plot(kind='bar', color='green')
    plt.title('RQ03 - Descrição vs Feedback')
    plt.ylabel('Tamanho Descrição')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq03.png'))
    plt.close()

    # --------- RQ 04 ---------
    feedback_interactions = df.groupby('Estado')[['Comentários', 'Revisões', 'Participantes']].median()
    print("\nRQ04 - Interações vs Feedback")
    print(feedback_interactions)
    feedback_interactions.plot(kind='bar')
    plt.title('RQ04 - Interações vs Feedback')
    plt.ylabel('Mediana')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq04.png'))
    plt.close()

    # --------- RQ 05 ---------
    size_revisions = df.groupby('Revisões')[['Arquivos Modificados', 'Linhas Adicionadas', 'Linhas Removidas']].median()
    print("\nRQ05 - Tamanho dos PRs vs Revisões")
    print(size_revisions)
    size_revisions.plot()
    plt.title('RQ05 - Tamanho dos PRs vs Revisões')
    plt.ylabel('Mediana')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq05.png'))
    plt.close()

    # --------- RQ 06 ---------
    time_revisions = df.groupby('Revisões')['Duração (h)'].median()
    print("\nRQ06 - Tempo de Análise vs Revisões")
    print(time_revisions)
    time_revisions.plot()
    plt.title('RQ06 - Tempo de Análise vs Revisões')
    plt.ylabel('Duração (h)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq06.png'))
    plt.close()

    # --------- RQ 07 ---------
    description_revisions = df.groupby('Revisões')['Tamanho Descrição'].median()
    print("\nRQ07 - Descrição vs Revisões")
    print(description_revisions)
    description_revisions.plot()
    plt.title('RQ07 - Descrição vs Revisões')
    plt.ylabel('Tamanho Descrição')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq07.png'))
    plt.close()

    # --------- RQ 08 ---------
    interactions_revisions = df.groupby('Revisões')[['Comentários', 'Participantes']].median()
    print("\nRQ08 - Interações vs Revisões")
    print(interactions_revisions)
    interactions_revisions.plot()
    plt.title('RQ08 - Interações vs Revisões')
    plt.ylabel('Mediana')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rq08.png'))
    plt.close()

    # Carregar CSV
    df = pd.read_csv('../outputs/pull_requests.csv', sep=';')

    # Selecionar apenas colunas numéricas
    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    # Transformar Estado em número
    df['Estado_num'] = df['Estado'].map({'MERGED': 1, 'CLOSED': 0})

    # Selecionar apenas colunas numéricas, agora incluindo Estado_num
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calcular correlação de Spearman
    spearman_corr = numeric_df.corr(method='spearman')

    # Plotar o heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(spearman_corr, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)

    plt.title('Matriz de Correlação (Spearman)', fontsize=16)
    plt.tight_layout()

    # Salvar como PNG
    plt.savefig(os.path.join(output_dir_correlacao, 'correlacao_spearman.png'), dpi=300)

    # Exibir na tela (opcional)
    plt.show()

