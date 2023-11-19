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
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    if doc.custom_target_warehouse:
        new_doc = frappe.get_doc(
            {
                "doctype": "Stock Entry",
                "stock_entry_type": "تحويل من مخزن الوارد",
                "posting_date": doc.posting_date,
                "fiscal_year": frappe.db.get_single_value("System Defaults", "default_fiscal_year"),
                "from_warehouse": "مخزن الوارد - V",
                "to_warehouse": doc.custom_target_warehouse,
            }
        )
        for row in doc.items:
            table = new_doc.append("items", {})
            table.item_code = row.item_code
            table.item_name = row.item_name
            table.item_group = row.item_group
            table.description = row.description
            table.qty = row.qty
            table.uom = row.uom
        new_doc.insert(ignore_permissions=True)
        frappe.msgprint(" تم إنشاء حركة تحويل من مخزن الوارد إلى مخزن " + str(doc.custom_target_warehouse) + " تلقائيا ... برجاء مراجعة الحركة وتسجيلها ")

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
