"""
Configuration management for the application.
Loads environment variables and provides typed configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Database Configuration
    DATABASE_URL: str

    # JWT Configuration
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    # Application
    APP_NAME: str = "Todo App - Authentication API"
    APP_VERSION: str = "1.0.0"

    # Password Hashing
    BCRYPT_ROUNDS: int = 10

    # OpenAI Configuration (Phase III)
    OPENAI_API_KEY: str

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS_ORIGINS string into a list of allowed origins.
        Supports comma-separated values.
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
