from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from src.database.config import get_db
from src.database.repositorio import ReservasRepositorio
from pydantic import BaseModel

app = FastAPI()

_HTML = """<!DOCTYPE html><html><body>
<input data-testid="input-email-cliente" type="email">
<select data-testid="select-zona-evento">
  <option value="VIP">VIP</option>
  <option value="General">General</option>
</select>
<input data-testid="input-cantidad-asientos" type="number">
<button data-testid="btn-confirmar-reserva" type="button">Confirmar</button>
<div data-testid="seccion-resumen-total" style="display:none"></div>
<script>
document.querySelector('[data-testid="btn-confirmar-reserva"]').addEventListener('click',async()=>{
  const email=document.querySelector('[data-testid="input-email-cliente"]').value;
  const zona=document.querySelector('[data-testid="select-zona-evento"]').value;
  const cantidad=parseInt(document.querySelector('[data-testid="input-cantidad-asientos"]').value);
  await fetch('/reservas/evento-frontend-test',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cliente_email:email,zona:zona,cantidad:cantidad})});
  const res=await fetch('/reservas/evento-frontend-test/resumen');
  const data=await res.json();
  const s=document.querySelector('[data-testid="seccion-resumen-total"]');
  s.textContent=data.total_recaudado.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.');
  s.style.display='block';
});
</script>
</body></html>"""

@app.get("/reservas", response_class=HTMLResponse)
def frontend_reservas():
    return _HTML

class ReservaInput(BaseModel):
    cliente_email: str
    zona: str
    cantidad: int

@app.post("/reservas/{evento_id}", status_code=201)
def crear_reserva(evento_id: str, reserva: ReservaInput, db: Session = Depends(get_db)):
    if reserva.zona not in ["VIP", "General"]:
        raise HTTPException(status_code=400, detail="Zona invalida")
    if reserva.cantidad < 1:
        raise HTTPException(status_code=400, detail="Cantidad invalida")

    repo = ReservasRepositorio(db)
    nueva_reserva = repo.guardar_reserva(evento_id, reserva.cliente_email, reserva.zona, reserva.cantidad)
    return {"mensaje": "Reserva creada con exito", "reserva_id": nueva_reserva.id}

@app.get("/reservas/{evento_id}/resumen", status_code=200)
def obtener_resumen(evento_id: str, db: Session = Depends(get_db)):
    repo = ReservasRepositorio(db)
    total_recaudado = repo.calcular_total_evento(evento_id)
    return {"evento_id": evento_id, "total_recaudado": total_recaudado}
