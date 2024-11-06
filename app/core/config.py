from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = '<Заголовок не найден в файле конфигураций>'
    description: str = '<Описание не найдено в файле конфигураций>'
    database_url: str
    secret: str = 'secret'

    class Config:
        env_file: str = '.env'


settings = Settings()
