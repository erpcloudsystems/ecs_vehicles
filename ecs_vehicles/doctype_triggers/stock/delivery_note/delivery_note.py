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
    if doc.get_items == 0 and doc.is_bundle == 1:
        doc.items = {}
        bundle_items = frappe.db.sql(""" select a.parent_item, a.idx, a.item_code,a.rate,a.amount,a.description,a.qty
                                                                  from `tabNew Product Bundle Item` a join `tabSales Invoice` b
                                                                  on a.parent = b.name
                                                                  where b.name = '{name}'
                                                              """.format(name=doc.sales_invoice), as_dict=1)

        for y in bundle_items:
            items = doc.append("items", {})
            items.idx = y.idx
            items.item_code = y.item_code
            items.description = y.description
            items.qty = y.qty
            items.rate = y.rate
            items.amount = y.amount
    doc.get_items = 1
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    new_doc = frappe.get_doc({
        "doctype": "Installation Note",
	"delivery_note": doc.name,
        "customer": doc.customer,
        "customer_group": doc.customer_group,
        "territory": doc.territory,
        "customer_address": doc.customer_address,
        "contact_person": doc.contact_person,
	"inst_date": doc.posting_date,
    })
    dn_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.description, a.qty
                                   from `tabDelivery Note Item` a join `tabDelivery Note` b
                                   on a.parent = b.name
                                   where b.name = '{name}'
                               """.format(name=doc.name), as_dict=1)

    for c in dn_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.description = c.description
        items.qty = c.qty
        items.prevdoc_detail_docname = c.name
        items.prevdoc_docname = doc.name
        items.prevdoc_doctype = "Delivery Note"


    new_doc.insert()
    frappe.msgprint(" Installation Note Record " + new_doc.name + " created ")

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
