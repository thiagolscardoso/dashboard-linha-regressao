_# Dashboard de Regressão Linear com Streamlit

Este é um aplicativo de dashboard interativo construído com a biblioteca Streamlit em Python. O objetivo principal do aplicativo é visualizar um conjunto de pontos em um gráfico de dispersão e traçar uma linha de regressão linear sobre esses pontos, além de analisar as métricas de correlação.

## Funcionalidades

O aplicativo oferece diversas funcionalidades para geração e análise de dados:

*   **Geração de Dados:**
    *   **Com Correlação (Tendência):** Gera dados com uma tendência linear clara.
    *   **Sem Correlação (Ruído Puro):** Gera dados completamente aleatórios (ruído branco).
    *   **Simular Correlação:** Permite ao usuário definir um Coeficiente de Determinação (R²) desejado para simular dados com um nível de correlação específico.
*   **Carregar Arquivo Excel:** Permite o upload de arquivos `.xls` ou `.xlsx` e a seleção das colunas para os eixos X e Y.
*   **Adicionar Outliers:** Opção para adicionar um número customizável de outliers com um valor definido, para analisar seu impacto na regressão.
*   **Renomear Eixos:** Campos de texto para renomear os eixos X e Y, que são refletidos no gráfico e nas métricas.
*   **Visualização Interativa:** Exibe um gráfico de dispersão com a linha de regressão sobreposta, utilizando a biblioteca Plotly Express.
*   **Métricas de Regressão:** Apresenta de forma clara o **Coeficiente de Correlação (r)**, o **Coeficiente de Determinação (R²)** e a **Equação da Linha**.

## Como Executar o Aplicativo Localmente

Para executar o dashboard em seu ambiente local, siga os passos abaixo:

### 1. Pré-requisitos

*   Python 3.7 ou superior.
*   `pip` (gerenciador de pacotes do Python).

### 2. Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_SEU_REPOSITORIO>
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com o conteúdo abaixo e execute o comando `pip install -r requirements.txt`.

    **Conteúdo do `requirements.txt`:**
    ```
    streamlit
    pandas
    numpy
    plotly
    scikit-learn
    scipy
    openpyxl
    ```

### 3. Execução

Com as dependências instaladas, execute o seguinte comando no terminal:

```bash
streamlit run streamlit_dashboard_v5.py
```

O Streamlit abrirá automaticamente o aplicativo em seu navegador padrão.

## Publicação no Streamlit Community Cloud

Para publicar o aplicativo online:

1.  Certifique-se de que os arquivos `streamlit_dashboard_v5.py` e `requirements.txt` estejam no seu repositório GitHub público.
2.  Crie uma conta no [Streamlit Community Cloud](https://streamlit.io/cloud).
3.  Clique em **"New App"** e conecte seu repositório, selecionando o branch e o caminho para o arquivo principal (`streamlit_dashboard_v5.py`).
4.  Clique em **"Deploy!"**.
