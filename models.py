from typing import List, Optional, Annotated
from pydantic import BaseModel, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    API_KEY: str
    DEBUG_MODE: bool = False
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

class Product(BaseModel):
    id: Annotated[int, Field(description="The unique identifier for a product")]
    name: str
    price: float
    tags: List[str]
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('name cannot be empty')
        return v

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('price must be positive')
        return v
