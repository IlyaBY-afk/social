from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("testuser1@example.com", "Champ1on_FAS", 400),
    ('testuser@gmail.com', 'Ch@mp1on_TES', 201),
    ('testuser@gmail.com', 'Ch@mp1on_TES', 400),
    ('testuser2@gmail.com', '', 400),
    ('abcde', 'Champ1on_TES', 422),
    ('@', 'Champ1on_TES', 422),
    ('a@b', 'Champ1on_TES', 422),
], )

async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email': email,
        'password': password
    })
    print(response.json())
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("testuser1@example.com", "Ch@mp1on_TES", 200),
    ("testuser1@example.com", "abc", 400),
    ("abc", "abc", 400)
], )

async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/jwt/login', data={
        'username': email,
        'password': password
    })
    print(response.json())
    assert response.status_code == status_code