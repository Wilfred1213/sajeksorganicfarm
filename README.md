# Sajeks Organic Farm

Live Website: https://wilfred7.pythonanywhere.com/
Repository: https://github.com/Wilfred1213/sajeksorganicfarm

Sajeks Organic Farm is a Django web application for selling organic vegetables, poultry and farm produce directly to customers. It also includes farm tutorials via video blogs.

## Features
- Homepage with carousel and product categories
- Fresh vegetables listing (Carrot, Cucumber, Kale, etc)
- Poultry and livestock section
- Video tutorials for farming
- Services and newsletter subscription

## Tech Stack
- **Backend:** Django 4, Python
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Database:** SQLite (local)
- **Deployment:** PythonAnywhere, WhiteNoise for static files

## How to Run Locally
git clone https://github.com/Wilfred1213/sajeksorganicfarm.git
cd sajeksorganicfarm

# create virtual env
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# setup env
copy .env.example .env

# run
python manage.py migrate
python manage.py runserver