from flask import Flask, request
from utils import encrypt, decrypt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

KEYS = {
    "TGS_SS": 'tgs-ss-secret'
}

def validate_ticket(tgs_username, aut2_username, tgs_start_time, aut2_time, tgs_end_time):
    if tgs_username != aut2_username:
        return "Forbidden (invalid user)", 403

    if not (int(tgs_start_time) <= int(aut2_time) <= int(tgs_end_time)):
        return "Unauthorized (ticket expired)", 401

    return None

@app.route('/', methods=['POST'])
def handle():
    data = request.data.decode('utf-8')
    logger.info(f'data={data}')

    TGS_encrypted, aut2_encrypted = data.split(';')
    logger.info(f'TGS_encrypted={TGS_encrypted}')
    logger.info(f'aut2_encrypted={aut2_encrypted}')

    TGS_decrypted = decrypt(TGS_encrypted, KEYS['TGS_SS'])
    logger.info(f'TGS_decrypted={TGS_decrypted} | decrypted with TGS_SS={KEYS["TGS_SS"]}')

    tgs_username, ss_id, tgs_start_time, tgs_end_time, K_c_ss = TGS_decrypted.split(';')
    logger.info(f'tgs_username={tgs_username}, ss_id={ss_id}, tgs_start_time={tgs_start_time}, tgs_end_time={tgs_end_time}, K_c_ss={K_c_ss}')

    aut2_decrypted = decrypt(aut2_encrypted, K_c_ss)
    logger.info(f'aut2_decrypted={aut2_decrypted} | decrypted with K_c_ss={K_c_ss}')

    aut2_username, aut2_time = aut2_decrypted.split(';')
    logger.info(f'aut2_username={aut2_username}, aut2_time={aut2_time}')

    validation_error = validate_ticket(tgs_username, aut2_username, tgs_start_time, aut2_time, tgs_end_time)
    if validation_error:
        return validation_error

    answer = f'{int(aut2_time) + 1}'
    logger.info(f'answer={answer}')

    answer_encrypted = encrypt(answer, K_c_ss)
    logger.info(f'answer_encrypted={answer_encrypted} | encrypted with K_c_ss={K_c_ss}')

    return answer_encrypted, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082)