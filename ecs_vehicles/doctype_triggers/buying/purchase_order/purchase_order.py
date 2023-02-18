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
	
    items = frappe.db.sql(""" select a.item_group,
                                    a.maintenance_type,
                                    a.item_code,
                                    b.name,
                                    b.supplier,
                                    a.item_name,
                                    a.description,
                                    a.default_unit_of_measure,
                                    a.brand,
                                    a.qty,
                                    a.rate,
                                    a.amount,
                                    a.vehicles,
                                    a.vehicle_no,
                                    a.vehicle_brand,
                                    a.maintenance_order,
                                    a.entity_name,
                                    a.vehicle_model
                                    
                            from `tabPresentation Note Item` a join `tabPresentation Note` b
                            on a.parent = b.name
                            where b.name = '{presentation_note}'
                        """.format(presentation_note=doc.presentation_note), as_dict=1)
    if not doc.items:
        for x in items:
            table = doc.append("items", {})
            table.item_group = x.item_group
            table.maintenance_type = x.maintenance_type
            table.item_code = x.item_code
            table.item_name = x.item_name
            table.description = x.description
            table.description = x.description
            table.uom = x.default_unit_of_measure
            table.stock_uom = x.default_unit_of_measure
            table.brand = x.brand
            table.qty = x.qty
            table.rate = x.rate
            table.amount = x.amount
            table.vehicles = x.vehicles
            table.vehicle_no = x.vehicle_no
            table.vehicle_brand = x.vehicle_brand
            table.maintenance_order = x.maintenance_order
            table.entity_name = x.entity_name
            table.vehicle_model = x.vehicle_model

            doc.supplier = x.supplier
@frappe.whitelist()
def validate(doc, method=None):
    pass
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
