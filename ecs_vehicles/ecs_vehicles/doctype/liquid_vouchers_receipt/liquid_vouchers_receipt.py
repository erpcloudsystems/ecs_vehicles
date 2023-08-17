# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now, nowdate
from frappe.model.document import Document


def liquid_voucher_receipt(name):
    self = frappe.get_doc("Liquid Vouchers Receipt", name)
    release_date = frappe.db.get_value("Release Date", self.release_date, "name")
    liquid_voucher = ""
    if self.liquid_type == "وقود":
        liquid_voucher = self.fuel_voucher
    if self.liquid_type == "زيت":
        liquid_voucher = self.oil_type
    if self.liquid_type == "غاز":
        liquid_voucher = self.gas_type
    if self.liquid_type == "غسيل":
        liquid_voucher = self.washing_voucher
    record_name = 1

    max_id = frappe.db.sql(
        """
                SELECT MAX(name) as max_name
                FROM `tabReceipt Voucher Table`
                """,
        as_dict=1,
    )
    if frappe.db.exists("Receipt Voucher Table", 1):
        record_name = int(max_id[0]["max_name"]) + 1
    frappe.db.sql(
        """ INSERT INTO `tabReceipt Voucher Table` (receipt_id, receipt_no, receipt_group, receipt_date, po_no, 
                                po_date, liquid_voucher,edition_no, notebook_count, from_voucher, to_voucher,
                                parent, parenttype, parentfield, name, creation)
                            VALUES ('{receipt_id}', '{receipt_no}', '{receipt_group}', '{receipt_date}', '{po_no}', 
                            '{po_date}', '{liquid_voucher}','{edition_no}', '{notebook_count}', '{from_voucher}', '{to_voucher}',
                            '{parent}', '{parenttype}', '{parentfield}', '{name}', '{creation}' )
                    """.format(
            receipt_id=self.name,
            receipt_no=self.receipt_no,
            receipt_group=self.group,
            receipt_date=self.receipt_date,
            po_no=self.po_no,
            po_date=self.po_date,
            liquid_voucher=liquid_voucher,
            edition_no=self.edition_no,
            notebook_count=self.notebook_count,
            from_voucher=self.from_voucher,
            to_voucher=self.to_voucher,
            parent=release_date,
            parenttype="Release Date",
            parentfield="receipt_table",
            name=record_name,
            creation=now(),
        )
    )

    voucher_type = ""
    fuel_type = ""
    barcode_no = ""
    barcode = ""
    notebook_no = self.from_notebook
    for no in range(self.from_voucher, self.to_voucher + 1):
        if no % 25 == 0:
            notebook_no += 1

        if self.liquid_type == "وقود":
            voucher_type = self.fuel_voucher
            fuel_type = frappe.db.get_value(
                "Fuel Voucher", self.fuel_voucher, "fuel_type"
            )
            barcode_no = (
                str(frappe.db.get_value("Release Date", self.release_date, "code"))
                + "-"
                + str(frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code"))
                + "-"
                + str(no)
            )
            barcode = (
                str(frappe.db.get_value("Release Date", self.release_date, "code"))
                + "-"
                + str(frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code"))
                + "-"
                + str(no)
            )
            price = frappe.db.get_value(
                "Fuel Voucher", self.fuel_voucher, "litre_count"
            ) * frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "litre_rate")

        if self.liquid_type == "زيت":
            voucher_type = self.oil_type
            fuel_type = self.oil_type
            barcode_no = (
                str(frappe.db.get_value("Oil Type", self.oil_type, "code"))
                + "-"
                + str(no)
            )
            barcode = (
                str(frappe.db.get_value("Oil Type", self.oil_type, "code"))
                + "-"
                + str(no)
            )
            price = frappe.db.get_value("Oil Type", self.oil_type, "rate")

        if self.liquid_type == "غاز":
            voucher_type = self.gas_type
            fuel_type = "غاز طبيعي"
            barcode_no = (
                str(frappe.db.get_value("Release Date", self.release_date, "code"))
                + "-"
                + str(frappe.db.get_value("Gas Voucher", self.gas_type, "code"))
                + "-"
                + str(no)
            )
            barcode = (
                str(frappe.db.get_value("Release Date", self.release_date, "code"))
                + "-"
                + str(frappe.db.get_value("Gas Voucher", self.gas_type, "code"))
                + "-"
                + str(no)
            )
            price = frappe.db.get_value(
                "Gas Voucher", self.gas_type, "gas_count"
            ) * frappe.db.get_value("Gas Voucher", self.gas_type, "meter_rate")

        if self.liquid_type == "غسيل":
            voucher_type = self.washing_voucher
            fuel_type = self.washing_voucher
            barcode_no = (
                str(
                    frappe.db.get_value(
                        "Washing Vouchers", self.washing_voucher, "code"
                    )
                )
                + "-"
                + str(no)
            )
            barcode = (
                str(
                    frappe.db.get_value(
                        "Washing Vouchers", self.washing_voucher, "code"
                    )
                )
                + "-"
                + str(no)
            )
            price = frappe.db.get_value(
                "Washing Vouchers", self.washing_voucher, "rate"
            )

        frappe.db.sql(
            """ INSERT INTO `tabVoucher` (serial_no, liquid_type, voucher_type, fuel_type, barcode_no, 
                                barcode, release_date, receipt_date, receipt_id, receipt_no, receipt_group, po_no, po_date, name, creation, voucher_price, notebook_no)
                            VALUES ('{serial_no}', '{liquid_type}', '{voucher_type}', '{fuel_type}', '{barcode_no}', 
                            '{barcode}', '{release_date}', '{receipt_date}', '{receipt_id}', '{receipt_no}', '{receipt_group}',
                            '{po_no}', '{po_date}', '{name}', '{creation}', '{price}', '{notebook_no}')
                    """.format(
                serial_no=no,
                liquid_type=self.liquid_type,
                voucher_type=voucher_type,
                fuel_type=fuel_type,
                barcode_no=barcode_no,
                barcode=barcode,
                release_date=self.release_date,
                receipt_date=self.receipt_date,
                receipt_id=self.name,
                receipt_no=self.receipt_no,
                receipt_group=self.group,
                po_no=self.po_no,
                po_date=self.po_date,
                name=barcode,
                creation=now(),
                price=price,
                notebook_no=notebook_no,
            )
        )
        frappe.db.commit()


class LiquidVouchersReceipt(Document):
    @frappe.whitelist()
    def set_today_date(doc, method=None):
        if not doc.receipt_date:
            doc.receipt_date = nowdate()


    def before_insert(self):
        if (
            frappe.db.exists(
                "Liquid Vouchers Receipt",
                {
                    "docstatus": 1,
                    "liquid_type": "وقود",
                    "fuel_voucher": self.fuel_voucher,
                },
            )
            and self.liquid_type == "وقود"
        ):
            last_doc = frappe.get_last_doc(
                "Liquid Vouchers Receipt",
                {
                    "docstatus": 1,
                    "liquid_type": self.liquid_type,
                    "fuel_voucher": self.fuel_voucher,
                },
            )

            self.from_voucher = last_doc.to_voucher + 1

        if (
            frappe.db.exists(
                "Liquid Vouchers Receipt",
                {"docstatus": 1, "liquid_type": "زيت", "oil_type": self.oil_type},
            )
            and self.liquid_type == "زيت"
        ):
            last_doc = frappe.get_last_doc(
                "Liquid Vouchers Receipt",
                {
                    "docstatus": 1,
                    "liquid_type": self.liquid_type,
                    "oil_type": self.oil_type,
                },
            )

            self.from_voucher = last_doc.to_voucher + 1

        if (
            frappe.db.exists(
                "Liquid Vouchers Receipt",
                {"docstatus": 1, "liquid_type": "غاز", "gas_type": self.gas_type},
            )
            and self.liquid_type == "غاز"
        ):
            last_doc = frappe.get_last_doc(
                "Liquid Vouchers Receipt",
                {"docstatus": 1, "liquid_type": self.liquid_type},
            )

            self.from_voucher = last_doc.to_voucher + 1

        if (
            frappe.db.exists(
                "Liquid Vouchers Receipt",
                {
                    "docstatus": 1,
                    "liquid_type": "غسيل",
                    "washing_voucher": self.washing_voucher,
                },
            )
            and self.liquid_type == "غسيل"
        ):
            last_doc = frappe.get_last_doc(
                "Liquid Vouchers Receipt",
                {"docstatus": 1, "liquid_type": self.liquid_type},
            )

            self.from_voucher = last_doc.to_voucher + 1

    def validate(self):
        self.set("notebook_table", [])
        if not self.from_voucher:
            frappe.throw(" برجاء إدخال خانة من مسلسل بون ")
        self.to_voucher = (
            self.from_voucher
            - 1
            + (self.notebook_count * self.voucher_count_per_notebook)
        )
        if self.liquid_type == "وقود":
            self.qty = (
                frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "litre_count")
                * self.voucher_count_per_notebook
                * self.notebook_count
            )
        # if self.liquid_type == "زيت":
        # 	self.qty = frappe.db.get_value("Oil Type", self.oil_type, "litre_count") * self.voucher_count_per_notebook * self.notebook_count
        if self.liquid_type == "غاز":
            self.qty = (
                frappe.db.get_value("Gas Voucher", self.gas_type, "gas_count")
                * self.voucher_count_per_notebook
                * self.notebook_count
            )
        notebook_count = int(self.notebook_count)
        from_notebook = int(self.from_notebook)
        from_voucher = int(self.from_voucher)
        voucher_count_per_notebook = int(self.voucher_count_per_notebook)
        to_voucher = from_voucher + voucher_count_per_notebook - 1

        while notebook_count > 0:
            self.append(
                "notebook_table",
                {
                    "notebook_no": from_notebook,
                    "from_voucher": from_voucher,
                    "to_voucher": to_voucher,
                },
            )
            next_from_nootbook = from_notebook + 1
            from_notebook = next_from_nootbook
            next_from_voucher = to_voucher + 1
            from_voucher = next_from_voucher
            next_to_voucher = next_from_voucher + voucher_count_per_notebook - 1
            to_voucher = next_to_voucher

            notebook_count -= 1

    def on_submit(self):
        # directly pass the function
        frappe.enqueue(
            liquid_voucher_receipt,
            queue="long",
            timeout=3600,
            is_async=True,
            job_name=self.name,
            at_front=True,
            name=self.name,
        )

    def on_cancel(self):
        frappe.db.sql(
            """ DELETE FROM `tabVoucher` WHERE receipt_id='{receipt_id}' 
                        """.format(
                receipt_id=self.name
            )
        )
        frappe.db.sql(
            """ DELETE FROM `tabReceipt Voucher Table` WHERE receipt_id='{receipt_id}' 
                        """.format(
                receipt_id=self.name
            )
        )
