# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitWriteOff(Document):
	def on_submit(self):
		frappe.db.set_value('Employee', self.recruit, 'status', "Suspended")
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("recruit_write_off_logs", {})
		log.transaction_no = self.name
		log.recruit_degree = self.recruit_degree
		log.notes = self.notes
		log.write_off_date = self.write_off_date
		log.return_date = self.return_date
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Recruit Write Off Logs", {"transaction_no": self.name})
		log.delete()
