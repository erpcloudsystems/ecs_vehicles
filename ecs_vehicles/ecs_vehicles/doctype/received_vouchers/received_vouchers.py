# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReceivedVouchers(Document):
	def validate(self):
		batch_list = frappe.db.sql(""" Select batch_no from `tabReceived Vouchers`
		where fiscal_year = '{fiscal_year}' and name != '{name}' and docstatus = 1 """.format(name=self.name, fiscal_year=self.fiscal_year), as_dict=1)

		for x in batch_list:
			if self.batch_no == x.batch_no:
				frappe.throw(
					" لا يمكن إستخدام رقم الدفعة " + str(x.batch_no) + " أكثر من مرة لنفس السنة المالية ")

		new_batch_no = self.batch_no
		new_fiscal_year = self.fiscal_year
		self.document_name = "دفعة " + "(" + str(new_batch_no) + ")" + " لسنة " + str(new_fiscal_year)
		if (not frappe.db.exists("Received Vouchers", self.document_name)) and (self.document_name != self.name):
			frappe.db.sql(""" update `tabReceived Vouchers` set name = '{document_name}' where name = '{old_name}'
				""".format(document_name=self.document_name, old_name=self.name))


	@frappe.whitelist()
	def append_vouchers(self):
		fuel_vouchers = frappe.db.get_all("Fuel Voucher")
		oil_vouchers = frappe.db.get_all("Oil Type")
		gas_vouchers = frappe.db.get_all("Gas Voucher")
		washing_vouchers = frappe.db.get_all("Washing Vouchers")

		if self.liquid_type == "وقود":
			self.set("vouchers_count_table", [])
			for x in fuel_vouchers:
				row = self.append("vouchers_count_table", {})
				row.voucher_type = x.name
		if self.liquid_type == "زيت":
			self.set("vouchers_count_table", [])
			for y in oil_vouchers:
				row = self.append("vouchers_count_table", {})
				row.voucher_type = y.name
		if self.liquid_type == "غاز":
			self.set("vouchers_count_table", [])
			for z in gas_vouchers:
				row = self.append("vouchers_count_table", {})
				row.voucher_type = z.name
		if self.liquid_type == "غسيل":
			self.set("vouchers_count_table", [])
			for w in washing_vouchers:
				row = self.append("vouchers_count_table", {})
				row.voucher_type = w.name


	@frappe.whitelist()
	def get_max_batch(self):
		last_batch = frappe.db.sql(""" select max(batch_no) as max from `tabReceived Vouchers` 
				where name != '{name}' and fiscal_year = '{fiscal_year}' and docstatus = 1
				""".format(name=self.name, fiscal_year=self.fiscal_year), as_dict=1)
		
		for x in last_batch:
			if not x.max:
				batch_no = 1
			else:
				batch_no = int(x.max) + 1
			return batch_no
