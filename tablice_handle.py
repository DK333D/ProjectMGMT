from fastapi import APIRouter, Request
import help
import logging
from typing import List

router: APIRouter = APIRouter()

def select_tablice_by_query(request: Request, query: str):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request, query,
                                       "tablice.html")


@router.get('/tablice', description="Wybierz wszystkie tablice")
def select_tablice(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request,
                                       'SELECT  t.id, t."Nazwa", t."Opis", p."Nazwa" FROM "Tablica" t INNER JOIN public."Projekt" p on p.id = t."Projekt_ID"'
                                       , "tablice.html")

@router.get('/tablice_z_0_zadaniami', description="")
def f1():
    return help.try_query_get_table('SELECT id, "Nazwa", "Liczba zadan" \
                            FROM "tablice_z_0_zadaniami"')

@router.get('/tablice_z_min_1_zadaniem', description="")
def f2():
    return help.try_query_get_table('SELECT  id, "Nazwa", "Liczba zadan" \
                            FROM "tablice_z_min_1_zadaniem"')

@router.get('/tablice_z_suma_punktow_mniejsza_niz_100', description="")
def f3():
    return help.try_query_get_table('SELECT  id, "Nazwa", "Punkty" \
                            FROM "tablice_z_suma_punktow_mniejsza_niz_100"')

@router.get('/tablice_z_liczba_punktow_minimum_100', description="")
def f4():
    return help.try_query_get_table('SELECT  id, "Nazwa", "Punkty" \
                            FROM "tablice_z_liczba_punktow_minimum_100"')

@router.post('/dodaj_tablica', description="Dodaj tablica")
async def insert_tablica(request: Request):
    form = await request.form()
    nazwa: str = form.get('Nazwa')
    opis: str = form.get('Opis')
    projekt_id: int = form.get('Projekt_ID')
    connection = None
    try:

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Tablica' table
        insert_query = 'INSERT INTO "Tablica" ("Nazwa", "Opis", "Projekt_ID") VALUES ($1, $2, $3)'

        # Printing the query with parameters
        final_query = insert_query\
            .replace('$1', f"'{nazwa}'") \
            .replace('$2', f"'{opis}'") \
            .replace('$3', f"'{projekt_id}'")

        await connection.execute(
            final_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_tablica/{_id}', description="Usuń tablica")
async def delete_tablica(_id: int):
    await help.delete_id_from_table(_id, "Tablica")


@router.get("/pobierz_projekty", response_model=List)
def pobierz_projekty():
    return help.try_query_get_table('SELECT id, p."Nazwa", "Opis" FROM "Projekt" p')
