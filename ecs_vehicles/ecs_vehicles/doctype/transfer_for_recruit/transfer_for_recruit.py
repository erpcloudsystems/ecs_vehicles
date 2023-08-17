# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransferForRecruit(Document):
	def on_submit(self):
		frappe.db.set_value('Employee', self.recruit, 'main_department', self.transfer_to)
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("transfer_for_recruit_logs", {})
		log.transaction_no = self.name
		log.transfer_date = self.transfer_date
		log.decision_number = self.decision_number
		log.transfer_from = self.transfer_from
		log.transfer_to = self.transfer_to
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Transfer For Recruit Logs", {"transaction_no": self.name})
		log.delete()
