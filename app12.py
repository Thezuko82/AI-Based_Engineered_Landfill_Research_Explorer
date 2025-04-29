import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data with caching
@st.cache_data
def load_data():
    data = pd.read_csv("engineered_landfill_research.csv")
    return data

# App title and intro
st.title("🔍 AI-Based Engineered Landfill Research Explorer")
st.markdown("""
Welcome to the **AI-powered search engine for engineered landfill research papers**. 
Use the filters on the sidebar to find relevant literature and explore trends via interactive visualizations.
""")

# Load dataset
df = load_data()

# Sidebar filters
st.sidebar.header("📚 Filter Your Search")

years = sorted(df['Year'].dropna().unique())
year_range = st.sidebar.slider("🗓️ Year of Publication", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
title_search = st.sidebar.text_input("🔎 Search in Title or Abstract", "")
authors = sorted(df['Author'].dropna().unique())
selected_authors = st.sidebar.multiselect("👤 Select Author(s)", authors)
journals = sorted(df['Journal'].dropna().unique())
selected_journals = st.sidebar.multiselect("📔 Select Journal(s)", journals)
domains = sorted(df['Domain'].dropna().unique())
selected_domains = st.sidebar.multiselect("🌐 Select Domain(s)", domains)
countries = sorted(df['Country'].dropna().unique())
selected_countries = st.sidebar.multiselect("🌍 Select Country(ies)", countries)

# Apply filters
filtered_df = df[
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
]
if title_search:
    filtered_df = filtered_df[
        filtered_df['Title'].str.contains(title_search, case=False, na=False) |
        filtered_df['Abstract'].str.contains(title_search, case=False, na=False)
    ]
if selected_authors:
    filtered_df = filtered_df[filtered_df['Author'].isin(selected_authors)]
if selected_journals:
    filtered_df = filtered_df[filtered_df['Journal'].isin(selected_journals)]
if selected_domains:
    filtered_df = filtered_df[filtered_df['Domain'].isin(selected_domains)]
if selected_countries:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]

# Display results
st.subheader("🔬 Filtered Research Papers")
st.write(f"Total Results: {len(filtered_df)}")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.warning("No results found. Try changing your filters.")

# Download filtered results
st.download_button("📥 Download Results (CSV)", data=filtered_df.to_csv(index=False), file_name="filtered_landfill_papers.csv", mime="text/csv")

# Graphical Insights Section
st.subheader("📊 Visual Analytics")

def plot_papers_per_year(data):
    yearly = data['Year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    sns.barplot(x=yearly.index, y=yearly.values, ax=ax, palette="Blues_d")
    ax.set_title("📈 Number of Papers per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_domain_distribution(data):
    domain_counts = data['Domain'].value_counts()
    fig, ax = plt.subplots()
    domain_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax)
    ax.set_ylabel("")
    ax.set_title("🌐 Distribution of Research Domains")
    st.pyplot(fig)

def plot_country_trends(data):
    country_counts = data['Country'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(y=country_counts.index, x=country_counts.values, ax=ax, palette="Greens_d")
    ax.set_title("🌍 Top 10 Countries by Publication")
    ax.set_xlabel("Number of Papers")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# Show graphs based on filtered data
if not filtered_df.empty:
    plot_papers_per_year(filtered_df)
    plot_domain_distribution(filtered_df)
    plot_country_trends(filtered_df)

# Footer
st.markdown("---")
st.markdown("Created for enhanced exploration of engineered landfill research 🔬🚀")
