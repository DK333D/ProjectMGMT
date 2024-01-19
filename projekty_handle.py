from datetime import datetime
from fastapi import APIRouter, Request
import help

router: APIRouter = APIRouter()


@router.get('/projekty', description="Wybierz wszystkie projekty")
def select_projekty(request: Request):
    # print(request.session.get('email'))
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request,
                          'select id, "Nazwa", "Opis", "Start_Data", "Koniec_Data", liczba_tablic, liczba_zadan from projekt_z_liczbami',
                          "projekty.html")


@router.post('/dodaj_projekt', description="Dodaj projekt")
async def insert_projekt(request: Request):
    form = await request.form()
    nazwa = form.get('Nazwa')
    opis = form.get('Opis')
    start_data = form.get('Start_Data')
    koniec_data = form.get('Koniec_Data')
    connection = None
    try:
        # Przekształć stringi daty na obiekty datetime
        start_data = datetime.strptime(start_data, "%Y-%m-%d").date()
        koniec_data = datetime.strptime(koniec_data, "%Y-%m-%d").date()

        connection = await help.create_async_connection()

        # SQL query to insert data into the 'Projekty' table
        insert_query = 'INSERT INTO "Projekt" ("Nazwa", "Opis", "Start_Data", "Koniec_Data") VALUES ($1, $2, $3, $4)'
        final_query = insert_query.replace('$1', f"'{nazwa}'") \
            .replace('$2', f"'{opis}'") \
            .replace('$3', f"'{start_data}'") \
            .replace('$4', f"'{koniec_data}'")
        print(final_query)
        await connection.execute(final_query)
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
