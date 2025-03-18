from flask import Flask, request
import time
from utils import encrypt, decrypt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

KEYS = {
    "AS_TGS": 'as-tgs-secret',
    "C_SS": 'c-ss-secret',
    "TGS_SS": 'tgs-ss-secret'
}

def validate_ticket(tgt_username, aut1_username, tgt_start_time, aut1_time, tgt_end_time):
    if tgt_username != aut1_username:
        return "Forbidden (invalid user)", 403

    if not (int(tgt_start_time) <= int(aut1_time) <= int(tgt_end_time)):
        return "Unauthorized (ticket expired)", 401

    return None

def generate_tgs(tgt_username, ss_id):
    current_time = int(time.time())
    end_time = current_time + 3600
    logger.info(f'current_time={current_time}, end_time={end_time}')

    tgs = f"{tgt_username};{ss_id};{current_time};{end_time};{KEYS['C_SS']}"
    logger.info(f'tgs={tgs}')

    tgs_encrypted = encrypt(tgs, KEYS['TGS_SS'])
    logger.info(f'tgs_encrypted={tgs_encrypted} | encrypted with TGS_SS={KEYS["TGS_SS"]}')

    return tgs_encrypted

@app.route('/', methods=['POST'])
def handle():
    data = request.data.decode('utf-8')
    logger.info(f'data={data}')

    tgt_encrypted, aut1_encrypted, ss_id = data.split(';')
    logger.info(f'tgt_encrypted={tgt_encrypted}, aut1_encrypted={aut1_encrypted}, ss_id={ss_id}')

    tgt_decrypted = decrypt(tgt_encrypted, KEYS['AS_TGS'])
    logger.info(f'tgt_decrypted={tgt_decrypted}')

    tgt_username, tgs_id, tgt_start_time, tgt_end_time, k_c_tgs = tgt_decrypted.split(';')
    logger.info(f'tgt_username={tgt_username}, tgs_id={tgs_id}, tgt_start_time={tgt_start_time}, tgt_end_time={tgt_end_time}, k_c_tgs={k_c_tgs}')

    aut1_decrypted = decrypt(aut1_encrypted, k_c_tgs)
    logger.info(f'aut1_decrypted={aut1_decrypted} | decrypted with k_c_tgs={k_c_tgs}')

    aut1_username, aut1_time = aut1_decrypted.split(';')
    logger.info(f'aut1_username={aut1_username}, aut1_time={aut1_time}')

    validation_error = validate_ticket(tgt_username, aut1_username, tgt_start_time, aut1_time, tgt_end_time)
    if validation_error:
        return validation_error

    tgs_encrypted = generate_tgs(tgt_username, ss_id)

    answer = f"{tgs_encrypted};{KEYS['C_SS']}"
    logger.info(f'answer={answer}')

    answer_encrypted = encrypt(answer, k_c_tgs)
    logger.info(f'answer_encrypted={answer_encrypted} | encrypted with k_c_tgs={k_c_tgs}')

    return answer_encrypted, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)