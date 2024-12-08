from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str 
    
    @model_validator
    def get_database_url(cls, v):
        v["DATABASE_URL"] = f"postgresql+asyncpg://{v["DB_USER"]}:{v["DB_PASS"]}@{v["DB_HOST"]}:{v["DB_PORT"]}/{v["DB_NAME"]}"
        return v
    
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str 
    
    @model_validator
    def get_test_database_url(cls, v):
        v["TEST_DATABASE_URL"] = f"postgresql+asyncpg://{v["TEST_DB_USER"]}:{v["TEST_DB_PASS"]}@{v["TEST_DB_HOST"]}:{v["TEST_DB_PORT"]}/{v["TEST_DB_NAME"]}"
        return v
    
    BROKER: str
    
    USER: str
    PASSWORD: str
        
    
    class Config:
        env_file = ".env"
    
settings = Settings()    

