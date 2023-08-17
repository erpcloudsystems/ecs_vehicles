# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PresentationNoteOut(Document):
	@frappe.whitelist()
	def create_job_order(doc, method=None):
		new_doc = frappe.get_doc({
		"doctype": "Job Order",
		"presentation_note_out" : doc.name,
		"maintenance_request_for_quotations" : doc.maintenance_request_for_quotations,
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
		"vehicle_style" : doc.vehicle_style,
		"pre_no_type" : doc.pre_no_type,
		"pre_no_type" : doc.pre_no_type,
		"maintenance_entity" : doc.maintenance_entity,
		"maintenance_order" : doc.maintenance_order,
        	                })
		for x in doc.presentation_note_out_item:
			table = new_doc.append("job_order_item", {})
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
		doc.job_order = new_doc.name
		#frappe.msgprint(new_doc.name + " تم إنشاء امر شغل رقم ")

	@frappe.whitelist()
	def validate(self):
		if self.jop_number:
			mozakira_no_list = frappe.db.sql(""" Select jop_number, name from `tabPresentation Note Out`
			where docstatus != 2 and fiscal_year = '{fiscal_year}' and name != '{name}' """.format(name=self.name, fiscal_year=self.fiscal_year), as_dict=1)

			for x in mozakira_no_list:
				if self.jop_number == x.jop_number:
					frappe.throw(
						" لا يمكن تكرار رقم المذكرة " + str(x.jop_number) + " أكثر من مرة قي نفس السنة المالية حيث أنه مستخدم في المذكرة " + x.name)

		
