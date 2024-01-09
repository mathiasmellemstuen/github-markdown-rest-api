from flask import Flask, Response, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def add_visitor(address, time): 
    database = sqlite3.connect("database.db")

    query = f"INSERT INTO visitors VALUES ('{address}','{time}')"
    database.execute(query)
    database.commit()
    database.close()

def get_amount_of_unique_visitors():
    database = sqlite3.connect("database.db")
    
    # Count all unique ip addresses in the database
    query = f"SELECT COUNT(DISTINCT address) FROM visitors;"
    data = database.execute(query).fetchall()
    database.commit()
    database.close()
    
    return data[0][0]

@app.route("/amount_of_visitors.svg")
def amount_of_visitors():

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    address = str(request.remote_addr)

    add_visitor(address, time)

    # res = database.execute("SELECT * FROM visitors")
    # print(res.fetchall())
    content = get_amount_of_unique_visitors()
    content = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="20"><g font-family="Verdana,DejaVu Sans,Geneva,sans-serif" font-size="11"><text x="0" y="14">{content}</text></g></svg>'
    # content = Markup(content)
    response = Response(content)
    response.content_type = "image/svg+xml"
    # response.cache_control = "no-cache, no-store, must-revalidate"
    response.expires = 0

    return response 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
