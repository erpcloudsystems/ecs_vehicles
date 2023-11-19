from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    phrases = frappe.db.sql("""
    SELECT old_phrase, new_phrase
    FROM `tabPhrases to Merge`
    """, as_dict=1)
    for phrase in phrases:
        doc.item_name = doc.item_name.replace(phrase.old_phrase, phrase.new_phrase)
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
