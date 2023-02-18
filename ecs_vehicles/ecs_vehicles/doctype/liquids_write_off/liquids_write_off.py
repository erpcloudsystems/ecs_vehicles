# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LiquidsWriteOff(Document):
	def before_insert(self):
		fuel_vouchers = frappe.db.get_all("Fuel Voucher")
		oil_vouchers = frappe.db.get_all("Oil Type")
		gas_vouchers = frappe.db.get_all("Gas Voucher")
		washing_vouchers = frappe.db.get_all("Washing Vouchers")
		for x in fuel_vouchers:
			row = self.append("liquids_write_off_table", {})
			row.liquid_voucher = x.name
		for y in oil_vouchers:
			row = self.append("liquids_write_off_table", {})
			row.liquid_voucher = y.name
		for z in gas_vouchers:
			row = self.append("liquids_write_off_table", {})
			row.liquid_voucher = z.name
		for w in washing_vouchers:
			row = self.append("liquids_write_off_table", {})
			row.liquid_voucher = w.name

