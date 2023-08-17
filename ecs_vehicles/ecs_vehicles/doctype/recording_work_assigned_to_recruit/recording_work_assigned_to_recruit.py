# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RecordingWorkAssignedToRecruit(Document):
	def on_submit(self):
		frappe.db.set_value('Employee', self.recruit, 'work_assigned_to_recruit', self.work_assigned)
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("recording_work_assigned_to_recruit_logs", {})
		log.transaction_no = self.name
		log.work_assigned = self.work_assigned
		log.notes = self.notes
		log.assigned_date = self.assigned_date
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Recording Work Assigned To Recruit Logs", {"transaction_no": self.name})
		log.delete()
