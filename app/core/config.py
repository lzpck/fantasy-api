from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configurar_cors(app: FastAPI) -> None:
    """
    Configura CORS para permitir acesso de todos os domínios.
    Para desenvolvimento - em produção deve ser mais restritivo.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todos os domínios
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos os métodos HTTP
        allow_headers=["*"],  # Permite todos os headers
    )