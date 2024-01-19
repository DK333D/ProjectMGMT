from fastapi import APIRouter, Request
import help

router: APIRouter = APIRouter()


@router.get('/role', description="Wybierz wszystkie role")
def select_role(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request, 'SELECT id, r."Nazwa", "Opis" FROM "Rola" r',
                          "role.html")


@router.post('/dodaj_rola', description="Dodaj rola")
async def insert_rola(request: Request):
    form = await request.form()
    nazwa = form.get('Nazwa')
    opis = form.get('Opis')
    connection = None
    try:

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Rolay' table
        insert_query = 'INSERT INTO "Rola" ("Nazwa", "Opis") VALUES ($1, $2)'
        await connection.execute(insert_query, nazwa, opis)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_rola/{_id}', description="Usuń rola")
async def delete_rola(_id: int):
    await help.delete_id_from_table(_id, "Rola")
