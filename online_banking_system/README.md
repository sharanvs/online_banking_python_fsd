# Online Banking System — Complete Project

This project contains:
- Personal finance tools module (finance_tools.py)
- Django app (banking_project / bank_app) with user auth, account, deposit/withdraw, and 10 financial tools
- Unit tests
- Simple ML loan estimation module (ml/)

How to run (local dev):
1. Create virtualenv and install:
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt

2. Run migrations:
   python manage.py migrate

3. Create superuser (optional):
   python manage.py createsuperuser

4. Run server:
   python manage.py runserver

5. Run tests:
   python manage.py test

Notes:
- Provided `finance_tools.py` contains validated functions.
- ML module is a simple example training script that uses synthetic data.
