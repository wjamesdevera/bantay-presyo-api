from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

database_file = "db.sqlite3"
sql_database_url = f"sqlite:///{database_file}"

engine = create_engine(sql_database_url, echo=True)

Session = sessionmaker(bind=engine)
