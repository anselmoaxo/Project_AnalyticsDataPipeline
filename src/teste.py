from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtendo as variáveis de ambiente
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Verifica se as variáveis de ambiente foram carregadas corretamente
if None in [DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD]:
    raise ValueError("Uma ou mais variáveis de ambiente não foram encontradas.")

# Montando a URL de conexão
url = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print("URL de conexão:", url)

# Função para criar e retornar a engine do SQLAlchemy
def get_db_engine():
    try:
        # Criando o engine
        engine = create_engine(url)
        print("Engine criada com sucesso!")
        return engine
    except Exception as e:
        print(f"Ocorreu um erro ao criar a engine: {e}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    engine = get_db_engine()
    if engine:
        # Aqui você pode testar a conexão com o banco de dados, se necessário
        try:
            with engine.connect() as connection:
                print("Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
