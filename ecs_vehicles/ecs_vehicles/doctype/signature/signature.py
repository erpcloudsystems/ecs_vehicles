# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SIgnature(Document):
	def validate(self):
		if self.is_default == 1:
			signature_list = frappe.db.sql(
			""" Select `tabSIgnature`.name 
				from `tabSIgnature`
				where `tabSIgnature`.name != '{name}'
				and `tabSIgnature`.is_default = 1
			""".format(name=self.name), as_dict=1)

			for x in signature_list:
				old_signature = frappe.get_doc("SIgnature", x.name)
				old_signature.is_default = 0
				old_signature.save()

	# def on_update_after_submit(self):
	# 	if self.is_default == 1:
	# 		signature_list = frappe.db.sql(
	# 		""" Select `tabSIgnature`.name
	# 			from `tabSIgnature`
	# 			where `tabSIgnature`.name != '{name}'
	# 			and `tabSIgnature`.is_default = 1
	# 		""".format(name=self.name), as_dict=1)
	#
	# 		for x in signature_list:
	# 			old_signature = frappe.get_doc("SIgnature", x.name)
	# 			old_signature.is_default = 0
	# 			old_signature.save()