from app.services.quickbooks_client import QuickBooksClient


class CustomerService:

    @staticmethod
    def get_customers(realm_id: str):

        query = """
        SELECT *
        FROM Customer
        MAXRESULTS 100
        """

        response = QuickBooksClient.post_query(
            realm_id=realm_id,
            query=query,
        )

        return response.get(
            "QueryResponse",
            {}
        ).get(
            "Customer",
            []
        )