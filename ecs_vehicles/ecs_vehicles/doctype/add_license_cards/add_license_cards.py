# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AddLicenseCards(Document):
	def on_submit(self):
		serial_count = self.to_serial - self.from_serial + 1
		serial_no = self.from_serial
		while serial_count > 0:
			new_doc = frappe.new_doc("License Card")
			new_doc.serial = serial_no
			new_doc.code = self.card_code
			new_doc.group_no = self.group_no
			new_doc.insert()

			next_serial = serial_no + 1
			serial_no = next_serial
			serial_count -= 1
