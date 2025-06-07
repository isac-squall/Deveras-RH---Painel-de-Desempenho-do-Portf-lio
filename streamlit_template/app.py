import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Deveras RH - Portfolio Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load data
@st.cache_data
def load_data():
    # Load the processed data
    try:
        df = pd.read_csv('assets/processed_data.csv')
        # Convert currency columns to numeric
        df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def load_summary():
    # Load the summary data
    try:
        summary = pd.read_csv('assets/portfolio_summary.csv')
        return summary
    except Exception as e:
        st.error(f"Error loading summary data: {e}")
        return None

# Function to display portfolio metrics
def display_metrics(df, summary):
    st.subheader("Portfolio Overview")
    
    # Row 1 - Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_portfolio = summary['total_value'].sum()
    total_contracts = summary['n_contracts'].sum()
    valid_contracts = summary['n_valid_contracts'].sum()
    avg_value = total_portfolio / valid_contracts if valid_contracts > 0 else 0
    
    col1.metric("Total Portfolio Value", f"R$ {total_portfolio:,.2f}")
    col2.metric("Total Contracts", f"{int(total_contracts):,}")
    col3.metric("Valid Contracts", f"{int(valid_contracts):,} ({valid_contracts/total_contracts*100:.1f}%)")
    col4.metric("Avg Contract Value", f"R$ {avg_value:,.2f}")

