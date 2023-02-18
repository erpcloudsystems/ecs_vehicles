# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class EditVehicle(Document):
	def on_submit(self):
		vehicle = frappe.get_doc('Vehicles', self.vehicle_no)
		# police_plate = frappe.get_doc('Police Plate', self.new_police_plate)
		# if self.edit == "رقم شرطة":
		# 	vehicle.vehicle_no = self.new_police_plate
		# 	row = vehicle.append("vehicle_no_table", {})
		# 	row.date = self.edit_date
		# 	row.value = self.new_police_plate
		# 	row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# 	row.doctype_name = "Edit Vehicle"
		# 	row.edit_vehicle = self.name
		# 	row.remarks = self.remarks
		# 	vehicle.save()
		#
		# 	police_plate.current_vehicle = self.vehicle
		# 	x = police_plate.append("plate_table", {})
		# 	x.date = self.edit_date
		# 	x.value = self.vehicle
		# 	x.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# 	x.doctype_name = "Edit Vehicle"
		# 	x.edit_vehicle = self.name
		# 	x.remarks = self.remarks
		# 	police_plate.save()
		#
		# if self.edit == "جهة":
		# 	vehicle.entity_name = self.new_entity
		# 	row = vehicle.append("entity_table", {})
		# 	row.date = self.edit_date
		# 	row.value = self.new_entity
		# 	row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# 	row.doctype_name = "Edit Vehicle"
		# 	row.edit_vehicle = self.name
		# 	row.remarks = self.remarks
		# 	vehicle.save()
		#
		# if self.edit == "لون":
		# 	vehicle.vehicle_color = self.new_color
		# 	row = vehicle.append("color_table", {})
		# 	row.date = self.edit_date
		# 	row.value = self.new_color
		# 	row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# 	row.doctype_name = "Edit Vehicle"
		# 	row.edit_vehicle = self.name
		# 	row.remarks = self.remarks
		# 	vehicle.save()
		#
		# if self.edit == "رقم الموتور":
		# 	vehicle.motor_no = self.new_motor_no
		# 	row = vehicle.append("motor_table", {})
		# 	row.date = self.edit_date
		# 	row.value = self.new_motor_no
		# 	row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# 	row.doctype_name = "Edit Vehicle"
		# 	row.edit_vehicle = self.name
		# 	row.remarks = self.remarks
		# 	vehicle.save()
		#
		# if self.edit == "جهة الصيانة":
		# 	vehicle.maintenance_entity = self.new_maintenance_entity
		# 	row = vehicle.append("maintenance_entity_table", {})
		# 	row.date = self.edit_date
		# 	row.value = self.new_maintenance_entity
		# 	row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
		# 	row.doctype_name = "Edit Vehicle"
		# 	row.edit_vehicle = self.name
		# 	row.remarks = self.remarks
		# 	vehicle.save()
			
		# if self.edit == "صلاحية المركبة":
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
		# if self.edit == "رقم شرطة":
		# 	vehicle.vehicle_no = self.current_police_plate
		# if self.edit == "جهة":
		# 	vehicle.entity_name = self.current_entity
		# if self.edit == "لون":
		# 	vehicle.vehicle_color = self.current_color
		# if self.edit == "رقم الشاسيه":
		# 	vehicle.chassis_no = self.current_chassis_no
		# if self.edit == "رقم الموتور":
		# 	vehicle.motor_no = self.current_motor_no
		# if self.edit == "جهة الصيانة":
		# 	vehicle.maintenance_entity = self.current_maintenance_entity
		# if self.edit == "صلاحية المركبة":
		vehicle.vehicle_status = self.current_status
		vehicle.save()
		


