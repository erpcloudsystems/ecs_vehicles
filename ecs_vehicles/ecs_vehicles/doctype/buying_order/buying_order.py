# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils import in_words

class BuyingOrder(Document):

	@frappe.whitelist()
	def add_purchase_order(doc, method=None):
		today = date.today()
		new_doc = frappe.get_doc({
		"doctype": "Purchase Order",
		"transaction_date": today,
		"schedule_date": today,
		"supplier": doc.supplier,
		"supplier": doc.supplier,
		"buying_order": doc.name,
		})
		
		is_items = frappe.db.sql(""" select a.item, a.idx, a.item_name, a.description, a.quantity, a.uom, a.rate, a.amount, a.warehouse
																			from `tabBuying Order Items` a join `tabBuying Order` b
																			on a.parent = b.name
																			where b.name = '{name}'
																		""".format(name=doc.name), as_dict=1)
		for c in is_items:
			items = new_doc.append("items", {})
			items.idx = c.idx
			items.item_code = c.item
			items.item_name = c.item_name
			items.description = c.description
			items.qty = c.quantity
			items.uom = c.uom
			items.rate = c.rate
			items.amount = c.amount
			items.stock_uom = c.uom
			items.warehouse = c.warehouse
			items.conversion_factor = 1
			items.expected_delivery_date = today
		new_doc.insert(ignore_permissions=True, ignore_links=True, ignore_mandatory=True )

		frappe.msgprint("  تم إنشاء أمر توريد رقم " + "<a href=/app/purchase-order/" + new_doc.name + ">" + new_doc.name + "</a>")  
		doc.purchase_order = new_doc.name
		doc.save()
  
	@frappe.whitelist()
	def add_financial_approval(doc, method=None):
		today = date.today()
		new_doc = frappe.get_doc({
		"doctype": "Financial Approval",
		"creation_date": today,
		"buying_order":doc.name,
		
		})
		
		items = frappe.db.sql(""" select a.item, a.idx, a.item_name, a.description, a.quantity, a.uom, a.rate, a.amount, a.warehouse
																			from `tabBuying Order Items` a join `tabBuying Order` b
																			on a.parent = b.name
																			where b.name = '{name}'
																		""".format(name=doc.name), as_dict=1)
		for c in items:
			items = new_doc.append("buying_order_items", {})
			items.idx = c.idx
			items.item = c.item
			items.item_name = c.item_name
			items.description = c.description
			items.quantity = c.quantity
			items.uom = c.uom
			items.rate = c.rate
			items.amount = c.amount
			items.uom = c.uom
			items.warehouse = c.warehouse
		new_doc.insert(ignore_permissions=True)
		frappe.msgprint("  تم إنشاء ارتباط مالي رقم " + new_doc.name)
		doc.financial_approval = new_doc.name
		doc.financial_approval_status = new_doc.workflow_state
		doc.save()
	
	@frappe.whitelist()
	def add_presentation_note(doc, method=None):
		today = date.today()
		new_doc = frappe.get_doc({
		"doctype": "Presentation Notes",
		"creation_date": today,
		"buying_order":doc.name,
		
		})
			
		new_doc.insert(ignore_permissions=True)
		frappe.msgprint("  تم إنشاء مذكرة طرح رقم " + str(new_doc.name))
		doc.presentation_note = new_doc.name
		doc.presentation_note_status = new_doc.workflow_state
		doc.save()
  
	@frappe.whitelist()
	def add_technical_clearance(doc, method=None):
		today = date.today()
		new_doc = frappe.get_doc({
		"doctype": "Technical Clearance",
		"date": today,
		"buying_order":doc.name,
		
		})
			
		new_doc.insert(ignore_permissions=True)
		frappe.msgprint("  تم إنشاء لجنة فض فني رقم " + new_doc.name)
		doc.technical_clearance = new_doc.name
		doc.technical_clearance_status = new_doc.workflow_state
		doc.save()
	
	@frappe.whitelist()
	def add_financial_clearance(doc, method=None):
		today = date.today()
		new_doc = frappe.get_doc({
		"doctype": "Financial Clearance",
		"date": today,
		"buying_order":doc.name,
		
		})
			
		new_doc.insert(ignore_permissions=True)
		frappe.msgprint("  تم إنشاء لجنة فض مالي رقم " + new_doc.name)
		doc.financial_clearance = new_doc.name
		doc.financial_clearance_status = new_doc.workflow_state 
		doc.save()

	@frappe.whitelist()
	def validate(doc, method=None):
		total = 0
		total2 = 0
		total4 = 0
		for x in doc.buying_order_items :
			total4 = x.rate * x.quantity
			x.amount = total4
			total += x.amount
			total2 += x.quantity
		doc.total_quantity = total2
		doc.total_amount = total