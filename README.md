# Todo App FastAPI

## 🚀 Description

Application de gestion de TODOs construite avec FastAPI, respectant une architecture propre (Clean Architecture). Le projet gère :

- authentification JWT (connexion / inscription)
- liaison des TODO avec l’utilisateur (propriété sécurisée)
- base de données PostgreSQL (SQLAlchemy Async)
- migrations Alembic
- validation Pydantic (v2+, `ConfigDict`, `from_attributes`)
- documentation OpenAPI automatique (/docs et /redoc)
- gestion globale des erreurs avec exceptions fonctionnelles / techniques

## 📦 Structure

- `app/main.py` : application FastAPI + gestion d’exceptions globale
- `app/api/routes/` : routes API (auth, users, todos)
- `app/api/deps.py` : dépendances FastAPI (auth, DB)
- `app/core/config.py` : configuration (pydantic-settings + .env)
- `app/core/security.py` : hash/mot de passe (`bcrypt`, SHA256 pré-hash), JWT
- `app/db/` : configuration DB SQLAlchemy async
- `app/repositories/` : accès DB (user / todo)
- `app/services/` : logique métier (user / todo)
- `app/schemas/` : schémas Pydantic (DTO)
- `alembic/` : migrations

## ⚙️ Setup

1. Créer et activer un virtualenv :
   - Windows PowerShell :
     ```powershell
     cd D:\projects\todo
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
2. Installer les dépendances :
   ```powershell
   pip install -r requirements.txt
   ```
3. Créer le fichier `.env` (déjà présent), cocher les valeurs suivantes :
   ```bash
   POSTGRES_USER=todo_user
   POSTGRES_PASSWORD=todo_password
   POSTGRES_DB=todo_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   SECRET_KEY=ChangeMeToASecureRandomString
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
4. Lancer la base de données PostgreSQL et créer la base :
   ```bash
   createdb -U todo_user todo_db
   ```
5. Lancer les migrations :
   ```powershell
   alembic upgrade head
   ```

## ▶️ Lancer l’application

### Local (virtualenv)

```powershell
cd D:\projects\todo
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```powershell
cd D:\projects\todo
docker compose up --build
```

Accès API (préfixe `/api` configuré) :
- OpenAPI : `http://127.0.0.1:8000/api/docs`
- ReDoc : `http://127.0.0.1:8000/api/redoc`

## 🧪 Tests

```powershell
.\venv\Scripts\Activate.ps1
set PYTHONPATH=%CD%
py -m pytest -q
```

### Correctifs récents implémentés
- `app/core/config.py` : passage à Pydantic v2 (`model_config` + `ConfigDict`)
- `app/schemas/*` : `from_attributes=True` (remplace `orm_mode` obsolète)
- `app/core/security.py` : timestamp JWT avec `datetime.now(timezone.utc)` (aucun warning UTC)
- `app/core/security.py` : passage en `bcrypt` direct (pré-hash SHA256 + bcrypt, compatible journalisation et limite 72 octets)
- tests : `pytest.mark.anyio` (à la place de `pytest.mark.asyncio`)

## 🌐 Endpoints principaux

- `POST /auth/token` : authentification (email/password)
- `POST /users/register` : inscription
- `GET /todos/` : liste des todos user
- `POST /todos/` : création de todo
- `GET /todos/{todo_id}` : lire todo
- `PUT /todos/{todo_id}` : mise à jour todo
- `DELETE /todos/{todo_id}` : suppression todo

## 🔒 Notes

- Utilise JWT bearer dans header `Authorization: Bearer <token>` pour routes `/todos`.
- Les erreurs sont gérées via des exceptions propres (`AppError`, `FunctionalError`, `TechnicalError`) avec status codes personnalisés.

