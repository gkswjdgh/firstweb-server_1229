import uvicorn
import webbrowser
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles       # 추가됨
from fastapi.templating import Jinja2Templates    # 추가됨
from pythonosc import udp_client

app = FastAPI()

# 1. 터치디자이너 연결
td_client = udp_client.SimpleUDPClient("127.0.0.1", 10000)

# 2. [핵심] 폴더 연결 설정
# static 폴더를 '/static' 주소로 연결 (CSS, JS용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates 폴더를 HTML 템플릿용으로 설정
templates = Jinja2Templates(directory="templates")


# 3. 라우팅
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # 이제 변수가 아니라, templates 폴더 안의 파일을 찾아 보여줌
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/btn/{name}")
async def process_btn(name: str):
    print(f"[BTN] {name}")
    td_client.send_message("/click", name)
    return "ok"

@app.get("/slider/{name}/{val}")
async def process_slider(name: str, val: int):
    val_float = val / 100.0
    print(f"[SLIDER] {name}: {val_float}")
    td_client.send_message(f"/{name}", val_float)
    return "ok"

if __name__ == "__main__":
    # Hot Reload 켜기 (코드 수정하면 자동 재부팅)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # 주의: reload=True를 쓸 때는 webbrowser.open이 중복 실행될 수 있어서 뺍니다.
    # 브라우저 주소창에 직접 http://127.0.0.1:8000 입력해주세요.