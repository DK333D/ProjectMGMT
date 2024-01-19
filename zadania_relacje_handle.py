from fastapi import APIRouter, Request
import help
from typing import List

router: APIRouter = APIRouter()

@router.get('/zadania_relacje', description="Wybierz wszystkie zadania_relacje")
def select_zadania_relacje(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request,
                          'SELECT zr.id, z1."Tytul" AS Z1_Tytul, z2."Tytul" AS Z2_Tytul, zrt."Nazwa" AS Relacja_Nazwa, zrt."Opis" AS Relacja_Opis FROM "Zadania_Relacja" zr INNER JOIN "Zadania_Relacja_Typ" zrt on zrt.id = zr."Relacja_Typ_ID" INNER JOIN "Zadanie" z1 ON z1.id=zr."Zadanie_1_ID" INNER JOIN "Zadanie" z2 ON z2.id=zr."Zadanie_2_ID"',
                          "zadania_relacje.html")


@router.post('/dodaj_zadania_relacja', description="Dodaj zadania_relacja")
async def insert_zadania_relacja(request: Request):
    form = await request.form()
    zadanie_1_ID = form.get('Zadanie_1_ID')
    zadanie_2_ID = form.get('Zadanie_2_ID')
    relacja_typ_ID = form.get('Relacja_Typ_ID')
    connection = None
    try:

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Tablica' table
        insert_query = 'INSERT INTO "Zadania_Relacja" ("Zadanie_1_ID", "Zadanie_2_ID", "Relacja_Typ_ID") VALUES ($1, $2, $3)'


        final_query = insert_query.replace('$1', f"'{zadanie_1_ID}'") \
            .replace('$2', f"'{zadanie_2_ID}'") \
            .replace('$3', f"'{relacja_typ_ID}'")

        print(final_query)
        await connection.execute(final_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_zadania_relacja/{_id}', description="Usuń zadania_relacja")
async def delete_zadania_relacja(_id: int):
    await help.delete_id_from_table(_id, "Zadania_Relacja")


@router.get("/pobierz_zadania", response_model=List)
def pobierz_zadania():
    return help.try_query_get_table('SELECT id, z."Tytul", z."Opis" FROM "Zadanie" z')


@router.get("/pobierz_zadania_relacje", response_model=List)
def pobierz_zadania_relacje():
    return help.try_query_get_table('SELECT id, z."Nazwa", z."Opis" FROM "Zadania_Relacja_Typ" z')
