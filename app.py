from flask import Flask, request, jsonify
import telegram
from telebot.credentials import bot_token, URL
from telebot.mastermind import get_response
from database import setup_db,Movie,db_drop_and_create_all
from flask_cors import CORS
from database import db


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route("/movies")
def get_movies():
    movies = Movie.query.order_by(Movie.release_date).all()
    movie=[]
    movie=[mov.release_date for mov in movies]
    return jsonify(
        {
            "success": True,
            "movie name": movie
        }
    ), 200

@app.route('/')
def index():
    return jsonify({'message': 'Hello,hello, World!'})

if __name__ == "__main__":
    setup_db(app)
    CORS(app)
    db_drop_and_create_all()
    app.run(threaded=True)