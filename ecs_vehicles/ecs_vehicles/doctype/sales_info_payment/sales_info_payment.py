# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesInfoPayment(Document):
	@frappe.whitelist()
	def get_accumulated_lot_vehicles(doc, method=None):
		doc.auction_sales_slips = []
		vehicle_list = frappe.db.get_all("Auction Sales Slips",
										 filters={"parent": doc.auction_info,
												  "accumulated_lot": doc.accumulated_lot},
										 fields={"idx", "lot_no", "accumulated_lot", "vehicle", "police_id", "entity",
												 "vehicle_type", "vehicle_shape", "vehicle_brand", "vehicle_model",
												 "vehicle_style", "vehicle_color", "chassis_no", "motor_no"})

		for x in vehicle_list:
			vehicle = doc.append("auction_sales_slips", {})
			vehicle.lot_no = x.idx
			vehicle.accumulated_lot = x.accumulated_lot
			vehicle.vehicle = x.vehicle
			vehicle.police_id = x.police_id
			vehicle.entity = x.entity
			vehicle.vehicle_type = x.vehicle_type
			vehicle.vehicle_shape = x.vehicle_shape
			vehicle.vehicle_brand = x.vehicle_brand
			vehicle.vehicle_model = x.vehicle_model
			vehicle.vehicle_style = x.vehicle_style
			vehicle.vehicle_color = x.vehicle_color
			vehicle.chassis_no = x.chassis_no
			vehicle.motor_no = x.motor_no

	def validate(self):
		if not self.auction_sales_slips:
			frappe.throw(" رقم اللوط المجمع غير صحيح ... برجاء تحديد رقم اللوط المجمع ")

		if self.accumulated_lot == 0:
			frappe.throw(" برجاء تحديد رقم اللوط المجمع ")

		total = 0
		for x in self.auction_sales_slips:
			total += x.selling_price

		self.total_price = total


	def on_submit(self):
		for x in self.auction_sales_slips:
			vehicle_status = frappe.db.get_value("Vehicles", x.vehicle, "vehicle_status")
			if vehicle_status != "مخردة":
				frappe.throw(" الصف # " + str(x.idx) + " : المركبة رقم " + x.police_id + " ليست مخردة ")


			remarks = " تم تسديد بيانات البيع للتاجر " + self.customer_name + " بمزاد رقم " + self.auction_info + " بتاريخ " + self.auction_date
			value = "تحت البيع بالمزاد"
			record_name = str(self.name) + str(x.vehicle)

			frappe.db.sql(""" UPDATE `tabVehicles` set vehicle_status = "تحت البيع بالمزاد" where name = '{name}' 
						  """.format(name=x.vehicle))

			frappe.db.sql(""" INSERT INTO `tabVehicle Status Logs`
			                                        (date, value, remarks, edited_by, parent, parentfield, parenttype, name, idx)
			                                VALUES ('{date}', '{value}', '{remarks}', '{edited_by}', '{parent}', '{parentfield}', '{parenttype}', '{record_name}', '{idx}')
			                              """.format(date=self.auction_date, remarks=remarks,
													 value=value, edited_by=frappe.session.user,
													 parenttype="Vehicles", parent=x.vehicle,
													 parentfield="status_table", record_name=record_name,idx=9000))

		if self.total_price == 0:
			frappe.throw(" برجاء تحديد سعر البيع ")



	def on_cancel(self):
		for x in self.auction_sales_slips:
			frappe.db.sql(""" UPDATE `tabVehicles` set vehicle_status = "مخردة" where name = '{name}' 
						  """.format(name=x.vehicle))

			frappe.db.sql(""" DELETE FROM `tabVehicle Status Logs` where parent = '{parent}' and value = '{value}'
			 """.format(value="تحت البيع بالمزاد", parent=x.vehicle))