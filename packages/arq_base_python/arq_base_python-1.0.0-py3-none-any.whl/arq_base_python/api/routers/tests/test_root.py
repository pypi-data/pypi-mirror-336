from fastapi.testclient import TestClient
from api.routes import router
client = TestClient(router)


def test_health_check():
    """
    Testea el endpoint de health check
    """
    # Arrange: Preparar cualquier configuración necesaria (en este caso no es necesario)

    # Act: Realizar la solicitud GET al endpoint de health check
    response = client.get("/anon/health")

    # Assert: Verificar que el resultado es el esperado
    assert response.status_code == 200
    assert response.text == "OK"
