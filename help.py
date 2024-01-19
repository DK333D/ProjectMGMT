# Uzupełnij dane użytkownika do bazy danych


import sqlite3
from sqlite3 import Error
from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException
import asyncpg
import psycopg2
from pydantic import BaseModel
from passlib.context import CryptContext

templates = Jinja2Templates(directory="templates")
SECRET_KEY = "your_secret_key"

# User model
class User(BaseModel):
    email: str
    haslo: str

# User model
class UserAll(BaseModel):
    imie: str
    nazwisko: str
    haslo: str
    email: str
    stanowisko_ID: int

def get_template_try_query(request: Request, query: str, webpage):
    connection = None
    try:
        connection = create_connection()
        result = execute_read_query(connection, query)
        return templates.TemplateResponse(webpage, {"request": request, "result": result, "session_data": request.session.get('email'), "isAdmin": request.session.get('isAdmin')})
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if connection:
            connection.close()


def get_template_no_query(request: Request, webpage):
    try:
        return templates.TemplateResponse(webpage, {"request": request, "result": None, "session_data": request.session.get('email')})
    except Exception as e:
        return f"Error: {str(e)}"


def try_query_get_table(query: str):
    connection = None
    try:
        connection = create_connection()
        result = execute_read_query(connection, query)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if connection:
            connection.close()


def create_connection_sqlite(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Establish an async PostgreSQL connection
async def create_async_connection():
    dbname = ''
    user = ''
    password = ''
    host = ''
    port = ''
    # Replace with your actual PostgreSQL database credentials
    conn = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn


def create_connection():
    dbname = ''
    user = ''
    password = ''
    host = ''
    port = ''

    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return connection

async def execute_insert_query(connection, query):
    connection = None
    try:
        connection = await help.create_async_connection()
        connection.execute(query)
        connection.commit()
        print("Record inserted successfully")

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data:", error)

    finally:
        if connection:
            connection.close()
            print("Connection is closed")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


async def get_FK_table_names(tabela: str):
    connection = None
    try:
        connection = await create_async_connection()
        query: str = """
        SELECT tc.table_name,
               kcu.column_name,
               ccu.table_name  AS foreign_table_name,
               ccu.column_name AS foreign_column_name

        FROM information_schema.table_constraints AS tc
                 JOIN
             information_schema.key_column_usage AS kcu
             ON tc.constraint_name = kcu.constraint_name
                 JOIN
             information_schema.constraint_column_usage AS ccu
             ON ccu.constraint_name = tc.constraint_name
        WHERE
            constraint_type = 'FOREIGN KEY'
          AND
            tc.table_name = {tabela};"""
        return

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas wczytywania: {str(e)}")

    finally:
        if connection:
            await connection.close()

async def delete_id_from_table(_id: int, tabela: str):
    connection = None
    if _id is not None:
        try:
            connection = await create_async_connection()
            delete_query = 'DELETE FROM "{}" WHERE "id" = $1'.format(tabela)
            await connection.execute(delete_query, _id)

            return
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Błąd podczas usuwania: {str(e)}")

        finally:
            if connection:
                await connection.close()

async def remove_admin_for_id(_id: int, tabela: str):
    connection = None
    if _id is not None:
        try:
            connection = await create_async_connection()
            delete_query = 'UPDATE "{}" SET "Administrator"=\'false\' WHERE "id" = $1'.format(tabela)
            await connection.execute(delete_query, _id)

            return
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Błąd podczas usuwania: {str(e)}")

        finally:
            if connection:
                await connection.close()

async def add_admin_for_id(_id: int, tabela: str):
    connection = None
    if _id is not None:
        try:
            connection = await create_async_connection()
            # DELETE query
            delete_query = 'UPDATE "{}" SET "Administrator"=\'true\' WHERE "id" = $1'.format(tabela)
            # Execute the DELETE query
            await connection.execute(delete_query, _id)

            return
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Błąd podczas usuwania: {str(e)}")

        finally:
            if connection:
                await connection.close()

    raise HTTPException(status_code=400, detail="Nie udało się usunąć - brak rekordu w bazie")


async def verify_user(email: str, haslo: str):
    connection = None
    try:
        connection = await create_async_connection()
        # query
        query = 'SELECT "Email", "Haslo" from "Osoba" WHERE "Email" = $1'
        final_query = query.replace('$1', f"'{email}'")
        # Execute the query
        result = try_query_get_table(final_query)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if(pwd_context.verify(haslo, result[0][1])):
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas weryfikacji użytkownika: {str(e)}")

    finally:
        if connection:
            await connection.close()


def check_if_user_exists(email: str):
    connection = None
    try:
        connection = create_connection()
        query = 'SELECT "Email" from "Osoba" WHERE "Email" = $1'
        final_query = query.replace('$1', f"'{email}'")
        result = try_query_get_table(final_query)
        print(result)
        return len(result) > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas weryfikacji użytkownika: {str(e)}")

    finally:
        if connection:
            connection.close()

def verify_user_is_admin(email: str):
    connection = None
    try:
        connection = create_connection()
        # query
        query = 'SELECT "Email" from "Osoba" WHERE "Email" = $1 AND "Administrator"=true'
        final_query = query.replace('$1', f"'{email}'")
        # Execute the query
        result = try_query_get_table(final_query)
        print(result)
        return len(result) > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas weryfikacji użytkownika: {str(e)}")

    finally:
        if connection:
            connection.close()
