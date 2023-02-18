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
    if doc.quotation:
        rate = frappe.db.sql(""" select  a.item_code,a.rate,a.amount
                                                                       from `tabQuotation Item` a join `tabQuotation` b
                                                                       on a.parent = b.name
                                                                       where b.name = '{name}'
                                                                   """.format(name=doc.quotation), as_dict=1)
        for x in rate:
            for i in doc.items:
                if x.item_code == i.item_code:
                    i.rate = x.rate
                    i.amount = x.amount
@frappe.whitelist()
def validate(doc, method=None):
    if doc.quotation:
        rate = frappe.db.sql(""" select  a.item_code,a.rate,a.amount
                                                                       from `tabQuotation Item` a join `tabQuotation` b
                                                                       on a.parent = b.name
                                                                       where b.name = '{name}'
                                                                   """.format(name=doc.quotation), as_dict=1)
        for x in rate:
            for i in doc.items:
                if x.item_code == i.item_code:
                    i.rate = x.rate
                    i.amount = x.amount
@frappe.whitelist()
def on_submit(doc, method=None):
    pass
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
