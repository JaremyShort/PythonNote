import sqlalchemy as sa

engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
