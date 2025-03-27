from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine, event, Pool, text, NullPool
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .config import DatabaseConfig


class DatabaseInstance:
    def __init__(self, config: DatabaseConfig):
        self.db_user = config.get('db_user')
        self.db_password = config.get('db_password')
        self.db_host_write = config.get('db_host')
        self.db_host_read = config.get('db_host_read') or self.db_host_write
        self.db_port = config.get('db_port')
        self.db_name = config.get('db_name')
        self.db_ssl = config.get('db_ssl', False)
        self.db_pool_size = config.get('db_pool_size', None)
        self.db_max_overflow = config.get('db_max_overflow', 0)

        self.active_connections = 0

        # Build connection URLs for sync and async for both write and read.
        db_url = config.get('db_url')
        db_url_read = config.get('db_url_read')

        if db_url:
            self.database_path_write = db_url
            self.async_database_path_write = (
                db_url
                .replace("postgresql://", "postgresql+asyncpg://", 1)
                .replace("sslmode=require", "ssl=require", 1)
            )
        else:
            self.database_path_write = self._build_database_url(async_mode=False, host=self.db_host_write)
            self.async_database_path_write = self._build_database_url(async_mode=True, host=self.db_host_write)

        if db_url_read:
            self.database_path_read = db_url_read
            self.async_database_path_read = (
                db_url_read
                .replace("postgresql://", "postgresql+asyncpg://", 1)
                .replace("sslmode=require", "ssl=require", 1)
            )
        else:
            self.database_path_read = self._build_database_url(async_mode=False, host=self.db_host_read)
            self.async_database_path_read = self._build_database_url(async_mode=True, host=self.db_host_read)

        # Database settings
        db_settings = self._initialize_db_settings()

        # Create synchronous engines for write and read.
        self.engine_write = create_engine(self.database_path_write, **db_settings)
        self.engine_read = create_engine(self.database_path_read, **db_settings)

        self.write_session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine_write,
            expire_on_commit=True
        ))
        self.read_session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine_read,
            expire_on_commit=True
        ))

        # Create asynchronous engines for write and read.
        self.async_engine_write = create_async_engine(self.async_database_path_write, **db_settings)
        self.async_engine_read = create_async_engine(self.async_database_path_read, **db_settings)
        self.async_write_session = async_sessionmaker(
            bind=self.async_engine_write,
            class_=AsyncSession,
            expire_on_commit=True,
            autocommit=False,
            autoflush=False
        )
        self.async_read_session = async_sessionmaker(
            bind=self.async_engine_read,
            class_=AsyncSession,
            expire_on_commit=True,
            autocommit=False,
            autoflush=False
        )

        # Declarative base for ORM models
        self.base = declarative_base(name="Base")

    def _build_database_url(self, async_mode=False, host=None):
        if host is None:
            host = self.db_host_write
        scheme = "postgresql+asyncpg" if async_mode else "postgresql"
        url = f"{scheme}://{self.db_user}:{self.db_password}@{host}:{self.db_port}/{self.db_name}"
        if self.db_ssl:
            url += "?ssl=require" if async_mode else "?sslmode=require"
        return url

    def _initialize_db_settings(self):
        db_settings = {"pool_pre_ping": True, "echo": False}

        if self.db_pool_size:
            db_settings.update({
                "pool_size": self.db_pool_size,
                "pool_recycle": 300,
                "pool_use_lifo": True,
                "max_overflow": self.db_max_overflow,
            })
        else:
            db_settings["poolclass"] = NullPool

        return db_settings

    def session_local(self):
        return self.write_session()

    def session_local_read(self):
        return self.read_session()

    def get_db(self, force: str = None):
        if force == 'read':
            db = self.session_local_read()
        else:
            db = self.session_local()

        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    def get_db_cm(self, force: str = None):
        if force == 'read':
            db = self.session_local_read()
        else:
            db = self.session_local()

        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get_db_read(self):
        yield from self.get_db(force="read")

    def get_db_write(self):
        yield from self.get_db(force="write")

    @contextmanager
    def get_db_cm_read(self):
        with self.get_db_cm(force="read") as db:
            yield db

    @contextmanager
    def get_db_cm_write(self):
        with self.get_db_cm(force="write") as db:
            yield db

    def create_tables(self):
        self.base.metadata.create_all(self.engine_write)

    def close_all_connections(self):
        self.engine_write.dispose()
        self.engine_read.dispose()
        print("All connections closed gracefully.")

    def setup_connection_monitoring(self):
        @event.listens_for(Pool, "connect")
        def connect_listener(dbapi_connection, connection_record):
            self.active_connections += 1
            print(f"New database connection created. Total active connections: {self.active_connections}")

        @event.listens_for(Pool, "close")
        def close_listener(dbapi_connection, connection_record):
            self.active_connections -= 1
            print(f"A database connection closed. Total active connections: {self.active_connections}")

    def check_database_health(self):
        try:
            with self.engine_write.connect() as connection:
                connection.execute(text("SELECT 1"))

            with self.engine_read.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False

    def async_session_local(self):
        return self.async_write_session()

    def async_session_local_read(self):
        return self.async_read_session()

    async def async_get_db(self, force: str = None):
        if force == 'read':
            db = self.async_session_local_read()
        else:
            db = self.async_session_local()

        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

    @asynccontextmanager
    async def async_get_db_cm(self, force: str = None):
        if force == 'read':
            db = self.async_session_local_read()
        else:
            db = self.async_session_local()

        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

    async def async_get_db_read(self):
        async for db in self.async_get_db(force="read"):
            yield db

    async def async_get_db_write(self):
        async for db in self.async_get_db(force="write"):
            yield db

    @asynccontextmanager
    async def async_get_db_cm_read(self):
        async with self.async_get_db_cm(force="read") as db:
            yield db

    @asynccontextmanager
    async def async_get_db_cm_write(self):
        async with self.async_get_db_cm(force="write") as db:
            yield db
