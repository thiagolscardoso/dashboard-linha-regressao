import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr


# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Regressão Linear",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard de Regressão Linear")
st.markdown("Visualize dados, calcule a regressão linear e analise as métricas.")

# --- Sidebar para Seleção de Fonte de Dados ---
st.sidebar.header("Configuração de Dados")
data_source = st.sidebar.radio(
    "Selecione a Fonte de Dados:",
    ("Gerar Dados", "Carregar Arquivo Excel")
)

# --- Variáveis para armazenar os dados X e Y ---
data_x = None
data_y = None
df = None

# --- Lógica de Geração/Carregamento de Dados ---

if data_source == "Gerar Dados":
    st.sidebar.subheader("Geração de Dados")

    # Campos para renomear os eixos
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Opcional: Renomear Eixos**")
    custom_x_label = st.sidebar.text_input("Novo Rótulo para Eixo X (Opcional):", value="X")
    custom_y_label = st.sidebar.text_input("Novo Rótulo para Eixo Y (Opcional):", value="Y")

    data_type = st.sidebar.radio(
        "Tipo de Geração:",
        ("Com Correlação (Tendência)", "Sem Correlação (Ruído Puro)", "Simular Correlação")
    )
    
    r_squared_target = None
    if data_type == "Simular Correlação":
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Simulação de Correlação**")
        r_squared_target = st.sidebar.slider(
            "R² Desejado (0.001 a 1.0):",
            min_value=0.001,
            max_value=1.0,
            value=0.8,
            step=0.001,
            format="%.3f",
            help="Define o Coeficiente de Determinação (R²) que o modelo tentará simular."
        )

    # Configuração Opcional de Outliers
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Opcional: Adicionar Outliers**")
    outlier_enabled = st.sidebar.checkbox("Incluir Outliers Extremos (X, Y)")
    
    outlier_value = None
    n_outliers = 0
    
    if outlier_enabled:
        outlier_value = st.sidebar.number_input(
            "Valor do Outlier (Ex: 1000 para X e Y):",
            value=1000.0,
            step=100.0
        )
        n_outliers = st.sidebar.number_input(
            "Quantidade de Outliers:",
            min_value=1,
            value=1,
            step=1
        )
    
    n_points = st.sidebar.number_input(
        "Quantidade de Pontos a Gerar:",
        min_value=10,
        max_value=1000000,
        value=100,
        step=10
    )

    if st.sidebar.button("Gerar Dados"):
        # Armazena os rótulos personalizados
        st.session_state['custom_x_label'] = custom_x_label if custom_x_label else 'X'
        st.session_state['custom_y_label'] = custom_y_label if custom_y_label else 'Y'
        # Valores padrão para ranges (usados para a geração de dados base)
        x_min_val, x_max_val = 0.0, 100.0
        y_min_val, y_max_val = 0.0, 200.0
        x_range = x_max_val - x_min_val
        y_range = y_max_val - y_min_val

        if data_type == "Com Correlação (Tendência)":
            # Geração de dados com uma leve tendência linear
            np.random.seed(42) # Para reprodutibilidade
            
            # Gera X uniformemente distribuído no range padrão
            data_x = np.random.rand(n_points) * x_range + x_min_val
            
            # Gera Y com tendência linear e ruído
            # y = 1.5*x + 10 + ruído
            data_y = 1.5 * data_x + 10 + np.random.randn(n_points) * 20
            
        elif data_type == "Sem Correlação (Ruído Puro)":
            # Geração de dados completamente aleatórios (ruído puro)
            np.random.seed(42) # Para reprodutibilidade
            
            # Gera X e Y uniformemente distribuídos no range padrão
            data_x = np.random.rand(n_points) * x_range + x_min_val
            data_y = np.random.rand(n_points) * y_range + y_min_val
        
        elif data_type == "Simular Correlação":
            # Lógica para gerar dados com R² próximo ao alvo
            # O coeficiente de correlação (r) é a raiz quadrada do R² (assumindo inclinação positiva)
            r_target = np.sqrt(r_squared_target)
            
            # Gera X e Y com correlação específica usando np.random.multivariate_normal
            # Matriz de covariância: [[variância_x, covariância], [covariância, variância_y]]
            # Covariância = r * desvio_padrao_x * desvio_padrao_y
            
            # Define desvios padrão para X e Y
            std_x = x_range / 6  # Aproximadamente 99.7% dos dados estarão dentro de 3 desvios padrão
            std_y = y_range / 6
            
            # Calcula a covariância
            cov = r_target * std_x * std_y
            
            # Matriz de covariância
            cov_matrix = [[std_x**2, cov], [cov, std_y**2]]
            
            # Gera os dados
            mean = [x_min_val + x_range/2, y_min_val + y_range/2]
            data = np.random.multivariate_normal(mean, cov_matrix, n_points)
            
            data_x = data[:, 0]
            data_y = data[:, 1]
            
            # Garante que os dados estejam dentro dos limites visuais (embora a geração multivariada possa extrapolar)
            data_x = np.clip(data_x, x_min_val, x_max_val)
            data_y = np.clip(data_y, y_min_val, y_max_val)
        
        # Adiciona os outliers, se habilitado
        if outlier_enabled and outlier_value is not None and n_outliers > 0:
            outlier_array = np.full(n_outliers, outlier_value)
            data_x = np.append(data_x, outlier_array)
            data_y = np.append(data_y, outlier_array)
        
        # Cria o DataFrame com os rótulos padrão (X e Y)
        df = pd.DataFrame({'X': data_x, 'Y': data_y})
        st.session_state['df'] = df
        st.session_state['x_col'] = 'X'
        st.session_state['y_col'] = 'Y'

