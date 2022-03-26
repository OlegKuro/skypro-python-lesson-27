import pytest


@pytest.mark.django_db
def test_create_selection(client, create_selection_test_cases_provider):
    for (hint, body, expected_response_code, token) in create_selection_test_cases_provider:
        response = client.post("/selections/create/", body, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response.status_code == expected_response_code, hint
