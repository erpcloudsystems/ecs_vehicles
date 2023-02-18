
# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VouchersReview(Document):
	def validate(self):
		if not self.review_vouchers_table:
			frappe.throw(" برجاء عمل مسح للباركود الخاص بالبونات ")

	def on_submit(self):
		user = frappe.session.user
		username = frappe.db.get_value("User", user, "full_name")
		for x in self.review_vouchers_table:
			frappe.db.sql(""" UPDATE `tabVoucher` set reviewed = 1, review_date='{review_date}', batch_no='{batch_no}', 
							  group_no='{group_no}', company_name='{company_name}', voucher_review='{voucher_review}',
							  username='{username}', vehicle='{vehicle}', police_no='{police_no}', 
							  entity_name='{entity_name}', private_no='{private_no}', motor_no='{motor_no}', 
							  chassis_no='{chassis_no}', vehicle_fuel_type='{vehicle_fuel_type}', 
							  vehicle_shape='{vehicle_shape}', vehicle_brand='{vehicle_brand}', 
							  vehicle_style='{vehicle_style}', vehicle_model='{vehicle_model}', 
							  vehicle_color='{vehicle_color}', processing_type='{processing_type}'
						      where name = '{barcode_no}'
						  """.format(review_date=self.date, batch_no=self.batch_no, group_no=self.group_no, username=username,
							  company_name=self.company_name, voucher_review=self.name, barcode_no=x.barcode_no,
							  vehicle=x.vehicle, police_no=x.police_no, entity_name=x.entity_name, private_no=x.private_no,
							  motor_no=x.motor_no, chassis_no=x.chassis_no, vehicle_fuel_type=x.vehicle_fuel_type,
							  vehicle_shape=x.vehicle_shape, vehicle_brand=x.vehicle_brand, vehicle_style=x.vehicle_style,
							  vehicle_model=x.vehicle_model, vehicle_color=x.vehicle_color, processing_type=x.processing_type))


	def on_cancel(self):
		for x in self.review_vouchers_table:
			frappe.db.sql(""" UPDATE `tabVoucher` set reviewed = 0, review_date=Null, batch_no=Null, 
							  group_no=Null, company_name=Null, voucher_review=Null, username=Null,
							  vehicle=Null, police_no=Null, entity_name=Null, private_no=Null, motor_no=Null, 
							  chassis_no=Null, vehicle_fuel_type=Null, vehicle_shape=Null, vehicle_brand=Null, 
							  vehicle_style=Null, vehicle_model=Null, vehicle_color=Null, processing_type=Null
						      where name = '{barcode_no}'
						  """.format(barcode_no=x.barcode_no))
