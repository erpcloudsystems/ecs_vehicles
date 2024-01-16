# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AddLicenseCards(Document):
    
	def on_submit(self):
		frappe.db.sql(f"""
				UPDATE `tabAdd License Cards`
				set `tabAdd License Cards`.default = 0
				where `tabAdd License Cards`.name != "{self.name}"
	""")
