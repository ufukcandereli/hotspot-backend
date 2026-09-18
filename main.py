from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Aşama: URL'deki MikroTik parametrelerini (mac ve link_login) yakala
@app.get("/", response_class=HTMLResponse)
async def read_survey(request: Request, mac: str = "", link_login: str = ""):
    # Parametreleri HTML'deki {{ mac }} ve {{ link_login }} alanlarına gönderiyoruz
    return templates.TemplateResponse(
        request=request, 
        name="survey.html",
        context={"mac": mac, "link_login": link_login}
    )

# 2. Aşama: Veriyi kaydet ve MikroTik'e (link_login) geri yönlendir
@app.post("/submit")
async def submit_survey(
    full_name: str = Form(...),
    phone: str = Form(...),
    satisfaction: int = Form(...),
    mac: str = Form(""),         # Formdan gelen gizli veri
    link_login: str = Form(""),  # Formdan gelen gizli veri
    db: Session = Depends(get_db)
):
    # Veritabanına kaydet
    yeni_kayit = models.Survey(
        full_name=full_name,
        phone=phone,
        satisfaction=satisfaction
    )
    db.add(yeni_kayit)
    db.commit()

    # Eğer formda MikroTik'in yönlendirme linki varsa, müşteriyi oraya fırlat
    if link_login:
        # Şifre ve kullanıcı adını form doldurulduktan SONRA ekliyoruz
        hedef_url = f"{link_login}?username=misafir&password=123"
        return RedirectResponse(url=hedef_url, status_code=303)
    
    # URL'den test edilirse ve parametre yoksa bu mesaj görünür
    return {"durum": "basarili", "mesaj": f"Kaydedildi. Test ortamı olduğu için yönlendirme yapılmadı. MAC: {mac}"}