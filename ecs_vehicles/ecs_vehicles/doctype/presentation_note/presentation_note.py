# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class PresentationNote(Document):
	@frappe.whitelist()
	def get_data(doc, method=None):
		items = frappe.db.sql(""" select a.item_group,
										a.maintenance_type,
										a.item_code,
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
										a.vehicle_model,
										b.supplier
										
								from `tabRequest for Quotations Item` a join `tabRequest for Quotations` b
								on a.parent = b.name
								where b.name = '{request_for_quotations}'
							""".format(request_for_quotations=doc.request_for_quotations), as_dict=1)
		
		for x in items:
			table = doc.append("presentation_note_item", {})
			table.item_group = x.item_group
			table.maintenance_type = x.maintenance_type
			table.item_code = x.item_code
			table.item_name = x.item_name
			table.description = x.description
			table.description = x.description
			table.default_unit_of_measure = x.default_unit_of_measure
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
		total1 =0
		total2 =0
		for d in doc.presentation_note_item:
			total = d.rate * d.qty
			d.amount = total
			total2 += d.amount
			doc.total = total2

	@frappe.whitelist()
	def on_submit(doc, method=None):
		if not doc.supplier:
			frappe.throw(" برجاء تحديد المورد المقبول ")

	@frappe.whitelist()
	def add_po(doc, method=None):
		today = date.today()
		new_doc = frappe.get_doc({
        "doctype": "Purchase Order",
        "posting_date": today,
        "schedule_date": today,
        "supplier": doc.supplier,
        "presentation_note": doc.name,
		  })
		items = frappe.db.sql(""" select a.item_group,
										a.maintenance_type,
										a.item_code,
										b.name,
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
								where b.name = '{request_for_quotations}'
							""".format(request_for_quotations=doc.request_for_quotations), as_dict=1)
		
		for x in items:
			table = new_doc.append("items", {})
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

		new_doc.insert(ignore_permissions=True)
		frappe.msgprint("  تم إنشاء امر توريد برقم رقم " + new_doc.name)
    