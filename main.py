from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import db_utils

# Инициализация приложения
app = FastAPI(title="CyberSecurity Info")

# Подключаем папки со статикой и шаблонами
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Запускаем инициализацию БД при старте
@app.on_event("startup")
def startup():
    db_utils.init_db()

# Главная страница (список инструкций + поиск)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, q: str = Query(None)):
    if q:
        instructions = db_utils.search_instructions(q.lower())
        print(f"DEBUG: Search results for '{q}': {instructions}")
    else:
        instructions = db_utils.get_all_instructions()
        print(f"DEBUG: All instructions: {instructions}")
        q = ""
    
    print(f"DEBUG: Type of instructions: {type(instructions)}")
    if instructions:
        print(f"DEBUG: First item type: {type(instructions[0])}, value: {instructions[0]}")
    
    return templates.TemplateResponse(request,
        "index.html",
        {
            "request": request,
            "instructions": instructions,
            "search_query": q
        }
    )
   
    

# Страница просмотра конкретной инструкции
@app.get("/instruction/{instr_id}", response_class=HTMLResponse)
async def read_instruction(request: Request, instr_id: int):
    result = db_utils.get_instruction_by_id(instr_id)
    if not result:
        return HTMLResponse("<h1>Инструкция не найдена</h1>", status_code=404)
    
    title, content = result
    # Заменяем переносы строк на тег <br> для отображения в HTML
    content_html = content.replace('\n', '<br>')
    
    return templates.TemplateResponse(request,"index.html", {
        "request": request, 
        "detail_title": title, 
        "detail_content": content_html,
        "instructions": db_utils.get_all_instructions() # Для бокового меню
    })