from datetime import datetime
from fastapi import APIRouter, Request
import help

router: APIRouter = APIRouter()


@router.get('/projekt_info/{_id}', description="Wybierz wszystkie projekty")
def select_projekty(request: Request, _id: int):

    query='SELECT id, "Nazwa", "Opis", "Start_Data", "Koniec_Data", "liczba_tablic", "liczba_zadan" FROM "projekt_z_liczbami" WHERE id={}'.format(_id)
    return help.get_template_try_query(request, query, "projekt_info.html")

@router.delete('/usun_projekt/{_id}', description="Usun projekt")
async def delete_projekt(_id: int):
    await help.delete_id_from_table(_id, "Projekt")
