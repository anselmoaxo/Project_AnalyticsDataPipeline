import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random
import logging
from airflow.hooks.base_hook import BaseHook
from sqlalchemy.exc import SQLAlchemyError


# Configuração de logging
logger = logging.getLogger(__name__)

# Inicializando o Faker
fake = Faker('pt_BR')

def gerar_dados_postgres(postgres_conn_id):
    try:
        # Recupera a conexão do Airflow
        conn = BaseHook.get_connection(postgres_conn_id)
        
        # Criação da string de conexão
        postgres_url = f"postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        
        # Conexão com PostgreSQL via SQLAlchemy
        engine = create_engine(postgres_url)

        logger.info("Conexão com o banco de dados estabelecida.")

        # Gerar Clientes
        num_clientes = 50
        clientes = [{
            'nome': fake.company(),
            'cnpj': fake.cnpj(),
            'endereco': fake.address(),
            'uf': fake.state_abbr()
        } for _ in range(num_clientes)]

        df_clientes = pd.DataFrame(clientes)
        df_clientes.to_sql('clientes', con=engine, if_exists='append', index=False)

        # Gerar Fornecedores
        num_fornecedores = 10
        fornecedores = [{
            'nome': fake.company(),
            'cnpj': fake.cnpj(),
            'endereco': fake.address(),
            'uf': fake.state_abbr()
        } for _ in range(num_fornecedores)]

        df_fornecedores = pd.DataFrame(fornecedores)
        df_fornecedores.to_sql('fornecedores', con=engine, if_exists='append', index=False)

        # Gerar Produtos
        num_produtos = 100
        df_fornecedores_ids = pd.read_sql("SELECT id FROM fornecedores", con=engine)
        produtos = []
        for _ in range(num_produtos):
            produto_nome = fake.catch_phrase()
            fornecedor_id = random.choice(df_fornecedores_ids['id'].tolist())
            preco = round(random.uniform(10.0, 500.0), 2)
            quantidade = random.randint(1, 100)  # Adicionando quantidade

            produtos.append({
                'descricao': produto_nome,
                'fornecedor_id': fornecedor_id,
                'preco': preco,
                'quantidade': quantidade
            })

        df_produtos = pd.DataFrame(produtos)
        df_produtos.to_sql('produtos', con=engine, if_exists='append', index=False)

        # Aqui, é importante garantir que pegamos os IDs dos produtos recém-inseridos no banco
        df_produtos_ids = pd.read_sql("SELECT id FROM produtos", con=engine)

        # Gerar Vendas
        df_clientes_ids = pd.read_sql("SELECT id FROM clientes", con=engine)
        num_vendas = 150
        vendas = []
        for _ in range(num_vendas):
            cliente_id = random.choice(df_clientes_ids['id'].tolist())
            produto_id = random.choice(df_produtos_ids['id'].tolist())  # Garantindo que o produto_id seja válido
            data_venda = fake.date_this_year()
            quantidade = random.randint(1, 10)
            preco_venda = round(random.uniform(15.0, 600.0), 2)

            vendas.append({
                'cliente_id': cliente_id,
                'produto_id': produto_id,
                'data_venda': data_venda,
                'quantidade': quantidade,
                'preco_venda': preco_venda
            })

        df_vendas = pd.DataFrame(vendas)
        df_vendas.to_sql('vendas', con=engine, if_exists='append', index=False)

        logger.info("Dados gerados e inseridos no PostgreSQL com sucesso!")

    except SQLAlchemyError as e:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