elif data_source == "Carregar Arquivo Excel":
    st.sidebar.subheader("Carregar Arquivo Excel")
    uploaded_file = st.sidebar.file_uploader(
        "Escolha um arquivo Excel (.xls, .xlsx)",
        type=["xls", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            # Leitura do arquivo Excel
            df = pd.read_excel(uploaded_file)
            st.session_state['df'] = df
            
            st.sidebar.success("Arquivo carregado com sucesso!")
            
            # Seleção de colunas
            all_columns = df.columns.tolist()
            
            if all_columns:
                # Tenta pré-selecionar colunas com nomes comuns
                default_x = all_columns[0]
                default_y = all_columns[1] if len(all_columns) > 1 else all_columns[0]
                
                x_col = st.sidebar.selectbox(
                    "Selecione a Coluna para o Eixo X:",
                    all_columns,
                    index=all_columns.index(default_x) if default_x in all_columns else 0
                )
                
                y_col = st.sidebar.selectbox(
                    "Selecione a Coluna para o Eixo Y:",
                    all_columns,
                    index=all_columns.index(default_y) if default_y in all_columns else (1 if len(all_columns) > 1 else 0)
                )
                
                # Armazena as colunas selecionadas no session_state
                st.session_state['x_col'] = x_col
                st.session_state['y_col'] = y_col
                
                # Armazena os rótulos personalizados (usa o nome da coluna como padrão)
                st.session_state['custom_x_label'] = x_col
                st.session_state['custom_y_label'] = y_col
                
                # Converte as colunas selecionadas para arrays numpy
                data_x = df[x_col].values
                data_y = df[y_col].values
                
            else:
                st.error("O arquivo Excel não contém colunas de dados.")
                df = None
                st.session_state['df'] = None
                
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            df = None
            st.session_state['df'] = None

# --- Lógica Principal do Dashboard ---

# Verifica se há dados disponíveis (seja por geração ou upload)
if 'df' in st.session_state and st.session_state['df'] is not None:
    df = st.session_state['df']
    x_col = st.session_state['x_col']
    y_col = st.session_state['y_col']
    
    # Obtém os rótulos personalizados ou usa os nomes das colunas
    custom_x_label = st.session_state.get('custom_x_label', x_col)
    custom_y_label = st.session_state.get('custom_y_label', y_col)
    
    # Garante que as colunas selecionadas existam e sejam numéricas
    if x_col in df.columns and y_col in df.columns:
        try:
            # Limpeza e conversão para numérico (ignora erros para manter a robustez)
            data_x = pd.to_numeric(df[x_col], errors='coerce').dropna().values
            data_y = pd.to_numeric(df[y_col], errors='coerce').dropna().values
            
            # Alinha os dados (apenas pares completos)
            min_len = min(len(data_x), len(data_y))
            data_x = data_x[:min_len]
            data_y = data_y[:min_len]
            
            if min_len < 2:
                st.warning("Dados insuficientes para regressão linear (mínimo de 2 pontos).")
            else:
                # --- 1. Cálculo da Regressão Linear ---
                
                # Redimensiona X para o formato exigido pelo scikit-learn (n_samples, n_features)
                X = data_x.reshape(-1, 1)
                Y = data_y
                
                model = LinearRegression()
                model.fit(X, Y)
                
                # Previsões da linha de regressão
                y_pred = model.predict(X)
                
                # --- 2. Cálculo das Métricas ---
                
                # Coeficiente de Determinação (R²)
                r_squared = model.score(X, Y)
                
                # Coeficiente de Correlação de Pearson (r)
                # scipy.stats.pearsonr retorna (r, p-value)
                r, p_value = pearsonr(data_x, data_y)
                
                # --- 3. Visualização ---
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader("Gráfico de Dispersão e Linha de Regressão")
                    
                    # Cria um DataFrame para o Plotly
                    plot_df = pd.DataFrame({
                        x_col: data_x,
                        y_col: data_y,
                        'Regressão': y_pred
                    })
                    
                    # Gráfico de Dispersão (Scatter Plot)
                    fig = px.scatter(
                        plot_df, 
                        x=x_col, 
                        y=y_col, 
                        title=f"Regressão Linear: {custom_y_label} vs {custom_x_label}"
                    )
                    
                    # Adiciona a Linha de Regressão
                    fig.add_scatter(
                        x=plot_df[x_col], 
                        y=plot_df['Regressão'], 
                        mode='lines', 
                        name='Linha de Regressão',
                        line=dict(color='red', width=3)
                    )
                    
                    # Atualiza layout para melhor visualização
                    fig.update_layout(
                        hovermode="x unified",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        xaxis_title=custom_x_label,
                        yaxis_title=custom_y_label
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'modeBarButtonsToRemove': ['toggleHover', 'sendDataToCloud', 'hoverClosestCartesian', 'hoverCompareCartesian', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'select2d', 'lasso2d', 'toggleSpikelines']})
                    
                with col2:
                    st.subheader("Métricas de Regressão")
                    
                    # Exibição das Métricas
                    st.metric(
                        label=f"Coeficiente de Correlação (r) entre {custom_x_label} e {custom_y_label}", 
                        value=f"{r:.4f}",
                        help="Mede a força e a direção da relação linear entre as variáveis X e Y. Varia de -1 a +1."
                    )
                    
                    st.metric(
                        label=f"Coeficiente de Determinação (R²) para {custom_y_label}", 
                        value=f"{r_squared:.4f}",
                        help="Representa a proporção da variância na variável dependente (Y) que é previsível a partir da variável independente (X). Varia de 0 a 1."
                    )
                    
                    st.markdown("---")
                    st.subheader("Equação da Linha")
                    st.info(f"**{custom_y_label} = {model.coef_[0]:.4f} * {custom_x_label} + {model.intercept_:.4f}**")
                    
        except Exception as e:
            st.error(f"Erro no processamento dos dados ou cálculo da regressão: {e}")
            st.warning("Verifique se as colunas selecionadas contêm dados numéricos válidos.")
    else:
        st.warning("Selecione colunas válidas para X e Y.")

else:
    st.info("Selecione uma fonte de dados na barra lateral para começar.")

# --- Fim do Script ---
