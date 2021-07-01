import sqlite3
import os
import json
import time

class Signal:

    def __init__(self, rootPath, version, sqlcipherPath):
        self.conn = None
        self.version = version
        self.rootPath = rootPath
        self.sqlcipherPath=sqlcipherPath
        self.findPrimaryDatabase()
        self.decryptDatabase()
        self.loadData()

    def decryptDatabase(self):
        print("DECRYTPING \n\n\n\n\n")
        script = ""

        if(self.primaryDatabase == self.rootPath + "/sql/plaintext.db"):
            pass
            #return

        if(self.version == "3"):
            script += "PRAGMA cipher_compatibility = 3;"
        else:
            script += "PRAGMA cipher_compatibility = 4;"

        script += "PRAGMA key=\\\"x\'" + self.getDatabaseKey() +"\'\\\";ATTACH DATABASE '" + self.rootPath + "/sql/plaintext.db' AS plaintext KEY '';SELECT sqlcipher_export('plaintext');DETACH DATABASE plaintext;"
        cmd = "echo \"" + script + "\" | " + self.sqlcipherPath + " " + self.primaryDatabase
        
        os.system(cmd)
        print(self.rootPath)
        self.findPrimaryDatabase()

    def getDatabaseKey(self):
        with open(self.rootPath + "/config.json") as file:
            data = json.load(file)
            return data['key']

    def findPrimaryDatabase(self):
        if(self.conn):
            self.conn.close()
        if(os.path.exists(self.rootPath + "/sql/plaintext.db")):
            self.primaryDatabase = self.rootPath + "/sql/plaintext.db"
            self.conn = sqlite3.connect(self.primaryDatabase)
            return
        else:
            self.primaryDatabase = self.rootPath + "/sql/db.sqlite"
        self.conn = sqlite3.connect(self.primaryDatabase)

    def loadData(self):

        self.conversations = {}

        cur = self.conn.cursor()

        print(self.primaryDatabase)

        conversationsTable = cur.execute("SELECT id, active_at, type, members, name, profileName FROM conversations").fetchall()

        for conversation in conversationsTable:
            conversationId = bytes(str(conversation[0]), 'utf-8').hex()
            #print(conversationId)
            #print(str(conversationId.encode('utf-8')))
            self.conversations[conversationId] = {"last_active":conversation[1], "type":conversation[2], "members":conversation[3], "messages":{}}
            
            if(conversation[4]):
                self.conversations[conversationId]["name"] = conversation[4]
            elif(conversation[5]):
                self.conversations[conversationId]["name"] = conversation[5]
            elif(conversation[3]):
                self.conversations[conversationId]["name"] = conversation[3]
            else:
                self.conversations[conversationId]["name"] = '+' + str(conversation[0])


            if(conversation[1]):
                self.conversations[conversationId]["last_active"] = time.strftime('%d %B, %Y %I:%M %p', time.localtime(conversation[1]/1000))
            else:
                self.conversations[conversationId]["last_active"] = "UNKNOWN"


        messages = cur.execute("SELECT id, conversationId, sent_at, json, hasAttachments, body FROM messages ORDER BY sent_at ASC").fetchall()

        self.conn.commit()

        for row in messages:
            message = {}
            message["sent_at"] = time.strftime('%d %B, %Y %I:%M %p', time.localtime(row[2]/1000))

            data = json.loads(row[3])

            message["body"] = row[5]
            message["direction"] = data["type"]

            message["hasAttachment"] = row[4]
            if(row[4]):
                message["attachment"] = data["attachments"][0]
                message["attachment"]["path"] = message["attachment"]["path"].replace('\\', '/')
                print(message["attachment"]["path"])
                message["attachment"]["type"] = message["attachment"]["contentType"].split("/")[0]

            self.conversations[bytes(str(row[1]), 'utf-8').hex()]["messages"][row[0]] = message
            
    def getConversations(self):
        return list(self.conversations.keys())
        
    def close(self):
        if(self.conn):
            self.conn.close()


if __name__ == "__main__":
    s = Signal("Signal")
    s.close()
    

