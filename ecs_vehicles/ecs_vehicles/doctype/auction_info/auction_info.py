# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AuctionInfo(Document):
	@frappe.whitelist()
	def validate(self):
		for d in self.auction_sales_slips:
			vehicle_status = frappe.db.get_value("Vehicles", d.vehicle, "vehicle_status")
			if vehicle_status != "مخردة":
				frappe.throw(" الصف # " + str(d.idx) + " : المركبة رقم " + d.police_id + " ليست مخردة ")
			if d.idx >= self.from_lot and d.idx <= self.to_lot:
				d.accumulated_lot = self.accumulated_lot

		self.from_lot = 0
		self.to_lot = 0
		self.accumulated_lot = 0

	@frappe.whitelist()
	def on_submit(self):
		for d in self.auction_sales_slips:
			vehicle_status = frappe.db.get_value("Vehicles", d.vehicle, "vehicle_status")
			if vehicle_status != "مخردة":
				frappe.throw(" الصف # " + str(d.idx) + " : المركبة رقم " + d.police_id + " ليست مخردة ")

	@frappe.whitelist()
	def on_update_after_submit(self):
		if self.sort_by == "الماركة":
			brand_order = frappe.db.sql(
				""" Select accumulated_lot, vehicle, police_id, entity, vehicle_type, vehicle_shape, vehicle_brand,
					vehicle_model, vehicle_style, vehicle_color, chassis_no, motor_no
					from `tabAuction Sales Slips` 
					where parent = '{parent}'
					order by vehicle_brand asc
				""".format(parent=self.name), as_dict=1)


			self.set("auction_sales_slips", [])
			for x in brand_order:
				row = self.append("auction_sales_slips", {})
				row.accumulated_lot = x.accumulated_lot
				row.vehicle = x.vehicle
				row.police_id = x.police_id
				row.entity = x.entity
				row.vehicle_type = x.vehicle_type
				row.vehicle_shape = x.vehicle_shape
				row.vehicle_brand = x.vehicle_brand
				row.vehicle_model = x.vehicle_model
				row.vehicle_style = x.vehicle_style
				row.vehicle_color = x.vehicle_color
				row.chassis_no = x.chassis_no
				row.motor_no = x.motor_no


		if self.sort_by == "اللوط المجمع":
			lot_order = frappe.db.sql(
				""" Select accumulated_lot, vehicle, police_id, entity, vehicle_type, vehicle_shape, vehicle_brand,
					vehicle_model, vehicle_style, vehicle_color, chassis_no, motor_no
					from `tabAuction Sales Slips` 
					where parent = '{parent}'
					order by accumulated_lot asc
				""".format(parent=self.name), as_dict=1)


			self.set("auction_sales_slips", [])
			for x in lot_order:
				row = self.append("auction_sales_slips", {})
				row.accumulated_lot = x.accumulated_lot
				row.vehicle = x.vehicle
				row.police_id = x.police_id
				row.entity = x.entity
				row.vehicle_type = x.vehicle_type
				row.vehicle_shape = x.vehicle_shape
				row.vehicle_brand = x.vehicle_brand
				row.vehicle_model = x.vehicle_model
				row.vehicle_style = x.vehicle_style
				row.vehicle_color = x.vehicle_color
				row.chassis_no = x.chassis_no
				row.motor_no = x.motor_no


		if self.sort_by == "الشكل":
			shape_order = frappe.db.sql(
				""" Select accumulated_lot, vehicle, police_id, entity, vehicle_type, vehicle_shape, vehicle_brand,
					vehicle_model, vehicle_style, vehicle_color, chassis_no, motor_no
					from `tabAuction Sales Slips` 
					where parent = '{parent}'
					order by vehicle_shape asc
				""".format(parent=self.name), as_dict=1)


			self.set("auction_sales_slips", [])
			for x in shape_order:
				row = self.append("auction_sales_slips", {})
				row.accumulated_lot = x.accumulated_lot
				row.vehicle = x.vehicle
				row.police_id = x.police_id
				row.entity = x.entity
				row.vehicle_type = x.vehicle_type
				row.vehicle_shape = x.vehicle_shape
				row.vehicle_brand = x.vehicle_brand
				row.vehicle_model = x.vehicle_model
				row.vehicle_style = x.vehicle_style
				row.vehicle_color = x.vehicle_color
				row.chassis_no = x.chassis_no
				row.motor_no = x.motor_no


		self.sort_by = ""