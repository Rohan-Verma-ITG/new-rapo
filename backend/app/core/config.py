from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Shopify AI Helpdesk"
    env: str = "development"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "shopify_helpdesk"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 1440

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    shopify_store_domain: str = ""
    shopify_admin_token: str = ""
    shopify_webhook_secret: str = ""

    mailgun_signing_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
