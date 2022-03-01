from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_dsn: Optional[str] = 'postgresql://postgres@localhost:5432/wmp_backend'

    class Config:
        fields = {
            'port': {'env': 'PORT'},
            'pg_dsn': {'env': 'DATABASE_URL'},
        }
