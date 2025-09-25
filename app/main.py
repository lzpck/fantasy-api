from fastapi import FastAPI
from app.api.routes import router
from app.core.config import configurar_cors

# Criar instância da aplicação FastAPI
app = FastAPI(
    title="Fantasy API",
    description="API para gerenciamento de fantasy sports",
    version="1.0.0"
)

# Configurar CORS
configurar_cors(app)

# Incluir rotas
app.include_router(router)