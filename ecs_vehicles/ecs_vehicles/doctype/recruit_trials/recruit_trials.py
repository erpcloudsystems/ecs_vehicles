# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecruitTrials(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("recruit_trials_logs", {})
		log.transaction_no = self.name
		log.violation_description = self.violation_description
		log.trial_type = self.trial_type
		log.trial_date = self.trial_date
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Recruit Trials Logs", {"transaction_no": self.name})
		log.delete()
