from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import JSON, Integer, String

POSTGRES_PASSWORD = "123"
POSTGRES_USER = "postgres"
POSTGRES_DB = "swapi_hw"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5431"

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeopleHW(Base):
    __tablename__ = "swapi_people_hw"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(Integer, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(10), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(20), nullable=True)
    films: Mapped[str] = mapped_column(String(512), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(20), nullable=True)
    height: Mapped[str] = mapped_column(String(10), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(100), nullable=True)
    mass: Mapped[str] = mapped_column(String(10), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    species: Mapped[str] = mapped_column(String(256), nullable=True)
    starships: Mapped[str] = mapped_column(String(256), nullable=True)
    vehicles: Mapped[str] = mapped_column(String(256), nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
