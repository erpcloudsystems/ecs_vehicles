# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, rounded, add_months, nowdate, getdate, now_datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
import datetime


@frappe.whitelist()
def add_maintenance_order(doc, method=None):

		# doc = frappe.get_doc("Custody Report", name)
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
			table = new_doc.append("maintenance_order_item", {})
			table.item_group = x.item_group
			table.item_code = x.item_code
			table.item_name = x.item_name
			table.default_unit_of_measure = x.default_unit_of_measure
			table.brand = x.brand
			table.last_issue_detail = x.last_issue_detail

			table.description = x.description
		new_doc.insert(ignore_permissions=True)
		cur_doc = frappe.get_doc("Custody Report", doc.name)
		cur_doc.maintenance_order = new_doc.name

# @frappe.whitelist()
# def wheels_update_table(doc):
# 	from datetime import datetime
# 	doc.custody_report_item = []
# 	first_list = frappe.db.sql(""" select  a.last_issue_detail, b.item_name, b.item_group, b.description, b.item_code
# 											from `tabCustody Report Item` a join `tabitem` b 
# 											on a.item_code = b.name 
# 											where b.item_group = '{last_issue_detail}'
# 											and a.last_issue_detail is not NULL
# 											AND a.last_issue_detail !="لم يتم الصرف من قبل"
# 											AND a.last_issue_detail != ""
# 											""".format( last_issue_detail= "اطارات خارجية"), as_dict=1)
# 	list_of_dates = []
# 	list_of_items = {}
	
# 	frappe.msgprint("ss")
# 	for row in first_list:
# 		# counter +=1
# 		# if row.last_issue_detail != "لم يتم الصرف من قبل" and row.last_issue_detail != "" and  row.last_issue_detail != None:
# 		# 	list_of_items[row.item_code]
# 		# 	list_of_dates.append(datetime.strptime(row.last_issue_detail, "%y/%m/%d"))
	
