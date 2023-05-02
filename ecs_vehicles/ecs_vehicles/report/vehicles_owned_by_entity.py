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
		conditions += " AND vehicles_entity_logs.value = '{}'".format(filters.get("entity"))
	return conditions
def get_data(filters):
	conditions = get_conditions(filters)
	query = get_query(conditions)
	response = []
	for row in query:
		idx = frappe.db.sql(
		"""
		SELECT vehicles_entity_logs.name as child, vehicles_entity_logs.idx as idx, vehicles_entity_logs.date date, vehicles.vehicle_no vehicle_no, vehicles.vehicle_shape shape, vehicles.vehicle_brand brand,
			vehicles.vehicle_style style , vehicles.name as name, vehicles_entity_logs.value value, vehicles.police_id as police_id, vehicles.exchange_allowance as exchange_allowance
		FROM `tabEntity Logs` vehicles_entity_logs
			JOIN `tabVehicles` vehicles ON vehicles_entity_logs.parent = vehicles.name

		where vehicles_entity_logs.parenttype = "Vehicles"
		AND vehicles_entity_logs.value = "{entity}"
		AND vehicles_entity_logs.parent = "{parent}"
		AND vehicles_entity_logs.date <= "{posting_date}"
		ORDER BY vehicles_entity_logs.date   desc
		LIMIT 1
		""".format(parent=row.parent,entity=filters.get("entity"),posting_date=filters.get("posting_date") ),as_dict=1)
		if idx:
			to_date = frappe.db.sql("""
				SELECT vehicles_entity_logs.date date, vehicles.vehicle_no vehicle_no, vehicles.vehicle_shape shape, vehicles.vehicle_brand brand,
				vehicles.vehicle_style style, vehicles.name as name, vehicles_entity_logs.value value, vehicles.police_id as police_id, vehicles.exchange_allowance as exchange_allowance
				FROM `tabEntity Logs` vehicles_entity_logs 
				JOIN `tabVehicles` vehicles ON vehicles_entity_logs.parent = vehicles.name
				WHERE vehicles_entity_logs.parent = "{parent}"
				AND vehicles_entity_logs.idx = {idx}
				AND vehicles_entity_logs.parenttype = "Vehicles"
				ORDER BY vehicles_entity_logs.date desc
				""".format(parent=row.parent,idx=idx[0].idx+1), as_dict=1)
			previous_status = None
			vehicle_entity_status = ""
			current_status = frappe.db.sql(""" 
			 	SELECT date, idx, value
				FROM `tabVehicle Status Logs`
				WHERE parent = "{parent}"
				AND date <= "{posting_date}"
				ORDER BY date DESC
			 """.format(parent=row.parent, posting_date=filters.get("posting_date")), as_dict=1)
			if len(current_status) > 1:
				previous_status = frappe.db.sql(""" 
					SELECT date, idx, value
					FROM `tabVehicle Status Logs`
					WHERE parent = "{parent}"
					and date <= "{posting_date}"
					and idx = {idx}
					ORDER BY date DESC
					LIMIT 1 

				""".format(idx=current_status[0].idx - 1,parent=row.parent, posting_date=filters.get("posting_date")), as_dict=1)
			if len(current_status) == 0:
				current_status = frappe.db.sql(""" 
			 	SELECT date, idx, value
				FROM `tabVehicle Status Logs`
				WHERE parent = "{parent}"
				AND date >= "{posting_date}"
				ORDER BY date 
				limit 1
			 """.format(parent=row.parent, posting_date=filters.get("posting_date")), as_dict=1)
			if to_date:
				if to_date[0].date:
					post_date = datetime.datetime.strptime(filters.get("posting_date"), "%Y-%m-%d")
					to_d = datetime.datetime.strptime(str(to_date[0].date), "%Y-%m-%d")
					if to_d > post_date:
						
						row= {
							"vehicle_name":to_date[0].name,
							"vehicle_date":idx[0].date,
							"vehicle_no": to_date[0].vehicle_no if to_date[0].vehicle_no else to_date[0].police_id ,
							"vehicle_shape": to_date[0].shape,
							"vehicle_brand": to_date[0].brand,
							"vehicle_style": to_date[0].style,
							"cur_user": frappe.session.user,
							"vehicle_status": "{0}".format(current_status[0].value if current_status[0].value in ["عاطلة", "تحت التخريد"] else " "),
							"notes": "{0}".format(to_date[0].exchange_allowance if to_date[0].exchange_allowance in ["لوحة فقط", "لوحة وخدمة كاملة فقط"] else " "),

						}
						response.append(row)
			else:
				row= {
						"vehicle_name":idx[0].name,
						"vehicle_date":idx[0].date,
						"vehicle_no": idx[0].vehicle_no if idx[0].vehicle_no else idx[0].police_id ,
						"vehicle_shape": idx[0].shape,
						"vehicle_brand": idx[0].brand,
						"vehicle_style": idx[0].style,
						"cur_user": frappe.session.user,
						# "vehicle_status": "{0}".format(current_status[0].value if current_status[0].value in ["عاطلة", "تحت التخريد"] else " "),
						"vehicle_status": " ",
						"notes": "{0}".format(idx[0].exchange_allowance if idx[0].exchange_allowance in ["لوحة فقط", "لوحة وخدمة كاملة فقط"] else " "),

					}
				response.append(row)
	return response

