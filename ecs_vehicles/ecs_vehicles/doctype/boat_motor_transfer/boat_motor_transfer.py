# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BoatMotorTransfer(Document):
	def on_submit(self):
		record = frappe.get_doc('Engine Table', {'engine_no': self.engine_no, 'parent': self.from_boat})
		record.delete()
		from_boat = frappe.get_doc('Boats', self.from_boat)
		from_boat.save()
		from_boat.engine_count = len(from_boat.engine_table)
		from_boat.save()
		
		to_boat = frappe.get_doc('Boats', self.to_boat)
		row = to_boat.append("engine_table", {})
		row.engine_no = self.engine_no
		row.engine_brand = self.engine_brand
		row.engine_style = self.engine_style
		row.engine_power = self.engine_power
		row.cylinder_count = self.cylinder_count
		row.feeding_type = self.feeding_type
		row.fuel_type = self.fuel_type
		row.entity = self.entity
		to_boat.save()
		to_boat.engine_count = len(to_boat.engine_table)
		to_boat.save()

		engine = to_boat.append("engines_table", {})
		engine.date = self.transfer_date
		engine.value = self.engine_no
		engine.remarks = self.remarks
		engine.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		engine.doctype_name = "Boat Motor Transfer"
		engine.edit_vehicle = self.name
		engine.save()


		engine_no = frappe.get_doc('Boat Motor', self.engine_no)
		engine_no.boat_no = self.to_boat
		launch = engine_no.append("transfer_history", {})
		launch.date = self.transfer_date
		launch.value = self.to_boat
		launch.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		launch.doctype_name = "Boat Motor Transfer"
		launch.edit_vehicle = self.name
		launch.remarks = self.remarks
		engine_no.save()
