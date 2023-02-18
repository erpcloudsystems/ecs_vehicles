# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FollowScrapVehicleData(Document):
	def on_submit(self):
		vehicle = frappe.get_doc('Vehicles', self.vehicle_no)
		if self.scrap_status == "عاملة":
			vehicle.vehicle_status = "عاطلة"
			row = vehicle.append("status_table", {})
			row.date = self.scrap_date
			row.value = "عاطلة"
			row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
			row.doctype_name = "Follow Scrap Vehicle Data"
			row.edit_vehicle = self.name
			row.remarks = self.remarks
			vehicle.save()

		else:
			vehicle.vehicle_status = self.scrap_status
			row = vehicle.append("status_table", {})
			row.date = self.scrap_date
			row.value = self.scrap_status
			row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
			row.doctype_name = "Follow Scrap Vehicle Data"
			row.edit_vehicle = self.name
			row.remarks = self.remarks
			vehicle.save()

	def on_cancel(self):
		record = frappe.get_doc('Editing Table', {'edit_vehicle': self.name}, 'name')
		record.delete()
		vehicle = frappe.get_doc('Vehicles', self.vehicle_no)
		vehicle.vehicle_status = self.vehicle_status
		vehicle.save()
