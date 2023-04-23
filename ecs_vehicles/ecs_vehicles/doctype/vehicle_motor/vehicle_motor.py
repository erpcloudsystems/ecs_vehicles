# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class VehicleMotor(Document):
	def after_insert(self):
		# self.current_vehicle = "إحتياطي مخزن"
		# motor = self.append("motor_table", {})
		# motor.date = datetime.now()
		# motor.value = "إحتياطي مخزن"
		# motor.remarks = "إحتياطي مخزن"
		# motor.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# motor.doctype_name = "Vehicle Motor"
		# motor.edit_vehicle = self.name
		# self.save()
		pass