# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class PrivatePlate(Document):
	def before_insert(self):
		self.plate_no = self.letter1 + "." + self.letter2 + "." + self.letter3 + " " + str(self.no)
	
	def after_insert(self):
		self.current_vehicle = ""
		self.current_entity = "إحتياطي مخزن لوحات"
		self.status = "صالحة"
		plate = self.append("plate_table", {})
		plate.date = datetime.now()
		plate.value = "إحتياطي مخزن لوحات"
		plate.remarks = "إحتياطي مخزن لوحات"
		plate.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		plate.doctype_name = "Private Plate"
		plate.edit_vehicle = self.name
		self.save()