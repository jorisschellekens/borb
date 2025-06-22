import unittest

from borb.pdf.document_layout.a4_portrait_invoice import A4PortraitInvoice


class TestA4PortraitInvoice(unittest.TestCase):

    def test_a4_portrait_invoice(self):

        (
            (
                A4PortraitInvoice()
                .set_logo(
                    bytes_path_pil_image_or_url="https://raw.githubusercontent.com/jorisschellekens/borb/refs/heads/master/logo/borb_square_64_64.png"
                )
                .set_address(
                    address_line_1="123 Maple Street",
                    address_line_2="Apt 4B",
                    address_line_3="Downtown",
                    address_line_4="Springfield",
                    address_line_5="IL 62704",
                )
                .set_bill_to(
                    address_line_1="456 Oak Avenue",
                    address_line_2="Suite 300",
                    address_line_3="Business District",
                    address_line_4="Metropolis",
                    address_line_5="NY 10001",
                )
                .set_ship_to(
                    address_line_1="789 Pine Street",
                    address_line_2="Warehouse B",
                    address_line_3="Industrial Park",
                    address_line_4="Gotham City",
                    address_line_5="NJ 07001",
                )
                .append_item(
                    amount=100, description="Wireless Mouse", quantity=2, unit_price=50
                )
                .append_item(
                    amount=300,
                    description="Mechanical Keyboard",
                    quantity=3,
                    unit_price=100,
                )
                .append_item(
                    amount=150,
                    description="USB-C Docking Station",
                    quantity=1,
                    unit_price=150,
                )
                .append_item(
                    amount=400,
                    description="27-inch Monitor",
                    quantity=2,
                    unit_price=200,
                )
                .append_item(
                    amount=50,
                    description="Ergonomic Mouse Pad",
                    quantity=5,
                    unit_price=10,
                )
                .set_terms_and_conditions(
                    "Payment is due within 30 days of the invoice date. "
                    "Late payments incur a 1.5% monthly fee. "
                    "Products ship within 5-7 business days after payment. "
                    "Returns are accepted within 14 days of delivery, with the buyer covering return shipping. "
                    "A 1-year limited warranty applies to all items, excluding misuse or unauthorized repairs. "
                    "Cancellations are allowed within 24 hours. The seller is not responsible for indirect damages. "
                    "Any disputes will be governed by the laws of Texas. These terms may be updated at the seller's discretion."
                )
            ).save("assets/test_a4_portrait_invoice.pdf")
        )
