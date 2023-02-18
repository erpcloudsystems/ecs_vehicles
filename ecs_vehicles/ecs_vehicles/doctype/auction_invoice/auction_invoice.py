# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import in_words

class AuctionInvoice(Document):
	def before_insert(self):
		last_invoice_no = frappe.db.sql(
			""" select max(invoice_number) as max from `tabAuction Invoice` 
				where auction_info = '{auction_info}' 
			""".format(auction_info=self.auction_info), as_dict=1)
		for x in last_invoice_no:
			if not x.max:
				self.invoice_number = 1
			else:
				self.invoice_number = int(x.max) + 1

	def validate(self):
		invoice_no_list = frappe.db.sql(""" Select invoice_number, name from `tabAuction Invoice`
				where docstatus = 1 and auction_info = '{auction_info}' and name != '{name}' """.format(name=self.name, auction_info=self.auction_info), as_dict=1)

		for x in invoice_no_list:
			if self.invoice_number == x.invoice_number:
				frappe.throw(
					" لا يمكن إستخدام رقم الفاتورة " + str(
						x.invoice_number) + " أكثر من مرة حيث أنه مستخدم في الفاتورة " + x.name)

		total_tax = 0
		for x in self.auction_sales_slips:
			total_tax += x.selling_price * x.tax_percent / 100

		self.indication = self.total_price * 5 / 100
		self.business_profits = self.total_price * 2 / 100
		self.tax_amount = total_tax
		self.total_amount = self.total_price + self.indication + self.business_profits + self.tax_amount
		self.outstanding_amount = self.total_amount - self.total_paid_amount
		self.in_words = in_words(self.outstanding_amount)

	def on_submit(self):
		for x in self.auction_sales_slips:
			remarks = " تم بيع المركبة بمزاد رقم " + self.auction_info
			value = "بيعت بالمزاد"
			record_name = str(self.name) + str(x.vehicle)

			frappe.db.sql(""" UPDATE `tabVehicles` set vehicle_status = "بيعت بالمزاد" where name = '{name}' 
						  """.format(name=x.vehicle))

			frappe.db.sql(""" INSERT INTO `tabVehicle Status Logs`
			                                        (date, value, remarks, edited_by, parent, parentfield, parenttype, name, idx)
			                                VALUES ('{date}', '{value}', '{remarks}', '{edited_by}', '{parent}', '{parentfield}', '{parenttype}', '{record_name}', '{idx}')
			                              """.format(date=self.auction_date, remarks=remarks,
													 value=value, edited_by=frappe.session.user,
													 parenttype="Vehicles", parent=x.vehicle,
													 parentfield="status_table", record_name=record_name,idx=10000))


	def on_cancel(self):
		for x in self.auction_sales_slips:
			frappe.db.sql(""" UPDATE `tabVehicles` set vehicle_status = "تحت البيع بالمزاد" where name = '{name}' 
						  """.format(name=x.vehicle))

			frappe.db.sql(""" DELETE FROM `tabVehicle Status Logs` where parent = '{parent}' and value = '{value}'
			 """.format(value="بيعت بالمزاد", parent=x.vehicle))
