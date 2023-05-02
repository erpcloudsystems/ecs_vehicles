# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceOrder(Document):
	def validate(self):
		maintenance_order_list = frappe.db.sql(""" Select ezn_no, name from `tabMaintenance Order` 
		where docstatus = 1 and fis_year = '{fis_year}' and name != '{name}' """.format(name=self.name, fis_year=self.fis_year), as_dict=1)

		for x in maintenance_order_list:
			if self.ezn_no == x.ezn_no:
				frappe.throw(
					" لا يمكن إستخدام رقم الإذن " + str(
						x.ezn_no) + " أكثر من مرة حيث أنه مستخدم في إذن الإصلاح " + x.name)
