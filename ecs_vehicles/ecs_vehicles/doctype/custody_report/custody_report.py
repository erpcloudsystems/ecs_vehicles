# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

from time import sleep
import frappe
from frappe.model.document import Document
from frappe.utils import flt, rounded, add_months, nowdate, getdate, now_datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
import datetime


@frappe.whitelist()
def get_last_sarf_detail(vehicles,item_code):
	last_sarf_date = frappe.db.sql(""" select
												stock_ledger.action_date, stock_ledger.part_qty
												from `tabKarta Ledger Entry` stock_ledger 
												where stock_ledger.vic_serial = '{vehicles}'
												and stock_ledger.part_universal_code = '{item_code}'
												and stock_ledger.del_flag = "0"
												order by stock_ledger.action_date desc limit 1
												""".format(vehicles=vehicles, item_code=item_code), as_dict=1)
	try:
		return last_sarf_date[0].action_date, last_sarf_date[0].part_qty 
	except:
		return "لم يسبق"
		
class CustodyReport(Document):
	@frappe.whitelist()
	def add_maintenance_order(doc, method=None):
		# job_order_list = frappe.db.get_list("Job Order", filters={"vehicles": doc.vehicles, "fiscal_year": doc.fiscal_year}, fields={"name", "jop_number"})
		# if job_order_list:
		# 	for y in job_order_list:
		# 		purchase_invoices_list = frappe.db.get_list("Purchase Invoices", filters={"vehicles": doc.vehicles, "jop_order": y.name}, fields={"name"})
		# 		if not purchase_invoices_list and doc.pass_order == 0:
		# 			frappe.throw(" لا يجوز إضافة إجراء إصلاح خارجي للمركبة وذلك لوجود أمر شغل ساري رقم " + str(y.jop_number) + " لعام " + str(doc.fiscal_year))

		items_count = frappe.db.count('Custody Report Item', {'parent':doc.name ,'include_in_maintenance_order': 1})
		if items_count == 0:
			frappe.throw(" برجاء تحديد الأصناف المطلوب عمل لها إجراء إصلاح ")
		items_count2 = frappe.db.count('Custody Report Item', {'parent':doc.name ,'include_in_maintenance_order': 1, "maintenance_order": None})
		if items_count2 == 0:
			frappe.throw("لا يوجد اصناف لم تحصل على إجراء إصلاح")

		new_doc = frappe.get_doc({
			"doctype": "Maintenance Order",
			"fis_year" : doc.fiscal_year,
			"driver" : doc.driver,
			"ezn_no" : doc.ezn_no,
			"car_in_date" : doc.date,
			"vehicles" : doc.vehicles,
			"vehicle_no" : doc.vehicle_no,
			"vehicle_brand" : doc.vehicle_brand,
			"group_shape" : doc.group_shape,
			"chassis_no" : doc.chassis_no,
			"entity_name" : doc.entity_name,
			"possession_type" : doc.possession_type,
			"vehicle_shape" : doc.vehicle_shape,
			"maintenance_entity" : doc.entity_name,
			"vehicle_style" : doc.vehicle_style,
			"custody_report" : doc.name,
		})

		for x in doc.custody_report_item:
			if x.include_in_maintenance_order and not x.maintenance_order:
				table = new_doc.append("maintenance_order_item", {})
				table.item_group = x.item_group
				table.item_code = x.item_code
				table.item_name = x.item_name
				table.default_unit_of_measure = x.default_unit_of_measure
				table.brand = x.brand
				table.last_issue_detail = x.last_issue_detail
				table.description = x.description
				table.namozg_no2 = x.namozag_no
				table.custody_report = doc.name
				table.custody_report_item = x.name

		new_doc.insert(ignore_permissions=True)
		frappe.msgprint(" تم إنشاء إذن إصلاح رقم <a href=/app/maintenance-order/{0}>{1}</a>".format(new_doc.name,new_doc.name))
		doc.reload()

	@frappe.whitelist()
	def wheels_update_table(doc, method=None):
		today = date.today()
		past_date = add_months(today, -32)
		last_sarf_date = frappe.db.sql(""" select  item.item_code, item.item_name, item.item_group, item.description,
												karta_ledger.action_date, karta_ledger.part_qty
												from `tabKarta Ledger Entry` karta_ledger
												JOIN  `tabItem` item ON item.item_code = part_universal_code
												where karta_ledger.vic_serial = '{vehicles}'
												and item.item_group = '{item_group}'
												and karta_ledger.del_flag = "0"
												and karta_ledger.action_date > "{past_date}"
												""".format(vehicles=doc.vehicles, item_group="اطارات خارجية",past_date=past_date), as_dict=1)
		for row in last_sarf_date:
				table = doc.append("custody_report_item", {})
				table.item_code = row.item_code
				table.item_name = row.item_name
				table.item_group = row.item_group
				table.description = row.description
				table.include_in_maintenance_order = 0
				table.namozag_no = "1"
				table.last_issue_detail = row.action_date
				table.last_sarf_qty = row.part_qty


	@frappe.whitelist()
	def battaries_update_table(doc, method=None):
		today = date.today()
		past_date = add_months(today, -32)
		last_sarf_date = frappe.db.sql(""" select 
		 		 								item.item_code, item.item_name, item.item_group, item.description,
												karta_ledger.action_date, karta_ledger.part_qty	
												from `tabKarta Ledger Entry` karta_ledger
												JOIN  `tabItem` item ON item.item_code = part_universal_code
												where karta_ledger.vic_serial = '{vehicles}'
												and item.item_group = '{item_group}'
												and karta_ledger.del_flag = "0"
												and karta_ledger.action_date > "{past_date}"
												""".format(vehicles=doc.vehicles, item_group="البطاريات",past_date=past_date), as_dict=1)
		for row in last_sarf_date:
				table = doc.append("custody_report_item", {})
				table.item_code = row.item_code
				table.item_name = row.item_name
				table.item_group = row.item_group
				table.description = row.description
				table.include_in_maintenance_order = 0
				table.namozag_no = "1"
				table.last_issue_detail = row.action_date
				table.last_sarf_qty = row.part_qty

	@frappe.whitelist()
	def update_table(doc, method=None):
		if doc.select_type == "مجموعات متوافقة":
			# last_sarf_date = frappe._dict(frappe.db.sql(""" select CONCAT(karta_ledger.part_universal_code, karta_ledger.vic_serial),
		 	# 													 CONCAT(karta_ledger.action_date,"$", karta_ledger.part_qty)
			# 													from `tabKarta Ledger Entry` karta_ledger 
			# 													where karta_ledger.del_flag = "0"
			# 													order by karta_ledger.action_date
			# 								"""))
			custody_report_items = []
			first_list = frappe.db.sql(""" select  a.item_code, c.item_name, c.item_group, c.description
											from `tabProduct Bundle Item` a join `tabProduct Bundle` b 
											on a.parent = b.name join `tabItem` c on a.item_code = c.name
											where b.new_item_code = '{new_item_code}'
											""".format(new_item_code=doc.bundle), as_dict=1)

			if not custody_report_items:
				for z in first_list:
					table = doc.append("custody_report_item", {})
					table.item_code = z.item_code
					table.item_name = z.item_name
					table.item_group = z.item_group
					table.description = z.description
					table.include_in_maintenance_order = 0
					table.namozag_no = "1"
				
			
		# for d in doc.custody_report_item:
		# 	d.last_issue_detail = "لم يتم الصرف من قبل"
		# 	last_maint = frappe.db.sql(""" select  a.item_code,b.posting_date
		# 								from `tabStock Entry Detail` a join `tabStock Entry` b
		# 								on a.parent = b.name
		# 								where b.vehicles = '{vehicles}'
		# 								and a.item_code = '{item_code}'
		# 								order by b.posting_date asc
		# 								""".format(vehicles=doc.vehicles,item_code=d.item_code), as_dict=1)

		# 	for x in last_maint:
		# 		if x.item_code:
		# 			d.last_issue_detail = x.posting_date


	@frappe.whitelist()
	def validate(doc, method=None):
		custody_report_list = frappe.db.sql(""" Select ezn_no, name from `tabCustody Report` 
		where docstatus = 1 and fiscal_year = '{fiscal_year}' and name != '{name}' """.format(name=doc.name, fiscal_year=doc.fiscal_year), as_dict=1)

		for x in custody_report_list:
			if doc.ezn_no == x.ezn_no:
				frappe.throw(
					" لا يمكن إستخدام رقم الإذن " + str(
						x.ezn_no) + " أكثر من مرة حيث أنه مستخدم في كشف العهدة " + x.name)

		today = date.today()
		past_date = add_months(today, -24)
		

		for item in doc.custody_report_item:
			item.last_issue_detail = "لم يسبق"
			last_sarf_date = frappe.db.sql(""" select
												stock_ledger.action_date, stock_ledger.part_qty
												from `tabKarta Ledger Entry` stock_ledger 
												where stock_ledger.vic_serial = '{vehicles}'
												and stock_ledger.part_universal_code = '{item_code}'
												and stock_ledger.del_flag = "0"
												order by stock_ledger.action_date desc limit 1
												""".format(vehicles=doc.vehicles, item_code=item.item_code), as_dict=1)
			
			
			try:
					
				item.last_sarf_qty = last_sarf_date[0].part_qty
				item.last_issue_detail = last_sarf_date[0].action_date
			except:
				item.last_issue_detail = "لم يسبق"



	@frappe.whitelist()
	def on_update_after_submit(doc, method=None):
		# today = date.today()
		# past_date = add_months(today, -24)
		# if doc.select_type == "مجموعات فرعية":
		# 	if doc.group_type == "البطاريات" and not doc.custody_report_item:
		# 		battery_list = frappe.db.sql(""" select b.name, b.date, b.ezn_no, a.item_code, a.item_name, a.item_group, a.description
		# 								from `tabMaintenance Order Item` a join `tabMaintenance Order` b
		# 								on a.parent = b.name
		# 								where b.vehicles = '{vehicles}'
		# 								and a.item_group = "البطاريات"
		# 								and b.date >= '{past_date}'
		# 								order by a.item_code desc, b.date desc
		# 								""".format(vehicles=doc.vehicles, past_date=past_date), as_dict=1)
		
		# 		doc.custody_report_item = []
		# 		for x in battery_list:
		# 			table = doc.append("custody_report_item", {})
		# 			table.item_code = x.item_code
		# 			table.item_name = x.item_name
		# 			table.item_group = x.item_group
		# 			table.description = x.description
		# 			table.last_issue_detail = x.date
		# 			table.reference_doc = x.name
		# 			table.ezn_no = x.ezn_no
		# 			table.save()
		
		# 	if doc.group_type == "اطارات خارجية" and not doc.custody_report_item:
		# 		wheel_list = frappe.db.sql(""" select b.name, b.date, b.ezn_no, a.item_code, a.item_name, a.item_group, a.description
		# 								from `tabMaintenance Order Item` a join `tabMaintenance Order` b
		# 								on a.parent = b.name
		# 								where b.vehicles = '{vehicles}'
		# 								and a.item_group = "اطارات خارجية"
		# 								and b.date >= '{past_date}'
		# 								order by a.item_code desc, b.date desc
		# 								""".format(vehicles=doc.vehicles, past_date=past_date), as_dict=1)
		
		# 		doc.custody_report_item = []
		# 		for x in wheel_list:
		# 			table = doc.append("custody_report_item", {})
		# 			table.item_code = x.item_code
		# 			table.item_name = x.item_name
		# 			table.item_group = x.item_group
		# 			table.description = x.description
		# 			table.last_issue_detail = x.date
		# 			table.reference_doc = x.name
		# 			table.ezn_no = x.ezn_no
		# 			table.save()

		for item in doc.custody_report_item:
			item.last_issue_detail = "لم يسبق"
			last_sarf_date = frappe.db.sql(""" select
												stock_ledger.action_date, stock_ledger.part_qty
												from `tabKarta Ledger Entry` stock_ledger 
												where stock_ledger.vic_serial = '{vehicles}'
												and stock_ledger.part_universal_code = '{item_code}'
												and stock_ledger.del_flag = "0"
												order by stock_ledger.action_date desc limit 1
												""".format(vehicles=doc.vehicles, item_code=item.item_code), as_dict=1)
			
			
			try:
					
				item.last_sarf_qty = last_sarf_date[0].part_qty
				item.last_issue_detail = last_sarf_date[0].action_date
			except:
				item.last_issue_detail = "لم يسبق"