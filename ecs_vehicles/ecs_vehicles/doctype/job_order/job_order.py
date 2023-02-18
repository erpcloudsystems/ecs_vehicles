# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobOrder(Document):
	@frappe.whitelist()
	def create_invoice(doc, method=None):
		new_doc = frappe.get_doc({
		"doctype": "Purchase Invoices",
		"jop_order" : doc.name,
		"jop_number" : doc.jop_number,
		"supplier" : doc.supplier,
		"jop_number" : doc.jop_number,
		"vehicles" : doc.vehicles,
		"total" : doc.total,
		"vehicle_no" : doc.vehicle_no,
		"vehicle_brand" : doc.vehicle_brand,
		"group_shape" : doc.group_shape,
		"vehicle_model" : doc.vehicle_model,
		"chassis_no" : doc.chassis_no,
		"entity_name" : doc.entity_name,
		"possession_type" : doc.possession_type,
		"vehicle_shape" : doc.vehicle_shape,
		"pre_no_type" : doc.pre_no_type,
		"vehicle_style" : doc.vehicle_style,
		"maintenance_entity" : doc.maintenance_entity,
		"maintenance_order" : doc.maintenance_order,
        	                })
		for x in doc.job_order_item:
			table = new_doc.append("purchase_invoices_table", {})
			table.item_group = x.item_group
			table.maintenance_type = x.maintenance_type
			table.item_code = x.item_code
			table.item_name = x.item_name
			table.default_unit_of_measure = x.default_unit_of_measure
			table.brand = x.brand
			table.qty = x.qty
			table.description = x.description
			table.rat = 0
			table.amount = 0
			
		new_doc.insert(ignore_permissions=True)
		doc.purchase_invoices = new_doc.name
		

	@frappe.whitelist()
	def validate(doc, method=None):
		pass
