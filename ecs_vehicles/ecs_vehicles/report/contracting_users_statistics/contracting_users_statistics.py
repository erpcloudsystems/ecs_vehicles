# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters, columns)
	return columns, data


def get_columns():
	return [
		{
			"label": _("اسم المستخدم"),
			"fieldname": "username",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("عدد طلبات عروض الأسعار"),
			"fieldname": "rfq_count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"label": _("عدد مذكرات العرض"),
			"fieldname": "note_count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"label": _("عدد أوامر الشغل"),
			"fieldname": "jo_count",
			"fieldtype": "Int",
			"width": 200
		},
		{
			"label": _("إجمالي العدد"),
			"fieldname": "total_count",
			"fieldtype": "Int",
			"width": 200
		}
	]


def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data


def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and `tabMaintenance Print Logs`.print_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " and `tabMaintenance Print Logs`.print_date <= %(to_date)s"

	# user_list = frappe.db.sql("""
	# 	select distinct `tabMaintenance Print Logs`.printed_by
	# 	from `tabMaintenance Print Logs`
	# 	where format_name in ("طلب عروض أسعار" ,"مذكرة عرض" ,"أمر شغل")
	# 	{conditions}
	# 	order by printed_by
	# 	""".format(conditions=conditions), filters, as_dict=1)
		
	# result = []
	# data = {}
	# if user_list:
	# 	for x in user_list:
	# 		data = {
	# 			'username': x.printed_by
	# 		}
	# 		item_results = frappe.db.sql("""
	# 			select distinct
	# 				(select count(name) from `tabMaintenance Print Logs`
	# 				where format_name = "طلب عروض أسعار" and printed_by = '{username}' {conditions}) as rfq_count,
	# 				(select count(name) from `tabMaintenance Print Logs`
	# 				where format_name = "مذكرة عرض" and printed_by = '{username}' {conditions}) as note_count,
	# 				(select count(name) from `tabMaintenance Print Logs`
	# 				where format_name = "أمر شغل" and printed_by = '{username}' {conditions}) as jo_count,
	# 				(select count(name) from `tabMaintenance Print Logs`
	# 				where format_name in ("طلب عروض أسعار" ,"مذكرة عرض" ,"أمر شغل") and printed_by = '{username}' {conditions}) as total_count
	# 			from
	# 				`tabMaintenance Print Logs`
	# 			where 1=1
	# 			{conditions}
	# 			""".format(conditions=conditions, username=x.printed_by), filters, as_dict=1)
	
	# 		for item_dict in item_results:
	# 			data['rfq_count'] = item_dict.rfq_count
	# 			data['note_count'] = item_dict.note_count
	# 			data['jo_count'] = item_dict.jo_count
	# 			data['total_count'] = item_dict.total_count

	# 		result.append(data)
	# return result

	user_list = frappe.db.sql("""
		SELECT distinct
			printed_by as printed_by
		FROM
			`tabMaintenance Print Logs`
		WHERE
			format_name in ("طلب عروض أسعار" ,"مذكرة عرض" ,"أمر شغل")
			{conditions}	
		Group BY printed_by
	  order by printed_by
		""".format(conditions=conditions), filters, as_dict=1)

	result = []
	if user_list:
		for item_dict in user_list:
			data = {
				'username': item_dict.printed_by
			}
			rfq = frappe.db.sql("""
					SELECT 
						count(name) as rfq_count
					FROM
						`tabMaintenance Print Logs`
					WHERE 
						format_name = "طلب عروض أسعار"
						and printed_by = '{username}'
						{conditions}
					""".format(conditions=conditions, username=item_dict.printed_by), filters, as_dict=1)
			note = frappe.db.sql("""
					SELECT 
						count(name) as note_count
					FROM
						`tabMaintenance Print Logs`
					WHERE 
						format_name = "مذكرة عرض"
						and printed_by = '{username}'
						{conditions}
					""".format(conditions=conditions, username=item_dict.printed_by), filters, as_dict=1)
			jo = frappe.db.sql("""
					SELECT 
						count(name) as jo_count
					FROM
						`tabMaintenance Print Logs`
					WHERE 
						format_name = "أمر شغل"
						and printed_by = '{username}'
						{conditions}
					""".format(conditions=conditions, username=item_dict.printed_by), filters, as_dict=1)
			for x in rfq:
				data['rfq_count'] = x.rfq_count
			for y in note:
				data['note_count'] = y.note_count
			for z in jo:
				data['jo_count'] = z.jo_count
			data['total_count'] = data['rfq_count'] + data['note_count'] + data['jo_count']
			result.append(data)
	try:
		result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
	except:
		pass	
	return result