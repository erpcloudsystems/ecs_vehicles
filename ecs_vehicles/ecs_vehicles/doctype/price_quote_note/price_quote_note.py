# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PriceQuoteNote(Document):
	@frappe.whitelist()
	def validate(doc, method=None):
		amount = 0
		doc.total = 0
		for d in doc.price_quote_note_item:
			amount = d.rate * d.qty
			d.amount = amount
		doc.total += d.amount
