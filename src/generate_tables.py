from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()



# Configurações básicas
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# Inicializa o motor de conexão
engine = create_engine(DATABASE_URL, echo=True)

# Base para os modelos ORM
Base = declarative_base()

# Definição das tabelas
class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(), nullable=False)  # Adicionando CNPJ
    endereco = Column(String(255), nullable=False)  # Adicionando Endereço
    uf = Column(String(2), nullable=False)  # Adicionando UF

    vendas = relationship("Venda", back_populates="cliente")

class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(), nullable=False)  # Adicionando CNPJ
    endereco = Column(String(255), nullable=False)  # Adicionando Endereço
    uf = Column(String(2), nullable=False)  # Adicionando UF

    produtos = relationship("Produto", back_populates="fornecedor")

class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)  # Alterando 'nome' para 'descricao'
    quantidade = Column(Integer, nullable=False)  # Adicionando quantidade
    preco = Column(Numeric(10, 2), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    vendas = relationship("Venda", back_populates="produto")

class Compra(Base):
    __tablename__ = 'compras'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    data_compra = Column(Date, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_compra = Column(Numeric(10, 2), nullable=False)  # Adicionando preco_compra
    
    produto = relationship("Produto")

class Venda(Base):
    __tablename__ = 'vendas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    data_venda = Column(Date, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_venda = Column(Numeric(10, 2), nullable=False)  # Adicionando preco_venda
    
    cliente = relationship("Cliente", back_populates="vendas")
    produto = relationship("Produto", back_populates="vendas")

def verificar_tabelas_existentes(engine, tabela_nome):
    inspetor = inspect(engine)
    return inspetor.has_table(tabela_nome)

def criar_tabelas(engine):
    tabelas = ['clientes', 'fornecedores', 'produtos', 'compras', 'vendas']
    
    for tabela in tabelas:
        if not verificar_tabelas_existentes(engine, tabela):
            print(f"A tabela '{tabela}' não existe. Criando agora...")
            Base.metadata.create_all(engine)  # Cria a tabela
        else:
            print(f"A tabela '{tabela}' já existe. Nenhuma ação necessária.")

Session = sessionmaker(bind=engine)
session = Session()

def main():
    criar_tabelas(engine)
    print("Verificação completa.")

if __name__ == "__main__":
    main()
