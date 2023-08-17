# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitPenalty(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit )
		log = employee.append("recruit_penalty_logs", {})
		log.transaction_no = self.name
		log.recruit_penalty_type = self.recruit_penalty_type
		log.reason = self.reason
		log.penalty_date = self.penalty_date
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Recruit Penalty Logs", {"transaction_no": self.name})
		log.delete()
