import pytest


@pytest.mark.django_db
def test_create_ad(client, create_ad_test_cases_provider):
    for (hint, body, expected_response_code, token) in create_ad_test_cases_provider:
        response = client.post("/ad/", body, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        assert response.status_code == expected_response_code, hint
