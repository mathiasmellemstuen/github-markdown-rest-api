from flask import Flask, Response, request
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def is_ipv4(ip_string): 
    regex_ipv4 = "(\d{1,3}\.){3}\d{1,3}"
    return bool(re.search(regex_ipv4, ip_string))

def is_ipv6(ip_string): 
    regex_ipv6 = "((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9a-f]{1,4}:){7}([0-9a-f]{1,4}|:))|(([0-9a-f]{1,4}:){6}(:[0-9a-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9a-f]{1,4}:){5}(((:[0-9a-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9a-f]{1,4}:){4}(((:[0-9a-f]{1,4}){1,3})|((:[0-9a-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9a-f]{1,4}:){3}(((:[0-9a-f]{1,4}){1,4})|((:[0-9a-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9a-f]{1,4}:){2}(((:[0-9a-f]{1,4}){1,5})|((:[0-9a-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9a-f]{1,4}:){1}(((:[0-9a-f]{1,4}){1,6})|((:[0-9a-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9a-f]{1,4}){1,7})|((:[0-9a-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))"
    return bool(re.search(regex_ipv6, ip_string))

def add_visitor(address, time): 

    # Checking the input address, if its not valid
    if not is_ipv4(address) and not is_ipv6(address):
        return

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

def get_amount_of_visitors(): 
    database = sqlite3.connect("database.db")
    
    # Count all unique ip addresses in the database
    query = f"SELECT COUNT(address) FROM visitors;"
    data = database.execute(query).fetchall()
    database.commit()
    database.close()
    
    return data[0][0]


@app.route("/amount_of_unique_visitors.svg")
def amount_of_unique_visitors():

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # address = str(request.remote_addr)
    addr_list = request.headers.getlist("HTTP_X_FORWARDED_FOR")
    address = str(addr_list[0]) if addr_list else str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr))

    print(f"Request from {address}", flush=True)

    add_visitor(address, time)

    content = get_amount_of_unique_visitors()
    
    first_part = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="17" height="17"><style>.letters { fill: #2E2E2E; } @media (prefers-color-scheme: dark) { .letters { fill: #ffffff; }}</style><g font-family="Verdana,DejaVu Sans,Geneva,sans-serif" font-size="17"><text class="letters" x="0" y="17">'
    end_part = "</text></g></svg>"
    content = f'{first_part}{content}{end_part}'
    response = Response(content)
    response.content_type = "image/svg+xml"
    response.expires = 0

    return response 

@app.route("/amount_of_visitors.svg")
def amount_of_visitors():

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # address = str(request.remote_addr)
    addr_list = request.headers.getlist("HTTP_X_FORWARDED_FOR")
    address = str(addr_list[0]) if addr_list else str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr))

    print(f"Request from {address}", flush=True)

    add_visitor(address, time)

    content = get_amount_of_visitors()
    
    first_part = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="17" height="17"><style>.letters { fill: #2E2E2E; } @media (prefers-color-scheme: dark) { .letters { fill: #ffffff; }}</style><g font-family="Verdana,DejaVu Sans,Geneva,sans-serif" font-size="17"><text class="letters" x="0" y="17">'
    end_part = "</text></g></svg>"
    content = f'{first_part}{content}{end_part}'
    response = Response(content)
    response.content_type = "image/svg+xml"
    response.expires = 0

    return response 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
