from typing import Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    dev_mode: bool = False
    pg_dsn: Optional[str] = 'postgresql://postgres@localhost:5432/wmp_backend'

    @validator('pg_dsn')
    def heroku_ready_pg_dsn(cls, v):
        return v.replace('gres://', 'gresql://')

    class Config:
        fields = {
            'dev_mode': {'env': 'DEV_MODE'},
            'port': {'env': 'PORT'},
            'pg_dsn': {'env': 'DATABASE_URL'},
        }
