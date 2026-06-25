from playwright.sync_api import sync_playwright

def test_reserva_vip_muestra_total_en_frontend():
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
