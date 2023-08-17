from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import add_to_date, nowdate

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
    po_receipt_date_plus_seven = add_to_date(doc.po_receipt_date, days=7, as_string=True)
    doc.receipt_date = po_receipt_date_plus_seven

    for item in doc.items:
        item.receipt_date = po_receipt_date_plus_seven
   
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    po_receipt_date_plus_seven = add_to_date(doc.po_receipt_date, days=7, as_string=True)

    doc.receipt_date = po_receipt_date_plus_seven
    for item in doc.items:
        item.receipt_date = po_receipt_date_plus_seven
    # doc.save()
    
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
def add_maintenance_invoice(name, method=None):
        doc = frappe.get_doc("Purchase Order", name)
        new_doc = frappe.get_doc({
        "doctype": "Purchase Invoices",
        "year": doc.fiscal_year_purchase,
        "date": nowdate(),
        # "ezn_no": doc.ezn_no,
        # "vehicle_maintenance_process": doc.name,
        # "jop_order" : doc.name,
        # "order_no" : doc.job_order_no,
        "purchase_invoice" : doc.name,
        "order_date": doc.transaction_date,
        # "pre_no_type" : doc.fix_type,
        "supplier" : doc.supplier,
        # "vehicles" : doc.vehicles,
        "total" : doc.grand_total,
        "tawreed_no" : doc.mozakira_no,
        # "vehicle_no" : doc.vehicle_no,
        # "vehicle_brand" : doc.vehicle_brand,
        # "group_shape" : doc.group_shape,
        # "vehicle_model" : doc.vehicle_model,
        # "chassis_no" : doc.chassis_no,
        # "entity_name" : doc.entity_name,
        # "possession_type" : doc.possession_type,
        # "vehicle_shape" : doc.vehicle_shape,
        # "vehicle_style" : doc.vehicle_style,
        # "maintenance_entity" : doc.maintenance_entity,
                            })
        
        for x in doc.items:
            table = new_doc.append("purchase_invoices_table", {})
            table.item_group = x.item_group
            # table.maintenance_type = x.maintenance_type
            # table.dis_cause = x.consumption_type
            table.item_code = x.item_code
            table.item_name = x.item_name
            table.description = x.description
            table.default_unit_of_measure = x.uom
            table.brand = x.brand
            table.part_qty = x.qty
            table.part_price = x.rate
            table.amount = x.amount
            table.vehicles = x.vehicles
            table.entity_name = x.entity_name
            table.vehicle_model = x.vehicle_model
            table.vehicle_brand = x.vehicle_brand
            table.vehicle_no = x.vehicle_no
            table.ezn_no = x.ezn_no
            table.vehicle_maintenance_process = x.vehicle_maintenance_process

            
        new_doc.insert(ignore_permissions=True)
        frappe.msgprint(" تم إنشاء فاتورة صيانة <a href=/app/purchase-invoices/{0}>{1}</a>".format(new_doc.name,new_doc.name))