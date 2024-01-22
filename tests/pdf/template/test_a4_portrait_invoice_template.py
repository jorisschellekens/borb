from borb.pdf.template.a4_portrait_invoice_template import A4PortraitInvoiceTemplate
from tests.test_case import TestCase


class TestA4PortraitInvoiceTemplate(TestCase):
    def test_a4_portrait_invoice_template_001(self):
        (
            (
                A4PortraitInvoiceTemplate()
                .set_address(
                    "789 Business Boulevard",
                    "Business City, CA",
                    "67890, USA",
                    "ABC Corporation",
                    "John Doe",
                )
                .set_vat(0)
                .set_company_logo(
                    "https://raw.githubusercontent.com/jorisschellekens/borb/master/logo/borb_64.png"
                )
            )
            .set_notes(
                "For inquiries regarding this invoice, please contact our Accounts Receivable department at ar@abccorp.com or call (123) 456-7890."
            )
            .set_terms(
                "All payments must be made in the currency specified on the invoice. "
                "Late payments may be subject to a 2% interest charge per month. "
                "Goods remain property of ABC Corporation until fully paid."
            )
            .add_item("Widget A", "Widget A", 3, 10)
            .add_item("Gadget B", "Gadget B", 2, 15)
            .add_item("Gizmo C", "Gizmo C", 1, 25)
            .set_bill_to(
                "123 Main Street",
                "Anytown, CA",
                "12345, USA",
                "XYZ Enterprises",
                "Jane Smith",
            )
            .set_ship_to(
                "456 Shipping Lane",
                "Shippingville, CA",
                "54321, USA",
                "ABC Logistics",
                "Jane Smith",
            )
            .set_currency_abbreviation("USD")
        ).save(self.get_first_output_file())

    def test_a4_portrait_invoice_template_002(self):
        (
            (
                A4PortraitInvoiceTemplate()
                .set_address(
                    "789 Business Boulevard",
                    "Business City, CA",
                    "67890, USA",
                    "ABC Corporation",
                    "John Doe",
                )
                .set_vat(0)
                .set_company_logo(
                    "https://raw.githubusercontent.com/jorisschellekens/borb/master/logo/borb_64.png"
                )
            )
            .set_notes(
                "For inquiries regarding this invoice, please contact our Accounts Receivable department at ar@abccorp.com or call (123) 456-7890."
            )
            .set_terms(
                "All payments must be made in the currency specified on the invoice. "
                "Late payments may be subject to a 2% interest charge per month. "
                "Goods remain property of ABC Corporation until fully paid."
            )
            .add_item("Widget A", "Widget A", 3, 10)
            .add_item("Gadget B", "Gadget B", 2, 15)
            .add_item("Gizmo C", "Gizmo C", 1, 25)
            .set_bill_to(
                "123 Main Street",
                "Anytown, CA",
                "12345, USA",
                "XYZ Enterprises",
                "Jane Smith",
            )
            .set_currency_abbreviation("USD")
        ).save(self.get_second_output_file())

    def test_a4_portrait_invoice_template_003(self):
        (
            (
                A4PortraitInvoiceTemplate()
                .set_address(
                    "789 Business Boulevard",
                    "Business City, CA",
                    "67890, USA",
                    "ABC Corporation",
                    "John Doe",
                )
                .set_vat(0)
                .set_company_logo(
                    "https://raw.githubusercontent.com/jorisschellekens/borb/master/logo/borb_64.png"
                )
            )
            .set_notes(
                "For inquiries regarding this invoice, please contact our Accounts Receivable department at ar@abccorp.com or call (123) 456-7890."
            )
            .set_terms(
                "All payments must be made in the currency specified on the invoice. "
                "Late payments may be subject to a 2% interest charge per month. "
                "Goods remain property of ABC Corporation until fully paid."
            )
            .add_item("Widget A", "Widget A", 3, 10)
            .add_item("Gadget B", "Gadget B", 2, 15)
            .add_item("Gizmo C", "Gizmo C", 1, 25)
            .set_currency_abbreviation("USD")
        ).save(self.get_third_output_file())

    def test_a4_portrait_invoice_template_004(self):
        (
            (
                A4PortraitInvoiceTemplate()
                .set_address(
                    "789 Business Boulevard",
                    "Business City, CA",
                    "67890, USA",
                    "ABC Corporation",
                    "John Doe",
                )
                .set_vat(0)
                .set_company_logo(
                    "https://raw.githubusercontent.com/jorisschellekens/borb/master/logo/borb_64.png"
                )
            )
            .set_notes(
                "For inquiries regarding this invoice, please contact our Accounts Receivable department at https://abccorp.com/ar or call (123) 456-7890."
            )
            .set_terms(
                "All payments must be made in the currency specified on the invoice. "
                "Late payments may be subject to a 2% interest charge per month. "
                "Goods remain property of ABC Corporation until fully paid."
            )
            .add_item("Widget A", "Widget A", 3, 10)
            .add_item("Gadget B", "Gadget B", 2, 15)
            .add_item("Gizmo C", "Gizmo C", 1, 25)
            .set_currency_abbreviation("USD")
        ).save(self.get_fourth_output_file())
