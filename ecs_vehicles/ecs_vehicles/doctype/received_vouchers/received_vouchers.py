# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReceivedVouchers(Document):
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
