from datetime import datetime
from fastapi import APIRouter, Request
import help
from typing import List

router: APIRouter = APIRouter()


@router.get('/moje_projekty', description="Wybierz wszystkie projekty")
def select_projekty(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")

    email = request.session["email"]
    query = 'SELECT "Projekt_ID", "Osoba_ID", "Rola_ID", "Projekt_Nazwa", "Projekt_Opis", "Start_Data", "Koniec_Data", "Imie", "Nazwisko", "Email", "Rola_Nazwa", "Rola_Opis" FROM "moje_projekty_widok" WHERE "Email"=$1'

    final_query = query.replace('$1', f"'{email}'")
    print(final_query)
    return help.get_template_try_query(request, final_query,
                                       "moje_projekty.html")


@router.post('/dodaj_moj_projekt', description="Dodaj projekt")
async def insert_projekt(request: Request):
    form = await request.form()
    nazwa = form.get('Nazwa')
    opis = form.get('Opis')
    start_data = form.get('Start_Data')
    koniec_data = form.get('Koniec_Data')
    rola_id = form.get('Rola_ID')

    email = request.session["email"]
    connection = None
    try:
        start_data = datetime.strptime(start_data, "%Y-%m-%d").date()
        koniec_data = datetime.strptime(koniec_data, "%Y-%m-%d").date()

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Projekty' table
        insert_query = 'INSERT INTO "Projekt" ("Nazwa", "Opis", "Start_Data", "Koniec_Data") VALUES ($1, $2, $3, $4) RETURNING "id"'
        final_query = insert_query.replace('$1', f"'{nazwa}'") \
            .replace('$2', f"'{opis}'") \
            .replace('$3', f"'{start_data}'") \
            .replace('$4', f"'{koniec_data}'")
        print(final_query)
        print(email)
        inserted_id = await connection.fetchval(final_query)
        print(inserted_id)

        insert_por_query = 'INSERT INTO "Projekt_Osoba_Rola" ("Projekt_ID", "Osoba_ID", "Rola_ID") VALUES ($1,(SELECT id FROM "Osoba" o WHERE o."Email" = $2),$3)'
        final_por_query = insert_por_query.replace('$1', f"'{inserted_id}'") \
            .replace('$2', f"'{email}'") \
            .replace('$3', f"'{rola_id}'")
        print(final_por_query)
        await connection.execute(final_por_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()


@router.delete('/usun_projekt/{_id}', description="Usun projekt")
async def delete_projekt(_id: int):
    await help.delete_id_from_table(_id, "Projekt")


@router.post('/dashboard', description="Zobacz dashboard")
async def go_to_dashboard(request: Request):
    form = await request.form()
    nazwa = form.get("nazwa")
    if nazwa is None:
        return {"error": "Parameter 'nazwa' is missing"}
    return help.templates.TemplateResponse("panel.html", {"request": request, "nazwa": nazwa})


@router.get("/pobierz_role", response_model=List)
def pobierz_role():
    return help.try_query_get_table('SELECT r."id", r."Nazwa", r."Opis" FROM "Rola" r')
