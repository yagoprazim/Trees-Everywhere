# 🚀 Trees-Everywhere (YOUSHOP)

This is an application in Django with sqlite, used to manage tree planting records by registered users, using the Django administration page as a form of control of the datas.


## Requirements
- Python 3+

## Tutorial to run the project:
``` bash
git clone https://github.com/yagoprazim/Trees-Everywhere.git # Clone repo in a directory of your choice:
cd .\Trees-Everywhere\ # Be in the root directory of the repository
py -3 -m venv ./venv # Create virtual enviroment for dependencies
./venv/scripts/activate  # Start virtual enviroment

#CREATE a file called '.env' in the root directory 
                              # Content example:
                              SECRET_KEY=django-insecure-br$crxaa#t)#r+nioij=d+9!%7#mk@+3%vbc(u)bd%0p)k=npj
                              DEBUG=True

pip install -r requirements.txt  # Install dependecies
py manage.py migrate # Migration to database
py manage.py createsuperuser # To acess admin page and manage most of the functionalities
py manage.py runserver # Run project =)
```
## Main Endpoints:
- http://localhost:8000/admin/
It is recommended that you access it first to: create users, accounts and trees, which will allow you to freely use the features available from the URL below.
In addition, the admin page is well customized using jazzmin, allowing several ways to view, filter and control most of the data.

- http://localhost:8000/te/
Once you have created the necessary settings on the admin page, you will be ready to use the application's full endpoints. Simply access this main endpoint and it will guide you through the other pages.
Once you are logged into your account, you will be able to edit your profile, plant one or more trees at once, view your planted trees and their details, view a list of all the trees of the accounts you are a part of...

## Tests:
The tests can be found in tests.py.
To run them, simply:
``` bash
py manage.py test
```
