import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create plots directory
os.makedirs("plots", exist_ok=True)

# Set style for premium look
plt.style.use('ggplot')
sns.set_theme(style="whitegrid", palette="viridis")

def generate_visualizations():
    # Load data
    print("Loading datasets...")
    df_users = pd.read_csv("data/users_peru_full.csv")
    df_repos = pd.read_csv("data/repos_1200_users.csv")

    # 1. Top 10 Cities in Peru
    print("Generating Plot 1: Top Cities...")
    plt.figure(figsize=(12, 6))
    top_cities = df_users['location'].str.title().value_counts().head(10)
    sns.barplot(x=top_cities.values, y=top_cities.index, hue=top_cities.index, palette="mako")
    plt.title("Top 10 Ciudades con más Desarrolladores en Perú (GitHub)", fontsize=15, pad=20)
    plt.xlabel("Número de Usuarios")
    plt.ylabel("Ubicación")
    plt.tight_layout()
    plt.savefig("plots/1_top_cities.png", dpi=300)
    plt.close()

    # 2. Growth of Users over Time
    print("Generating Plot 2: Growth Over Time...")
    plt.figure(figsize=(12, 6))
    df_users['year'] = pd.to_datetime(df_users['created_at']).dt.year
    growth = df_users['year'].value_counts().sort_index()
    plt.plot(growth.index, growth.values, marker='o', color='#2ecc71', linewidth=3, markersize=8)
    plt.fill_between(growth.index, growth.values, color='#2ecc71', alpha=0.2)
    plt.title("Crecimiento de la Comunidad de Desarrolladores en Perú (2008-2025)", fontsize=15, pad=20)
    plt.xlabel("Año de Creación de Cuenta")
    plt.ylabel("Nuevos Usuarios")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("plots/2_user_growth.png", dpi=300)
    plt.close()

    # 3. Top 10 Languages
    print("Generating Plot 3: Top Languages...")
    plt.figure(figsize=(12, 6))
    top_languages = df_repos['language'].dropna().value_counts().head(10)
    sns.barplot(x=top_languages.index, y=top_languages.values, hue=top_languages.index, palette="magma")
    plt.title("Top 10 Lenguajes de Programación Preferidos en Perú", fontsize=15, pad=20)
    plt.xlabel("Lenguaje")
    plt.ylabel("Cantidad de Repositorios")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/3_top_languages.png", dpi=300)
    plt.close()

    # 4. Stars vs Forks (Bubble correlation)
    print("Generating Plot 4: Stars vs Forks...")
    plt.figure(figsize=(10, 8))
    # Filter onlyrepos with at least some activity to make the plot clean
    df_active = df_repos[(df_repos['stargazers_count'] > 0) | (df_repos['forks_count'] > 0)].copy()
    sns.scatterplot(data=df_active.head(1000), x="stargazers_count", y="forks_count", 
                    size="size", sizes=(20, 500), alpha=0.6, color="#3498db")
    plt.title("Relación entre Estrellas (Popularidad) y Forks (Colaboración)", fontsize=15, pad=20)
    plt.xlabel("Estrellas")
    plt.ylabel("Forks")
    plt.tight_layout()
    plt.savefig("plots/4_stars_vs_forks.png", dpi=300)
    plt.close()

    # 5. Top 10 Most Starred Repos
    print("Generating Plot 5: Top Starring Repos...")
    plt.figure(figsize=(12, 7))
    top_repos = df_repos.nlargest(10, 'stargazers_count')[['full_name', 'stargazers_count']]
    sns.barplot(x='stargazers_count', y='full_name', data=top_repos, hue='full_name', palette="coolwarm")
    plt.title("Top 10 Proyectos Peruanos más Populares (Por Estrellas)", fontsize=15, pad=20)
    plt.xlabel("Estrellas")
    plt.ylabel("Repositorio (Usuario/Proyecto)")
    plt.tight_layout()
    plt.savefig("plots/5_top_projects.png", dpi=300)
    plt.close()

    print("\nVisualizations successfully generated in 'plots/' directory!")

if __name__ == "__main__":
    generate_visualizations()
