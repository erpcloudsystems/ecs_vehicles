import frappe
from frappe.model.document import Document

class PossessionType(Document):
	def before_insert(self):
		self.generate_code()

	@frappe.whitelist()
	def generate_code(self):
		last_code = frappe.db.sql(""" select max(code) as max from `tabPossession Type` """, as_dict=1)
		for x in last_code:
			if not x.max:
				self.code = 1
			else:
				self.code = int(x.max) + 1


	def validate(self):
		possession_type_list = frappe.db.sql(""" Select code, possession_type from `tabPossession Type`
		where docstatus = 0 """, as_dict=1)

		for x in possession_type_list:
			if self.code == x.code:
				frappe.throw(
					" ?? ???? ??????? ????? " + str(x.code) + " ???? ?? ??? ??? ??? ?????? ?? ??? ??????? " + x.possession_type)
