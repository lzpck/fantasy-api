from typing import Optional, List
from pydantic import BaseModel


class Player(BaseModel):
    """
    Modelo Pydantic para representar um jogador de NFL.
    Schema reduzido baseado nos dados da API do Sleeper.
    """
    id: str
    full_name: str
    team: Optional[str] = None
    fantasy_positions: Optional[List[str]] = None
    status: Optional[str] = None
    injury_status: Optional[str] = None
    years_exp: Optional[int] = None
    birth_date: Optional[str] = None
    number: Optional[int] = None