from fastapi import APIRouter, Request
import help
import logging
from typing import List

router: APIRouter = APIRouter()


@router.get('/zadania', description="Wybierz wszystkie zadania")
def select_zadania(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request,
                          'select z.id, z."Tytul", z."Opis", z."Utworzenie_Data", z."Koniec_Data", z."Priorytet", z."Punkty", T."Nazwa" from "Zadanie" z INNER JOIN public."Tablica" T on T.id = z."Tablica_ID"',
                          "zadania.html")


@router.post('/dodaj_zadanie', description="Dodaj zadanie")
async def insert_zadanie(request: Request):
    form = await request.form()
    tytul: str = form.get('Tytul')
    opis: str = form.get('Opis')
    utworzenie_data = form.get('Utworzenie_Data')
    koniec_data = form.get('Koniec_Data')

    priorytet = form.get('Priorytet')
    punkty = form.get('Zadanie_Punkty')
    tablica_id = form.get('Tablica_ID')

    connection = None
    try:

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Zadanie' table
        insert_query = 'insert into "Zadanie" ("Tytul", "Opis", "Utworzenie_Data", "Koniec_Data", "Priorytet", "Punkty", "Tablica_ID") VALUES ($1, $2, $3, $4, $5, $6, $7);'

        # Printing the query with parameters
        final_query = insert_query.replace('$1', f"'{tytul}'")\
            .replace('$2', f"'{opis}'")\
            .replace('$3', f"'{utworzenie_data}'")\
            .replace('$4', f"'{koniec_data}'")\
            .replace('$5', f"'{priorytet}'")\
            .replace('$6', f"'{punkty}'")\
            .replace('$7', f"'{tablica_id}'")\

        await connection.execute(
            final_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_zadanie/{_id}', description="Usuń zadanie")
async def delete_zadanie(_id: int):
    await help.delete_id_from_table(_id, "Zadanie")


@router.get("/pobierz_tablice", response_model=List)
def pobierz_projekty():
    return help.try_query_get_table('SELECT id, t."Nazwa", t."Opis" FROM "Tablica" t')
