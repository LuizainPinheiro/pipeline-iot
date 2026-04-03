# Pipeline de Dados IoT - Monitoramento de Temperatura 🌡️

Este projeto foi desenvolvido para a disciplina de **IoT, Big Data e IA**. Ele consiste em um pipeline que automatiza a leitura, armazenamento e visualização de dados de sensores de temperatura.

## 🚀 Tecnologias Utilizadas
* **Python 3.12**: Linguagem principal para processamento de dados.
* **Docker**: Utilizado para rodar o banco de dados PostgreSQL em um ambiente isolado.
* **PostgreSQL**: Banco de dados relacional para persistência das leituras.
* **Pandas & SQLAlchemy**: Bibliotecas para ETL (Extração, Transformação e Carga).
* **Streamlit**: Framework para criação do Dashboard interativo.

## 📂 Estrutura do Projeto
* `data/`: Contém o arquivo CSV original (Kaggle).
* `src/processamento.py`: Script que lê o CSV e envia para o banco de dados no Docker.
* `src/dashboard.py`: Aplicação web que consulta o banco e gera gráficos.
* `venv/`: Ambiente virtual para isolamento de dependências.

## 🛠️ Como Executar
1. Iniciar o contêiner do banco: `docker start postgres-iot`
2. Ativar o ambiente virtual: `.\venv\Scripts\activate`
3. Rodar o processamento: `python src/processamento.py`
4. Abrir o Dashboard: `streamlit run src/dashboard.py`