from odoo.tests.common import tagged
from odoo.addons.account_avatax.tests.common import TestAccountAvataxCommon
from odoo.addons.sale_subscription.tests.common_sale_subscription import TestSubscriptionCommon


@tagged("-at_install", "post_install")
class TestSaleSubscriptionAvalara(TestAccountAvataxCommon, TestSubscriptionCommon):
    def test_01_subscription_avatax_called(self):
        partner = self.user_portal.partner_id
        partner.property_account_position_id = self.fp_avatax
        partner.country_id = self.env.ref('base.us')
        partner.zip = '94134'
        partner.state_id = self.env.ref('base.state_us_5') # California

        with self._capture_request({'lines': [], 'summary': []}) as capture:
            invoices = self.subscription.with_context(auto_commit=False)._recurring_create_invoice(automatic=True)

        self.assertEqual(
            capture.val and capture.val['json']['referenceCode'],
            invoices[0].name,
            'Should have queried avatax for the right taxes on the new invoice.'
        )
