# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CriminalAndPoliticalInvestigations(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("criminal_and_political_investigations_logs", {})
		log.transaction_no = self.name
		log.political_investigation_date = self.political_investigation_date
		log.receipt_the_result_of_political_investigation_date = self.receipt_the_result_of_political_investigation_date
		log.political_investigation_result = self.political_investigation_result
		log.criminal_investigation_date = self.criminal_investigation_date
		log.receipt_the_result_of_criminal_investigation_date = self.receipt_the_result_of_criminal_investigation_date
		log.criminal_investigation_result = self.criminal_investigation_result
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Criminal And Political Investigations Logs", {"transaction_no": self.name})
		log.delete()