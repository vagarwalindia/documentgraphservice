from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #Postgres
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    #aws
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET: str
    S3_REGION: str

    #kafka
    KAFKA_BOOTSTRAP_SERVERS: str

    #redis
    REDIS_HOST: str
    REDIS_PORT: int

    ENV: str

    class Config:
        env_file = ".env.dev"
        case_sensitive = False

settings = Settings()