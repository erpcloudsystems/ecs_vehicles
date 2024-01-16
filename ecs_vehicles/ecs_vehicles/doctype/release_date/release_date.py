# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

   
@frappe.whitelist()
def update_voucher_status(name):
    release_date_doc = frappe.get_doc("Release Date", name)
    condition = ""

    if release_date_doc.liquid_type == 'وقود' and release_date_doc.fuel_voucher:
        condition += " AND voucher_type = '{fuel_voucher}' ".format(fuel_voucher=release_date_doc.fuel_voucher)

    elif release_date_doc.liquid_type == 'زيت' and release_date_doc.oil_type:
        condition += " AND voucher_type = '{oil_type}' ".format(oil_type=release_date_doc.oil_type)

    elif release_date_doc.liquid_type == 'غاز' and release_date_doc.gas_type:
        condition += " AND voucher_type = '{gas_type}' ".format(gas_type=release_date_doc.gas_type)

    elif release_date_doc.liquid_type == 'غسيل' and release_date_doc.washing_voucher:
        condition += " AND voucher_type = '{washing_voucher}' ".format(washing_voucher=release_date_doc.washing_voucher)

    frappe.db.sql("""
        UPDATE `tabVoucher` SET disabled = '{disabled}' 
        WHERE release_date = '{release_date}'
        {condition}
    """.format(disabled=release_date_doc.disabled, release_date=release_date_doc.name, condition=condition))

class ReleaseDate(Document):
    @frappe.whitelist()
    def before_insert(self):
        self.generate_code()

    @frappe.whitelist()
    def generate_code(self):
        last_code = frappe.db.sql(""" select max(code) as max from `tabRelease Date` """, as_dict=1)
        for x in last_code:
            if not x.max and not self.code:
                self.code = 1
            else:
                self.code = int(x.max) + 1



    @frappe.whitelist()
    def validate(self):
        release_date_list = frappe.db.sql(""" Select code, name from `tabRelease Date`
                where name != '{name}' """.format(name=self.name), as_dict=1)

        for x in release_date_list:
            if self.code == x.code:
                frappe.throw(
                    " لا يمكن إستخدام الكود " + str(x.code) + " أكثر من مرة حيث أنه مستخدم في الإصدار " + x.name)
                
        frappe.enqueue(
            update_voucher_status,
            queue="long",
            timeout=3600,
            is_async=True,
            job_name=self.name,
            at_front=True,
            name=self.name,
        )


    # @frappe.whitelist()
    # def validate(self):
    # 	if self.receipt_table:
    # 		for x in self.receipt_table:
    # 			serial_count = int(x.to_voucher) - int(x.from_voucher) + 1
    # 			serial_no = int(x.from_voucher)
    # 			while serial_count > 0:
    # 				voucher = frappe.get_doc("Voucher", {'serial_no': serial_no, 'voucher_type': x.liquid_voucher, 'release_date': self.name})
    # 				voucher.disabled = self.disabled
    # 				voucher.save()
    # 				next_serial = serial_no + 1
    # 				serial_no = next_serial
    # 				serial_count -= 1

    # 	release_date_list = frappe.db.sql(""" Select code, name from `tabRelease Date`
    # 			where name != '{name}' """.format(name=self.name), as_dict=1)

    # 	for x in release_date_list:
    # 		if self.code == x.code:
    # 			frappe.throw(
    # 				" لا يمكن إستخدام الكود " + str(x.code) + " أكثر من مرة حيث أنه مستخدم في الإصدار " + x.name)