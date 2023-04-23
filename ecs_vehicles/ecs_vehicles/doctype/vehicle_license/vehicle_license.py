# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, getdate
from frappe.model.document import Document

class VehicleLicense(Document):
	def before_insert(self):
		min_code_list = frappe.db.sql(""" select min(serial) as min from `tabLicense Card`
				 							  where vehicle is null	""", as_dict=1)
		for x in min_code_list:
			if frappe.db.exists("License Card", {'serial': x.min}):
				serial_1 = int(x.min)
				serial_2 = int(x.min) + 1
				serial_3 = int(x.min) + 2
				serial_4 = int(x.min) + 3

				if frappe.db.exists("License Card", {'serial': serial_1}):
					min_code1 = frappe.get_doc("License Card", {'serial': serial_1})
					# self.license_no = min_code1.name
				else:
					frappe.throw(" برجاء إضافة كروت جديدة ")


				if frappe.db.exists("License Card", {'serial': serial_2}):
					min_code2 = frappe.get_doc("License Card", {'serial': serial_2})
					# self.license_no2 = min_code2.name
				else:
					frappe.throw(" برجاء إضافة كروت جديدة ")


				if frappe.db.exists("License Card", {'serial': serial_3}):
					min_code3 = frappe.get_doc("License Card", {'serial': serial_3})
					# self.license_no3 = min_code3.name
				else:
					frappe.throw(" برجاء إضافة كروت جديدة ")


				if frappe.db.exists("License Card", {'serial': serial_4}):
					min_code4 = frappe.get_doc("License Card", {'serial': serial_4})
					# self.license_no4 = min_code4.name
				else:
					frappe.throw(" برجاء إضافة كروت جديدة ")

			else:
				frappe.throw(" برجاء إضافة كروت جديدة ")

	def validate(self):
		if self.vehicle == self.vehicle2:
			frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (2) ")

		if self.vehicle == self.vehicle3:
			frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (3) ")

		if self.vehicle == self.vehicle4:
			frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (4) ")

		if self.vehicle2 == self.vehicle3:
			frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (2) والمركبة (3) ")

		if self.vehicle2 == self.vehicle4:
			frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (2) والمركبة (4) ")

		if self.vehicle3 == self.vehicle4:
			frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (3) والمركبة (4) ")


		user = frappe.session.user
		user_name = frappe.db.get_value("User", user, "full_name")

		self.set("license_entry_summary", [])
		license_entry_summary = self.append("license_entry_summary", {})
		license_entry_summary.vehicle = self.vehicle
		license_entry_summary.police_no = self.police_no
		license_entry_summary.private_no = self.private_no
		license_entry_summary.vehicle_type = self.vehicle_type
		license_entry_summary.entity = self.entity
		license_entry_summary.from_date = self.from_date
		license_entry_summary.to_date = self.to_date
		license_entry_summary.license_no = self.license_no
		license_entry_summary.issue_status = self.issue_status
		license_entry_summary.user = user_name
		if self.issue_status == "تجديد":
			license_entry_summary.renewal_type = self.renewal_type
		else:
			license_entry_summary.renewal_type = "ترخيص أول مرة"

		license_entry_summary = self.append("license_entry_summary", {})
		license_entry_summary.vehicle = self.vehicle2
		license_entry_summary.police_no = self.police_no2
		license_entry_summary.private_no = self.private_no2
		license_entry_summary.vehicle_type = self.vehicle_type2
		license_entry_summary.entity = self.entity2
		license_entry_summary.from_date = self.from_date2
		license_entry_summary.to_date = self.to_date2
		license_entry_summary.license_no = self.license_no2
		license_entry_summary.issue_status = self.issue_status2
		license_entry_summary.user = user_name
		if self.issue_status2 == "تجديد":
			license_entry_summary.renewal_type = self.renewal_type2
		else:
			license_entry_summary.renewal_type = "ترخيص أول مرة"

		license_entry_summary = self.append("license_entry_summary", {})
		license_entry_summary.vehicle = self.vehicle3
		license_entry_summary.police_no = self.police_no3
		license_entry_summary.private_no = self.private_no3
		license_entry_summary.vehicle_type = self.vehicle_type3
		license_entry_summary.entity = self.entity3
		license_entry_summary.from_date = self.from_date3
		license_entry_summary.to_date = self.to_date3
		license_entry_summary.license_no = self.license_no3
		license_entry_summary.issue_status = self.issue_status3
		license_entry_summary.user = user_name
		if self.issue_status3 == "تجديد":
			license_entry_summary.renewal_type = self.renewal_type3
		else:
			license_entry_summary.renewal_type = "ترخيص أول مرة"

		license_entry_summary = self.append("license_entry_summary", {})
		license_entry_summary.vehicle = self.vehicle4
		license_entry_summary.police_no = self.police_no4
		license_entry_summary.private_no = self.private_no4
		license_entry_summary.vehicle_type = self.vehicle_type4
		license_entry_summary.entity = self.entity4
		license_entry_summary.from_date = self.from_date4
		license_entry_summary.to_date = self.to_date4
		license_entry_summary.license_no = self.license_no4
		license_entry_summary.issue_status = self.issue_status4
		license_entry_summary.user = user_name
		if self.issue_status4 == "تجديد":
			license_entry_summary.renewal_type = self.renewal_type4
		else:
			license_entry_summary.renewal_type = "ترخيص أول مرة"


	def on_submit(self):
		user = frappe.session.user
		user_name = frappe.db.get_value("User", user, "full_name")

		vehicle = frappe.get_doc('Vehicles', self.vehicle)
		vehicle.license_no = self.license_no
		vehicle.license_status = "سارية"
		vehicle.license_duration = self.license_duration
		vehicle.license_from_date = self.from_date
		vehicle.license_to_date = self.to_date
		license_no = vehicle.append("vehicle_license_logs", {})
		license_no.license_no = self.license_no
		license_no.issue_status = self.issue_status
		if self.issue_status == "تجديد":
			license_no.renewal_type = self.renewal_type
		else:
			license_no.renewal_type = "ترخيص أول مرة"
		license_no.license_duration = self.license_duration
		license_no.license_from_date = self.from_date
		license_no.license_to_date = self.to_date
		license_no.license_status = self.license_status
		license_no.user = user_name
		license_no.save()
		vehicle.save()

		vehicle2 = frappe.get_doc('Vehicles', self.vehicle2)
		vehicle2.license_no = self.license_no2
		vehicle2.license_status = "سارية"
		vehicle2.license_duration = self.license_duration2
		vehicle2.license_from_date = self.from_date2
		vehicle2.license_to_date = self.to_date2
		license_no2 = vehicle2.append("vehicle_license_logs", {})
		license_no2.license_no = self.license_no2
		license_no2.issue_status = self.issue_status2
		if self.issue_status2 == "تجديد":
			license_no2.renewal_type = self.renewal_type2
		else:
			license_no2.renewal_type = "ترخيص أول مرة"
		license_no2.license_duration = self.license_duration2
		license_no2.license_from_date = self.from_date2
		license_no2.license_to_date = self.to_date2
		license_no2.license_status = self.license_status2
		license_no2.user = user_name
		license_no2.save()
		vehicle2.save()

		vehicle3 = frappe.get_doc('Vehicles', self.vehicle3)
		vehicle3.license_no = self.license_no3
		vehicle3.license_status = "سارية"
		vehicle3.license_duration = self.license_duration3
		vehicle3.license_from_date = self.from_date3
		vehicle3.license_to_date = self.to_date3
		license_no3 = vehicle3.append("vehicle_license_logs", {})
		license_no3.license_no = self.license_no3
		license_no3.issue_status = self.issue_status3
		if self.issue_status3 == "تجديد":
			license_no3.renewal_type = self.renewal_type3
		else:
			license_no3.renewal_type = "ترخيص أول مرة"
		license_no3.license_duration = self.license_duration3
		license_no3.license_from_date = self.from_date3
		license_no3.license_to_date = self.to_date3
		license_no3.license_status = self.license_status3
		license_no3.user = user_name
		license_no3.save()
		vehicle3.save()

		vehicle4 = frappe.get_doc('Vehicles', self.vehicle4)
		vehicle4.license_no = self.license_no4
		vehicle4.license_status = "سارية"
		vehicle4.license_duration = self.license_duration4
		vehicle4.license_from_date = self.from_date4
		vehicle4.license_to_date = self.to_date4
		license_no4 = vehicle4.append("vehicle_license_logs", {})
		license_no4.license_no = self.license_no4
		license_no4.issue_status = self.issue_status4
		if self.issue_status4 == "تجديد":
			license_no4.renewal_type = self.renewal_type4
		else:
			license_no4.renewal_type = "ترخيص أول مرة"
		license_no4.license_duration = self.license_duration4
		license_no4.license_from_date = self.from_date4
		license_no4.license_to_date = self.to_date4
		license_no4.license_status = self.license_status4
		license_no4.user = user_name
		license_no4.save()
		vehicle4.save()

		license_card = frappe.get_doc('License Card', self.license_no)
		license_card.vehicle = self.vehicle
		license_card.vehicle_license = self.name
		license_card.license_status = self.license_status
		license_card.issue_status = self.issue_status
		license_card.renewal_type = self.renewal_type
		license_card.license_duration = self.license_duration
		license_card.from_date = self.from_date
		license_card.to_date = self.to_date
		license_card.letter = self.letter
		license_card.police_no = self.police_no
		license_card.private_no = self.private_no
		license_card.vehicle_type = self.vehicle_type
		license_card.entity = self.entity
		license_card.vehicle_shape = self.vehicle_shape
		license_card.vehicle_brand = self.vehicle_brand
		license_card.vehicle_style = self.vehicle_style
		license_card.vehicle_model = self.vehicle_model
		license_card.vehicle_color = self.vehicle_color
		license_card.motor_no = self.motor_no
		license_card.chassis_no = self.chassis_no
		license_card.cylinder_count = self.cylinder_count
		license_card.litre_capacity = self.litre_capacity
		license_card.fuel_type = self.fuel_type
		license_card.possession_date = self.possession_date
		license_card.processing_type = self.processing_type
		license_card.save()

		license_card2 = frappe.get_doc('License Card', self.license_no2)
		license_card2.vehicle = self.vehicle2
		license_card2.vehicle_license = self.name
		license_card2.license_status = self.license_status2
		license_card2.issue_status = self.issue_status2
		license_card2.renewal_type = self.renewal_type2
		license_card2.license_duration = self.license_duration2
		license_card2.from_date = self.from_date2
		license_card2.to_date = self.to_date2
		license_card2.letter = self.letter2
		license_card2.police_no = self.police_no2
		license_card2.private_no = self.private_no2
		license_card2.vehicle_type = self.vehicle_type2
		license_card2.entity = self.entity2
		license_card2.vehicle_shape = self.vehicle_shape2
		license_card2.vehicle_brand = self.vehicle_brand2
		license_card2.vehicle_style = self.vehicle_style2
		license_card2.vehicle_model = self.vehicle_model2
		license_card2.vehicle_color = self.vehicle_color2
		license_card2.motor_no = self.motor_no2
		license_card2.chassis_no = self.chassis_no2
		license_card2.cylinder_count = self.cylinder_count2
		license_card2.litre_capacity = self.litre_capacity2
		license_card2.fuel_type = self.fuel_type2
		license_card2.possession_date = self.possession_date2
		license_card2.processing_type = self.processing_type2
		license_card2.save()

		license_card3 = frappe.get_doc('License Card', self.license_no3)
		license_card3.vehicle = self.vehicle3
		license_card3.vehicle_license = self.name
		license_card3.license_status = self.license_status3
		license_card3.issue_status = self.issue_status3
		license_card3.renewal_type = self.renewal_type3
		license_card3.license_duration = self.license_duration3
		license_card3.from_date = self.from_date3
		license_card3.to_date = self.to_date3
		license_card3.letter = self.letter3
		license_card3.police_no = self.police_no3
		license_card3.private_no = self.private_no3
		license_card3.vehicle_type = self.vehicle_type3
		license_card3.entity = self.entity3
		license_card3.vehicle_shape = self.vehicle_shape3
		license_card3.vehicle_brand = self.vehicle_brand3
		license_card3.vehicle_style = self.vehicle_style3
		license_card3.vehicle_model = self.vehicle_model3
		license_card3.vehicle_color = self.vehicle_color3
		license_card3.motor_no = self.motor_no3
		license_card3.chassis_no = self.chassis_no3
		license_card3.cylinder_count = self.cylinder_count3
		license_card3.litre_capacity = self.litre_capacity3
		license_card3.fuel_type = self.fuel_type3
		license_card3.possession_date = self.possession_date3
		license_card3.processing_type = self.processing_type3
		license_card3.save()

		license_card4 = frappe.get_doc('License Card', self.license_no4)
		license_card4.vehicle = self.vehicle4
		license_card4.vehicle_license = self.name
		license_card4.license_status = self.license_status4
		license_card4.issue_status = self.issue_status4
		license_card4.renewal_type = self.renewal_type4
		license_card4.license_duration = self.license_duration4
		license_card4.from_date = self.from_date4
		license_card4.to_date = self.to_date4
		license_card4.letter = self.letter4
		license_card4.police_no = self.police_no4
		license_card4.private_no = self.private_no4
		license_card4.vehicle_type = self.vehicle_type4
		license_card4.entity = self.entity4
		license_card4.vehicle_shape = self.vehicle_shape4
		license_card4.vehicle_brand = self.vehicle_brand4
		license_card4.vehicle_style = self.vehicle_style4
		license_card4.vehicle_model = self.vehicle_model4
		license_card4.vehicle_color = self.vehicle_color4
		license_card4.motor_no = self.motor_no4
		license_card4.chassis_no = self.chassis_no4
		license_card4.cylinder_count = self.cylinder_count4
		license_card4.litre_capacity = self.litre_capacity4
		license_card4.fuel_type = self.fuel_type4
		license_card4.possession_date = self.possession_date4
		license_card4.processing_type = self.processing_type4
		license_card4.save()

	def on_update_after_submit(self):
		license_card = frappe.get_doc('License Card', self.license_no)
		license_card.license_status = self.license_status
		license_card.save()
		license_record = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle, "license_no": self.license_no})
		license_record.license_status = self.license_status
		license_record.save()

		license_card2 = frappe.get_doc('License Card', self.license_no2)
		license_card2.license_status = self.license_status2
		license_card2.save()
		license_record2 = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle2, "license_no": self.license_no2})
		license_record2.license_status = self.license_status2
		license_record2.save()

		license_card3 = frappe.get_doc('License Card', self.license_no3)
		license_card3.license_status = self.license_status3
		license_card3.save()
		license_record3 = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle3, "license_no": self.license_no3})
		license_record3.license_status = self.license_status3
		license_record3.save()

		license_card4 = frappe.get_doc('License Card', self.license_no4)
		license_card4.license_status = self.license_status4
		license_card4.save()
		license_record4 = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle4, "license_no": self.license_no4})
		license_record4.license_status = self.license_status4
		license_record4.save()


