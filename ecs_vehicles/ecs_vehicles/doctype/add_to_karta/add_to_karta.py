# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AddToKarta(Document):
	def on_submit(self):
		if not self.items:
			frappe.throw(" برجاء إضافة قطع الغيار ")
		for row in self.items:
			new_doc = frappe.get_doc({
				"doctype": "Karta Ledger Entry",
				"ord_serial" : self.name,
				"detail_serial" : row.name,
				"vic_serial" : self.vehicles,
				"part_universal_code" : row.item_code,
				"action_date" : self.transaction_date,
				"part_unit" : row.uom,
				"part_status_ratio" : row.quality,
				"part_country" : row.origin,
				"workshop_type" : row.workshop_type,
				"workshop_name" : row.workshop_name,
				"ezn_no" : self.add_no,
				"ezn_date" : self.transaction_date,
				"doc_type" : "Add To Karta",
				"geha_code" : self.entity_name,
				"maintenance_method" : self.add_type,
				"part_qty" : row.qty,
				"del_flag": "0"
			})
			new_doc.insert(ignore_permissions=True)
			row.kle = new_doc.name

	def on_cancel(self):
		frappe.db.sql(
            """ update `tabKarta Ledger Entry` set del_flag = "1"
                where ord_serial ='{ord_serial}'
            """.format(ord_serial=self.name))