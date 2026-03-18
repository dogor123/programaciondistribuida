import aiomysql
import asyncio

async def get_connection():
    try:
        conn = await aiomysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='admin1234',
            db='citas_db'
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise e
