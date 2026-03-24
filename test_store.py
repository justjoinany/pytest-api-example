from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_, any_of, equal_to

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture
def post_order(request):
    test_endpoint = "/store/order"
    params = {
        "pet_id": request.param,
    }
    response = api_helpers.post_api_data(test_endpoint, params)
    if response.status_code != 201:
        pytest.skip(f"Pet with ID {params["pet_id"]} is not available for order")
    return response.json()

@pytest.mark.parametrize("post_order, target_status", [
    (0, "available"), #pet_id, expectd status
    (1, "pending"),
    (2, "available"),
    (3, "sold"),
], indirect=["post_order"])
def test_patch_order_by_id(post_order, target_status):
    order_id = post_order["id"]
    pet_id = post_order["pet_id"]
    test_endpoint = f"/store/order/{order_id}"
    params = {
        "status": target_status,
    }
    response = api_helpers.patch_api_data(test_endpoint, params)
    assert response.status_code == 200
    assert_that(response.json()["message"], equal_to("Order and pet status updated successfully"))

    test_endpoint = f"/pets/{pet_id}"
    check_pet_applied = api_helpers.get_api_data(test_endpoint)
    assert_that(check_pet_applied.json()["status"], equal_to(target_status))

