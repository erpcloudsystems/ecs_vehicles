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
            "label": _("رقم الشرطة"),
            "fieldname": "police_no",
            "fieldtype": "Data",
            "width": 100
        },
		{
			"label": _("الجهة"),
			"fieldname": "entity",
			"fieldtype": "Data",
			"width": 200
		},
        {
            "label": _("السنة المالية"),
			"fieldname": "fiscal_year",
			"fieldtype": "Data",
			"width": 100,
		},
        {
            "label": _("رقم الواقعة"),
            "fieldname": "accident_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("كود الواقعة"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Accident",
            "width": 150
        },
		{
			"label": _("تاريخ الواقعة"),
			"fieldname": "accident_date",
			"fieldtype": "Date",
			"width": 110
		},
        {
            "label": _("نوع الواقعة"),
            "fieldname": "accident_type",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("رقم الموتور"),
            "fieldname": "motor_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("رقم الشاسيه"),
            "fieldname": "chassis_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("شكل المركبة"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("الموديل"),
            "fieldname": "vehicle_model",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("اللون"),
            "fieldname": "vehicle_color",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("نوع التجهيز"),
            "fieldname": "processing_type",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("نوع الوقود"),
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 110
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("police_no"):
        conditions += "and police_no = %(police_no)s"
    if filters.get("entity"):
        conditions += "and entity = %(entity)s"
    if filters.get("from_date"):
        conditions += " and accident_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and accident_date <= %(to_date)s"
    if filters.get("fiscal_year"):
        conditions += "and fiscal_year = %(fiscal_year)s"
    if filters.get("accident_type"):
        conditions += "and accident_type = %(accident_type)s"
    if filters.get("accident_no"):
        conditions += "and accident_no = %(accident_no)s"
    if filters.get("name"):
        conditions += "and name = %(name)s"

    result = []
    item_results = frappe.db.sql("""
        select
            name, police_no, fiscal_year, accident_no, accident_date, accident_type, entity, motor_no, chassis_no, 
            fuel_type, vehicle_shape, vehicle_brand, vehicle_style, vehicle_model, vehicle_color, processing_type
        from
            `tabAccident`
        where
            `tabAccident`.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'police_no': item_dict.police_no,
            'entity': item_dict.entity,
            'name': item_dict.name,
            'fiscal_year': item_dict.fiscal_year,
            'accident_no': item_dict.accident_no,
            'accident_date': item_dict.accident_date,
            'accident_type': item_dict.accident_type,
            'motor_no': item_dict.motor_no,
            'chassis_no': item_dict.chassis_no,
            'vehicle_shape': item_dict.vehicle_shape,
            'vehicle_brand': item_dict.vehicle_brand,
            'vehicle_style': item_dict.vehicle_style,
            'vehicle_model': item_dict.vehicle_model,
            'vehicle_color': item_dict.vehicle_color,
            'processing_type': item_dict.processing_type,
            'fuel_type': item_dict.fuel_type,
        }
        result.append(data)
    return result