def get_query (conditions):
	return frappe.db.sql(
		"""
		SELECT DISTINCT vehicles_entity_logs.parent as parent
		FROM `tabEntity Logs` vehicles_entity_logs
		JOIN `tabVehicles` veh On veh.name = vehicles_entity_logs.parent
		where vehicles_entity_logs.parenttype = "Vehicles"
		AND veh.vehicle_status IN ("عاطلة","صالحة", "تحت التخريد")
		{conditions}

	""".format(conditions=conditions), as_dict=1)

	# entity_logs = frappe.db.sql("""
	#     SELECT DISTINCT vehicles.name as parent
	#     FROM `tabEntity Logs` vehicles_entity_logs
	#     JOIN `tabVehicles` vehicles ON vehicles_entity_logs.parent = vehicles.name
	#     where vehicles_entity_logs.parenttype = "Vehicles"
	#     AND vehicles_entity_logs.value = filters.get("entity")
	#     ORDER BY parent    DESC
  
	# """, as_dict=1)
	for log in entity_logs:
		idx = frappe.db.sql(
		"""
		SELECT vehicles_entity_logs.name as child, vehicles_entity_logs.idx as idx
		FROM `tabEntity Logs` vehicles_entity_logs
		where vehicles_entity_logs.parenttype = "Vehicles"
		AND vehicles_entity_logs.value = filters.get("entity")
		AND vehicles_entity_logs.parent = "VEH-21241"
		ORDER BY vehicles_entity_logs.date   desc
		LIMIT 1
		""",as_dict=1)

		to_date = frappe.db.sql("""
			SELECT vehicles_entity_logs.date, vehicles_entity_logs.idx, vehicles_entity_logs.name
			FROM `tabEntity Logs` vehicles_entity_logs 
			WHERE parent = "VEH-21241"
			AND idx = {idx}
			AND vehicles_entity_logs.parenttype = "Vehicles"
			ORDER BY vehicles_entity_logs.date
			""".format(idx=idx[0].idx+1), as_dict=1)
		if to_date:
			entity_logs2 = frappe.db.sql("""
				SELECT vehicles_entity_logs.name, vehicles_entity_logs.date
				FROM `tabEntity Logs` vehicles_entity_logs
				where vehicles_entity_logs.parenttype = "Vehicles"
				AND vehicles_entity_logs.date > "1994-08-02"
				AND vehicles_entity_logs.parent = "VEH-21241"
				AND vehicles_entity_logs.date < "{to_date}"

			""".format(to_date=to_date[0].date), as_dict=1)
	return vehicles