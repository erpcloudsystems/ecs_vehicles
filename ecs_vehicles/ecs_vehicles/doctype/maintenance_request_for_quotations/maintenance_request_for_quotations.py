# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceRequestforQuotations(Document):
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
		if not doc.supplier :
			frappe.throw("برجاء تحديد المورد المقبول")
		if doc.total == 0:
			frappe.throw("برجاء تسجيل الاجمالي النهائي")
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
	def create_Presentation(doc, method=None):
		new_doc = frappe.get_doc({
		"doctype": "Presentation Note Out",
		"maintenance_request_for_quotations" : doc.name,
		"supplier" : doc.supplier,
		"total" : doc.total,
		"maintenance_order" : doc.maintenance_order,
        	                })
		for x in doc.request_for_quotations_item:
			table = new_doc.append("presentation_note_out_item", {})
			table.item_group = x.item_group
			table.maintenance_type = x.maintenance_type
			table.item_code = x.item_code
			table.item_name = x.item_name
			table.default_unit_of_measure = x.default_unit_of_measure
			table.brand = x.brand
			table.qty = x.qty
			table.description = x.description
			table.rate = 0
			table.amount = 0
			
		new_doc.insert(ignore_permissions=True)
		doc.presentation_note_out = new_doc.name
		frappe.msgprint(str(new_doc.name) + " تم إنشاء مذكرة رقم ")
	
	@frappe.whitelist()
	def get_data(doc, method=None):
		doc.request_for_quotations_item = []
		items = frappe.db.sql(""" select a.item_group,
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
								and a.maintenance_method = "إصلاح خارجي"
							""".format(maintenance_order=doc.maintenance_order), as_dict=1)
		
		for x in items:
				table = doc.append("request_for_quotations_item", {})
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
				table.entity_name = x.entity_name
				table.maintenance_order = x.name
				table.vehicle_brand = x.vehicle_brand
				table.vehicle_no = x.vehicle_no
				table.vehicles = x.vehicles
				table.vehicle_model = x.vehicle_model
		
		
		# if not doc.request_for_quotations_item:
			
		# 	for x in items:
		# 		table = doc.append("request_for_quotations_item", {})
		# 		table.item_group = x.item_group
		# 		table.maintenance_type = x.maintenance_type
		# 		table.item_code = x.item_code
		# 		table.item_name = x.item_name
		# 		table.default_unit_of_measure = x.default_unit_of_measure
		# 		table.brand = x.brand
		# 		table.qty = x.qty
		# 		table.description = x.description
		# 		table.rat = 0
		# 		table.amount = 0
		# 		table.entity_name = x.entity_name
		# 		table.maintenance_order = x.name
		# 		table.vehicle_brand = x.vehicle_brand
		# 		table.vehicle_no = x.vehicle_no
		# 		table.vehicles = x.vehicles
		# 		table.vehicle_model = x.vehicle_model
		# if  doc.request_for_quotations_item:
		# 	for a in doc.request_for_quotations_item:
		# 		if doc.maintenance_order == a.maintenance_order:
		# 			pass
		# 		else:
		# 			for s in items:
		# 				table = doc.append("request_for_quotations_item", {})
		# 				table.item_group = s.item_group
		# 				table.maintenance_type = s.maintenance_type
		# 				table.item_code = s.item_code
		# 				table.item_name = s.item_name
		# 				table.default_unit_of_measure = s.default_unit_of_measure
		# 				table.brand = s.brand
		# 				table.qty = s.qty
		# 				table.description = s.description
		# 				table.rat = 0
		# 				table.amount = 0
		# 				table.entity_name = s.entity_name
		# 				table.maintenance_order = s.name
		# 				table.vehicle_brand = s.vehicle_brand
		# 				table.vehicle_no = s.vehicle_no
		# 				table.vehicles = s.vehicles
		# 				table.vehicle_model = s.vehicle_model
		# #doc.maintenance_order = ""
