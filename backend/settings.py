from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Literal


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD'] = Field('DEV')

    DB_USERNAME: str = Field('postgres')
    DB_PASSWORD: str = Field('password')
    DB_HOST: str = Field('localhost')
    DB_PORT: int = Field('5432')
    DB_NAME: str = Field('db')

    @model_validator(mode='before')
    def get_database_url(cls, v):
        v["DB_URL"] = f"postgresql+asyncpg://{v['DB_USERNAME']}:{v['DB_PASSWORD']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v
    
    TEST_DB_USERNAME: str = Field('postgres')
    TEST_DB_PASSWORD: str = Field('password')
    TEST_DB_HOST: str = Field('localhost')
    TEST_DB_PORT: int = Field(5432)
    TEST_DB_NAME: str = Field('db')

    @model_validator(mode='before')
    def get_test_database_url(cls, v):
        v["TEST_DB_URL"] = f"postgresql+asyncpg://{v['TEST_DB_USERNAME']}:{v['TEST_DB_PASSWORD']}@{v['TEST_DB_HOST']}:{v['TEST_DB_PORT']}/{v['TEST_DB_NAME']}"
        return v

    ACCESS_SECRET_KEY: str = Field()
    ACCESS_EXPIRE_MINUTES: int = Field()

    REFRESH_SECRET_KEY: str = Field()
    REFRESH_EXPIRE_MINUTES: int = Field()

    model_config = SettingsConfigDict(env_file='../.env', extra='allow')


settings = Settings()