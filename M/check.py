from crypt import methods
import os
import sys
import typing as t
import json

from datetime import datetime
from flask import Flask, jsonify, url_for, request, redirect

LISTENING_PORT = int(sys.argv[1])
FORMATO = sys.argv[2]
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

def run_command(username: str, action: int) -> t.Optional[str]:
    try:
        command = f'check {username} {action}'
        result = os.popen(command).readlines()
        final = result[0].strip()
        return final
    except Exception as e:
        print(f"Erro ao executar comando para {username}: {e}")
        return None

def user_usuario(username: str) -> t.Optional[str]:
    return run_command(username, 1)

def user_conectados(username: str) -> t.Optional[str]:
    return run_command(username, 2)

def user_limite(username: str) -> t.Optional[str]:
    return run_command(username, 3)

def user_data(username: str) -> t.Optional[str]:
    return run_command(username, 4)

def user_dias_restantes(username: str) -> t.Optional[str]:
    return run_command(username, 5)

def format_date_for_anymod(date_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    formatted_date = date.strftime("%Y-%m-%d-")
    return formatted_date
    

@app.route('/checkUser', methods=['POST', 'GET'])
def c4g():
    if request.method == 'POST':
        try:
            req_data = request.get_json()
            username = user_usuario(req_data.get("user"))

            if username == "Not exist":
                user_info = {
                    "username": username,
                    "count_connection": None,
                    "expiration_date": None,
                    "expiration_days": None,
                    "limiter_user": None
                }
            else:
                user_info = {
                    "username": username,
                    "count_connection": user_conectados(username),
                    "expiration_date": user_data(username),
                    "expiration_days": user_dias_restantes(username),
                    "limiter_user": user_limite(username)
                }
            return user_info

        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        try:
            return 'Por favor, use o metodo de requisição correto ! \n\n Checkuser CONECTA4G'
        except Exception as e:
            return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(sys.argv[1]) if len(sys.argv) > 1 else LISTENING_PORT,
    )
