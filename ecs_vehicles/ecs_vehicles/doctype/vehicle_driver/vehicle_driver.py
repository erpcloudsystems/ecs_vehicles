# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VehicleDriver(Document):
	def before_insert(self):
		self.generate_code()

	@frappe.whitelist()
	def generate_code(self):
		last_code = frappe.db.sql(""" select max(code) as max from `tabVehicle Driver` """, as_dict=1)
		for x in last_code:
			if not x.max:
				self.code = 1
			else:
				self.code = int(x.max) + 1

	def validate(self):
		driver_list = frappe.db.sql(""" Select code, driver_name from `tabVehicle Driver` 
		where docstatus = 0 """, as_dict=1)

		for x in driver_list:
			if self.code == x.code:
				frappe.throw(
					" لا يمكن إستخدام الكود " + str(
						x.code) + " أكثر من مرة حيث أنه مستخدم في السائق " + x.driver_name)
