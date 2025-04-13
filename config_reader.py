from typing import Literal, Union

from os import getenv
from os.path import join

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr



class DotEnvConfig(BaseSettings):
    """
    ## Используется для чтения информации из .env файла

    ### Пример использования:
    dot_env_config = DotEnvConfig()
    admin_id = int(config.ADMIN_ID.get_secret_value())
    """
    # Желательно вместо str использовать SecretStr 
    
    # База данных Data Collector
    POSTGRES_DB: SecretStr
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: SecretStr
    POSTGRES_PORT: SecretStr # convert to int


    @property
    def DATABASE_URL_asyncpg(self):
        """ ## Строка подключения к базе данных Data Collector """
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER.get_secret_value()}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRES_HOST.get_secret_value()}:"
            f"{self.POSTGRES_PORT.get_secret_value()}"
            f"/{self.POSTGRES_DB.get_secret_value()}"
        )
    
    # Начиная со второй версии pydantic, настройки класса настроек задаются
    # через model_config
    # В данном случае будет использоваться файла .env, который будет прочитан
    # с кодировкой UTF-8
    # Указываем путь к .env файлу
    
    model_config = SettingsConfigDict(env_file=join('.env'), env_file_encoding='utf-8')


class ServerEnvConfig(BaseSettings):
    """
    ## Используется для получения инфы из переменных сред сервера.
    
    ### Пример использования:
        dot_env_config = DotEnvConfig()
        admin_id = int(config.ADMIN_ID.get_secret_value())
    """
    # База данных Data Collector
    POSTGRES_DB: SecretStr = SecretStr(getenv("POSTGRES_DB"))
    POSTGRES_USER: SecretStr = SecretStr(getenv("POSTGRES_USER"))
    POSTGRES_PASSWORD: SecretStr = SecretStr(getenv("POSTGRES_PASSWORD"))
    POSTGRES_HOST: SecretStr = SecretStr(getenv("POSTGRES_HOST"))
    POSTGRES_PORT: SecretStr = SecretStr(getenv("POSTGRES_PORT"))  # convert to int


    @property
    def DATABASE_URL_asyncpg(self):
        """ ## Строка подключения к базе данных Data Collector """
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER.get_secret_value()}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRES_HOST.get_secret_value()}:"
            f"{self.POSTGRES_PORT.get_secret_value()}"
            f"/{self.POSTGRES_DB.get_secret_value()}"
        )
        

    model_config = SettingsConfigDict()  # Убираем env_file, так как мы не используем .env файл


class GetEnv:
    """
    ## Создаёт объект конфигурации env.
    
    ### Args:
        set_env (Literal['dot_env', 'git_lab_env']): dot_env получает информацию из .env файла\
        , а git_lab_env получает переменные окружения от GitLab. По-умолчанию 'dot_env'.

    ### Пример использования:
        # ge = GetEnv(set_env='dot_env')
        ge = GetEnv(set_env='server_env')
        config = ge.config
        token = config.BOT_TOKEN.get_secret_value()
    """
    def __init__(self, set_env: Literal['dot_env', 'server_env'] = 'dot_env') -> None:
        self.config: Union[DotEnvConfig, ServerEnvConfig] = None
        self.set_env: Literal['dot_env', 'server_env'] = set_env
        self._make_env()

    def __make_dot_env(self) -> None:
        """ ## Создание объекта конфигурации для .env . """
        self.config = DotEnvConfig()

    def __make_server_env(self) -> None:
        """ ## Создание объекта конфигурации для переменных сервера. """
        self.config = ServerEnvConfig()

    def _make_env(self) -> None:
        """
        ## Создаёт объект конфигурации env.
        ### Проверяет какой env был выбран и запускает его создание.
        """ 
        if self.set_env == 'dot_env':
            self.__make_dot_env()
        elif self.set_env == 'server_env':
            self.__make_server_env()
    
            
            
ge = GetEnv(set_env='dot_env')
env_config: DotEnvConfig  = ge.config