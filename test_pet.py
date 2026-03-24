from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_, equal_to, any_of

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    if response.status_code in [403, 404]:
        pytest.fail("Forbidden. Server is blocking the request")

    assert response.status_code == 200
    # Validate the response schema against the defined schema in schemas.py
    # vernon = response.json()
    validate(instance=response.json(), schema=schemas.pet)
    # print(vernon)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    # TODO...
    assert response.status_code == 200
    pets = response.json()
    for pet in pets:
        assert_that(pet["status"], is_(equal_to(status)))
        validate(instance=pet, schema=schemas.pet)
    print(pets)

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''

@pytest.mark.parametrize("pet_id", [4, 1000, -1, "vernon", 0.01, "v"])
def test_get_by_id_404(pet_id):
    # TODO...
    test_endpoint = "/pets/" + str(pet_id)
    params = {
        "pet_id": pet_id
    }
    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 404
    assert_that(response.text, any_of(
        contains_string(f"Pet with ID {pet_id} not found"),
        contains_string(f"404 Not Found")
    ))
    # print(response)