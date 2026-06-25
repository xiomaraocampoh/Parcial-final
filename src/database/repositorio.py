from sqlalchemy.orm import Session
from src.database.models import ReservaDB

PRECIOS = {
    "VIP": 150000,
    "General": 50000
}

class ReservasRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def guardar_reserva(self, evento_id: str, cliente_email: str, zona: str, cantidad: int) -> ReservaDB:
        reserva = ReservaDB(
            evento_id=evento_id,
            cliente_email=cliente_email,
            zona=zona,
            cantidad=cantidad
        )
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def calcular_total_evento(self, evento_id: str) -> float:
        reservas = self.db.query(ReservaDB).filter(ReservaDB.evento_id == evento_id).all()
        total = 0
        for reserva in reservas:
            precio = PRECIOS.get(reserva.zona, 0)
            total += precio * reserva.cantidad
        return total
