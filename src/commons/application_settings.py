from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):

    openai_api_key : str
    ws_token:str
    url_becat: str
    

    class Config:
        env_file = ".env"

