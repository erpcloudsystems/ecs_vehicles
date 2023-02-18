# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class PolicePlate(Document):
	pass
	'''
	def after_insert(self):
		self.current_vehicle = "إحتياطي مخزن"
		self.status = "صالحة"
		plate = self.append("plate_table", {})
		plate.date = datetime.now()
		plate.value = "إحتياطي مخزن"
		plate.remarks = "إحتياطي مخزن"
		plate.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		plate.doctype_name = "Police Plate"
		plate.edit_vehicle = self.name
		self.save()
	'''