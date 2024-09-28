from src.faker_generate import gerar_dados_postgres 
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Definir argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir a DAG
dag = DAG(
    'ingestao_dados_faker_postgres',
    default_args=default_args,
    description='Ingestão de dados Faker no Dataset',
    schedule_interval='@daily',  # Você pode ajustar o schedule_interval conforme a necessidade
    catchup=False
)


# Tarefa para gerar e inserir dados no PostgreSQL
generate_data_task = PythonOperator(
    task_id='gerar_dados',
    python_callable=gerar_dados_postgres,
    op_args=['postgres_conn'],  # Nome da conexão do Airflow para PostgreSQL
    dag=dag,
)

# Definir a sequência das tarefas
generate_data_task
