# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TrafficEntity(Document):
	def before_insert(self):
		self.generate_code()

	@frappe.whitelist()
	def generate_code(self):
		last_code = frappe.db.sql(""" select max(code) as max from `tabTraffic Entity` """, as_dict=1)
		for x in last_code:
			if not x.max:
				self.code = 1
			else:
				self.code = int(x.max) + 1

	def validate(self):
		traffic_entity_list = frappe.db.sql(""" Select code, traffic_entity from `tabTraffic Entity` 
		where docstatus = 0 and name != '{name}' """.format(name=self.name), as_dict=1)

		for x in traffic_entity_list:
			if self.code == x.code:
				frappe.throw(
					" لا يمكن إستخدام الكود " + str(
						x.code) + " أكثر من مرة حيث أنه مستخدم في جهة المرور " + x.traffic_entity)
