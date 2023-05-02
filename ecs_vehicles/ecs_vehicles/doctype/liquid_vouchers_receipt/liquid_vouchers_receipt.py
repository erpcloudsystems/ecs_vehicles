# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now
from frappe.model.document import Document


class LiquidVouchersReceipt(Document):
    def before_insert(self):
        if frappe.db.exists('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": "وقود",
                                                        "fuel_voucher": self.fuel_voucher}) and self.liquid_type == "وقود":
            last_doc = frappe.get_last_doc('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": self.liquid_type,
                                                                       "fuel_voucher": self.fuel_voucher})

            self.from_voucher = last_doc.to_voucher + 1 

        if frappe.db.exists('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": "زيت",
                                                        "oil_type": self.oil_type}) and self.liquid_type == "زيت":
            last_doc = frappe.get_last_doc('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": self.liquid_type,
                                                                       "oil_type": self.oil_type})

            self.from_voucher = last_doc.to_voucher + 1

        if frappe.db.exists('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": "غاز",
                                                        "gas_type": self.gas_type}) and self.liquid_type == "غاز":
            last_doc = frappe.get_last_doc('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": self.liquid_type})

            self.from_voucher = last_doc.to_voucher + 1

        if frappe.db.exists('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": "غسيل",
                                                        "washing_voucher": self.washing_voucher}) and self.liquid_type == "غسيل":
            last_doc = frappe.get_last_doc('Liquid Vouchers Receipt', {"docstatus": 1, "liquid_type": self.liquid_type})

            self.from_voucher = last_doc.to_voucher + 1

    def validate(self):
        self.set("notebook_table", [])
        if not self.from_voucher:
            frappe.throw(" برجاء إدخال خانة من مسلسل بون ")
        self.to_voucher = self.from_voucher - 1 + (self.notebook_count * self.voucher_count_per_notebook)
        if self.liquid_type == "وقود":
            self.qty = frappe.db.get_value("Fuel Voucher", self.fuel_voucher,
                                           "litre_count") * self.voucher_count_per_notebook * self.notebook_count
        # if self.liquid_type == "زيت":
        # 	self.qty = frappe.db.get_value("Oil Type", self.oil_type, "litre_count") * self.voucher_count_per_notebook * self.notebook_count
        if self.liquid_type == "غاز":
            self.qty = frappe.db.get_value("Gas Voucher", self.gas_type,
                                           "gas_count") * self.voucher_count_per_notebook * self.notebook_count
        notebook_count = int(self.notebook_count)
        from_notebook = int(self.from_notebook)
        from_voucher = int(self.from_voucher)
        voucher_count_per_notebook = int(self.voucher_count_per_notebook)
        to_voucher = from_voucher + voucher_count_per_notebook - 1

        while (notebook_count > 0):
            self.append("notebook_table", {
                "notebook_no": from_notebook,
                "from_voucher": from_voucher,
                "to_voucher": to_voucher
            })
            next_from_nootbook = from_notebook + 1
            from_notebook = next_from_nootbook
            next_from_voucher = to_voucher + 1
            from_voucher = next_from_voucher
            next_to_voucher = next_from_voucher + voucher_count_per_notebook - 1
            to_voucher = next_to_voucher

            notebook_count -= 1

    def on_submit(self):
        release_date = frappe.get_doc("Release Date", self.release_date)
        row = release_date.append("receipt_table", {})
        row.receipt_no = self.name
        row.receipt_date = self.receipt_date
        if self.liquid_type == "وقود":
            row.liquid_voucher = self.fuel_voucher
        if self.liquid_type == "زيت":
            row.liquid_voucher = self.oil_type
        if self.liquid_type == "غاز":
            row.liquid_voucher = self.gas_type
        if self.liquid_type == "غسيل":
            row.liquid_voucher = self.washing_voucher
        row.edition_no = self.edition_no
        row.notebook_count = self.notebook_count
        row.from_voucher = self.from_voucher
        row.to_voucher = self.to_voucher
        row.save()
        for item in self.notebook_table:
            notebook_no = item.notebook_no
            voucher_type = ""
            fuel_type = ""
            barcode_no = ""
            barcode = ""
            for no in range (item.from_voucher,item.to_voucher + 1):
                if self.liquid_type == "وقود":
                    voucher_type = self.fuel_voucher
                    fuel_type = frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "fuel_type")
                    barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
                        frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code")) + "-" + str(no)
                    barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
                        frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code")) + "-" + str(no)
                    price = frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "litre_count") * frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "litre_rate")

                if self.liquid_type == "زيت":
                    voucher_type = self.oil_type
                    fuel_type = self.oil_type
                    barcode_no = str(frappe.db.get_value("Oil Type", self.oil_type, "code")) + "-" + str(no)
                    barcode = str(frappe.db.get_value("Oil Type", self.oil_type, "code")) + "-" + str(no)
                    price = frappe.db.get_value("Oil Type", self.oil_type, "rate")
                    

                if self.liquid_type == "غاز":
                    voucher_type = self.gas_type
                    fuel_type = "غاز طبيعي"
                    barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
                        frappe.db.get_value("Gas Voucher", self.gas_type, "code")) + "-" + str(no)
                    barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
                        frappe.db.get_value("Gas Voucher", self.gas_type, "code")) + "-" + str(no)
                    price = frappe.db.get_value("Gas Voucher", self.gas_type, "gas_count") * frappe.db.get_value("Gas Voucher", self.gas_type, "meter_rate")


                if self.liquid_type == "غسيل":
                    voucher_type = self.washing_voucher
                    fuel_type = self.washing_voucher
                    barcode_no = str(frappe.db.get_value("Washing Vouchers", self.washing_voucher, "code")) + "-" + str(no)
                    barcode = str(frappe.db.get_value("Washing Vouchers", self.washing_voucher, "code")) + "-" + str(no)
                    price = frappe.db.get_value("Washing Vouchers", self.washing_voucher, "rate") 
                    

                frappe.db.sql(""" INSERT INTO `tabVoucher` (serial_no, liquid_type, voucher_type, fuel_type, barcode_no, 
                                        barcode, release_date, receipt_date, receipt_no, name, creation, voucher_price, notebook_no)
                                    VALUES ('{serial_no}', '{liquid_type}', '{voucher_type}', '{fuel_type}', '{barcode_no}', 
                                    '{barcode}', '{release_date}', '{receipt_date}', '{receipt_no}', '{name}', '{creation}', '{price}', '{notebook_no}')
                            """.format(serial_no=no, liquid_type=self.liquid_type, voucher_type=voucher_type,
                                        fuel_type=fuel_type,  barcode_no=barcode_no, barcode=barcode,
                                        release_date=self.release_date, receipt_date=self.receipt_date,
                                        receipt_no=self.name, name=barcode, creation=now(), price=price, notebook_no=notebook_no))

           


            # new_doc = frappe.new_doc("Voucher")
            # new_doc.serial_no = serial_no
            # new_doc.liquid_type = self.liquid_type
            # if self.liquid_type == "وقود":
            #     new_doc.voucher_type = self.fuel_voucher
            #     new_doc.fuel_type = frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "fuel_type")
            #     new_doc.barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code")) + "-" + str(serial_no)
            #     new_doc.barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code")) + "-" + str(serial_no)
            # if self.liquid_type == "زيت":
            #     new_doc.voucher_type = self.oil_type
            #     new_doc.fuel_type = self.oil_type
            #     new_doc.barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Oil Type", self.oil_type, "code")) + "-" + str(serial_no)
            #     new_doc.barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Oil Type", self.oil_type, "code")) + "-" + str(serial_no)
            # if self.liquid_type == "غاز":
            #     new_doc.voucher_type = self.gas_type
            #     new_doc.fuel_type = "غاز طبيعي"
            #     new_doc.barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Gas Voucher", self.gas_type, "code")) + "-" + str(serial_no)
            #     new_doc.barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Gas Voucher", self.gas_type, "code")) + "-" + str(serial_no)
            # if self.liquid_type == "غسيل":
            #     new_doc.voucher_type = self.washing_voucher
            #     new_doc.fuel_type = "غسيل"
            #     new_doc.barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Washing Voucher", self.washing_voucher, "code")) + "-" + str(serial_no)
            #     new_doc.barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #         frappe.db.get_value("Washing Voucher", self.washing_voucher, "code")) + "-" + str(serial_no)
            #
            # new_doc.release_date = self.release_date
            # new_doc.receipt_date = self.receipt_date
            # new_doc.receipt_no = self.name
            # new_doc.insert()
            # new_doc.save()

            # next_serial = serial_no + 1
            # serial_no = next_serial
            # serial_count -= 1
            #//////////////////////////////////////////////////////////////////////////////////////
            #//////////////////////////////////////////////////////////////////////////////////////
            #//////////////////////////////////////////////////////////////////////////////////////
            # serial_count = self.to_voucher - self.from_voucher + 1
            # serial_no = self.from_voucher

            # voucher_type = ""
            # fuel_type = ""
            # barcode_no = ""
            # barcode = ""

            # while serial_count > 0:
            #     if self.liquid_type == "وقود":
            #         voucher_type = self.fuel_voucher
            #         fuel_type = frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "fuel_type")
            #         barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code")) + "-" + str(serial_no)
            #         barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "code")) + "-" + str(serial_no)
            #         price = frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "litre_count") * frappe.db.get_value("Fuel Voucher", self.fuel_voucher, "litre_rate")

            #     if self.liquid_type == "زيت":
            #         voucher_type = self.oil_type
            #         fuel_type = self.oil_type
            #         barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Oil Type", self.oil_type, "code")) + "-" + str(serial_no)
            #         barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Oil Type", self.oil_type, "code")) + "-" + str(serial_no)
            #         price = frappe.db.get_value("Oil Type", self.oil_type, "rate")
                    

            #     if self.liquid_type == "غاز":
            #         voucher_type = self.gas_type
            #         fuel_type = "غاز طبيعي"
            #         barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Gas Voucher", self.gas_type, "code")) + "-" + str(serial_no)
            #         barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Gas Voucher", self.gas_type, "code")) + "-" + str(serial_no)
            #         price = frappe.db.get_value("Gas Voucher", self.gas_type, "gas_count") * frappe.db.get_value("Gas Voucher", self.gas_type, "meter_rate")
                    

            #     if self.liquid_type == "غسيل":
            #         voucher_type = self.washing_voucher
            #         fuel_type = "غسيل"
            #         barcode_no = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Washing Voucher", self.washing_voucher, "code")) + "-" + str(serial_no)
            #         barcode = str(frappe.db.get_value("Release Date", self.release_date, "code")) + "-" + str(
            #             frappe.db.get_value("Washing Voucher", self.washing_voucher, "code")) + "-" + str(serial_no)
            #         price = frappe.db.get_value("Washing Voucher", self.washing_voucher, "rate") 
                    

            #     notebook_no = self.notebook_table
            #     frappe.db.sql(""" INSERT INTO `tabVoucher` (serial_no, liquid_type, voucher_type, fuel_type, barcode_no, 
            #                             barcode, release_date, receipt_date, receipt_no, name, creation, voucher_price, notebook_no)
            #                         VALUES ('{serial_no}', '{liquid_type}', '{voucher_type}', '{fuel_type}', '{barcode_no}', 
            #                         '{barcode}', '{release_date}', '{receipt_date}', '{receipt_no}', '{name}', '{creation}', '{price}', '{notebook_no}')
            #                 """.format(serial_no=serial_no, liquid_type=self.liquid_type, voucher_type=voucher_type,
            #                             fuel_type=fuel_type,  barcode_no=barcode_no, barcode=barcode,
            #                             release_date=self.release_date, receipt_date=self.receipt_date,
            #                             receipt_no=self.name, name=barcode, creation=now(), price=price, notebook_no=notebook_no))

            #     next_serial = serial_no + 1
            #     serial_no = next_serial
            #     serial_count -= 1

