# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.utils import flt


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [

        {
            "label": _("رقم الشرطة"),
            "fieldname": "police_no",
            "fieldtype": "Data",
            "width": 90,
        },
		{
            "label": _("النوع"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 60,
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 60,
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 65,
        },
        {
            "label": _("رقم الموتور"),
            "fieldname": "motor_no",
            "fieldtype": "Data",
            "width": 80,
        },
        {
            "label": _("رقم الشاسيه"),
            "fieldname": "chasie_no",
            "fieldtype": "Data",

            "width": 200,
        },
        {
            "label": _("السلندرات"),
            "fieldname": "cylinder_count",
            "fieldtype": "Data",
            "width": 100,
        },
		{
            "label": _("نوع الوقود"),
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("المقرر"),
            "fieldname": "liter_capacity",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("نوع الوقود"),
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الحالة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("تاريخ اإللتحاق بالجهة"),
            "fieldname": "vehicle_join_date",
            "fieldtype": "Data",
            "width": 100,
        },
    ]
    return columns


def get_conditions(filters):
    query = ""
    if filters.get("change_type") == "المــــــركبات الملــتحقة بالجــهة":
        query = frappe.db.sql(
			""" Select DISTINCT
			`tabVehicles`.name as name,
			`tabVehicles`.vehicle_no as vehicle_no,
			`tabVehicles`.vehicle_type as vehicle_type,
			`tabVehicles`.vehicle_shape as vehicle_shape,
			`tabVehicles`.vehicle_brand as vehicle_brand,
			`tabVehicles`.vehicle_style as vehicle_style,
			`tabVehicles`.motor_no as motor_no,
			`tabVehicles`.chassis_no as chassis_no,
			`tabVehicles`.vehicle_status as vehicle_status,
			CEILING(`tabVehicles`.litre_count) as litre_count,
			`tabVehicles`.cylinder_count as cylinder_count,
			`tabVehicles`.fuel_type as fuel_type,
			`tabEntity Logs`.date as date
			from `tabVehicles` join `tabEntity Logs`
			on `tabVehicles`.name = `tabEntity Logs`.parent
			where `tabEntity Logs`.value = '{entity}'
			and `tabEntity Logs`.date between '{start_date}' and '{end_date}'
			order by `tabEntity Logs`.date
			""".format(
			start_date=filters.get("from_date"), end_date=filters.get("to_date"), entity=filters.get("entity")
			),
			as_dict=1,
			)
    if filters.get("change_type") == "المــــــركبات التي تم نقلها من الجهة":
        query = frappe.db.sql(
			""" Select
			`tabVehicles`.name as name,
			`tabEntity Logs`.value as entity_name,
			`tabVehicles`.vehicle_no as vehicle_no,
			`tabVehicles`.vehicle_type as vehicle_type,
			`tabVehicles`.vehicle_shape as vehicle_shape,
			`tabVehicles`.vehicle_brand as vehicle_brand,
			`tabVehicles`.vehicle_style as vehicle_style,
			`tabVehicles`.motor_no as motor_no,
			`tabVehicles`.chassis_no as chassis_no,
			`tabVehicles`.vehicle_status as vehicle_status,
			CEILING(`tabVehicles`.litre_count) as litre_count,
			`tabVehicles`.cylinder_count as cylinder_count,
			`tabVehicles`.fuel_type as fuel_type,
			`tabEntity Logs`.date as date
			from `tabVehicles` join `tabEntity Logs`
			on `tabVehicles`.name = `tabEntity Logs`.parent
			where  `tabVehicles`.entity_name != 'احتياطى مخازن المركبات'
			and `tabEntity Logs`.value = '{entity}'
			and `tabVehicles`.entity_name != '{entity}'
			and `tabEntity Logs`.date between '{start_date}' and '{end_date}'
			""".format(
			start_date=filters.get("from_date"), end_date=filters.get("to_date"), entity=filters.get("entity")
			),
			as_dict=1,
			)
    if filters.get("change_type") == "المــــــركبات التي تم إصالحها":
        query = frappe.db.sql(
				"""
				Select
				`tabVehicles`.name as name,
				`tabVehicle Status Logs`.value as entity_name,
				`tabVehicles`.vehicle_no as vehicle_no,
				`tabVehicles`.vehicle_type as vehicle_type,
				`tabVehicles`.vehicle_shape as vehicle_shape,
				`tabVehicles`.vehicle_brand as vehicle_brand,
				`tabVehicles`.vehicle_style as vehicle_style,
				`tabVehicles`.motor_no as motor_no,
				`tabVehicles`.chassis_no as chassis_no,
				CEILING(`tabVehicles`.litre_count) as litre_count,
				`tabVehicles`.cylinder_count as cylinder_count,
				`tabVehicles`.fuel_type as fuel_type,
				`tabVehicle Status Logs`.date as date
				from `tabVehicles` join `tabVehicle Status Logs`
				on `tabVehicles`.name = `tabVehicle Status Logs`.parent
				where `tabVehicle Status Logs`.value = 'صالحة'
				and `tabVehicles`.entity_name = '{entity}'
				and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
				order by `tabVehicle Status Logs`.date
				""".format(
			start_date=filters.get("from_date"), end_date=filters.get("to_date"), entity=filters.get("entity")
			),
			as_dict=1,
			)
    if filters.get("change_type") == "المــــــركبات التي تم تعطيلها":
        query = frappe.db.sql(
				"""
				Select DISTINCT
				`tabVehicles`.name as name,
				`tabVehicle Status Logs`.value as entity_name,
				`tabVehicles`.vehicle_no as vehicle_no,
				`tabVehicles`.vehicle_type as vehicle_type,
				`tabVehicles`.vehicle_shape as vehicle_shape,
				`tabVehicles`.vehicle_brand as vehicle_brand,
				`tabVehicles`.vehicle_style as vehicle_style,
				`tabVehicles`.motor_no as motor_no,
				`tabVehicles`.chassis_no as chassis_no,
				CEILING(`tabVehicles`.litre_count) as litre_count,
				`tabVehicles`.cylinder_count as cylinder_count,
				`tabVehicles`.fuel_type as fuel_type,
				`tabVehicle Status Logs`.date as date
				from `tabVehicles` join `tabVehicle Status Logs`
				on `tabVehicles`.name = `tabVehicle Status Logs`.parent
				where `tabVehicle Status Logs`.value = 'عاطلة'
				and `tabVehicles`.entity_name = '{entity}'
				and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
				order by `tabVehicle Status Logs`.date
				""".format(
			start_date=filters.get("from_date"), end_date=filters.get("to_date"), entity=filters.get("entity")
			),
			as_dict=1,
			)
    if filters.get("change_type") == "المــــــركبات التي تم تخريدها":
        query = frappe.db.sql(
			"""
			Select DISTINCT
			`tabVehicles`.name as name,
			`tabVehicle Status Logs`.value as entity_name,
			`tabVehicles`.police_id as vehicle_no,
			`tabVehicles`.vehicle_type as vehicle_type,
			`tabVehicles`.vehicle_shape as vehicle_shape,
			`tabVehicles`.vehicle_brand as vehicle_brand,
			`tabVehicles`.vehicle_style as vehicle_style,
			`tabVehicles`.motor_no as motor_no,
			`tabVehicles`.chassis_no as chassis_no,
			CEILING(`tabVehicles`.litre_count) as litre_count,
			`tabVehicles`.cylinder_count as cylinder_count,
			`tabVehicles`.fuel_type as fuel_type,
			`tabVehicle Status Logs`.date as date
			from `tabVehicles` join `tabVehicle Status Logs`
			on `tabVehicles`.name = `tabVehicle Status Logs`.parent
			where `tabVehicle Status Logs`.value = 'مخردة'
			and `tabVehicles`.entity_name = '{entity}'

			and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
			order by `tabVehicle Status Logs`.date
			""".format(
			start_date=filters.get("from_date"), end_date=filters.get("to_date"), entity=filters.get("entity")
			),
			as_dict=1,
			)
    return query


def get_data(filters):
    conditions = get_conditions(filters)
    # query = get_query(conditions)
    # license_details_query = license_details()
    # license_summary_entry = license_summary()
    # license_summary_entry = get_license_summary_entry(conditions)
    # projects_entry = get_projects_entry(conditions)
    # pr_records = get_mapped_pr_records()
    # pi_records = get_mapped_pi_records()

    ingaze_row = []

    for record in conditions:
        # fetch material records linked to the purchase order item
        # mr_record = mr_records.get(records.material_request_item, [{}])[0]
        row_detail = {
            "name": record.name,
            "police_no": record.vehicle_no,
            "vehicle_type": record.vehicle_type,
            "vehicle_shape": record.vehicle_shape,
            "vehicle_brand": record.vehicle_brand,
            "vehicle_style": record.vehicle_style,
            "motor_no": record.motor_no,
            "chasie_no": record.chasie_no,
            "cylinder_count": record.cylinder_count,
            "fuel_type": record.fuel_type,
            "liter_capacity": record.liter_capacity,
            "fuel_type": record.fuel_type,
            "vehicle_status": record.vehicle_status,
            "vehicle_join_date": record.vehicle_join_date,
            # "delivery_note_name": delivery_note_entry.get(record.sales_order),
            # "delivery_grand_total": flt(
            #     frappe.db.get_value(
            #         "Delivery Note",
            #         delivery_note_entry.get(record.sales_order),
            #         "grand_total",
            #     )
            # ),
            # "license_summary_name": license_summary_entry.get(record.sales_order),
            # "invoice_grand_total": flt(
            #     frappe.db.get_value(
            #         "Sales Invoice",
            #         license_summary_entry.get(record.sales_order),
            #         "grand_total",
            #     )
            # ),
            # "note": "note",
        }
        ingaze_row.append(row_detail)
   
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT 
            license_summary.name AS name,
            license_summary.vehicle AS vehicle_code,
            license_summary.police_no AS police_no,
            license_summary.private_no AS private_no,
            license_summary.vehicle_type AS vehicle_type,
            license_summary.entity AS entity,
            license_summary.from_date AS from_date,
            license_summary.to_date AS to_date,
            license_summary.license_no AS license_no,
            license_summary.license_status AS license_status,
            license_summary.issue_status AS issue_status,
            license_summary.renewal_type AS renewal_type,
            license_summary.user AS user,
            license_summary.card_code AS card_code

        FROM `tabVehicle License Entries` license_summary
        WHERE 1 =  1
        {conditions}
        ORDER BY license_summary.license_no, card_code DESC

        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )  # nosec


def license_details():
    return frappe._dict(
        frappe.db.sql(
            """
        SELECT 
            license_summary.parent AS license_summary_parent,
             vehicle_license.name AS vehicle_license_name

        FROM `tabLicense Entry Summary` license_summary
        JOIN `tabVehicle License` vehicle_license ON vehicle_license.name = license_summary.parent
        WHERE vehicle_license.docstatus =  1
        """
        )
    )  # nosec


def license_summary():
    return frappe._dict(
        frappe.db.sql(
            """
        SELECT 
            license_summary_item.sales_order AS against_sales_order,
             license_summary.name AS license_summary_name

        FROM `tabSales Invoice` license_summary
        JOIN `tabSales Invoice Item` license_summary_item ON license_summary.name = license_summary_item.parent
        WHERE license_summary.status != "Cancelled"
        """
        )
    )  # nosec

