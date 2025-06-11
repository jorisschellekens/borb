import unittest

from borb.pdf import (
    Document,
    Page,
    MultiColumnLayout,
    PageLayout,
    Paragraph,
    X11Color,
    PDF,
    MarkdownParagraph,
    LayoutElement,
    Shape,
    Emoji,
)


class TestCreateEULA(unittest.TestCase):

    def test_create_eula(self):

        eula: Document = Document()

        page: Page = Page()
        eula.append_page(page)

        layout: PageLayout = MultiColumnLayout(page=page, number_of_columns=2)

        # title
        layout.append_layout_element(
            Paragraph(
                "END USER LICENSE AGREEMENT",
                font_color=X11Color.PRUSSIAN_BLUE,
                font_size=18,
                font="Helvetica-Bold",
            )
        )

        your_license_version: str = "3.0.0"
        your_name: str = "Brightleaf Ltd."
        our_name: str = "Stonewell Systems"
        our_address_line_1: str = "42 Willow Lane"
        our_address_line_2: str = "Cambridge CB1 2AB"
        our_address_line_3: str = "United Kingdom"
        your_address_line_1: str = "14 Oakridge Drive"
        your_address_line_2: str = "81249 München"
        your_address_line_3: str = "Germany"

        # paragraph 1
        # fmt: off
        layout.append_layout_element(MarkdownParagraph(f"For borb Version **{your_license_version}** subsequent minor versions and previous versions"))
        layout.append_layout_element(MarkdownParagraph(f"""This end user license agreement (\"EULA\") is entered into between *{our_name}* (\"We\", \"Us\" or \"Our\"), a Belgian limited liability corporation, **{our_address_line_1}**, **{our_address_line_2}**, **{our_address_line_3}** and **{your_name}** (\"You\" or \"Yours\") *{your_address_line_1}*, *{your_address_line_2}*, *{your_address_line_3}* for the purpose of granting You a limited-scope and non-transferable end user license on the Software. To access or use the software, you must agree to be legally bound by the terms and conditions of this EULA.""", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # paragraph 2
        # fmt: off
        layout.append_layout_element(Paragraph("1. License", font_color=X11Color.PRUSSIAN_BLUE, font_size=16, font="Helvetica-Bold"))
        layout.append_layout_element(MarkdownParagraph(f"1.1. Software. \"Software\" means borb, Version *{your_license_version}*, subsequent minor Versions and previous Versions, in source or binary form, any other machine readable materials (including, but not limited to, libraries, source files, header files, and data files) and any end user manuals, programming guides and other documentation provided under this EULA, including any Updates", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("1.2. Professional License to use. Subject to the terms and conditions of this EULA, We hereby grant You, and third party contractors or consultants working on behalf of You, a limited-scope, non-exclusive, non-transferable, non-sublicensable, worldwide right to install,  access, use and modify the Software in support of or integrated in any of Your software products or software applications (\"Products\").", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("The Software or works derived therefrom may only be used as an integrated part of the Products or in support of the Products. You may not sell, lease, rent, loan, market, license, sub-license, distribute or otherwise grant to any person or entity any right to use any part of the Software, Documentation or Updates.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("The License to Use the Software is subject to You having fully paid up the license fee as specified in a separate quotation (\"Order\" or \"Invoice\") attached hereto. You may only install, access, use the Software or works derived therefrom up to the number of licenses granted in the Order or Invoice.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("1.3. Documentation and Updates. We may provide or make available to You additional documentation for the Software without charge, including instruction or operations manuals (\"Documentation\"). We may also provide or make available error corrections and such minor modifications, revisions, enhancements and updates to the Software which are designated by a change in the number to the right of the decimal point, e.g., from version 2.0.16 to version 2.0.17 (\"Minor Updates\").", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("We may provide or make available to You Updates that must be installed for You to be allowed to continue using the Software.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("This EULA does not include a license on migrations to the left of the leftmost decimal point, e.g., from version 2.0.16 to version 3.0.0 (\"Major Updates\").", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("1.4. Disclosure and Use Restrictions. The Software is licensed to You, not sold. The Software and any intellectual property rights to the Software, shall at all times remain with Us and our licensors.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("In the event that We obtain or are granted additional intellectual property rights (e.g. a patent) relating to the Software or its use or the combined use of the Software with any other software, system, business method or process, this EULA shall automatically grant You the further use of the Software as foreseen in this EULA not withstanding the protection obtained under any such additional intellectual property rights.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("You may not remove, erase or tamper with any copyright or proprietary notice printed or stamped on, affixed to, or encoded or recorded in the Software.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("1.5 Intellectual Property Rights. The incorporation of the Software in the Products does not grant or generate Us intellectual property rights in the Product beyond the parts of the Software actually incorporated into the Products.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # paragraph 3
        # fmt: off
        layout.append_layout_element(Paragraph("2. License Fee", font_color=X11Color.PRUSSIAN_BLUE, font_size=16, font="Helvetica-Bold"))
        layout.append_layout_element(Paragraph("2.1. License Rights. To obtain the license rights described in this EULA, You are held to fully pay up the license fee foreseen in the separate quotation (\"Order\" or \"Invoice\") attached hereto. Any purchase order or other document You have transmitted shall not alter or prevail over the terms of this EULA, unless explicitly accepted by Us in writing.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("2.2 Modalities. Unless otherwise stated, all payments must be made in euro. The license fee is exclusive of all local, state, federal and foreign taxes, levies or duties of any nature and You are responsible for payments of all such taxes, excluding only Belgian taxes on Our income. If We have the legal obligation to pay or collect such taxes for which You are responsible pursuant to this section, the appropriate amount shall be invoiced to and paid by You unless You provide Us with a valid tax exemption certificate authorized by the appropriate taxing authority. Any arrears in payment will automatically cause You to indebted to paying to Us a late payment interest equal to 12% per year (or part of year).", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # paragraph 4
        # fmt: off
        layout.append_layout_element(Paragraph("3. Support & Maintenance", font_color=X11Color.PRUSSIAN_BLUE, font_size=16, font="Helvetica-Bold"))
        layout.append_layout_element(Paragraph("This EULA does not include any support or maintenance by Us. Should You require support or maintenance, You may request from Us to propose a support and maintenance agreement. Your initial purchase of a License may include a limited-scope support or maintenance period to ensure You can easily integrate the Software. For the duration and scope of this support We defer to the attached Offer or Invoice.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # paragraph 5
        # fmt: off
        layout.append_layout_element(Paragraph("4. Warranties, Disclaimers And Limitation Of Liability", font_color=X11Color.PRUSSIAN_BLUE, font_size=16, font="Helvetica-Bold"))
        layout.append_layout_element(Paragraph("4.1.1. Each Party represents and warrants that the execution, delivery and performance by such party of this EULA are within its powers and have been duly authorized by all necessary action by such party and the execution, delivery and performance of this EULA will not violate any agreement to which it is a party or by which it is bound.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("4.1.2. We warrant the functionality of the Software will not be materially decreased during the Term.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("4.2. Disclaimer of warranty. We only offer the warranties explicitly provided in this EULA. All other warranties, representations or conditions, whether implied or otherwise, given oral or in writing, are disclaimed. The Software, Documentation, Updates and Support (where applicable) are provided \"AS IS\" and \"WITH ALL FAULTS\".", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("We do not guarantee non-interference, non-infringement, accuracy, merchantability, quality, system integration nor fitness for a particular purpose. Warranties that are given are solely for your benefit and not for the benefit of any third party.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("4.3. Limitation of liability. The limitation of liability and exclusions of certain damages stated herein shall apply regardless of the failure of essential purpose of any remedy. To the extent not prohibited by mandatory law, and except for the situation of willful misconduct or fraud by Us, We shall in no event be liable for lost revenues, lost profits, loss of business, loss of data, or any incidental, indirect, exemplary, consequential, special or punitive damages of any kind.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("Including such damages arising from any breach of this agreement or any termination of contract, tort or otherwise and whether or not foreseeable, even if We have been advised or were aware of the possibility of such loss or damages. Our aggregate liability in connection with this agreement, the licensed software or proprietary items shall, under no circumstances, exceed the fees paid or to be paid under this agreement to Us.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # paragraph 6
        # fmt: off
        layout.append_layout_element(Paragraph("5. Term", font_color=X11Color.PRUSSIAN_BLUE, font_size=16, font="Helvetica-Bold"))
        layout.append_layout_element(Paragraph("5.1. Term. Without prejudice to what is foreseen in sections 4.1 and 5, this EULA provides You with a perpetual end user license on the Software, effective as from the moment You have fully paid up the license fee.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("5.2. Termination for cause. We  may terminate this EULA for cause if You breach any material provision of this EULA and do not cure the breach within thirty (30) days after receiving written notice thereof. No thirty (30) days cure period will need to be respected by Us for a breach which by its nature cannot be cured. Termination for cause will be effective immediately upon Us serving notice by registered letter of its decision to terminate this EULA for cause.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("5.3. Effects of termination. Upon termination of this EULA for any reason, You must immediately destroy all copies, partial or complete, and wherever stored or available, of the Software, of Products in which the Software was integrated and of all Documentation and other tangible or intangible data relating to the Software.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # paragraph 7
        # fmt: off
        layout.append_layout_element(Paragraph("6. Miscellaneous", font_color=X11Color.PRUSSIAN_BLUE, font_size=16, font="Helvetica-Bold"))
        layout.append_layout_element(Paragraph("6.1. Notice. All notices, consents and other communications under this EULA shall be in writing and shall be deemed to have been received on the earlier of the date of actual receipt or the third Belgian business day after being sent by registered mail.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(MarkdownParagraph(f"Our address for notices is: *{our_address_line_1}*, *{our_address_line_2}*, *{our_address_line_3}*.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(MarkdownParagraph(f"Your address for notices is: *{your_address_line_1}*, *{your_address_line_2}*, *{your_address_line_3}*.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("Both We and You may communicate a new address for notices by serving notice thereof in accordance with the provisions of this section.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("6.2. Assignment. You may not assign or delegate this EULA or any or all of Your rights or obligations under this EULA, in whole or in part, by operation of law or otherwise, to any party or entity without the prior written consent of Us.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("6.3. Press Release. Upon the execution of this EULA, each party may issue a press release announcing that the parties have entered into this agreement, provided that the other party provides written pre-approval. You shall not use Our name, trade mark or logo unless You have obtained Our prior written approval.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("6.4. Governing Law and jurisdiction. This EULA shall be construed and enforced in accordance with Belgian law. The application of the Belgian conflict of laws rules is excluded. This EULA shall not be subject to the United Nations Convention on Contracts for the International Sale of Goods.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        layout.append_layout_element(Paragraph("The courts of Gent, Belgium, shall have exclusive jurisdiction to adjudicate any dispute arising out of or with regard to this EULA. Each party hereby expressly consents to such the exclusive jurisdiction.", text_alignment=LayoutElement.TextAlignment.JUSTIFIED))
        # fmt: on

        # add logo
        w, h = eula.get_page(0).get_size()
        Emoji.BORB.paint(
            available_space=(w // 20, h - 32 - h // 20, 32, 32), page=eula.get_page(0)
        )

        # add page nr to each page
        for i in range(0, eula.get_number_of_pages()):
            s = w // 10

            Shape(
                coordinates=[(w - s, 0), (w - s, s), (w, s), (w, 0), (w - s, 0)],
                fill_color=X11Color.YELLOW_MUNSELL,
                stroke_color=None,
            ).paint(available_space=(w - s, 0, s, s), page=eula.get_page(i))

            Paragraph(
                text=f"{i + 1}",
                font_color=X11Color.PRUSSIAN_BLUE,
                text_alignment=LayoutElement.TextAlignment.CENTERED,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            ).paint(available_space=(w - s, 0, s, s), page=eula.get_page(i))

        # save
        PDF.write(what=eula, where_to="assets/test_create_eula.pdf")
