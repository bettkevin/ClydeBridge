from app.services.quickbooks_client import QuickBooksClient


class InvoiceService:

    @staticmethod
    def get_invoices(realm_id: str):
        query = """
        SELECT *
        FROM Invoice
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
            "Invoice",
            []
        )

    @staticmethod
    def find_invoice_by_number(
        realm_id: str,
        invoice_number: str,
    ):
        query = f"""
        SELECT *
        FROM Invoice
        WHERE DocNumber = '{invoice_number}'
        """

        response = QuickBooksClient.post_query(
            realm_id=realm_id,
            query=query,
        )

        invoices = response.get(
            "QueryResponse",
            {}
        ).get(
            "Invoice",
            []
        )

        if not invoices:
            return None

        return invoices[0]

    @staticmethod
    def find_invoice_by_id(
        realm_id: str,
        invoice_id: str,
    ):
        query = f"""
        SELECT *
        FROM Invoice
        WHERE Id = '{invoice_id}'
        """

        response = QuickBooksClient.post_query(
            realm_id=realm_id,
            query=query,
        )

        invoices = response.get(
            "QueryResponse",
            {}
        ).get(
            "Invoice",
            []
        )

        if not invoices:
            return None

        return invoices[0]