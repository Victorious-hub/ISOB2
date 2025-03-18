from flask import Flask
from utils import encrypt
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

users = {
    "user": {
        # "username": "user",
        "password": "password"
    }
}

KEYS = {
    "AS_TGS": 'as-tgs-secret',
    "C_TGS": 'c-tgs-secret'
}

SERVER_ID = {
    "TGS": 'tgs'
}

def generate_tgt(username):
    """
    Generate a Ticket Granting Ticket (TGT)
    """
    current_time = int(time.time())
    end_time = current_time + 3600
    logger.info(f'current_time={current_time}, end_time={end_time}')

    tgt = f"{username};{SERVER_ID['TGS']};{current_time};{end_time};{KEYS['C_TGS']}"
    tgt_encrypted = encrypt(tgt, KEYS["AS_TGS"])
    logger.info(f'tgt={tgt}')
    logger.info(f'tgt_encrypted={tgt_encrypted} | encrypted with AS_TGS={KEYS["AS_TGS"]}')
    
    return tgt_encrypted

def generate_answer(username, tgt_encrypted):
    """
    Generate the encrypted response for the client
    """
    answer = f"{tgt_encrypted};{KEYS['C_TGS']}"
    answer_encrypted = encrypt(answer, users[username]['password'])
    logger.info(f'answer={answer}')
    logger.info(f'answer_encrypted={answer_encrypted} | encrypted with K_c={users[username]["password"]}')
    
    return answer_encrypted

@app.route('/<username>', methods=['GET'])
def handle(username):
    logger.info(f'username={username}')
    if username not in users:
        logger.warning(f'Unauthorized access attempt for username={username}')
        return "Forbidden", 403

    tgt_encrypted = generate_tgt(username)
    answer_encrypted = generate_answer(username, tgt_encrypted)

    return answer_encrypted, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)