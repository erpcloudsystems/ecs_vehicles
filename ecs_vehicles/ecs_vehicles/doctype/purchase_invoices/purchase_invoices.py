# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PurchaseInvoices(Document):
	@frappe.whitelist()
	def get_data(doc, method=None):
		
		items = frappe.db.sql(""" select a.item_group,
										a.maintenance_type,
										b.name,
										b.jop_number,
										b.supplier,
										b.total,
										a.item_code,
										a.item_name,
										a.default_unit_of_measure,
										a.brand,
										a.description,
										a.qty
                                   from `tabJob Order Item` a join `tabJob Order` b
                                   on a.parent = b.name
                                   where b.name = '{maintenance_order}'
                               """.format(maintenance_order=doc.maintenance_order), as_dict=1)
		if not doc.purchase_invoices_table:
			for x in items:
				doc.total = x.total
				doc.supplier = x.supplier
				doc.jop_number = x.jop_number
				
				table = doc.append("purchase_invoices_table", {})
				table.item_group = x.item_group
				table.maintenance_type = x.maintenance_type
				table.item_code = x.item_code
				table.item_name = x.item_name
				table.default_unit_of_measure = x.default_unit_of_measure
				table.brand = x.brand
				table.qty = x.qty
				table.description = x.description
				table.rat = 1
				table.amount = 1

		#doc.save()
	@frappe.whitelist()
	def validate(doc, method=None):
		pass

