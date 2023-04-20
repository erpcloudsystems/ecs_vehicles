from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import date


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
    total_rate = 0
    total_qty = 0
    for x in doc.items:
        total_qty += x.qty
        total_rate += x.rate
    doc.total_quantity = total_qty
    doc.total_amount = total_rate


@frappe.whitelist()
def on_submit(doc, method=None):
    today = date.today()
    new_doc = frappe.get_doc({
        "doctype": "Buying Order",
        "transaction_date": today,
        "material_request": doc.name,
        "presentation_style": "أتفاق مباشر",

    })

    items = frappe.db.sql(""" select a.item_code, a.idx, a.item_name, a.description, a.qty, a.uom, a.rate, a.amount, a.warehouse
                                                                        from `tabMaterial Request Item` a join `tabMaterial Request` b
                                                                        on a.parent = b.name
                                                                        where b.name = '{name}'
                                                                    """.format(name=doc.name), as_dict=1)
    for c in items:
        items = new_doc.append("buying_order_items", {})
        items.idx = c.idx
        items.item = c.item_code
        items.item_name = c.item_name
        items.description = c.description
        items.quantity = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.amount = c.amount
        items.warehouse = c.warehouse

    new_doc.insert(ignore_permissions=True)
    # frappe.msgprint("  تم إنشاء امر شراء رقم " + new_doc.name)
    doc.buying_order = new_doc.name
    doc.save()


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


@frappe.whitelist()
def add_buying_order(doc, method=None):
    today = date.today()
    new_doc = frappe.get_doc({
        "doctype": "Buying Order",
        "transaction_date": today,
        "material_request": doc.name,
        "presentation_style": "أتفاق مباشر",
    })
    items = frappe.db.sql(""" select a.item_code, a.idx, a.item_name, a.description, a.qty, a.uom, a.rate, a.amount
                                                                        from `tabMaterial Request Item` a join `tabMaterial Request` b
                                                                        on a.parent = b.name
                                                                        where b.name = '{name}'
                                                                    """.format(name=doc.name), as_dict=1)
    for c in items:
        items = new_doc.append("buying_order_items", {})
        items.idx = c.idx
        items.item = c.item_code
        items.item_name = c.item_name
        items.description = c.description
        items.quantity = c.qty
        items.uom = c.uom
        items.rate = c.rate
        items.amount = c.amount

    new_doc.insert(ignore_permissions=True)
