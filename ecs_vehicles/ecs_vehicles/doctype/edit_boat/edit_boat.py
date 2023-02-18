# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document


class EditBoat(Document):
	def on_submit(self):
		boat = frappe.get_doc('Boats', self.boat_no)
		if self.edit == "جهة":
			boat.entity_name = self.new_entity
			row = boat.append("entity_table", {})
			row.date = self.edit_date
			row.value = self.new_entity
			row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
			row.doctype_name = "Edit Boat"
			row.edit_vehicle = self.name
			row.remarks = self.remarks
			boat.save()

		if self.edit == "صلاحية اللانش":
			boat.boat_validity = self.new_status
			row = boat.append("validity_table", {})
			row.date = self.edit_date
			row.value = self.new_status
			row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
			row.doctype_name = "Edit Boat"
			row.edit_vehicle = self.name
			row.remarks = self.remarks
			boat.save()

	def on_cancel(self):
		record = frappe.get_doc('Editing Table', {'edit_vehicle': self.name}, 'name')
		record.delete()
		boat = frappe.get_doc('Boats', self.boat_no)
		if self.edit == "جهة":
			boat.entity_name = self.current_entity
		if self.edit == "صلاحية اللانش":
			boat.boat_validity = self.current_status
		boat.save()




