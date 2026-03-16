import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create plots directory
os.makedirs("plots", exist_ok=True)

# Set global style for professional feel
sns.set_theme(style="white", palette="viridis")

def generate_dashboard_stats():
    # Load data
    print("Loading datasets for dashboard...")
    df_users = pd.read_csv("data/users_peru_full.csv")
    df_repos = pd.read_csv("data/repos_1200_users.csv")

    # --- PLOT 1: HEATMAP OF CORRELATIONS ---
    print("Generating Heatmap: Correlation Matrix...")
    # Select numerical columns of interest
    cols_of_interest = [
        'stargazers_count', 'forks_count', 'size', 
        'open_issues_count', 'watchers_count', 'has_issues',
        'has_projects', 'has_wiki'
    ]
    
    # Filter columns that actually exist in the dataframe
    existing_cols = [c for c in cols_of_interest if c in df_repos.columns]
    corr_matrix = df_repos[existing_cols].corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("Matriz de Correlación: Métricas de Repositorios en Perú", fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig("plots/dashboard_heatmap_correlation.png", dpi=300)
    plt.close()

    # --- PLOT 2: STACKED AREA CHART (Language Evolution) ---
    print("Generating Stacked Area Chart: Evolution of Top Languages...")
    
    # Pre-process dates and languages
    df_repos['created_at'] = pd.to_datetime(df_repos['created_at'])
    df_repos['year'] = df_repos['created_at'].dt.year
    
    # Filter for years between 2014 and 2024 (where data is most dense)
    df_filtered = df_repos[(df_repos['year'] >= 2014) & (df_repos['year'] <= 2024)].copy()
    
    # Get top 5 languages overall
    top_5_langs = df_filtered['language'].dropna().value_counts().head(5).index.tolist()
    
    # Prepare data for stacked chart
    # Create a pivot table: Index=Year, Columns=Language, Values=Count
    lang_evolution = df_filtered[df_filtered['language'].isin(top_5_langs)].groupby(['year', 'language']).size().unstack(fill_value=0)
    
    # Normalizing to percentages to see relative popularity (Share of voice)
    lang_evolution_pct = lang_evolution.div(lang_evolution.sum(axis=1), axis=0) * 100

    plt.figure(figsize=(14, 8))
    lang_evolution_pct.plot(kind='area', stacked=True, alpha=0.8, figsize=(14, 8), colormap="Spectral")
    
    plt.title("Evolución de Popularidad Relativa: Top 5 Lenguajes en Perú (2014-2024)", fontsize=16, pad=20)
    plt.xlabel("Año de Creación del Repositorio")
    plt.ylabel("Porcentaje de Uso (%)")
    plt.legend(title="Lenguajes", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("plots/dashboard_stacked_area_languages.png", dpi=300)
    plt.close()

    print("\nDashboard graphics successfully generated in 'plots/' directory!")

if __name__ == "__main__":
    generate_dashboard_stats()
