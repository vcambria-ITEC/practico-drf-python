# Post-it Notes — Práctico DRF

Aplicación de notas tipo post-it con login de usuario, hecha con Django + Django REST Framework.

## Stack

- Django 6.1
- Django REST Framework (autenticación por Token)
- SQLite (dev)
- Gestor de entorno: [uv](https://docs.astral.sh/uv/)

## Modelo

`Note`: `title`, `content`, `color`, `owner` (FK a `User`), `tags` (M2M a `Tag`), `created_at`, `updated_at`.
Cada usuario solo ve y gestiona sus propias notas.

`Tag`: `name`. Las etiquetas son compartidas (no pertenecen a un usuario) y se relacionan con las notas mediante una
relación many-to-many.

En el serializer de `Note`, `tags` es un campo anidado de solo lectura (devuelve el objeto completo `{"id", "name"}`),
y `tag_ids` es el campo de escritura (recibe una lista de IDs de tags existentes) para crear/asignar tags al crear o
editar una nota.

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
| PUT / PATCH | `/api/notes/<id>/` | Edita una nota propia (PUT completo, PATCH parcial) | Sí |
| DELETE | `/api/notes/<id>/` | Borra una nota propia | Sí |
| GET | `/api/tags/` | Lista todos los tags | Sí |
| POST | `/api/tags/` | Crea un tag | Sí |
| GET | `/api/tags/<id>/` | Detalle de un tag | Sí |
| PUT / PATCH | `/api/tags/<id>/` | Edita un tag | Sí |
| DELETE | `/api/tags/<id>/` | Borra un tag | Sí |

La autenticación es por Token: mandar el header `Authorization: Token <token>`.

Las vistas de `notes` y `tags` están implementadas con **Concrete Generic Views** de DRF
(`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`).

## Ejemplo con curl

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","password":"unapass123"}'

curl -X POST http://127.0.0.1:8000/api/tags/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <TOKEN>" \
  -d '{"name":"urgente"}'

curl -X POST http://127.0.0.1:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <TOKEN>" \
  -d '{"title":"Comprar pan","content":"antes de las 20hs","color":"pink","tag_ids":[1]}'
```
