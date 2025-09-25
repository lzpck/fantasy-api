from sqlalchemy import Column, String, Integer, Boolean
from app.core.database import Base


class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    team = Column(String, nullable=True)
    position = Column(String, nullable=True)
    status = Column(String, nullable=True)
    injury_status = Column(String, nullable=True)
    years_exp = Column(Integer, nullable=True)
    birth_date = Column(String, nullable=True)
    number = Column(Integer, nullable=True)

    # Ownership tracking
    rostered_by = Column(String, nullable=True)  # user_id / team_id
    is_free_agent = Column(Boolean, default=True)