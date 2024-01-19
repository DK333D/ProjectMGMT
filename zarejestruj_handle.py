from fastapi import APIRouter, HTTPException, status, Request
from passlib.context import CryptContext
from starlette.responses import HTMLResponse
import help

router: APIRouter = APIRouter()

# Secret key and token settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Serve HTML file for login form
@router.get("/zarejestruj", response_class=HTMLResponse)
async def serve_login_form(request: Request):
    return help.get_template_no_query(request, "zarejestruj.html")


# Registration endpoint
@router.post("/zarejestruj")
async def zarejestruj(request: Request):
    form = await request.form()
    imie: str = form.get('Imie')
    nazwisko: str = form.get('Nazwisko')
    email: str = form.get('Email')
    haslo: str = form.get('Haslo')
    telefon: str = form.get('Telefon')
    stanowisko_id: int = int(form.get('Stanowisko_ID'))
    connection = None

    if help.check_if_user_exists(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = pwd_context.hash(haslo)

    query = 'INSERT INTO "Osoba" ("Imie", "Nazwisko", "Email", "Stanowisko_ID", "Haslo", "Administrator", "Telefon") VALUES ($1, $2, $3, $4, $5, $6, $7);'
    final_query = query\
        .replace('$1', f"'{imie}'") \
        .replace('$2', f"'{nazwisko}'") \
        .replace('$3', f"'{email}'") \
        .replace('$4', f"'{stanowisko_id}'") \
        .replace('$5', f"'{hashed_password}'")\
        .replace('$6', f"'false'")\
        .replace('$7', f"'{telefon}'")
    print(final_query)
    connection = None
    try:
        connection = await help.create_async_connection()
        await connection.execute(final_query)
        return

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        if connection:
            await connection.close()
            return {"message": "Registration successful"}


@router.get("/registration-form", response_class=HTMLResponse)
async def serve_registration_form():
    with open("zarejestruj.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)
