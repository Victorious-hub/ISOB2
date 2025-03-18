
import os


SERVER_URL = {
    "AS": os.getenv("AS_URL", "http://127.0.0.1:8080"),
    "TGS": os.getenv("TGS_URL", "http://127.0.0.1:8081"),
    "SS": os.getenv("SS_URL", "http://127.0.0.1:8082")
}

SERVER_ID = {
    "SS": os.getenv("SS_ID", "ss")
}

KEYS = {
    "AS_TGS" : 'as-tgs-secret',
    "C_TGS" : 'c-tgs-secret',
    "TGS_SS": 'tgs-ss-secret',
    "C_SS": 'c-ss-secret',
}

SERVER_ID = {
    "TGS": 'tgs'
}
