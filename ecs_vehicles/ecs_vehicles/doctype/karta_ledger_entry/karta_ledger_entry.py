# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class KartaLedgerEntry(Document):
	def after_insert(self):
		if self.doc_type == "Maintenance Order":
			frappe.db.sql(
				""" update `tabMaintenance Order Item` set kle = '{kle}'
					where parent='{parent}' and name='{name}'
				""".format(kle=self.name, parent=self.ord_serial, name=self.detail_serial)
			)
			maintenance_order = frappe.get_doc("Maintenance Order", self.ord_serial)
			maintenance_order.reload()

		if self.doc_type == "Purchase Invoices":
			frappe.db.sql(
				""" update `tabPurchase Invoices Table` set kle = '{kle}'
					where parent='{parent}' and name='{name}'
				""".format(kle=self.name, parent=self.ord_serial, name=self.detail_serial)
			)
			purchase_invoices = frappe.get_doc("Purchase Invoices", self.ord_serial)
			purchase_invoices.reload()

		