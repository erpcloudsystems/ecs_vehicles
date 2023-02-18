# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FollowScrapBoatData(Document):
	def on_submit(self):
		boat = frappe.get_doc('Boats', self.boat_no)
		if self.scrap_status == "عاملة":
			boat.boat_validity = "عاطلة"
			row = boat.append("validity_table", {})
			row.date = self.scrap_date
			row.value = "عاطلة"
			row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
			row.doctype_name = "Follow Scrap Boat Data"
			row.edit_vehicle = self.name
			row.remarks = self.remarks
			boat.save()

		else:
			boat.boat_validity = self.scrap_status
			row = boat.append("validity_table", {})
			row.date = self.scrap_date
			row.value = self.scrap_status
			row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
			row.doctype_name = "Follow Scrap Boat Data"
			row.edit_vehicle = self.name
			row.remarks = self.remarks
			boat.save()

	def on_cancel(self):
		record = frappe.get_doc('Editing Table', {'edit_vehicle': self.name}, 'name')
		record.delete()
		boat = frappe.get_doc('Boats', self.boat_no)
		boat.boat_validity = self.boat_status
		boat.save()
