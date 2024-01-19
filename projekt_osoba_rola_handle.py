from fastapi import APIRouter, Request
import help
from typing import List

router: APIRouter = APIRouter()


@router.get('/projekt_osoba_role', description="Wybierz wszystkie projekt_osoba_role")
def select_projekt_osoba_role(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request,
                          """SELECT por.id, p."Nazwa" AS "Nazwa projektu", o."Imie" || \' \' || o."Nazwisko" AS "Osoba", r."Nazwa" AS "Rola"
                            FROM "Projekt_Osoba_Rola" por
                            INNER JOIN "Projekt" p on p.id = por."Projekt_ID"
                            INNER JOIN "Osoba" o ON o.id=por."Osoba_ID"
                            INNER JOIN "Rola" r ON r.id=por."Rola_ID";""",
                          "projekt_osoba_role.html")


@router.post('/dodaj_projekt_osoba_rola', description="Dodaj projekt_osoba_rola")
async def insert_projekt_osoba_rola(request: Request):
    form = await request.form()
    projekt_ID = form.get('Projekt_ID')
    osoba_ID = form.get('Osoba_ID')
    rola_ID = form.get('Rola_ID')
    connection = None
    try:

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Tablica' table
        insert_query = 'INSERT INTO "Projekt_Osoba_Rola" ("Projekt_ID", "Osoba_ID", "Rola_ID") VALUES ($1, $2, $3)'


        final_query = insert_query.replace('$1', f"'{projekt_ID}'") \
            .replace('$2', f"'{osoba_ID}'") \
            .replace('$3', f"'{rola_ID}'")

        print(final_query)
        await connection.execute(final_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_projekt_osoba_rola/{_id}', description="Usuń relację")
async def delete_projekt_osoba_rola(_id: int):
    await help.delete_id_from_table(_id, "Projekt_Osoba_Rola")


@router.get("/pobierz_zadania", response_model=List)
def pobierz_zadania():
    return help.try_query_get_table('SELECT id, z."Tytul", z."Opis" FROM "Zadanie" z')

@router.get("/pobierz_osoby", response_model=List)
def pobierz_osoby():
    return help.try_query_get_table('SELECT id, o."Email" FROM "Osoba" o')

@router.get("/pobierz_role", response_model=List)
def pobierz_role():
    return help.try_query_get_table('SELECT id, o."Nazwa", "Opis" FROM "Rola" o')


@router.get("/pobierz_projekt_osoba_role", response_model=List)
def pobierz_projekt_osoba_role():
    return help.try_query_get_table('SELECT id, z."Nazwa", z."Opis" FROM "Projekt_Osoba_Rola_Typ" z')
