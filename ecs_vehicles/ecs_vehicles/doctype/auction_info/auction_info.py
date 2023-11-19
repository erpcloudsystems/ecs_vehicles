# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AuctionInfo(Document):
	@frappe.whitelist()
	def get_searched_vehicles(self):
		if frappe.db.exists(
			"Vehicles",
			{"vehicle_no": self.vehicle_no, "vehicle_status": "مخردة"},
		):
			if self.vehicle_type2:
				vic = frappe.get_doc(
					"Vehicles",
					{
						"vehicle_no": self.vehicle_no,
						"vehicle_status": "مخردة",
						"vehicle_type": self.vehicle_type2
					},
				)
				get_list_count = frappe.db.get_list(
					"Vehicles",
					filters={
						"vehicle_no": self.vehicle_no,
						"vehicle_status": "مخردة",
						"vehicle_type": self.vehicle_type2
					},
					fields=["vehicle_no", "vehicle_type"],
				)
				if len(get_list_count) > 1:
					vehicle_types = " <br> "
					for row in get_list_count:
						vehicle_types = vehicle_types + " <br> " + row.vehicle_type
					vehicle_no = "يوجد عدد {count} مركبة بنفس رقم الشرطة {vehicle_no} <br> \
					برجاء تحديد نوع المركبة : {vehicle_types}".format(
						count=len(get_list_count),
						vehicle_no=self.vehicle_no,
						vehicle_types=vehicle_types,
					)
					frappe.throw(vehicle_no)

			else:
				vic = frappe.get_doc(
					"Vehicles",
					{
						"vehicle_no": self.vehicle_no,
						"vehicle_status": "مخردة"
					},
				)

			if vic.vehicle_status != "مخردة":
				frappe.throw(
					"المركبة رقم {vehicle_no} ليست مخردة".format(
						vehicle_no=vic.vehicle_no
					)
				)


			vehicle = self.append("auction_sales_slips", {})
			vehicle.vehicle = vic.name
			vehicle.police_id = self.vehicle_no
			vehicle.entity = vic.entity_name
			vehicle.vehicle_type = vic.vehicle_type
			vehicle.vehicle_shape = vic.vehicle_shape
			vehicle.vehicle_brand = vic.vehicle_brand
			vehicle.vehicle_model = vic.vehicle_model
			vehicle.vehicle_style = vic.vehicle_style
			vehicle.vehicle_color = vic.vehicle_color
			vehicle.chassis_no = vic.chassis_no
			vehicle.motor_no = vic.motor_no

		elif frappe.db.exists(
			"Vehicles",
			{"police_id": self.vehicle_no, "vehicle_status": "مخردة"},
		):
			if self.vehicle_type2:
				vic = frappe.get_doc(
					"Vehicles",
					{
						"police_id": self.vehicle_no,
						"vehicle_type": self.vehicle_type2
					},
				)
				get_list_count = frappe.db.get_list(
					"Vehicles",
					filters={
						"police_id": self.vehicle_no,
						"vehicle_status": "مخردة",
						"vehicle_type": self.vehicle_type2,
					},
					fields=["police_id", "vehicle_type"],
				)
				if len(get_list_count) > 1:
					vehicle_types = " <br> "
					for row in get_list_count:
						vehicle_types = vehicle_types + " <br> " + row.vehicle_type
					vehicle_no = "يوجد عدد {count} مركبة بنفس رقم الشرطة {vehicle_no} <br> \
					برجاء تحديد نوع المركبة : {vehicle_types}".format(
						count=len(get_list_count),
						vehicle_no=self.vehicle_no,
						vehicle_types=vehicle_types,
					)
					frappe.throw(vehicle_no)
						
			else:
				vic = frappe.get_doc(
					"Vehicles",
					{
						"police_id": self.vehicle_no,
						"vehicle_status": "مخردة"
					},
				)


			if vic.vehicle_status != "مخردة":
				frappe.throw(
					"المركبة رقم {vehicle_no} ليست مخردة".format(
						vehicle_no=vic.vehicle_no
					)
				)


			vehicle = self.append("auction_sales_slips", {})
			vehicle.vehicle = vic.name
			vehicle.police_id = self.vehicle_no
			vehicle.entity = vic.entity_name
			vehicle.vehicle_type = vic.vehicle_type
			vehicle.vehicle_shape = vic.vehicle_shape
			vehicle.vehicle_brand = vic.vehicle_brand
			vehicle.vehicle_model = vic.vehicle_model
			vehicle.vehicle_style = vic.vehicle_style
			vehicle.vehicle_color = vic.vehicle_color
			vehicle.chassis_no = vic.chassis_no
			vehicle.motor_no = vic.motor_no

		else:
			vehicle_no = self.vehicle_no

			frappe.throw(
				"لا يوجد مركبة برقم {vehicle_no}".format(vehicle_no=vehicle_no)
			)

		self.vehicle_type2 = None
			

	
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