# Peer-to-Peer-Carpooling

The project is created using  HTML, CSS, JavaScript, Python, Django and MySQL. 
For the project to run, we need to install Python 3.8 version with MySQL's latest version.
The IDE used for the project is VS Code.
Steps for running the project:
1. Open the Major 2 folder in VS Code.
2. Create an environment for the project by opening command prompt in the VS Code and run the following commands for activating the environment:
   * python -m venv env
   * .\env\Scripts\activate
3. After running these commands, the environment will be activated. Now we have install the requires libraries of python. So run the following pip install commands:
   * pip install django
   * pip install requests
   * pip install cryptography
   * pip install mysql-connector-python
   * pip install pillow
   * pip install pymysql
4. After installing all these libraries, we need to create a database in mysql and give it's details to the settings.py file in Major 2>carpool>carpool folder. The same details
   should be added in the views.py file in Major 2>carpool>website folder.
5. Ater creating the database, run the following commands to run the server of Django:
   * cd carpool
   * python manage.py makemigrations
   * python manage.py sqlmigrate website 0001
   * python manage.py sqlmigrate website 0002
   * python manage.py sqlmigrate website 0003
   * python manage.py sqlmigrate website 0004
   * python manage.py sqlmigrate website 0005
   * python manage.py migrate
   * python manage.py runserver                //This command runs the Django server and for closing the server 'Ctrl+C' should be pressed in the command prompt terminal of VS Code.
6. The above commands will create the required tables in the database details provided by you and then run the server i.e. http://127.0.0.1:8000/ in your chrome browser.
7. All the images of the web application gets saved in the static folder, which contains of images, javascript files, and css files. All the images of cars that are uploaded in the ADD JOURNEY DETAILS page are saved in the static>images>cars folder by default.
8. All the html pages are present in templates folder.
