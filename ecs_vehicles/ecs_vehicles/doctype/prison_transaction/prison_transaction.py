# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PrisonTransaction(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("custom_prison_transaction_logs", {})
		log.transaction_no = self.name
		log.start_date = self.start_date
		log.end_date = self.end_date
		log.notes = self.notes
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Prison Transaction Logs", {"transaction_no": self.name})
		log.delete()