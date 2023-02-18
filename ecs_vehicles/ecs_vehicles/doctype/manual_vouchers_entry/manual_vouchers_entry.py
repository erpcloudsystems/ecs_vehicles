# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class ManualVouchersEntry(Document):
	def validate(self):
		if self.liquid_type_voucher == "وقود":
			self.oil_type = ""
			self.gas_type = ""
			self.washing_voucher = ""
			
		if self.liquid_type_voucher == "زيت":
			self.fuel_type_voucher = ""
			self.gas_type = ""
			self.washing_voucher = ""
		if self.liquid_type_voucher == "غاز":
			self.fuel_type_voucher = ""
			self.oil_type = ""
			self.washing_voucher = ""
		if self.liquid_type_voucher == "غسيل":
			self.fuel_type_voucher = ""
			self.oil_type = ""
			self.gas_type = ""

	def get_ammend_no(self):
		first = frappe.db.get_list('Manual Vouchers Entry',
									filters={
									'voucher': ['=', '{0}'.format(self.voucher)],
									"docstatus":DocStatus.submitted(),
									"name": ["!=", self.name]
											}
									)
		if len(first) == 0:
			return len(first) + 1
		latest = frappe.db.get_list('Voucher',
									filters={
									'name': ['like', '{0}-%'.format(self.voucher)],
											},
									)
		max_id = 0
		for late in latest:
			if max_id < int(late["name"].split("-")[-1]) :
				max_id = int(late["name"].split("-")[-1])
		# frappe.throw(str(max_id))
		return max_id + 1

	def duplicate_voucher_entry(self):
		no_amend = self.get_ammend_no()
		fuel_type = ""
		if self.liquid_type == "وقود":
			fuel_type = self.fuel_type
		if self.liquid_type == "زيت":
			fuel_type = self.voucher_type
		if self.liquid_type == "غاز":
			fuel_type = "غاز طبيعي"
		if self.liquid_type == "غسيل":
			fuel_type = self.voucher_type

		voucher = frappe.get_doc({
			"doctype": "Voucher",
			"serial_no": "",
			"liquid_type":self.liquid_type,
			"voucher_type": self.voucher_type,
			"fuel_type": fuel_type,
			"release_date": self.release_date,
			"receipt_date": self.receipt_date,
			"name": self.voucher + "-" + str(no_amend),
			"barcode":self.voucher + "-" + str(no_amend),
			"voucher_price": self.voucher_price,
			"receipt_no": self.receipt_no,
			"issue_no": self.issue_no,
			"issue_date": self.issue_date,
			"entity": self.entity,
			"review_date": self.review_date,
			"reviewed": 1,
			"company_name": self.company_name,
			"batch_no": self.batch_no,
			"group_no": self.group_no,
			"duplicated": 1,
		})
		voucher.insert()
		self.amended_from_voucher = voucher.name
		self.save()

	def manualy_add_voucher(self):
		price = 0
		voucher_type = ""
		if self.liquid_type_voucher == "وقود":
			price = frappe.db.get_value("Fuel Voucher", self.fuel_type_voucher, "litre_count") * frappe.db.get_value("Fuel Voucher", self.fuel_type_voucher, "litre_rate")
			voucher_type = self.fuel_type_voucher

		if self.liquid_type_voucher == "زيت":
			price = frappe.db.get_value("Oil Type", self.oil_type, "rate")
			voucher_type = self.oil_type

		if self.liquid_type_voucher == "غاز":
			price = frappe.db.get_value("Gas Voucher", self.gas_type, "gas_count") * frappe.db.get_value("Gas Voucher", self.gas_type, "meter_rate")
			voucher_type = self.gas_type

		if self.liquid_type_voucher == "غسيل":
			price = frappe.db.get_value("Washing Voucher", self.washing_voucher, "rate")
			voucher_type = self.washing_voucher

		self.voucher_price_voucher = price
		self.barcode_no = self.barcode
		self.save()
		if frappe.db.exists("Voucher", self.barcode):
			frappe.throw("يوجد بون بنفس الباركود")

		fuel_type = ""
		if self.liquid_type_voucher == "وقود":
			fuel_type = self.fuel_type_v
		if self.liquid_type_voucher == "زيت":
			fuel_type = voucher_type
		if self.liquid_type_voucher == "غاز":
			fuel_type = "غاز طبيعي"
		if self.liquid_type_voucher == "غسيل":
			fuel_type = voucher_type

		voucher = frappe.get_doc({
			"doctype": "Voucher",
			"serial_no": "",
			"notebook_no":self.notebook_no,
			"barcode_no":self.barcode_no,
			"barcode":self.barcode,
			"liquid_type":self.liquid_type_voucher,
			"voucher_type": voucher_type,
			"fuel_type": fuel_type,
			"voucher_price": self.voucher_price_voucher,
			"release_date": self.release_date_voucher,
			"receipt_date": self.receipt_date_voucher_date,
			"receipt_no": self.name,
			"name": self.barcode,
			"issue_no": self.name,
			"issue_date": self.issue_date_voucher,
			"entity": self.entity_voucher,
		})
		voucher.insert()
		self.voucher_new_name = voucher.name
		self.save()

	def on_submit (self):
		if self.voucher_select == "بون مكرر":
			self.duplicate_voucher_entry()
		elif self.voucher_select == "تكويد بون جديد":
			self.manualy_add_voucher()
		else:
			frappe.throw("برجاء اختيار نوع العملية")
			
	def before_insert(self):
		if self.voucher_select == "بون مكرر":
			self.naming_series= "DUP-"
		elif self.voucher_select == "تكويد بون جديد":
			self.naming_series= "NEW-"
		else:
			frappe.throw("برجاء اختيار نوع العملية")