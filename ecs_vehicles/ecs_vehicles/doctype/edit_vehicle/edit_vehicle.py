# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class EditVehicle(Document):
	def on_submit(self):
		vehicle = frappe.get_doc('Vehicles', self.vehicle_no)
		vehicle.vehicle_status = self.new_status
		row = vehicle.append("status_table", {})
		row.date = self.edit_date
		row.value = self.new_status
		row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		row.old_transaction_no = self.name
		row.remarks = self.remarks
		vehicle.save()

	def on_cancel(self):
		record = frappe.get_doc('Vehicle Status Logs',{'old_transaction_no':self.name}, 'name')
		record.delete()
		vehicle = frappe.get_doc('Vehicles', self.vehicle_no)
		vehicle.vehicle_status = self.current_status
		vehicle.save()
		


