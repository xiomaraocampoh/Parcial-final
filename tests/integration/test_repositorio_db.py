from src.database.repositorio import ReservasRepositorio
from src.database.models import ReservaDB

def test_guardar_reserva_persiste_en_bd(db_session):
    repo = ReservasRepositorio(db_session)
    reserva = repo.guardar_reserva("evento-repo-test", "cliente@test.com", "General", 2)

    resultado = db_session.query(ReservaDB).filter(ReservaDB.id == reserva.id).first()
    assert resultado is not None
    assert resultado.cliente_email == "cliente@test.com"
