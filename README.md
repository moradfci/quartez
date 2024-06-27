# Multi-Tenant Project

## Setup Instructions

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. make migration and run the server
    ``` bash
   python manage.py makemigrations 
   python manage.py migrate
   python manage.py runserver

4. to see swager doumnetation for the project 
    ```
    http://localhost:8000/swagger/

5. run tests
```bash
    python manage.py test commonbase.tests
