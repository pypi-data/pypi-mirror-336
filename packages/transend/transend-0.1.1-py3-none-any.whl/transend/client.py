import requests
import os
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class BaseAPI:
    def __init__(self, api_key: str, api_token: str, base_url: str) -> None:
        """
        Base class for all API classes
        """
        self.api_key = api_key
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def _make_request(self, method, endpoint, params=None, data=None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

class ProductAPI(BaseAPI):
    def __init__(self, api_key: str, api_token: str, base_url:str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/product"

    def get_all_sort_types(self) -> List[Dict]:
        """Get all sort types."""
        return self._make_request("GET", "/sort/type")

    def get_all_tags(self) -> List[Dict]:
        """Get all tags."""
        return self._make_request("GET", "/tag")

    def get_availability_by_item_id(self, item_id) -> List[Dict]:
        """Get availability by item id."""
        return self._make_request("GET", f"/{item_id}/availability")

    def get_available_quantity(self, item_id, branch_number: str, availability_type_id):
        """Get available quantity."""
        params = {
            "itemId": item_id,
            "branchNumber": branch_number,
            "availabilityTypeId": availability_type_id
        }
        return self._make_request("GET", "/quantity/available", params=params)

    def get_brands(self, vhid=None, phid=None) -> List[Dict]:
        """Get brands."""
        params = {}
        if vhid:
            params["vhid"] = vhid
        if phid:
            params["phid"] = phid
        return self._make_request("GET", "/brand", params=params)

    def get_categories(self, vhid=None, phid=None, search_id=None) -> List[Dict]:
        """Get categories."""
        params = {}
        if vhid:
            params["vhid"] = vhid
        if phid:
            params["phid"] = phid
        if search_id:
            params["searchId"] = search_id
        return self._make_request("GET", "/category", params=params)

class AccountAPI(BaseAPI):
    def __init__(self, api_key: str, api_token: str, base_url:str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/account"

    def delete_bank_account(self, customer_stripe_id: int) -> None:
        """Delete a bank account."""
        self._make_request("DELETE", f"/bank-account/{customer_stripe_id}")

    def update_credit_card_default(self, credit_card_guid: UUID) -> None:
        """Update the default credit card."""
        self._make_request("PUT", f"/credit-card/{credit_card_guid}")

    def delete_credit_card(self, credit_card_guid: UUID) -> None:
        """Delete a credit card."""
        self._make_request("DELETE", f"/credit-card/{credit_card_guid}")

    def get_active_bank_accounts(self) -> List[Dict]:
        """Get active bank accounts."""
        return self._make_request("GET", "/bank-account/active")

    def get_credit_cards(self) -> List[Dict]:
        """Get credit cards."""
        return self._make_request("GET", "/credit-card")

    def post_credit_card(self, card_data: Dict) -> UUID:
        """Post a credit card."""
        return self._make_request("POST", "/credit-card", data=card_data)

    def get_customer_info(self) -> Dict:
        """Get customer information."""
        return self._make_request("GET", "/customer/current")

    def get_verified_bank_accounts(self) -> List[Dict]:
        """Get verified bank accounts."""
        return self._make_request("GET", "/bank-account/verified")

    def post_bank_account(self, bank_account_data: Dict) -> UUID:
        """Add a bank account."""
        return self._make_request("POST", "/bank-account", data=bank_account_data)

    def verify_bank_account(self, verification_data: Dict) -> Dict:
        """Verify a bank account."""
        return self._make_request("PUT", "/bank-account/verify", data=verification_data)

class ContentAPI(BaseAPI):
    def __init__(self,api_key: str, api_token: str, base_url:str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/content"

    def get_article_resources(self, article_id: int) -> List[Dict]:
        """Get article resources."""
        return self._make_request("GET", f"/article/{article_id}/resource")

    def get_articles(self) -> List[Dict]:
        """Get articles."""
        return self._make_request("GET", "/article")

class CoreAPI(BaseAPI):
    def __init__(self, api_key: str, api_token: str, base_url: str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/core"

    def get_open_cores(self) -> List[Dict]:
        """Get open cores."""
        return self._make_request("GET", "/open")

class CustomerAPI(BaseAPI):
    def __init__(self, api_key: str, api_token: str, base_url: str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/customer"

    def get_users(self) -> List[Dict]:
        """Get users."""
        return self._make_request("GET", "/user")


class BranchAPI(BaseAPI):
    def __init__(self, api_key: str, api_token: str, base_url: str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/branch"

    def get_all_branches(self, active=None) -> List[Dict]:
        """Get all branches."""
        params = {"active": active} if active is not None else None
        return self._make_request("GET", "/", params=params)

    def get_branch_by_number(self, branch_number: str) -> List[Dict]:
        """Get branch by number."""
        return self._make_request("GET", f"/{branch_number}")


class VehicleAPI(BaseAPI):
    def __init__(self, api_key: str, api_token: str, base_url: str) -> None:
        super().__init__(api_key, api_token, base_url)
        self.base_url = f"{base_url}/vehicle"

    def get_all_dtcs(self) -> List[Dict]:
        """Get all Diagnostic Trouble Codes."""
        return self._make_request("GET", "/dtcs")

    def get_drive_types_by_vhid(self, vhid: str) -> List[Dict]:
        """Get drive types by vhid."""
        return self._make_request("GET", f"/drivetype/{vhid}")

    def get_engines_by_vhid(self, vhid: str) -> List[Dict]:
        """Get engines by vhid."""
        return self._make_request("GET", f"/engine/{vhid}")

    def get_makes_by_vhid(self, vhid: str) -> List[Dict]:
        """Get makes by vhid."""
        return self._make_request("GET", f"/make/{vhid}")

    def get_models_by_vhid(self, vhid: str) -> List[Dict]:
        """Get models by vhid."""
        return self._make_request("GET", f"/model/{vhid}")

    def get_submodels_by_vhid(self, vhid: str) -> List[Dict]:
        """Get submodels by vhid."""
        return self._make_request("GET", f"/submodel/{vhid}")

    def get_transmissions(self, tag_number=None, transmission_mfr_code=None) -> List[Dict]:
        """Get transmission information."""
        params = {}
        if tag_number:
            params["tagNumber"] = tag_number
        if transmission_mfr_code:
            params["transmissionMfrCode"] = transmission_mfr_code
        return self._make_request("GET", "/transmission", params=params)

    def get_vehicle_by_vhid(self, vhid: str) -> List[Dict]:
        """Get vehicle information by vhid."""
        return self._make_request("GET", f"/{vhid}")

    def get_vehicles_by_vin(self, vin: str) -> List[Dict]:
        """Get vehicle information by VIN."""
        return self._make_request("GET", f"/vin/{vin}")

    def get_years(self, vhid: str = None) -> List[Dict]:
        """Get the years for a given vhid."""
        if vhid:
            return self._make_request("GET", f"/years/{vhid}")
        return self._make_request("GET", f"/years")

    def get_year_make_model_vhid(self, year: int, make: str, model: str) -> Dict:
        """Get the vhid for a given year, make, and model."""
        make = make.lower()
        model = model.lower()
        # Fetch years and find the corresponding vhid
        years_data = self.get_years()
        year_vhid = self._find_vhid_by_attribute(years_data, "year", year)

        if not year_vhid:
                return {"error": "Year not found"}

        # Fetch makes and find the corresponding vhid
        makes_data = self.get_makes_by_vhid(year_vhid)
        make_vhid = self._find_vhid_by_attribute(makes_data, "name", make)

        if not make_vhid:
            return {"error": "Make not found"}

        # Fetch models and find the corresponding vhid
        models_data = self.get_models_by_vhid(make_vhid)
        model_vhid = self._find_vhid_by_attribute(models_data, "name", model)

        if not model_vhid:
            return {"error": "Model not found"}

        return {"vhid": model_vhid}

    def _find_vhid_by_attribute(
        self, data: List , attribute: str, value: Any) -> Optional[str]:
        """Find the vhid for a given attribute value in the list of dictionaries."""
        for item in data:
            if str(item.get(attribute, "")).lower() == str(value).lower():
                return item.get("vhid")
        return None


class TransendAPIClient:
    def __init__(self, api_key: str, api_token: str, base_url: str = "https://api.transend.us") -> None:
        self.product = ProductAPI(api_key, api_token, base_url)
        self.branch = BranchAPI(api_key, api_token, base_url)
        self.vehicle = VehicleAPI(api_key, api_token, base_url)
        self.account = AccountAPI(api_key, api_token, base_url)
        self.content = ContentAPI(api_key, api_token, base_url)
        self.core = CoreAPI(api_key, api_token, base_url)
        self.customer = CustomerAPI(api_key, api_token, base_url)


if __name__ == "__main__":
    api_key = os.getenv("TRANSEND_API_KEY")
    api_token = os.getenv("TRANSEND_API_TOKEN")
    client = TransendAPIClient(api_key, api_token)
    
    # Example usage of new APIs
    customer_info = client.account.get_customer_info()
    articles = client.content.get_articles()
    open_cores = client.core.get_open_cores()
    users = client.customer.get_users()
    print(customer_info)


    # Usage example:
    sort_types = client.product.get_all_sort_types()
    branches = client.branch.get_all_branches()
    dtcs = client.vehicle.get_all_dtcs()
    get_years = client.vehicle.get_years()
    print(sort_types, branches, dtcs)
    vhid = client.vehicle.get_year_make_model_vhid(2010, "Toyota", "Camry")
    vehicle = client.vehicle.get_vehicle_by_vhid(vhid["vhid"])
    branch = client.branch.get_branch_by_number("420")
    print(vehicle, branch)
