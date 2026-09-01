# Post-it Notes — Práctico DRF

Aplicación de notas tipo post-it con login de usuario, hecha con Django + Django REST Framework.

## Stack

- Django 6.1
- Django REST Framework (autenticación por Token)
- SQLite (dev)
- Gestor de entorno: [uv](https://docs.astral.sh/uv/)

## Modelo

`Note`: `title`, `content`, `color`, `owner` (FK a `User`), `created_at`, `updated_at`.
Cada usuario solo ve y gestiona sus propias notas.

## Setup

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser   # opcional, para /admin
uv run python manage.py runserver
```

Abrir `http://127.0.0.1:8000/register/` para crear un usuario, o `http://127.0.0.1:8000/login/` si ya tenés uno.

## Endpoints de la API

| Método | URL | Descripción | Auth |
|---|---|---|---|
| POST | `/api/register/` | Crea un usuario y devuelve el token | No |
| POST | `/api-token-auth/` | Login, devuelve el token | No |
| GET | `/api/notes/` | Lista las notas del usuario autenticado | Sí |
| POST | `/api/notes/` | Crea una nota | Sí |
| GET | `/api/notes/<id>/` | Detalle de una nota propia | Sí |
| PUT | `/api/notes/<id>/` | Edita una nota propia | Sí |
| DELETE | `/api/notes/<id>/` | Borra una nota propia | Sí |

La autenticación es por Token: mandar el header `Authorization: Token <token>`.

## Ejemplo con curl

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","password":"unapass123"}'

curl -X POST http://127.0.0.1:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <TOKEN>" \
  -d '{"title":"Comprar pan","content":"antes de las 20hs","color":"pink"}'
```
