# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceEntity(Document):
	def before_insert(self):
		self.generate_code()

	@frappe.whitelist()
	def generate_code(self):
		last_code = frappe.db.sql(""" select max(code) as max from `tabMaintenance Entity` """, as_dict=1)
		for x in last_code:
			if not x.max:
				self.code = 1
			else:
				self.code = int(x.max) + 1


	def validate(self):
		entity_list = frappe.db.sql(""" Select code, entity_name from `tabMaintenance Entity`
		where docstatus = 0 and name != '{name}' """.format(name=self.name), as_dict=1)

		for x in entity_list:
			if self.code == x.code:
				frappe.throw(
					" لا يمكن إستخدام الكود " + str(
						x.code) + " أكثر من مرة حيث أنه مستخدم في جهة الصيانة " + x.entity_name)
