from app import app, get_messages, init_db  # Import để test

def test_hello():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert "Hello World" in response.data.decode('utf-8')

# Mock test cho DB (không connect thật)
import os
os.environ['DB_HOST'] = 'invalid'  # Để test fail case
def test_get_messages_fail():
    messages = get_messages()
    assert "DB connection failed!" in messages

# Test init_db không crash
def test_init_db():
    # Không assert gì, chỉ call để check no error
    init_db()