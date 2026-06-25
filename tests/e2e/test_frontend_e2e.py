import threading
import time
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from playwright.sync_api import sync_playwright
from src.reservas.api import app
from src.database.models import Base
from src.database.config import get_db


def test_reserva_vip_muestra_total_en_frontend():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    config = uvicorn.Config(app, host="127.0.0.1", port=4200, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(1.5)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:4200/reservas")
            page.get_by_test_id("input-email-cliente").fill("frontend@test.com")
            page.get_by_test_id("select-zona-evento").select_option("VIP")
            page.get_by_test_id("input-cantidad-asientos").fill("1")
            page.get_by_test_id("btn-confirmar-reserva").click()
            seccion = page.get_by_test_id("seccion-resumen-total")
            seccion.wait_for()
            assert "150.000" in seccion.inner_text()
            browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        app.dependency_overrides.clear()
