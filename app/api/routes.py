from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.player import Player
from app.services.sleeper import fetch_players, fetch_player_by_id
from app.services.sync import sync_players
from app.models.player_db import PlayerDB
from app.core.database import SessionLocal
from sqlalchemy.future import select

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


@router.post("/sync")
async def sincronizar_jogadores():
    """
    Endpoint para forçar sincronização dos jogadores com a API Sleeper.
    Atualiza a base de dados PostgreSQL com os dados mais recentes.
    
    Returns:
        dict: Mensagem de sucesso com total de jogadores sincronizados
    """
    try:
        total = await sync_players()
        return {"message": f"{total} jogadores sincronizados com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na sincronização: {str(e)}")


@router.get("/waivers")
async def obter_waivers():
    """
    Endpoint para obter jogadores disponíveis no waiver wire.
    Retorna apenas jogadores que não estão em nenhum roster (is_free_agent=True).
    
    Returns:
        List[PlayerDB]: Lista de jogadores livres
    """
    try:
        async with SessionLocal() as session:
            result = await session.execute(
                select(PlayerDB).where(PlayerDB.is_free_agent == True)
            )
            players = result.scalars().all()
            return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar waivers: {str(e)}")


@router.post("/roster/{player_id}")
async def adicionar_ao_roster(player_id: str, user_id: str):
    """
    Endpoint para adicionar um jogador ao roster de um usuário.
    Remove o jogador do waiver wire e o atribui ao usuário especificado.
    
    Args:
        player_id (str): ID do jogador
        user_id (str): ID do usuário/time
        
    Returns:
        dict: Mensagem de confirmação
    """
    try:
        async with SessionLocal() as session:
            player = await session.get(PlayerDB, player_id)
            if not player:
                raise HTTPException(status_code=404, detail="Jogador não encontrado")
            
            if not player.is_free_agent:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Jogador já está no roster de {player.rostered_by}"
                )
            
            player.rostered_by = user_id
            player.is_free_agent = False
            await session.commit()
            
            return {"message": f"{player.full_name} adicionado ao roster de {user_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar ao roster: {str(e)}")


@router.post("/release/{player_id}")
async def liberar_jogador(player_id: str):
    """
    Endpoint para liberar um jogador de volta para o waiver wire.
    Remove o jogador do roster atual e o marca como free agent.
    
    Args:
        player_id (str): ID do jogador
        
    Returns:
        dict: Mensagem de confirmação
    """
    try:
        async with SessionLocal() as session:
            player = await session.get(PlayerDB, player_id)
            if not player:
                raise HTTPException(status_code=404, detail="Jogador não encontrado")
            
            if player.is_free_agent:
                raise HTTPException(
                    status_code=400, 
                    detail="Jogador já está disponível no waiver wire"
                )
            
            old_owner = player.rostered_by
            player.rostered_by = None
            player.is_free_agent = True
            await session.commit()
            
            return {"message": f"{player.full_name} liberado do roster de {old_owner} para waivers"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao liberar jogador: {str(e)}")