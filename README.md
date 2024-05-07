# # Desafio: Gerenciador de Arquivos

Este é um projeto de um gerenciador de arquivos simples, com recursos básicos de criação, edição e exclusão de arquivos, além da gestão de usuários e organizações.

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

    Exemplo de requisição para arquivo público:
    ```json
    {
        "file_name": "Nome do Arquivo",
        "file_type": "mp3",
        "file_size": 1,
        "uploader_user_id": 21,
        "permission_type": "Publico"
    }
    ```

    Exemplo de requisição para arquivo com acesso selecionado:
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

---

Este é um esboço básico da API para o gerenciador de arquivos. Sinta-se à vontade para adaptá-lo conforme suas necessidades específicas!
