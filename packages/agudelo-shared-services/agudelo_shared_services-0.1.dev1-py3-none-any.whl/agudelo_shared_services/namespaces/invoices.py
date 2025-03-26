from flask_restx import Resource, Namespace
from sqlalchemy import select
from agudelo_shared_services.models import Invoice
from agudelo_shared_services.db import db_session
# import gzip

inv_ns = Namespace("invoices", description="Facturas de la Familia")


@inv_ns.route("/")
@inv_ns.doc(
    responses={404: "Todo not found"},
)
class Invoices(Resource):
    """Shows you a Invoice"""

    @inv_ns.doc(description="It shows all invoices ")
    def get(self):
        inv_ns.logger.info("Showing all invoices")
        stm = select(Invoice)
        invoices = db_session.execute(stm)
        return invoices.all()