# 			table = doc.append("custody_report_item", {})
# 			table.item_code = row.item_code
# 			table.item_name = row.item_name
# 			table.item_group = row.item_group
# 			table.description = row.description
# 			table.last_issue_detail = row.last_issue_detail
class CustodyReport(Document):
	
	@frappe.whitelist()
	def add_maintenance_order(doc, method=None):

		# doc = frappe.get_doc("Custody Report", name)
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
			table = new_doc.append("maintenance_order_item", {})
			table.item_group = x.item_group
			table.item_code = x.item_code
			table.item_name = x.item_name
			table.default_unit_of_measure = x.default_unit_of_measure
			table.brand = x.brand
			table.last_issue_detail = x.last_issue_detail

			table.description = x.description
		new_doc.insert(ignore_permissions=True)
		cur_doc = frappe.get_doc("Custody Report", doc.name)
		cur_doc.maintenance_order = new_doc.name
		#frappe.msgprint(" تم إنشاء إذن إصلاح رقم <a href=/app/maintenance-order/ "+ new_doc.name>str(new_doc.name)+"</a> ")
		doc.save()

	@frappe.whitelist()
	def wheels_update_table(doc, method=None):

		etarat_items = frappe.db.sql("""
			SELECT name, item_code
			FROM `tabItem`
			where item_group = "اطارات خارجية"
		""", as_dict=1)
		doc.custody_report_item = []
		items = {}
		list_of_dates = []
		for row in etarat_items:
			first_list = frappe.db.sql(""" select  `tabCustody Report`.name, a.last_issue_detail, 
													b.item_name, b.item_group, b.description, b.item_code
													from `tabCustody Report Item` a
													join `tabItem` b on a.item_code = b.name 
													JOIN `tabCustody Report` ON a.parent = `tabCustody Report`.name
													WHERE a.item_code = "{item_code}" 
													and a.last_issue_detail is not NULL
													and `tabCustody Report`.vehicles ="{vehicle}"
													AND a.last_issue_detail !="لم يتم الصرف من قبل"
													AND a.last_issue_detail !="لم يسبق الصرف"
													AND a.last_issue_detail != ""
													AND `tabCustody Report`.date >"2015-06-06"
													AND `tabCustody Report`.docstatus =1
													ORDER BY `tabCustody Report`.date
													""".format( last_issue_detail= "اطارات خارجية",vehicle=doc.vehicles, item_code=row.item_code), as_dict=1)
			if first_list:
				list_of_dates.extend(first_list)
		for row in list_of_dates:
			if not items.get(row.item_code):
				items[row.item_code] = row.item_name
				table = doc.append("custody_report_item", {})
				table.item_code = row.item_code
				table.item_name = row.item_name
				table.item_group = row.item_group
				table.description = row.description
				table.last_issue_detail = row.last_issue_detail
	@frappe.whitelist()
	def battaries_update_table(doc, method=None):
		
		etarat_items = frappe.db.sql("""
			SELECT name, item_code
			FROM `tabItem`
			where item_group = "البطاريات"
		""", as_dict=1)
		doc.custody_report_item = []
		items = {}
		list_of_dates = []
		for row in etarat_items:
			first_list = frappe.db.sql(""" select  `tabCustody Report`.name, a.last_issue_detail, 
													b.item_name, b.item_group, b.description, b.item_code
													from `tabCustody Report Item` a
													join `tabItem` b on a.item_code = b.name 
													JOIN `tabCustody Report` ON a.parent = `tabCustody Report`.name
													 
													WHERE a.item_code = "{item_code}" 
													and a.last_issue_detail is not NULL
													and `tabCustody Report`.vehicles ="{vehicle}"
													AND a.last_issue_detail !="لم يتم الصرف من قبل"
													AND a.last_issue_detail !="لم يسبق الصرف"
													AND a.last_issue_detail != ""
													AND `tabCustody Report`.date >"2015-06-06"
													AND `tabCustody Report`.docstatus =1
													ORDER BY `tabCustody Report`.date
													""".format( last_issue_detail= "اطارات خارجية",vehicle=doc.vehicles, item_code=row.item_code), as_dict=1)
			if first_list:
				list_of_dates.extend(first_list)
		for row in list_of_dates:
			if not items.get(row.item_code):
				items[row.item_code] = row.item_name
				table = doc.append("custody_report_item", {})
				table.item_code = row.item_code
				table.item_name = row.item_name
				table.item_group = row.item_group
				table.description = row.description
				table.last_issue_detail = row.last_issue_detail
	@frappe.whitelist()
	def update_table(doc, method=None):
		if doc.select_type == "مجموعات متوافقة":
			doc.custody_report_item = []
			first_list = frappe.db.sql(""" select  a.item_code, c.item_name, c.item_group, c.description
											from `tabProduct Bundle Item` a join `tabProduct Bundle` b 
											on a.parent = b.name join `tabItem` c on a.item_code = c.name
											where b.new_item_code = '{new_item_code}'
											""".format(new_item_code=doc.bundle), as_dict=1)

			for z in first_list:
				table = doc.append("custody_report_item", {})
				table.item_code = z.item_code
				table.item_name = z.item_name
				table.item_group = z.item_group
				table.description = z.description
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
		today = date.today()
		past_date = add_months(today, -24)
		if doc.select_type == "مجموعات فرعية":
			if doc.group_type == "البطاريات" and not doc.custody_report_item:
				battery_list = frappe.db.sql(""" select b.name, b.date, b.ezn_no, a.item_code, a.item_name, a.item_group, a.description
										from `tabMaintenance Order Item` a join `tabMaintenance Order` b
										on a.parent = b.name
										where b.vehicles = '{vehicles}'
										and a.item_group = "البطاريات"
										and b.date >= '{past_date}'
										order by a.item_code desc, b.date desc
										""".format(vehicles=doc.vehicles, past_date=past_date), as_dict=1)
		
				doc.custody_report_item = []
				for x in battery_list:
					table = doc.append("custody_report_item", {})
					table.item_code = x.item_code
					table.item_name = x.item_name
					table.item_group = x.item_group
					table.description = x.description
					table.last_issue_detail = x.date
					table.reference_doc = x.name
					table.ezn_no = x.ezn_no
					table.save()
		
			if doc.group_type == "اطارات خارجية" and not doc.custody_report_item:
				wheel_list = frappe.db.sql(""" select b.name, b.date, b.ezn_no, a.item_code, a.item_name, a.item_group, a.description
										from `tabMaintenance Order Item` a join `tabMaintenance Order` b
										on a.parent = b.name
										where b.vehicles = '{vehicles}'
										and a.item_group = "اطارات خارجية"
										and b.date >= '{past_date}'
										order by a.item_code desc, b.date desc
										""".format(vehicles=doc.vehicles, past_date=past_date), as_dict=1)
		
				doc.custody_report_item = []
				for x in wheel_list:
					table = doc.append("custody_report_item", {})
					table.item_code = x.item_code
					table.item_name = x.item_name
					table.item_group = x.item_group
					table.description = x.description
					table.last_issue_detail = x.date
					table.reference_doc = x.name
					table.ezn_no = x.ezn_no
					table.save()

		for y in doc.custody_report_item:
			y.last_issue_detail = "لم يتم الصرف من قبل"
			x_list = frappe.db.sql(""" select e.name, e.date, e.ezn_no, d.item_code, d.item_name, d.item_group, d.description
												from `tabMaintenance Order Item` d join `tabMaintenance Order` e
												on d.parent = e.name
												where e.vehicles = '{vehicles}'
												and d.item_code = '{item_code}'
												and d.maintenance_method != "حافظة مشتريات"
												order by e.date desc limit 1
												""".format(vehicles=doc.vehicles, item_code=y.item_code), as_dict=1)

			for n in x_list:
				
				if n.item_code:
					y.last_issue_detail = n.date
				
"""
create index date_kashf 
on `Custody Report`(date);
"""