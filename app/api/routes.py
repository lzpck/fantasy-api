from fastapi import APIRouter
from typing import List, Optional
from app.models.player import Player
from app.services.sleeper import fetch_players, fetch_player_by_id

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


@router.get("/players/{player_id}", response_model=Player)
async def get_player(player_id: str):
    """
    Endpoint para obter um jogador específico pelo ID.
    Utiliza cache otimizado para busca individual.
    
    Args:
        player_id (str): ID do jogador
        
    Returns:
        Player: Dados do jogador ou erro se não encontrado
    """
    player = await fetch_player_by_id(player_id)
    if not player:
        return {"error": "Player not found"}
    return player