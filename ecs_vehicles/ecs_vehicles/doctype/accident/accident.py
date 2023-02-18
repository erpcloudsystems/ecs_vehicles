# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words

class Accident(Document):
	def before_insert(self):
		if not self.accident_no:
			self.generate_code()
		
	@frappe.whitelist()
	def generate_code(self):
		if not self.accident_no:
			last_code = frappe.db.sql(""" select max(accident_no) as max from `tabAccident` 
				where name != '{name}' and fiscal_year = '{fiscal_year}' 
				""".format(name=self.name, fiscal_year=self.fiscal_year), as_dict=1)
			for x in last_code:
				if not x.max:
					self.accident_no = 1
					self.journal_no2 = 1
				else:
					self.accident_no = int(x.max) + 1
					self.journal_no2 = int(x.max) + 1

	def validate(self):
		total = 0
		total_qty = 0
		for x in self.damage_table:
			x.deduction_amount = x.qty * x.rate * x.deduction_percent / 100
			total += x.deduction_amount
			total_qty += x.qty

		self.total_qty = total_qty
		self.deduction_amount = total
		self.administrative_expenses = total * 0.1
		self.total_deduction_amount = self.deduction_amount + self.administrative_expenses
		self.in_words = money_in_words(self.total_deduction_amount, "ج.م")

		if self.deduction_party == "أطراف الوزارة":
			self.party_name = self.ministry_party_type + "/ " + self.ministry_party_name
			self.party_id = self.id_no
			self.party_id_type = self.id_type
			self.party_id_issue_location = self.id_issue_location
			self.party_id_issue_date = self.id_issue_date

		if self.deduction_party == "أطراف أخرى":
			self.party_name = self.other_party_name
			self.party_id = self.id_no2
			self.party_id_type = self.id_type2
			self.party_id_issue_location = self.id_issue_location2
			self.party_id_issue_date = self.id_issue_date2

	def on_submit(self):
		if self.party_name:
			if not frappe.db.exists("Accident Party", self.party_name):
				new_party = frappe.get_doc({
					"doctype": "Accident Party",
					"accident_party": self.party_name
				})
				new_party.insert(ignore_permissions=True)

		vehicle = frappe.get_doc("Vehicles", self.vehicle)
		# vehicle.edit_status = 1
		# vehicle.new_status = "عاطلة"
		# vehicle.edit_status_date = self.accident_date
		# vehicle.status_remarks = "تم تسجيل واقعة رقم " + str(self.accident_no)

		accident = vehicle.append("accident_logs", {})
		accident.accident_code = self.name
		accident.accident_no = self.accident_no
		accident.accident_type = self.accident_type
		accident.accident_date = self.accident_date
		accident.party_name = self.party_name
		accident.party_id = self.party_id
		accident.save()
		vehicle.save()

	def on_update_after_submit(self):
		total = 0
		total_qty = 0
		for x in self.damage_table:
			x.deduction_amount = x.qty * x.rate * x.deduction_percent / 100
			total += x.deduction_amount
			total_qty += x.qty

		self.total_qty = total_qty
		self.deduction_amount = total
		self.administrative_expenses = total * 0.1
		self.total_deduction_amount = self.deduction_amount + self.administrative_expenses
		self.in_words = money_in_words(self.total_deduction_amount, "EGP")

		if self.deduction_party == "أطراف الوزارة":
			self.party_name = self.ministry_party_type + "/ " + self.ministry_party_name
			self.party_id = self.id_no
			self.party_id_type = self.id_type
			self.party_id_issue_location = self.id_issue_location
			self.party_id_issue_date = self.id_issue_date

			if not frappe.db.exists("Accident Party", self.party_name):
				new_party = frappe.get_doc({
					"doctype": "Accident Party",
					"accident_party": self.party_name
				})
				new_party.insert(ignore_permissions=True)

		if self.deduction_party == "أطراف أخرى":
			self.party_name = self.other_party_name
			self.party_id = self.id_no2
			self.party_id_type = self.id_type2
			self.party_id_issue_location = self.id_issue_location2
			self.party_id_issue_date = self.id_issue_date2

			if not frappe.db.exists("Accident Party", self.party_name):
				new_party = frappe.get_doc({
					"doctype": "Accident Party",
					"accident_party": self.party_name
				})
				new_party.insert(ignore_permissions=True)

	def on_cancel(self):
		record = frappe.get_doc('Accident Logs', {'accident_code': self.name, 'parent': self.vehicle})
		record.delete()



