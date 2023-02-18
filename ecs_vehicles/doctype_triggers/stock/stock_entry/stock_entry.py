from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass

@frappe.whitelist()
def get_item_table(doc, method=None):
    # frappe.throw(str(doc))
    # doc.items = []
    item = frappe.db.sql(""" select a.item_group,
                                    a.maintenance_type,
                                    b.name,
                                    b.vehicles,
                                    b.vehicle_no,
                                    b.vehicle_brand,
                                    b.entity_name,
                                    b.vehicle_model,
                                    a.item_code,
                                    a.item_name,
                                    a.default_unit_of_measure,
                                    a.brand,
                                    a.description,
                                    a.qty
                            from `tabMaintenance Order Item` a join `tabMaintenance Order` b
                            on a.parent = b.name
                            where b.name = '{maintenance_order}'
                        """.format(maintenance_order=doc), as_dict=1)
    return item
   
    # for x in item:
    #     table = doc.append("items", {})
    #     table.item_group = x.item_group
    #     table.item_code = x.item_code
    #     table.item_name = x.item_name
    #     table.uom = x.default_unit_of_measure
    #     table.qty = x.qty
    #     table.description = x.description

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
