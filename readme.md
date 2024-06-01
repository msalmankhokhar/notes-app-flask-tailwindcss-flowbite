
## How to run the project
- Clone the repository at your local machine or simply download zip from Github
```shell
git clone https://github.com/msalmankhokhar/notes-app-flask-tailwindcss-flowbite.git
```
- Open your terminal in the root directory of the cloned repo and run the following commands. Make sure you already installed node, npm, python and pip

### Installing node and python dependencies

```bash
npm i
```
```bash
pip install -r requirements.txt
```

Before starting the application you have to link a Microsoft SQL server with the application. You can do so by editing the `database_manager.py` and `db_credentials.py`. Replace content within these files with your correct credentials. Or if you don't wanna get this pain, simply configure the app to use SQLite database instead of MS SQL Server.

### Configuration for SQLite
- Open `app.py`
- Go to line number 15
```python
15 app.config["SQLALCHEMY_DATABASE_URI"] = sql_server_URI
```
- Replace it with this:
```python
15 app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_URI
```
---

### Running the app

```bash
python3 app.py
```
and for windows OS
```bash
python app.py
```
A flask dev server will be started and you can view the app by going to `http://localhost` in your browser

```bash
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:80
 * Running on http://192.168.100.125:80
Press CTRL+C to quit   
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 121-178-352
```

---

## Screenshots

### Log In Page
![App Screenshot](https://github.com/msalmankhokhar/notes-app-flask-tailwindcss-flowbite/blob/main/static/mockups/ssrock/login/dark.png?raw=true)

### Home Page
![App Screenshot](https://github.com/msalmankhokhar/notes-app-flask-tailwindcss-flowbite/blob/main/static/mockups/ssrock/index/dark.png?raw=true)

### Search Page
![App Screenshot](https://github.com/msalmankhokhar/notes-app-flask-tailwindcss-flowbite/blob/main/static/mockups/ssrock/search/dark.png?raw=true)



