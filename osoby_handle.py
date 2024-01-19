from fastapi import APIRouter, Request
import help
import logging
from typing import List

router: APIRouter = APIRouter()

# Create a logger instance
# logger = logging.getLogger("my_logger")
# logger.setLevel(logging.INFO)  # Set logging level (INFO, DEBUG, etc.)


@router.get('/osoby', description="Wybierz wszystkie osoby")
def select_osoby(request: Request):
    if not request.session.get('email'):
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request, 'SELECT o.id, o."Imie", "Nazwisko", "Email", "Telefon", s."Nazwa", o."Administrator" FROM "Osoba" o INNER JOIN "Stanowisko" s ON s.id = o."Stanowisko_ID"',
                          "osoby.html")

#
# #
# @router.post('/dodaj_osoba', description="Dodaj osoba")
# async def insert_osoba(request: Request):
#     form = await request.form()
#     imie: str = form.get('imie')
#     nazwisko: str = form.get('nazwisko')
#     email: str = form.get('email')
#     telefon: str = form.get('telefon')
#     stanowisko_id: int = int(form.get('Stanowisko_ID'))
#     connection = None
#     try:
# #
#         connection = await help.create_async_connection()
#
#         # SQL query to insert data into the 'Osoba' table
#         insert_query = 'INSERT INTO "Osoba" ("Imie", "Nazwisko", "Email", "Telefon", "Stanowisko_ID") VALUES ($1, $2, $3, $4, $5)'
#         await connection.execute(insert_query, imie, nazwisko, email, telefon, stanowisko_id)
#         return
# #
#     except Exception as e:
#         return {"error": f"Error: {str(e)}"}
#     finally:
#         if connection:
#             await connection.close()
#
#
@router.delete('/usun_osoba/{_id}', description="Usuń osoba")
async def delete_osoba(_id: int):
    await help.delete_id_from_table(_id, "Osoba")


@router.delete('/usun_admin/{_id}', description="Usuń uprawnienia administratora tej osobie")
async def usun_admin(_id: int):
    await help.remove_admin_for_id(_id, "Osoba")

@router.patch('/dodaj_admin/{_id}', description="Dodaj uprawnienia administratora dla tej osoby")
async def dodaj_admin(_id: int):
    await help.add_admin_for_id(_id, "Osoba")


@router.get("/pobierz_stanowiska", response_model=List)
def pobierz_stanowiska():
    return help.try_query_get_table('SELECT s."id", s."Nazwa", s."Opis" FROM "Stanowisko" s')
