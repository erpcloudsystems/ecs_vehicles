# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IssuingRules(Document):
	def validate(self):
		rule_text = ""
		vehicle_type = ""
		if self.all_types == 0:
			vehicle_type = self.vehicle_type
		if self.all_types == 1:
			vehicle_type = "كل الأنواع"
		vehicle_shape = ""
		if self.all_shapes == 0:
			vehicle_shape = self.vehicle_shape
		if self.all_shapes == 1:
			vehicle_shape = "كل الأشكال"
		vehicle_brand = ""
		if self.all_brands == 0:
			vehicle_brand = self.vehicle_brand
		if self.all_brands == 1:
			vehicle_brand = "كل الماركات"
		vehicle_style = ""
		if self.all_styles == 0:
			vehicle_style = self.vehicle_style
		if self.all_styles == 1:
			vehicle_style = "كل الطرازات"
		vehicle_model = ""
		if self.all_models == 0:
			vehicle_model = self.vehicle_model
		if self.all_models == 1:
			vehicle_model = "كل الموديلات"
		processing_type = ""
		if self.all_processing == 0:
			processing_type = self.processing_type
		if self.all_processing == 1:
			processing_type = "كل التجهيزات"


		if self.issue_type == "وقود":
			rule_text = "<b>" + " نوع المركبة: " + "</b>" + str(str(vehicle_type)
				+ "<br>" + "<b>" + " شكل: " + "</b>" + str(vehicle_shape)
				+ "<br>" + "<b>" + " ماركة: " + "</b>" + str(vehicle_brand)
				+ "<br>" + "<b>" + " طراز: " + "</b>" + str(vehicle_style)
				+ "<br>" + "<b>" + " موديل: " + "</b>" + str(vehicle_model)
				+ "<br>" + "<b>" + " نوع التجهيز: " + "</b>" + str(processing_type)
				+ "<br>" + "<b>" + " عدد السلندرات: " + "</b>" + str(self.cylinder_count)
				+ "<br>" + "<b>" + " نوع الوقود: " + "</b>" + str(self.fuel_type)
				+ "<br>" + "<b>" + " السعة اللترية: " + "</b>" + " من " + str(self.from_litre_capacity)
				+ " إلى " + str(self.to_litre_capacity)
				+ "<br>" + "<b>" + " (يصرف لها " + str(self.litre_count)
				+ " لتر " + str(self.fuel_type) + ")" + "</b>"
				)

		if self.issue_type == "زيت":
			rule_text = "<b>" + " نوع المركبة: " + "</b>" + str(str(vehicle_type)
				+ "<br>" + "<b>" + " شكل: " + "</b>" + str(vehicle_shape)
				+ "<br>" + "<b>" + " ماركة: " + "</b>" + str(vehicle_brand)
				+ "<br>" + "<b>" + " طراز: " + "</b>" + str(vehicle_style)
				+ "<br>" + "<b>" + " موديل: " + "</b>" + str(vehicle_model)
				+ "<br>" + "<b>" + " نوع التجهيز: " + "</b>" + str(processing_type)
				+ "<br>" + "<b>" + " عدد السلندرات: " + "</b>" + str(self.cylinder_count)
				+ "<br>" + "<b>" + " نوع الوقود: " + "</b>" + str(self.fuel_type)
				+ "<br>" + "<b>" + " السعة اللترية: " + "</b>" + " من " + str(self.from_litre_capacity)
				+ " إلى " + str(self.to_litre_capacity)
				+ "<br>" + "<b>" + " (يصرف لها " + str(self.oil_count)
				+ " لتر " + str(self.oil_type) + ")" + "</b>"
				)

		if self.issue_type == "غاز":
			rule_text = "<b>" + " نوع المركبة: " + "</b>" + str(str(vehicle_type)
				+ "<br>" + "<b>" + " شكل: " + "</b>" + str(vehicle_shape)
				+ "<br>" + "<b>" + " ماركة: " + "</b>" + str(vehicle_brand)
				+ "<br>" + "<b>" + " طراز: " + "</b>" + str(vehicle_style)
				+ "<br>" + "<b>" + " موديل: " + "</b>" + str(vehicle_model)
				+ "<br>" + "<b>" + " نوع التجهيز: " + "</b>" + str(processing_type)
				+ "<br>" + "<b>" + " عدد السلندرات: " + "</b>" + str(self.cylinder_count)
				+ "<br>" + "<b>" + " نوع الوقود: " + "</b>" + str(self.fuel_type)
				+ "<br>" + "<b>" + " السعة اللترية: " + "</b>" + " من " + str(self.from_litre_capacity)
				+ " إلى " + str(self.to_litre_capacity)
				+ "<br>" + "<b>" + " (يصرف لها " + str(self.gas_count)
				+ " متر مكعب " + str("غاز طبيعي") + ")" + "</b>"
				)

		if self.issue_type == "غسيل":
			rule_text = "<b>" + " نوع المركبة: " + "</b>" + str(str(vehicle_type)
				+ "<br>" + "<b>" + " الشكل: " + "</b>" + str(vehicle_shape)
				+ "<br>" + "<b>" + " الماركة: " + "</b>" + str(vehicle_brand)
				+ "<br>" + "<b>" + " الطراز: " + "</b>" + str(vehicle_style)
				+ "<br>" + "<b>" + " الموديل: " + "</b>" + str(vehicle_model)
				+ "<br>" + "<b>" + " نوع التجهيز: " + "</b>" + str(processing_type)
				+ "<br>" + "<b>" + " عدد السلندرات: " + "</b>" + str(self.cylinder_count)
				+ "<br>" + "<b>" + " نوع الوقود: " + "</b>" + str(self.fuel_type)
				+ "<br>" + "<b>" + " السعة اللترية: " + "</b>" + " من " + str(self.from_litre_capacity)
				+ " إلى " + str(self.to_litre_capacity)
				+ "<br>" + "<b>" + " (يصرف لها بون " + str(self.washing_voucher)
				+ ")" + "</b>"
				)

		self.rule_text = str(rule_text)

	def on_submit(self):
		if self.issue_type == "وقود":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["cylinder_count"] = self.cylinder_count
			conditions["fuel_type"] = self.fuel_type
			# conditions["issuing_rule"] = ""
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set issuing_rule = '{issuing_rule}' where name = '{name}'
							  """.format(issuing_rule=self.name, name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set litre_count = '{litre_count}' where name = '{name}'
							  """.format(litre_count=self.litre_count, name=vec.name))

				# vec.issuing_rule = self.name
				# vec.litre_count = self.litre_count
				# vec.save()

		if self.issue_type == "زيت":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["cylinder_count"] = self.cylinder_count
			conditions["fuel_type"] = self.fuel_type
			# conditions["oil_issuing_rule"] = ""
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set oil_issuing_rule = '{oil_issuing_rule}' where name = '{name}'
							  """.format(oil_issuing_rule=self.name, name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set oil_type = '{oil_type}' where name = '{name}'
							  """.format(oil_type=self.oil_type, name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set oil_count = '{oil_count}' where name = '{name}'
							  """.format(oil_count=self.oil_count, name=vec.name))

				# vec.oil_issuing_rule = self.name
				# vec.oil_type = self.oil_type
				# vec.oil_count = self.oil_count
				# vec.save()

		if self.issue_type == "غاز":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["cylinder_count"] = self.cylinder_count
			conditions["fuel_type"] = self.fuel_type
			# conditions["gas_issuing_rule"] = ""
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set gas_issuing_rule = '{gas_issuing_rule}' where name = '{name}'
							  """.format(gas_issuing_rule=self.name, name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set gas_count = '{gas_count}' where name = '{name}'
							  """.format(gas_count=self.gas_count, name=vec.name))

				# vec.gas_issuing_rule = self.name
				# vec.gas_count = self.gas_count
				# vec.save()

		if self.issue_type == "غسيل":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["cylinder_count"] = self.cylinder_count
			conditions["fuel_type"] = self.fuel_type
			# conditions["washing_voucher"] = ""
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set washing_issuing_rule = '{washing_issuing_rule}' where name = '{name}'
							  """.format(washing_issuing_rule=self.name, name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set washing_voucher = '{washing_voucher}' where name = '{name}'
							  """.format(washing_voucher=self.washing_voucher, name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set washing_count = 1 where name = '{name}'
							  """.format(name=vec.name))

				# vec.washing_issuing_rule = self.name
				# vec.washing_voucher = self.washing_voucher
				# vec.washing_count = 1
				# vec.save()


	def on_cancel(self):
		if self.issue_type == "وقود":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["fuel_type"] = self.fuel_type
			conditions["issuing_rule"] = self.name
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)
				frappe.db.sql(""" UPDATE `tabVehicles` set issuing_rule = "" where name = '{name}'
											  """.format(name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set litre_count = 0 where name = '{name}'
											  """.format(name=vec.name))

				# vec.issuing_rule = ""
				# vec.litre_count = 0
				# vec.save()

		if self.issue_type == "زيت":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["fuel_type"] = self.fuel_type
			conditions["oil_issuing_rule"] = self.name
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set oil_issuing_rule = "" where name = '{name}'
							  """.format(name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set oil_type = "" where name = '{name}'
							  """.format(name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set oil_count = 0 where name = '{name}'
							  """.format(name=vec.name))

				# vec.oil_issuing_rule = ""
				# vec.oil_type = ""
				# vec.oil_count = 0
				# vec.save()




		if self.issue_type == "غاز":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["fuel_type"] = self.fuel_type
			conditions["gas_issuing_rule"] = self.name
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set gas_issuing_rule = "" where name = '{name}'
											  """.format(name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set gas_count = 0 where name = '{name}'
											  """.format(name=vec.name))

				# vec.gas_issuing_rule = ""
				# vec.gas_count = 0
				# vec.save()


		if self.issue_type == "غسيل":
			conditions = {}
			if self.all_types == 0:
				conditions["vehicle_type"] = self.vehicle_type
			if self.all_shapes == 0:
				conditions["vehicle_shape"] = self.vehicle_shape
			if self.all_brands == 0:
				conditions["vehicle_brand"] = self.vehicle_brand
			if self.all_styles == 0:
				conditions["vehicle_style"] = self.vehicle_style
			if self.all_models == 0:
				conditions["vehicle_model"] = self.vehicle_model
			if self.all_processing == 0:
				conditions["processing_type"] = self.processing_type
			conditions["fuel_type"] = self.fuel_type
			conditions["washing_issuing_rule"] = self.name
			conditions["litre_capacity"] = [">=", self.from_litre_capacity]
			conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

			vehicles = frappe.db.get_all("Vehicles", filters=conditions)

			for v in vehicles:
				vec = frappe.get_doc("Vehicles", v.name)

				frappe.db.sql(""" UPDATE `tabVehicles` set washing_issuing_rule = "" where name = '{name}'
							  """.format(name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set washing_voucher = "" where name = '{name}'
							  """.format(name=vec.name))
				frappe.db.sql(""" UPDATE `tabVehicles` set washing_count = 0 where name = '{name}'
							  """.format(name=vec.name))

				# vec.washing_issuing_rule = ""
				# vec.washing_voucher = ""
				# vec.washing_count = 0
				# vec.save()



