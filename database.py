from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Docker'da PostgreSQL'i diğer projelerle çakışmasın diye 5433 portuna bağlamıştık.
# Kullanıcı adı ve şifre kısımlarını docker-compose.yml dosyandaki ayarlara göre yazdık (varsayılan: postgres)
SQLALCHEMY_DATABASE_URL = "postgresql://admin:123456@localhost:5433/hotspot_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()