# Function to create unit performance visualization
def unit_performance(summary):
    st.subheader("Operating Unit Performance")
    if summary is None or summary.empty:
        st.warning("Nenhum dado de unidade disponível.")
        return

    # Sort by total value
    sorted_summary = summary.sort_values(by='total_value', ascending=False)

    # Create bar chart for total values
    fig = px.bar(
        sorted_summary,
        x=sorted_summary.index,
        y='total_value',
        color='total_value',
        labels={'total_value': 'Portfolio Value (R$)', 'index': 'Operating Unit'},
        title='Total Portfolio Value by Operating Unit',
        color_continuous_scale='Viridis',
        text_auto='.2s'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Create metrics for top units
    st.subheader("Top Operating Units")
    cols = st.columns(3)

    # Display top 3 units
    for i, (idx, row) in enumerate(sorted_summary.head(3).iterrows()):
        if i < len(cols):
            col_metric = f"R$ {row['total_value']:,.2f}" if 'total_value' in row else "N/A"
            col_contracts = f"{row['n_valid_contracts']} contracts" if 'n_valid_contracts' in row else "N/A"
            cols[i].metric(f"{idx}", col_metric, col_contracts)
            # Só mostra avg_value/top_operator se existirem
            avg_value = f"Avg: R$ {row['avg_value']:,.2f}" if 'avg_value' in row else ""
            top_operator = f"Top Operator: {row['top_operator']}" if 'top_operator' in row else ""
            if avg_value or top_operator:
                cols[i].caption(f"{avg_value} | {top_operator}")

# Function to analyze contract status
def status_analysis(df, summary):
    st.subheader("Contract Status Analysis")
    if df is None or df.empty or summary is None or summary.empty:
        st.warning("Dados insuficientes para análise de status.")
        return

    # Filter for units with data
    valid_units = summary[summary['n_valid_contracts'] > 0].index.tolist()
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_unit = st.selectbox(
            "Select Operating Unit",
            options=["ALL"] + valid_units
        )
        if selected_unit != "ALL":
            if 'UNIDADE OPERADORA' in df.columns:
                filtered_df = df[df['UNIDADE OPERADORA'] == selected_unit]
            else:
                st.error("Coluna 'UNIDADE OPERADORA' não encontrada nos dados.")
                return
        else:
            filtered_df = df

        if 'STATUS' not in filtered_df.columns:
            st.error("Coluna 'STATUS' não encontrada nos dados.")
            return

        status_counts = filtered_df['STATUS'].value_counts().reset_index()
        status_counts.columns = ['STATUS', 'Count']
        total = status_counts['Count'].sum()
        st.metric("Total Contracts", f"{total:,}")

        st.subheader("Top Statuses")
        for i, row in status_counts.head(5).iterrows():
            st.caption(f"{row['STATUS']}: {row['Count']:,} ({row['Count']/total*100:.1f}%)")

    with col2:
        if not status_counts.empty:
            fig = px.pie(
                status_counts.head(10),
                values='Count',
                names='STATUS',
                title=f"Status Distribution for {selected_unit if selected_unit != 'ALL' else 'All Units'}"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum status encontrado para a seleção.")

# Function to analyze operators
def operator_analysis(df):
    st.subheader("Insurance Operator Analysis")
    if df is None or df.empty:
        st.warning("Dados insuficientes para análise de operadoras.")
        return

    if 'UNIDADE OPERADORA' not in df.columns or 'NF' not in df.columns:
        st.error("Colunas necessárias ('UNIDADE OPERADORA' ou 'NF') não encontradas nos dados.")
        return

    units = df['UNIDADE OPERADORA'].unique().tolist()
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_unit = st.selectbox(
            "Select Operating Unit",
            options=["ALL"] + units,
            key="operator_unit_filter"
        )
        if selected_unit != "ALL":
            filtered_df = df[df['UNIDADE OPERADORA'] == selected_unit]
        else:
            filtered_df = df

        operator_counts = filtered_df['NF'].value_counts().reset_index()
        operator_counts.columns = ['Operator', 'Count']
        total = operator_counts['Count'].sum()
        st.metric("Total Contracts", f"{total:,}")

        st.subheader("Top Operators")
        for i, row in operator_counts.head(5).iterrows():
            st.caption(f"{row['Operator']}: {row['Count']:,} ({row['Count']/total*100:.1f}%)")

    with col2:
        if not operator_counts.empty:
            fig = px.bar(
                operator_counts.head(10),
                x='Operator',
                y='Count',
                title=f"Top 10 Operators for {selected_unit if selected_unit != 'ALL' else 'All Units'}",
                color='Count',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum operador encontrado para a seleção.")

# Function to analyze contract values
def value_analysis(df, summary):
    st.subheader("Contract Value Analysis")
    if df is None or df.empty or summary is None or summary.empty:
        st.warning("Dados insuficientes para análise de valores.")
        return

    if 'UNIDADE OPERADORA' not in df.columns or 'VALOR' not in df.columns:
        st.error("Colunas necessárias ('UNIDADE OPERADORA' ou 'VALOR') não encontradas nos dados.")
        return

    valid_units = summary[summary['n_valid_contracts'] > 0].index.tolist()
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_unit = st.selectbox(
            "Select Operating Unit",
            options=["ALL"] + valid_units,
            key="value_unit_filter"
        )
        if selected_unit != "ALL":
            filtered_df = df[df['UNIDADE OPERADORA'] == selected_unit]
        else:
            filtered_df = df

        filtered_df = filtered_df[filtered_df['VALOR'].notna() & (filtered_df['VALOR'] > 0)]

        if filtered_df.empty:
            st.info("Nenhum contrato válido encontrado para a seleção.")
            return

        total_value = filtered_df['VALOR'].sum()
        avg_value = filtered_df['VALOR'].mean()
        min_value = filtered_df['VALOR'].min()
        max_value = filtered_df['VALOR'].max()

        st.metric("Total Value", f"R$ {total_value:,.2f}")
        st.metric("Average Value", f"R$ {avg_value:,.2f}")
        st.metric("Min Value", f"R$ {min_value:,.2f}")
        st.metric("Max Value", f"R$ {max_value:,.2f}")

    with col2:
        if not filtered_df.empty:
            fig = px.histogram(
                filtered_df,
                x='VALOR',
                nbins=20,
                title=f"Contract Value Distribution for {selected_unit if selected_unit != 'ALL' else 'All Units'}"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum valor para exibir no histograma.")

# Function to display pre-generated visualizations
def show_visualizations():
    st.subheader("Portfolio Visualizations")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Total by Unit", "Contract Count", "Avg Contract Value", "Status Distribution", "Operator Distribution"])
    
    with tab1:
        try:
            img = Image.open("assets/total_portfolio_by_unit.png")
            st.image(img, caption="Total Portfolio Value by Operating Unit")
        except Exception as e:
            st.error(f"Could not load image: {e}")
    
    with tab2:
        try:
            img = Image.open("assets/contract_count_by_unit.png")
            st.image(img, caption="Contract Count by Operating Unit")
        except Exception as e:
            st.error(f"Could not load image: {e}")
    
    with tab3:
        try:
            img = Image.open("assets/avg_contract_by_unit.png")
            st.image(img, caption="Average Contract Value by Operating Unit")
        except Exception as e:
            st.error(f"Could not load image: {e}")
    
    with tab4:
        try:
            img = Image.open("assets/status_distribution_by_unit.png")
            st.image(img, caption="Status Distribution by Operating Unit")
        except Exception as e:
            st.error(f"Could not load image: {e}")
    
    with tab5:
        try:
            img = Image.open("assets/operator_distribution_by_unit.png")
            st.image(img, caption="Operator Distribution by Operating Unit")
        except Exception as e:
            st.error(f"Could not load image: {e}")

# Main function to run the app
def main():
    # Sidebar
    st.sidebar.title("Deveras RH")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092113.png", width=100)
    st.sidebar.subheader("Portfolio Performance Dashboard")
    
    # Load data
    df = load_data()
    summary = load_summary()
    
    if df is not None and summary is not None:
        # Main dashboard
        st.title("📊 Deveras RH - Portfolio Performance Dashboard")
        
        # Tabs for different analysis sections
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Status Analysis", "Operator Analysis", "Value Analysis"])
        
        with tab1:
            display_metrics(df, summary)
            unit_performance(summary)
            show_visualizations()
        
        with tab2:
            status_analysis(df, summary)
        
        with tab3:
            operator_analysis(df)
        
        with tab4:
            value_analysis(df, summary)
            
        # Data explorer
        st.subheader("Data Explorer")
        with st.expander("View Raw Data"):
            st.dataframe(df.head(100))
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Full Data as CSV",
                data=csv,
                file_name="deveras_portfolio_data.csv",
                mime="text/csv"
            )
    else:
        st.error("Failed to load necessary data. Please check file paths and formats.")

# Run the app
if __name__ == "__main__":
    main()