# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PresentationNotes(Document):
	@frappe.whitelist()
	def on_submit(self):
		frappe.db.sql(""" update `tabBuying Order` set presentation_note_status = '{status}' where `tabBuying Order`.name = '{name}'  """.format(status= self.workflow_state, name=self.buying_order))
		buying_order = frappe.get_doc("Buying Order", self.buying_order)
		if buying_order.presentation_style == "أتفاق مباشر":
			frappe.db.sql(""" update `tabBuying Order` set workflow_state = "انتظار التوريد" where `tabBuying Order`.name = '{name}'  """.format(name=self.buying_order))
		else:
			frappe.db.sql(""" update `tabBuying Order` set workflow_state = "انتظار الفض الفني" where `tabBuying Order`.name = '{name}'  """.format( name=self.buying_order))
		
  
  
	@frappe.whitelist()
	def on_cancel(self):
		frappe.db.sql(""" update `tabBuying Order` set presentation_note = "" where `tabBuying Order`.name = '{name}'  """.format( name=self.buying_order))
		frappe.db.sql(""" update `tabBuying Order` set workflow_state = "انتظار مذكرة الطرح" where `tabBuying Order`.name = '{name}'  """.format( name=self.buying_order))
		frappe.db.sql(""" update `tabBuying Order` set presentation_note_status = "" where `tabBuying Order`.name = '{name}'  """.format( name=self.buying_order))
