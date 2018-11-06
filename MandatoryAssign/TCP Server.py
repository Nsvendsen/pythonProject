import socket
import threading
import ScriptTest
import ResponseGenerator
import datetime
import queue
host = "127.0.0.1"
port = 9000

connection = socket.socket()
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind((host,port))
connection.listen(1)


def acceptConnecetions():
    while True:
        conn, addr = connection.accept()
        conn.settimeout(60)
        request_queue = queue.Queue()
        request_queue.put(conn)
        if request_queue.qsize() < 5:
            t = threading.Thread(target = client_thread, args=(conn,))
            t.start()
            request_queue.get()



def client_thread(conn):
    inc_HTTP = conn.recv(1024).decode()
    logfile = open("RequestLogFile.txt", "a")

    print(inc_HTTP)
    header, rest = inc_HTTP.split('\r\n', 1)
    logfile.write(header + " Time " + str(datetime.datetime.now()) +"\n")
    request_type, path, rest2 = header.split(' ')
    if request_type == "GET":
        if path == "/":
            with open("index.html", 'r') as f:
                html_scriptTest = f.read()
                msg = ScriptTest.parse_html_custom(html_scriptTest)
                ResponseGenerator.response_parser_header(msg, conn)
        else:
            try:
                with open(path[1:], 'r') as f:
                    html_scriptTest = f.read()
                    msg = ScriptTest.parse_html_custom(html_scriptTest)
                    ResponseGenerator.response_parser_header(msg, conn)
            except FileNotFoundError:
                with open("404.html", 'r') as f:
                    html_scriptTest = f.read()
                    msg = ScriptTest.parse_html_custom(html_scriptTest)
                    ResponseGenerator.response_parser_404(msg, conn)
            except:
                print("Unknown exception")




acceptConnecetions()
