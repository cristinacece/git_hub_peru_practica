import plotly.express as px

def plot_growth_trend(df):
    fig = px.area(df, x='year', y='count', title="Account Creation Trend", color_discrete_sequence=['#2ecc71'])
    return fig

def plot_engagement_scatter(df):
    fig = px.scatter(df, x='stargazers_count', y='forks_count', color='language', 
                     hover_name='name', log_x=True, log_y=True, title="Engagement Correlation (Log Scale)")
    return fig

def plot_language_pie(df):
    fig = px.pie(df, names='language', values='count', hole=0.4, title="Top Languages")
    return fig

def plot_city_bar(df):
    fig = px.bar(df, x='count', y='location', orientation='h', color='count', color_continuous_scale='Viridis')
    return fig

def plot_industry_pie(df):
    fig = px.pie(df, names='industry_name', values='count', title="Distribution of Software by Industry")
    return fig

def plot_talent_scatter(df):
    fig = px.scatter(df, x='repos_per_year', y='followers', size='h_index', color='location', 
                     hover_name='login', title="Talent Clusters")
    return fig
