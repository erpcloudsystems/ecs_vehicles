# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
		if self.receipt_table:
			for x in self.receipt_table:
				serial_count = int(x.to_voucher) - int(x.from_voucher) + 1
				serial_no = int(x.from_voucher)
				while serial_count > 0:
					voucher = frappe.get_doc("Voucher", {'serial_no': serial_no, 'voucher_type': x.liquid_voucher, 'release_date': self.name})
					voucher.disabled = self.disabled
					voucher.save()
					next_serial = serial_no + 1
					serial_no = next_serial
					serial_count -= 1

		release_date_list = frappe.db.sql(""" Select code, name from `tabRelease Date`
				where name != '{name}' """.format(name=self.name), as_dict=1)

		for x in release_date_list:
			if self.code == x.code:
				frappe.throw(
					" لا يمكن إستخدام الكود " + str(x.code) + " أكثر من مرة حيث أنه مستخدم في الإصدار " + x.name)