# flask-cafe

This is a Flask app for managing cafes and users.

Starter code is provided by Rithm School. 

### Key learnings;

  * Many-to-many relationships in SQLAlchemy
  * Software design for web applications & OO thinking in models
  * Having Flask run JSON API routes
  * Jinja templating
  * Validating forms with WTForms

### App Information

#### Routes
```
  GET /cafes/add
  Show form for adding a cafe
  POST /cafes/add
  Handle adding new cafe. On success, redirect to new cafe detail page with flash message “CAFENAME added.”
  GET /cafes/[cafe-id]/edit
  Show form for editing cafe
  POST /cafes/[cafe-id]/edit
  Handle editing cafe. On success, redirect to cafe detail page with flash message “CAFENAME edited.”
 ```

### Getting Started
1. Make a virtual environment and add the project dependencies:
```
  mkvirtualenv flask-cafe  
  pip install -r requirements.txt

```
2. Setup and seed the database:
```
  createdb flaskcafe    
  python seed.py

```
3. Start the server:

```
  flask run
```
