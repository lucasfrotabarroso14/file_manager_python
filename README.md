# Desafio: Gerenciador de Arquivos

Este é um projeto de um gerenciador de arquivos simples, com recursos básicos de criação, edição e exclusão de arquivos, além da gestão de permissões e organizações.
### Executando o Projeto

Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina. Em seguida, siga estas etapas:

1. Clone o repositório do projeto:

    ```bash
    git clone https://github.com/lucasfrotabarroso14/file_manager_python.git
    ```

2. Crie o venv com o comando 

    ```bash
    python -m venv venv
    ```
    
3. Ative o venv

   
   Linux ou Mac:
    ```bash
    source venv/bin/activate
    ```

    Windows:
    ```bash
       .\venv\Scripts\activate
    ```




4. Instale as dependencias do projeto :
    ```bash
    pip install -r requirements.txt
    ```

   
5. Execute o comando Docker Compose para iniciar os contêineres e rodar os servicos do redis,mysql e admin:

    ```bash
    docker-compose up 
    ```

6. Digite na linha de comando o comando abaixo para criar as tabelas e popular dados:

    ```bash
    docker exec -i file_manager_python-db-1 mysql -u docker -pdocker file_manager < initial_data.sql

    ```

7. Para iniciar o backend python do certifique que está no diretorio raiz e digite :

    ```bash
    python main.py
    ```



## Rotas da API

### Organizações

- **Listar Organizações:** `GET /api/v1/organizations`

  Retorna uma lista de todas as organizações cadastradas.

- **Criar Organização:** `POST /api/v1/organizations`

  Cria uma nova organização com o nome especificado.

    Exemplo de requisição:
    ```json
    {
        "organization_name": "Nome da Organização"
    }
    ```

### Usuários

- **Criar Usuário:** `POST /api/v1/users`

  Cria um novo usuário e o associa a uma organização existente.

    Exemplo de requisição:
    ```json
    {
        "name": "Nome do Usuário",
        "email": "exemplo@email.com",
        "password": "senha123",
        "organization_id": 11
    }
    ```

- **Listar Todos os Usuários:** `GET /api/v1/users`

  Retorna uma lista de todos os usuários cadastrados.

### Arquivos

- **Upload de Arquivo:** `POST /api/v1/file`

  Faz o upload de um novo arquivo.

    - Exemplo de requisição para arquivo público:
    ```json
    {
        "file_name": "Nome do Arquivo",
        "file_type": "mp3",
        "file_size": 1,
        "uploader_user_id": 21,
        "permission_type": "Publico"
    }
    ```

    - Exemplo de requisição para arquivo com acesso selecionado:
    ```json
    {
        "file_name": "Nome do Arquivo",
        "file_type": "mp3",
        "file_size": 1,
        "uploader_user_id": 21,
        "permission_type": "Selecionados",
        "access_users_ids": [1, 4]
    }
    ```

- **Listar Todos os Arquivos:** `GET /api/v1/file`

  Retorna uma lista de todos os arquivos cadastrados.

- **Alterar Permissão de Arquivo:** `PUT /api/v1/file/<int:file_id>`

  Altera o tipo de permissão de um arquivo específico.

    Exemplo de requisição:
    ```json
    {
        "permission_type": "Geral"
    }
    ```

- **Deletar Arquivo:** `DELETE /api/v1/file/<int:file_id>`

  Remove um arquivo específico do sistema.

- **Listar Arquivos de um Usuário:** `GET /api/v1/user/files/<int:user_id>`

  Retorna uma lista de todos os arquivos aos quais um usuário específico tem acesso.

## Diagrama do Banco de Dados

![Diagrama do Banco de Dados](https://i.imgur.com/mFAU8pA.png)

## Docker Compose

Este projeto utiliza o Docker Compose para orquestrar os contêineres necessários. O arquivo `docker-compose.yml` contém as configurações para os serviços de banco de dados MySQL, Adminer (interface web para gerenciamento de banco de dados) e Redis (utilizado para cache de dados).


### Usando Cache de Dados com Redis

O sistema utiliza o Redis como uma solução de cache de dados para otimizar o desempenho da API, especialmente na busca de arquivos de um usuário específico.

Aqui está um exemplo de como o Redis é usado para armazenar em cache os arquivos de um usuário:

```python
class UserDetail(Resource):
    def __init__(self):
        self.redis_client = RedisClient()

    def get(self, user_id):
        try:
            # Código para buscar arquivos de um usuário específico...

            if available_files:
                file_id = available_files[0]['id']
                cached_data = self.redis_client.get_cache(f"file_{file_id}")
                if cached_data is not None and len(cached_data.get('result', [])) > 0:
                    return cached_data
                else:
                    self.redis_client.set_cache(f"file_{file_id}", response)

            return response

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }
```

