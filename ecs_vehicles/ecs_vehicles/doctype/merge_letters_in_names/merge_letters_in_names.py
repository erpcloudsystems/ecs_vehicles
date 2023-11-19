import frappe
from frappe.model.document import Document

class MergeLettersinNames(Document):
	def merge_names(self, doctype, item_name):
		items = frappe.db.sql("""
		SELECT *
		FROM `tabPhrases to Merge` item
		""",as_dict=1)
		for phrase in items:
			update_item = frappe.db.sql("""
			UPDATE `{doctype}` item
			set item.{item_name} = replace(item.{item_name},"{old_phrase}", "{new_phrase}")
			""".format(old_phrase=phrase.old_phrase, new_phrase=phrase.new_phrase,doctype=doctype, item_name=item_name))
			frappe.db.commit()
	def validate(self):
		self.merge_names("tabItem","item_name")