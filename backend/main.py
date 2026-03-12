# from import
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

#다른 도메인에서 이 서버 API를 호출할 수 있게 허용하는 것
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #허용하고 싶은 도메인입력 *=모든 문자(도메인)용
    allow_methods=["*"],
    allow_headers=["*"]
)

class Msg(BaseModel):
    text:str

#허깅페이스 접속정보
HF_URL = "https://router.huggingface.co/v1/chat/completions"
HF_MODEL = "Qwen/Qwen2.5-72B-Instruct" 

#채팅요청함수
def ask_ai(q):
    token=os.getenv("HF_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    payload={
        "model":HF_MODEL,
        "messages":[{"role":"user","content":q}],
        "max_tokens":300
    }
    res=requests.post(HF_URL,headers=headers,json=payload)

    #json 자바스크립트 객체 문법과 유사한 데이터베이스 형식
    data=res.json() #서버에서 응답받은걸 제이슨으로 바꾸는것
    return data["choices"][0]["message"]["content"]

@app.post("/chat")
def chat(msg : Msg): 
    reply=ask_ai(msg.text)
    return {"reply":reply}