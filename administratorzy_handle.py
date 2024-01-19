from fastapi import APIRouter, Request
import help
from typing import List

router: APIRouter = APIRouter()

@router.get('/administratorzy', description="Wybierz wszystkich administratoró")
def select_administratorzy(request: Request):
    if not request.session.get('email') or not request.session.get("isAmin")=="true":
        return help.get_template_no_query(request, "zaloguj.html")
    return help.get_template_try_query(request, 'SELECT o.id, o."Imie", "Nazwisko", "Email", "Telefon", s."Nazwa", o."Administrator" FROM "Osoba" o INNER JOIN "Stanowisko" s ON s.id = o."Stanowisko_ID"',
                          "administratorzy.html")



@router.delete('/usun_osoba/{_id}', description="Usuń osoba")
async def delete_osoba(_id: int):
    await help.delete_id_from_table(_id, "Osoba")


@router.get("/pobierz_stanowiska", response_model=List)
def pobierz_stanowiska():
    return help.try_query_get_table('SELECT s."id", s."Nazwa", s."Opis" FROM "Stanowisko" s')
