from fastapi import APIRouter
from typing import List, Optional
from app.models.player import Player
from app.services.sleeper import fetch_players

router = APIRouter()


@router.get("/health")
async def verificar_saude():
    """
    Endpoint de verificação de saúde da API.
    Retorna status ok quando a aplicação está funcionando.
    """
    return {"status": "ok"}


@router.get("/players", response_model=List[Player])
async def obter_jogadores(
    team: Optional[str] = None,
    position: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Endpoint para obter lista de jogadores da NFL.
    Busca dados da API do Sleeper e retorna formato normalizado.
    
    Args:
        team: Filtrar por time (ex: 'KC', 'SF')
        position: Filtrar por posição (ex: 'QB', 'RB', 'WR')
        status: Filtrar por status (ex: 'Active', 'Inactive')
    
    Returns:
        List[Player]: Lista de jogadores com schema reduzido
    """
    players = await fetch_players()
    
    # Aplicar filtros se fornecidos
    if team:
        players = [p for p in players if p.team and p.team.lower() == team.lower()]
    
    if position:
        players = [p for p in players if p.fantasy_positions and any(pos.lower() == position.lower() for pos in p.fantasy_positions)]
    
    if status:
        players = [p for p in players if p.status and p.status.lower() == status.lower()]
    
    return players