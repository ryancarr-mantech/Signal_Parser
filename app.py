from logging import root
from flask import Flask, send_from_directory
from flask import render_template
from SignalParser import Signal

app = Flask(__name__)

rootPath = "Signal"

data = Signal(rootPath)

@app.route("/")
@app.route("/<string:activeConversation>")
def indexPage(activeConversation=False):

    if(not activeConversation):
        activeConversation = data.getConversations()[0]

    print(str(activeConversation.encode('utf-8')))
    return render_template("index.html", conversations=data.getConversations(), conversationData = data.conversations, activeConversation=activeConversation)


@app.route("/media/<path:path>")
def loadMedia(path):
    return send_from_directory(rootPath + "/attachments.noindex", path)