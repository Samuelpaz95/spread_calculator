

from test.config import override_get_db
from test.e2e.boda_api_mock import buda_api_mock

from fastapi.testclient import TestClient

from app import app
from app.config import get_db
from app.services.buda_api import BudaApi

# environment variables
import os
os.environ['BUDA_API_URL'] = 'http://localhost:8000/api/v2'

client = TestClient(app)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[BudaApi] = lambda: buda_api_mock
