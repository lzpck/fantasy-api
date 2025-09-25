import httpx
import time
from typing import List, Optional
from app.models.player import Player

# Cache em memória
_cached_players: dict[str, Player] = {}
_last_fetch_time: Optional[float] = None
CACHE_TTL = 3600  # segundos (1 hora)


async def fetch_players() -> List[Player]:
    """
    Busca jogadores da API do Sleeper e retorna lista de objetos Player normalizados.
    Utiliza cache em memória com TTL de 1 hora para otimizar performance.
    
    Returns:
        List[Player]: Lista de jogadores com schema reduzido
    """
    global _cached_players, _last_fetch_time
    
    # Verificar se o cache é válido
    current_time = time.time()
    if (_cached_players and 
        _last_fetch_time is not None and 
        (current_time - _last_fetch_time) < CACHE_TTL):
        print("Retornando dados do cache")
        return list(_cached_players.values())
    
    print("Cache expirado ou vazio, buscando dados da API do Sleeper")
    url = "https://api.sleeper.app/v1/players/nfl"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            # Parse do JSON da resposta
            players_data = response.json()
            
            # Lista para armazenar jogadores normalizados
            players = []
            
            # Transformar cada jogador do formato Sleeper para nosso schema
            for player_id, player_info in players_data.items():
                try:
                    # Normalizar dados do jogador
                    normalized_player = Player(
                        id=player_id,
                        full_name=player_info.get("full_name", ""),
                        team=player_info.get("team"),  # Usar 'team' em vez de 'team_abbr'
                        fantasy_positions=player_info.get("fantasy_positions"),
                        status=player_info.get("status"),
                        injury_status=player_info.get("injury_status"),
                        years_exp=player_info.get("years_exp"),
                        birth_date=player_info.get("birth_date"),
                        number=player_info.get("number")
                    )
                    players.append(normalized_player)
                    
                except Exception as e:
                    # Log do erro mas continua processando outros jogadores
                    print(f"Erro ao processar jogador {player_id}: {e}")
                    continue
            
            # Atualizar cache como dicionário
            players_dict = {
                p.id: p for p in players
            }
            _cached_players = players_dict
            _last_fetch_time = current_time
            print(f"Cache atualizado com {len(players)} jogadores")
            
            return list(players_dict.values())
            
        except httpx.RequestError as e:
            print(f"Erro na requisição para API do Sleeper: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao buscar jogadores: {e}")
            return []


async def fetch_player_by_id(player_id: str) -> Player | None:
    """
    Busca um jogador específico pelo ID.
    Utiliza o cache em dicionário para busca otimizada.
    
    Args:
        player_id (str): ID do jogador
        
    Returns:
        Player | None: Jogador encontrado ou None se não existir
    """
    players = await fetch_players()
    return _cached_players.get(player_id)