import ssl
from typing import Optional

from os.path import exists, join

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from config.config_reader import env_config



class DbSession:
    """
    ## Класс для инициализации асинхронной сессии для работы с базой данных.

    ### Этот класс использует `SQLAlchemy` для создания асинхронного движка и сессии, \
    позволяя взаимодействовать с базой данных в асинхронном режиме.
    """
    def __init__(self, *,
        url: str = env_config.DATABASE_URL_asyncpg,
        echo: bool = False,
        pool_size: int = 20,  # Ограничение от 5 до 20
        max_overflow: int = 20,  # Ограничение от 5 до 20
        ssl_ca: Optional[str] = None,
        ssl_cert: Optional[str] = None,
        ssl_key: Optional[str] = None,
    ) -> None:
        """
        ## Инициализирует экземпляр `DbSession`.

        Args:
            url (str): URL подключения к базе данных.
            echo (bool): Если True, выводит SQL-запросы в консоль.
            pool_size (int): Максимальное количество соединений в пуле.
            max_overflow (int): Максимальное количество соединений, \
                которые могут быть созданы сверх pool_size.
            ssl_ca (Optional[str]): Путь к CA сертификату.
            ssl_cert (Optional[str]): Путь к клиентскому сертификату.
            ssl_key (Optional[str]): Путь к клиентскому ключу.
        
        ## Пример использования:
        ```python
        self.AsyncSessionLocal: AsyncSession = dc_db_session.AsyncSessionLocal
            async with (session or self.AsyncSessionLocal()) as session:
                pass
        ```
        """
        self.url: str = url
        self.echo: bool = echo
        self.pool_size: int = pool_size
        self.max_overflow: int = max_overflow
        self.ssl_ca: Optional[str] = ssl_ca  # Путь к CA сертификату
        self.ssl_cert: Optional[str] = ssl_cert  # Путь к клиентскому сертификату
        self.ssl_key: Optional[str] = ssl_key  # Путь к клиентскому ключу
        self.engine: AsyncEngine = None  # Асинхронный движок
        self.AsyncSessionLocal: AsyncSession = None  # Асинхронный менеджер сессий
        self._post_init()
        
    def _post_init(self) -> None:
        """ ## Выполняет методы после инициализации """
        self.__create_engine()
        self.__create_async_session()
        
    def __create_engine(self) -> None:
        """  ## Создаёт движок для работы с БД """
        # Добавляем параметры SSL в URL
        self.engine = create_async_engine(
            url=self.url,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_recycle=1800,  # Перезапуск соединения каждые 30 минут
            pool_timeout=30,     # Время ожидания получения соединения из пула (30 секунд)
            pool_pre_ping=True,     # Проверка соединения перед его использованием
            connect_args=self.ssl_args
        )

    @property
    def ssl_args(self) -> dict[str, ssl.SSLContext]:
        """ ## Создаём SSL контекст для подключения """
        if not all(map(exists, [self.ssl_ca, self.ssl_cert, self.ssl_key])):
            raise FileNotFoundError("SSL certificate files not found")

        context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH,
            cafile=self.ssl_ca
        )
        context.load_cert_chain(
            certfile=self.ssl_cert,
            keyfile=self.ssl_key
        )
        context.check_hostname = False  # Добавляем проверку hostname
        context.verify_mode = ssl.CERT_NONE
        return {"ssl": context}

    def __create_async_session(self) -> None:
        """  ## Создаёт асинхронную сессию для работы с БД """
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=True
        )
        
    async def db_close(self, engine: Optional[AsyncEngine] = None) -> None:
        """
        ## Закрывает соединение с базой данных
        
        ### Args:
            engine (Optional[AsyncEngine]): асинхронный движок.
        
        ### Пример использования:
        ```python
        async def stop(self, session: Optional[DbSession] = None):
            session = self.db_session if not session else session
                    await session.db_close(session.engine)
        ```
        """
        engine = self.engine if not engine else engine
        await engine.dispose()


session_echo = False
session_echo = True  # Для логов в консоль 

# Директория сертификатов
certs_dir = join('app', 'certs')

# Пример использования
db_session = DbSession(  # Объект сессии базы данных
    url=env_config.DATABASE_URL_asyncpg,
    pool_size=20,
    max_overflow=20,
    echo=session_echo,
    ssl_ca=join(certs_dir, 'ca.pem'),      # Укажите путь к CA сертификату
    ssl_cert=join(certs_dir, 'server.pem'), # Укажите путь к клиентскому сертификату
    ssl_key=join(certs_dir, 'server.key')    # Укажите путь к клиентскому ключу
)