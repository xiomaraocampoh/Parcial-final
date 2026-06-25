import httpx

def test_flujo_completo_calculo_total():
    base_url = "http://localhost:8000"

    payload = {
        "cliente_email": "sistema@test.com",
        "zona": "General",
        "cantidad": 3
    }
    response_post = httpx.post(f"{base_url}/reservas/sistema-evento-xyz", json=payload)
    assert response_post.status_code == 201

    response_get = httpx.get(f"{base_url}/reservas/sistema-evento-xyz/resumen")
    assert response_get.status_code == 200

    data = response_get.json()
    assert data["total_recaudado"] == 150000
