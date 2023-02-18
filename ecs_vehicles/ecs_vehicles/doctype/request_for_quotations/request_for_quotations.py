# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RequestforQuotations(Document):
	@frappe.whitelist()
	def get_data(doc, method=None):
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
							""".format(maintenance_order=doc.maintenance_order), as_dict=1)
		# if not doc.request_for_quotations_item:
		for row in items:
			table = doc.append("request_for_quotations_item", {})
			table.item_group = row.item_group
			table.maintenance_type = row.maintenance_type
			table.item_code = row.item_code
			table.item_name = row.item_name
			table.default_unit_of_measure = row.default_unit_of_measure
			table.brand = row.brand
			table.qty = row.qty
			table.description = row.description
			table.rat = 0
			table.amount = 0
			table.entity_name = row.entity_name
			table.maintenance_order = row.name
			table.vehicle_brand = row.vehicle_brand
			table.vehicle_no = row.vehicle_no
			table.vehicles = row.vehicles
			table.vehicle_model = row.vehicle_model

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
		
	@frappe.whitelist()
	def validate(doc, method=None):
		total1 =0
		total2 =0
		for d in doc.request_for_quotations_item:
			total = d.rate * d.qty
			d.amount = total
			total2 += d.amount
			doc.total = total2