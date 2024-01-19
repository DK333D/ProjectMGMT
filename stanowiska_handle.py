from fastapi import APIRouter, Request
import help

router: APIRouter = APIRouter()


@router.get('/stanowiska', description="Wybierz wszystkie stanowiska")
def select_stanowiska(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request, 'SELECT id, s."Nazwa", "Opis" FROM "Stanowisko" s',
                          "stanowiska.html")


@router.post('/dodaj_stanowisko', description="Dodaj stanowisko")
async def insert_stanowisko(request: Request):
    form = await request.form()
    nazwa = form.get('Nazwa')
    opis = form.get('Opis')
    connection = None
    try:
        connection = await help.create_async_connection()
        # SQL query to insert data into the 'Stanowiskoy' table
        insert_query = 'INSERT INTO "Stanowisko" ("Nazwa", "Opis") VALUES ($1, $2)'
        final_query = insert_query.replace('$1', f"'{nazwa}'") \
            .replace('$2', f"'{opis}'") \

        print(final_query)
        await connection.execute(final_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_stanowisko/{_id}', description="Usuń stanowisko")
async def delete_stanowisko(_id: int):
    await help.delete_id_from_table(_id, "Stanowisko")
