from flask import Flask, request, redirect, render_template
from dashboard.routes.discord_oauth import DiscordOauth
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login():
    return redirect(DiscordOauth.login_url)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    code = request.args.get('code')
    access_token = DiscordOauth.get_access_token(code)

    user_object = DiscordOauth.get_user(access_token)
    print(user_object)

    return f"HELLO"

def run():
  app.run(host='0.0.0.0',port=8080) 

def keep_alive():
    t = Thread(target=run)
    t.start()