from sqlalchemy.future import select
from app.services.sleeper import fetch_players
from app.models.player_db import PlayerDB
from app.core.database import SessionLocal


async def sync_players():
    """
    Sincroniza jogadores da API Sleeper com o banco PostgreSQL.
    Insere novos jogadores e atualiza os existentes.
    Por padrão, todos os jogadores são marcados como free agents.
    """
    players = await fetch_players()
    
    async with SessionLocal() as session:
        for p in players:
            # Busca jogador existente no banco
            db_player = await session.get(PlayerDB, p.id)
            
            if not db_player:
                # Cria novo jogador
                db_player = PlayerDB(
                    id=p.id,
                    full_name=p.name,
                    team=p.team,
                    position=p.position,
                    status=p.status,
                    injury_status=p.injury_status,
                    years_exp=p.years_exp,
                    birth_date=p.birth_date,
                    number=p.number,
                    rostered_by=None,
                    is_free_agent=True,
                )
                session.add(db_player)
            else:
                # Atualiza jogador existente (mantém ownership)
                db_player.full_name = p.name
                db_player.team = p.team
                db_player.position = p.position
                db_player.status = p.status
                db_player.injury_status = p.injury_status
                db_player.years_exp = p.years_exp
                db_player.birth_date = p.birth_date
                db_player.number = p.number
        
        await session.commit()
    
    return len(players)