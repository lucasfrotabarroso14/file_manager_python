from celery import Celery
import time

# Configure Celery
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # URL do Redis
    backend='redis://localhost:6379/0',  # URL do Redis
)

# Define uma tarefa simples
@celery.task
def upload_simulate_file():
    time.sleep(5)
    # Mensagem de conclusão após a contagem
    print("File uploaded successfully.")
    return

    # Aqui você pode adicionar a lógica real de upload do arquivo
    # No caso, como a tarefa não recebe um file_path, não estamos fazendo upload de nenhum arquivo



