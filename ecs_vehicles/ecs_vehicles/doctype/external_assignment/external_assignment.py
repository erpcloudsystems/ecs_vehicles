# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ExternalAssignment(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("external_assignment_logs", {})
		log.transaction_no = self.name
		log.assignment_date = self.assignment_date
		log.assignment_entities = self.assignment_entities
		log.notes = self.notes
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("External Assignment Logs", {"transaction_no": self.name})
		log.delete()