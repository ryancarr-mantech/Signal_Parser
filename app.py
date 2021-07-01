from logging import root
from flask import Flask, send_from_directory
from flask import render_template
from SignalParser import Signal
import os

app = Flask(__name__)

rootPath = os.getenv("TARGET_FOLDER")

data = Signal(rootPath, version=4, sqlcipherPath="sqlcipher/sqlcipher")

@app.route("/")
@app.route("/<string:activeConversation>")
def indexPage(activeConversation=False):
    print(os.getenv('SIGNAL_VERSION'))
    if(not activeConversation):
        activeConversation = data.getConversations()[0]

    if(not (activeConversation in data.getConversations())):
        activeConversation = data.getConversations()[0]
    
    return render_template("index.html", conversations=data.getConversations(), conversationData = data.conversations, activeConversation=activeConversation)


@app.route("/media/<path:path>")
def loadMedia(path):
    return send_from_directory(rootPath + "/attachments.noindex", path)