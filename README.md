# Sistema de Enquetes

API para criação e gerenciamento de enquetes com autenticação de usuários.

## Funcionalidades

- Registro e login de usuários
- Criação de enquetes
- Sistema de votação
- Listagem de enquetes
- Cache de dados

## Tecnologias

- Python 3.9+
- Flask
- MongoDB
- Redis
- JWT

## Como usar

1. **Instale as dependências**

```bash
pip install -r requirements.txt
```

2. **Configure o .env**

```env
MONGO_CONNECTION_STRING=sua_connection_string
MONGO_DATABASE_NAME=nome_do_banco
JWT_SECRET=sua_chave_secreta
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
```

3. **Execute o projeto**
```bash
python run.py
```

## Endpoints

### Autenticação
```bash
POST /auth/register
{
    "username": "usuario",
    "email": "usuario@email.com",
    "password": "senha123"
}

POST /auth/login
{
    "email": "usuario@email.com",
    "password": "senha123"
}
```

### Enquetes
```bash
# Criar enquete
POST /polls
{
    "title": "Sua enquete",
    "options": [
        {"text": "Opção 1"},
        {"text": "Opção 2"}
    ]
}

# Votar
POST /polls/{poll_id}/vote
{
    "option_index": 0
}

# Buscar enquete
GET /polls/{poll_id}

# Listar enquetes
GET /polls

# Enquetes do usuário
GET /polls/user
```

## Testes

```bash
# Executar testes
pytest -v 
```

## Estrutura

```
src/
├── controllers/    # Regras de negócio
├── models/         # Acesso a dados
├── services/       # Serviços auxiliares
├── validators/     # Validações
├── views/          # Rotas
├── errors/         # Tratamento de erros
└── main/           # Configuração da aplicação
```

