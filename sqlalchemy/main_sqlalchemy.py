import sqlalchemy as sa

from fastapi_pagination import Page

# region create_engine 创建新的 Engine 实例。

# 链接格式 dialect[+driver]://user:password@host/dbname[?key=value..]
# dialect 是数据库名称，例如 mysql ， oracle ， postgresql
# driver 是DBAPI的名称，例如 psycopg2 ， pyodbc ， cx_oracle

# '/:memory:' 使用模块 in-memory-only
engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
args, kwargs = engine.dialect.create_connect_args(engine.url)
print(args, kwargs)
print("*" * 20)
with engine.connect() as conn:

    result = conn.execute(sa.text("select 'Hello World'"))
    print(result.all())

    conn.execute(sa.text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        sa.text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

    result = conn.execute(sa.text("select * from some_table"))
    # print(result.all())

    # for x, y in result:
    #     print("x：" + str(x))
    #     print("y：" + str(y))

    # for row in result:
    #     print(row)

    for dict_row in result.mappings():
        print(dict_row)

    stmt = sa.text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(
        y=6
    )

# endregion
