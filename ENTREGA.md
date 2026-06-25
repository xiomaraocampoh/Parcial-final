

## Paso 3: Verificar antes de hacer commit

cd parcial
python -m pytest tests/integration/ -v

Deben pasar todas las pruebas de integracion antes de hacer el commit.

## Paso 4: Commits paso a paso

Hacer un commit por cada requerimiento cumplido. Desde la raiz del repositorio:

### Commit 1 - Contenerizacion
git add parcial/Dockerfile parcial/Dockerfile.test parcial/docker-compose.test.yml parcial/requirements.txt
git commit -m "feat: add Docker configuration for production and test environments"

### Commit 2 - Modelos y repositorio
git add parcial/src/
git commit -m "feat: add database models and repository layer"

### Commit 3 - API
git add parcial/src/reservas/api.py
git commit -m "feat: add FastAPI endpoints for reservas"

### Commit 4 - Fixtures de prueba
git add parcial/tests/conftest.py parcial/pytest.ini
git commit -m "feat: configure pytest fixtures with TestContainers and rollback pattern"

### Commit 5 - Pruebas de integracion
git add parcial/tests/integration/
git commit -m "test: add integration tests for repository and API"

### Commit 6 - Pruebas de sistema
git add parcial/tests/system/
git commit -m "test: add system E2E test with full business flow"

### Commit 7 - Pruebas E2E frontend
git add parcial/tests/e2e/
git commit -m "test: add Playwright E2E test for frontend flow"

## Paso 5: Push
git push origin main
