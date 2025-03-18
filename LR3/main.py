from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import requests
from utils import encrypt, decrypt

app = FastAPI()

SERVER_URL = {
    "AS": "http://127.0.0.1:8080",
    "TGS": "http://127.0.0.1:8081",
    "SS": "http://127.0.0.1:8082"
}

SERVER_ID = {
    "SS": "ss"
}

# Pydantic models for responses
class AuthResponse(BaseModel):
    step: str
    data: dict

class AuthenticationResult(BaseModel):
    status: str
    as_response: AuthResponse
    tgs_response: AuthResponse
    ss_response: AuthResponse

class AuthData(BaseModel):
    username: str
    password: str


@app.post("/auth", response_model=AuthenticationResult)
async def authenticate(auth_data: AuthData):
    username = auth_data.username
    password = auth_data.password

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be 8 symbols long.")

    # Step 1
    as_request_url = f"{SERVER_URL['AS']}/{username}"
    response = requests.get(as_request_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"AS server answered with: {response.status_code}")

    # Step 2
    decrypted_response = decrypt(response.text, password)
    TGT_encrypted, K_c_tgs = decrypted_response.split(';')

    # Step 3
    aut1 = f"{username};{int(time.time())}"
    aut1_encrypted = encrypt(aut1, K_c_tgs)

    tgs_request_data = f"{TGT_encrypted};{aut1_encrypted};{SERVER_ID['SS']}"
    response_tgs = requests.post(SERVER_URL["TGS"], data=tgs_request_data)
    if response_tgs.status_code != 200:
        raise HTTPException(status_code=response_tgs.status_code, detail=f"TGS server answered with: {response_tgs.status_code}")

    # Step 4
    decrypted_tgs_response = decrypt(response_tgs.text, K_c_tgs)
    TGS_encrypted, K_c_ss = decrypted_tgs_response.split(';')

    # Step 5
    t4 = int(time.time())
    aut2 = f"{username};{t4}"
    aut2_encrypted = encrypt(aut2, K_c_ss)

    ss_request_data = f"{TGS_encrypted};{aut2_encrypted}"
    response_ss = requests.post(SERVER_URL["SS"], data=ss_request_data)
    if response_ss.status_code != 200:
        raise HTTPException(status_code=response_ss.status_code, detail=f"SS server answered with: {response_ss.status_code}")

    # Step 6
    decrypted_ss_response = decrypt(response_ss.text, K_c_ss)
    if int(decrypted_ss_response.split(';')[0]) != t4 + 1:
        raise HTTPException(status_code=400, detail="SS server verification failed!")

    # Final response structure with all data
    return AuthenticationResult(
        status="OK!",
        as_response=AuthResponse(step="1 & 2", data={
            "TGT_encrypted": TGT_encrypted,
            "K_c_tgs": K_c_tgs
        }),
        tgs_response=AuthResponse(step="3 & 4", data={
            "TGS_encrypted": TGS_encrypted,
            "K_c_ss": K_c_ss
        }),
        ss_response=AuthResponse(step="5 & 6", data={
            "aut2_encrypted": aut2_encrypted,
            "ss_response_decrypted": decrypted_ss_response
        })
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
