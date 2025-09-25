# Fantasy API

API FastAPI para gerenciamento de fantasy sports com foco em performance.

## Objetivo

Criar uma API robusta e performática para gerenciar ligas de fantasy sports, permitindo operações CRUD em jogadores, times e estatísticas.

## Estrutura do Projeto

```
fantasy_api/
├── app/
│   ├── __init__.py
│   ├── main.py         # ponto de entrada da aplicação
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py   # definição dos endpoints
│   └── core/
│       ├── __init__.py
│       └── config.py   # configuração da API (CORS, etc.)
├── tests/
│   └── test_health.py  # teste inicial do endpoint de saúde
├── requirements.txt
└── run.sh              # script para rodar o servidor com uvicorn
```

## Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Servidor

#### Usando o script (Linux/Mac):
```bash
./run.sh
```

#### Usando uvicorn diretamente (Windows/Linux/Mac):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acessar a API

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Endpoint de Saúde**: http://localhost:8000/health

## Como Rodar os Testes

```bash
pytest tests/
```

## Endpoints Disponíveis

- `GET /health` - Verificação de saúde da API

## Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI de alta performance
- **Pydantic** - Validação de dados
- **Pytest** - Framework de testes