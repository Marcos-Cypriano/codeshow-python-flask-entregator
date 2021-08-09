#O módulo gunicorn não funciona em Windows, então usei o waitress (instalado no ambiente virtual)

def application(environ, start_response):
    body = b"<h1>Ola mundo!</h1>\n<button>Clique</button>"
    status = "200 OK"
    headers = [("Content-type", "text/html")]
    start_response(status, headers)
    return [body]