# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitAbsent(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("recruit_absent_logs", {})
		log.transaction_no = self.name
		log.absent_date = self.absent_date
		log.notes = self.notes
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Recruit Absent Logs", {"transaction_no": self.name})
		log.delete()
