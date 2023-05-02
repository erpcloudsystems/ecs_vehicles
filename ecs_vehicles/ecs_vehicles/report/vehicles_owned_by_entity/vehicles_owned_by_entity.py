# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
				{
			"label": _("كود المركبة"),
			"fieldname": "vehicle_name",
			"fieldtype": "Link",
			"options": "Vehicles",
			"width": 140
		},
		{
			"label": _("رقم الشرطة"),
			"fieldname": "vehicle_no",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("الشكل"),
			"fieldname": "vehicle_shape",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("الماركة"),
			"fieldname": "vehicle_brand",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("الطراز"),
			"fieldname": "vehicle_style",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("الحالة"),
			"fieldname": "vehicle_status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("الملحوظات"),
			"fieldname": "notes",
			"fieldtype": "Data",
			"width": 100
		}
	]
	return columns

def get_conditions (filters):
	conditions =""
	if filters.get("entity"):
		conditions += " AND vehicles.entity_name = '{}'".format(filters.get("entity"))
	return conditions
def get_data(filters):
	conditions = get_conditions(filters)
	query = get_query(conditions)
	response = []
	for row in query:
		row= {
				"vehicle_name":row.name,
				"vehicle_date":row.date,
				"vehicle_no": row.vehicle_no if row.vehicle_no else row.police_id ,
				"vehicle_shape": row.shape,
				"vehicle_brand": row.brand,
				"vehicle_style": row.style,
				"cur_user": frappe.session.user,
				# "vehicle_status": "{0}".format(current_status[0].value if current_status[0].value in ["عاطلة", "تحت التخريد"] else " "),
				"vehicle_status": " ",
				"notes": "{0}".format(row.exchange_allowance if row.exchange_allowance in ["لوحة فقط", "لوحة وخدمة كاملة فقط"] else " "),

			}
		response.append(row)
	return response

def get_query (conditions):
	return frappe.db.sql(
		"""
SELECT   vehicles.vehicle_no vehicle_no, vehicles.vehicle_shape shape, vehicles.vehicle_brand brand, vehicles.possession_date as date,
			vehicles.vehicle_style style , vehicles.name as name, vehicles.entity_name as entity_name, vehicles.police_id as police_id, vehicles.exchange_allowance as exchange_allowance
		FROM `tabVehicles` vehicles
		Where vehicles.vehicle_status IN ("عاطلة","صالحة", "تحت التخريد")
		{conditions}
	""".format(conditions=conditions), as_dict=1)

