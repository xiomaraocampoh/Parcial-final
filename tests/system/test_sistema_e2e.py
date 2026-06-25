def test_flujo_completo_calculo_total(client_con_bd):
    payload = {
        "cliente_email": "sistema@test.com",
        "zona": "General",
        "cantidad": 3
    }
    response_post = client_con_bd.post("/reservas/sistema-evento-xyz", json=payload)
    assert response_post.status_code == 201

    response_get = client_con_bd.get("/reservas/sistema-evento-xyz/resumen")
    assert response_get.status_code == 200

    data = response_get.json()
    assert data["total_recaudado"] == 150000
