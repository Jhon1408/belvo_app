import requests
from enviroment.helpers.get_variable import get_variable
from banking_api.helpers.save_request import save_request

ENDPOINTS = {
    "accouts": "api/accounts",
    "transactions": "api/transactions",
    "balances": "api/balances",
    "owners": "api/owners",
    "portfolios": "investments/portfolios",
    "receivable_transactions": "receivables/transactions",
}


class BelvoAPI:
    """Class to handle the requests to the Belvo API"""

    def __init__(self):
        self.url = get_variable("BELVO_API_URL")
        self.secret_id = get_variable("BELVO_API_SECRET")
        self.secret_password = get_variable("BELVO_API_PASSWORD")
        self.session = self._get_session()

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    # Account methods

    def get_all_accounts(self, filters=None):
        """Get all accounts"""
        endpoint = self._get_endpoint_url("accouts")
        response = self.session.get(endpoint, params=filters)
        self._save_request(endpoint, "GET", None, response.json())
        if filters and filters.get("page"):
            return self._get_paginated_response(response, [])
        return response.json()

    def get_account_details_by_id(self, account_id):
        """Get account details by id"""
        endpoint = f"{self._get_endpoint_url('accouts')}/{account_id}/"
        response = self.session.get(endpoint)
        self._save_request(endpoint, "GET", None, response.json())
        return response.json()

    # Transaction methods

    def get_all_transactions(self, filters=None):
        """Get all transactions"""
        endpoint = self._get_endpoint_url("transactions")
        response = self.session.get(endpoint, params=filters)
        self._save_request(endpoint, "GET", None, response.json())
        if filters and filters.get("page"):
            return self._get_paginated_response(response, [])
        return response.json()

    def get_transactions_by_id(self, transaction_id):
        """Get transactions by id"""
        endpoint = f"{self._get_endpoint_url('transactions')}/{transaction_id}/"
        response = self.session.get(endpoint)
        self._save_request(endpoint, "GET", None, response.json())
        return response.json()

    # Balance methods

    def get_all_balances(self, filters=None):
        """Get all balances"""
        endpoint = self._get_endpoint_url("balances")
        response = self.session.get(endpoint, params=filters)
        self._save_request(endpoint, "GET", None, response.json())
        if filters and filters.get("page"):
            return self._get_paginated_response(response, [])
        return response.json()

    def get_balance_by_id(self, balance_id):
        """Get balance by id"""
        endpoint = f"{self._get_endpoint_url('balances')}/{balance_id}/"
        response = self.session.get(endpoint)
        self._save_request(endpoint, "GET", None, response.json())
        return response.json()

    # Owner methods

    def get_all_owners(self, filters=None):
        """Get all owners"""
        endpoint = self._get_endpoint_url("owners")
        response = self.session.get(endpoint, params=filters)
        self._save_request(endpoint, "GET", None, response.json())
        if filters and filters.get("page"):
            return self._get_paginated_response(response, [])
        return response.json()

    def get_owner_by_id(self, owner_id):
        """Get owner by id"""
        endpoint = f"{self._get_endpoint_url('owners')}/{owner_id}/"
        response = self.session.get(endpoint)
        self._save_request(endpoint, "GET", None, response.json())
        return response.json()

    # Portfolio methods

    def get_all_portfolios(self, filters=None):
        """Get all portfolios"""
        endpoint = self._get_endpoint_url("portfolios")
        response = self.session.get(endpoint, params=filters)
        self._save_request(endpoint, "GET", None, response.json())
        if filters and filters.get("page"):
            return self._get_paginated_response(response, [])
        return response.json()

    def get_portfolio_by_id(self, portfolio_id):
        """Get portfolio by id"""
        endpoint = f"{self._get_endpoint_url('portfolios')}/{portfolio_id}/"
        response = self.session.get(endpoint)
        self._save_request(endpoint, "GET", None, response.json())
        return response.json()

    # Receivables transaction methods

    def get_all_receivables_transactions(self, filters=None):
        """Get all receivables transactions"""
        endpoint = self._get_endpoint_url("receivable_transactions")
        response = self.session.get(endpoint, params=filters)
        self._save_request(endpoint, "GET", None, response.json())
        if filters and filters.get("page"):
            return self._get_paginated_response(response, [])
        return response.json()

    def get_receivables_transaction_by_id(self, transaction_id):
        """Get receivables transaction by id"""
        endpoint = (
            f"{self._get_endpoint_url('receivable_transactions')}/{transaction_id}/"
        )
        response = self.session.get(endpoint)
        self._save_request(endpoint, "GET", None, response.json())
        return response.json()

    # ------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------

    def _get_session(self):
        """Get the session to the Belvo API"""
        session = requests.Session()
        session.auth = (self.secret_id, self.secret_password)
        session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )
        return session

    def _get_endpoint_url(self, endpoint):
        """Get the endpoint url"""
        return f"{self.url}{ENDPOINTS[endpoint]}"

    def _save_request(self, request_endpoint, request_method, request_data, response):
        """Save the request made to the Belvo API"""
        save_request(request_endpoint, request_method, request_data, response)

    def _get_paginated_response(self, response, results=None):
        """Handle the pagination of the Belvo API"""
        if results is None:
            results = []
        results += response.json()["results"]
        if "next" in response.json() and response.json()["next"] is not None:
            print("More pages found, getting the next page...")
            response = self.session.get(response.json()["next"])
            return self._get_paginated_response(response, results)
        return results
