from fastapi import APIRouter, Request
import help

router: APIRouter = APIRouter()


@router.get('/zadania_relacja_typy', description="Wybierz wszystkie typy")
def select_zadania_relacja_typy(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request, 'SELECT id, zrt."Nazwa", zrt."Opis" FROM "Zadania_Relacja_Typ" zrt',
                          "zadania_relacja_typy.html")


@router.post('/dodaj_typ', description="Dodaj typ")
async def insert_typ(request: Request):
    form = await request.form()
    typ_nazwa = form.get('Nazwa')
    typ_opis = form.get('Opis')
    connection = None
    try:

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Typy' table
        insert_query = 'INSERT INTO "Zadania_Relacja_Typ" ("Nazwa", "Opis") VALUES ($1, $2)'
        final_query = insert_query.replace('$1', f"'{typ_nazwa}'")\
            .replace('$2', f"'{typ_opis}'")
        print(final_query)
        await connection.execute(insert_query, typ_nazwa, typ_opis)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_typ/{_id}', description="Usuń typ")
async def delete_typ(_id: int):
    await help.delete_id_from_table(_id, "Zadania_Relacja_Typ")
