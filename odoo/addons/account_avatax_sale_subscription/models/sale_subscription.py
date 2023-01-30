from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _recurring_create_invoice(self, automatic=False, batch_size=20):
        invoices = super()._recurring_create_invoice(automatic, batch_size)
        # Already compute taxes for unvalidated documents as they can already be paid
        invoices.filtered(lambda m: m.state == 'draft').button_update_avatax()
        return invoices
