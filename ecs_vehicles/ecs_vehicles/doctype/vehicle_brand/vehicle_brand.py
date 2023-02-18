# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VehicleBrand(Document):
	def before_insert(self):
		self.generate_code()

	@frappe.whitelist()
	def generate_code(self):
		last_code = frappe.db.get_value("Vehicle Brand", {'name': ['!=', self.name]}, 'max(brand_code)')
		if not last_code:
			self.brand_code = 1
		else:
			self.brand_code = int(last_code) + 1


	def validate(self):
		brand_list = frappe.db.sql(""" Select brand_code, vehicle_brand from `tabVehicle Brand` 
		where docstatus = 0 and name != '{name}' """.format(name=self.name), as_dict=1)

		for x in brand_list:
			if self.brand_code == x.brand_code:
				frappe.throw(
					" لا يمكن إستخدام الكود " + str(x.brand_code) + " أكثر من مرة حيث أنه مستخدم في الماركة " + x.vehicle_brand)
