python -m venv .venv

.venv\Scripts\activate

pip install openai python-dotenv

pip freeze > requirements.txt

uvicorn app.main:app --reload