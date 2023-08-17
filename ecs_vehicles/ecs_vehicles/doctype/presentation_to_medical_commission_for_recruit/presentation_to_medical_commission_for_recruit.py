# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PresentationToMedicalCommissionForRecruit(Document):
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.recruit)
		log = employee.append("presentation_to_medical_commission_for_recruit_logs", {})
		log.transaction_no = self.name
		log.reason_of_injury = self.reason_of_injury
		log.injury_date = self.injury_date
		log.presentation_case = self.presentation_case
		log.the_committees_decision = self.the_committees_decision
		log.the_committees_date = self.the_committees_date
		log.presentation_date = self.presentation_date
		log.save()

	def on_cancel(self):
		log = frappe.get_doc("Presentation To Medical Commission For Recruit Logs", {"transaction_no": self.name})
		log.delete()
