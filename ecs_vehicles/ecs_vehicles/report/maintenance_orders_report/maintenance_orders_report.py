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
            "label": _("إجراء الإصلاح"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Maintenance Order",
            "width": 150
        },
        {
            "label": _("إسم الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Data",
            "width": 280
        },
		{
			"label": _("الماركة / الطراز"),
			"fieldname": "brand_style",
			"fieldtype": "Data",
			"width": 160
		},
        {
            "label": _("رقم الشرطة"),
			"fieldname": "vehicle_no",
			"fieldtype": "Data",
			"width": 90,
		},
        {
            "label": _("رقم الإذن"),
            "fieldname": "ezn_no",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("السنة المالية"),
            "fieldname": "fiscal_year",
            "fieldtype": "Data",
            "width": 100
        },
		{
			"label": _("تاريخ الدخول"),
			"fieldname": "car_in_date",
			"fieldtype": "Date",
			"width": 110
		},
		{
			"label": _("تاريخ الخروج"),
			"fieldname": "car_out_date",
			"fieldtype": "Date",
			"width": 110
		},
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("vehicle_no"):
        conditions += "and a.vehicle_no = %(vehicle_no)s"
    if filters.get("entity_name"):
        conditions += "and a.entity_name = %(entity_name)s"
    if filters.get("from_date"):
        conditions += " and a.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and a.date <= %(to_date)s"
    if filters.get("fiscal_year"):
        conditions += "and a.fis_year = %(fiscal_year)s"
    if filters.get("ezn_no"):
        conditions += "and a.ezn_no = %(ezn_no)s"
    if filters.get("maintenance_method"):
        conditions += "and b.maintenance_method = %(maintenance_method)s"


    result = []
    item_results = frappe.db.sql("""
        select distinct
            a.name, a.entity_name, a.vehicle_brand, a.vehicle_style, a.vehicle_no, a.ezn_no, a.fis_year, a.car_in_date, a.car_out_date
        from
            `tabMaintenance Order` a join `tabMaintenance Order Item` b on a.name = b.parent
        where
           a.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'entity_name': item_dict.entity_name,
            'brand_style': str(item_dict.vehicle_brand) + " / " + str(item_dict.vehicle_style),
            'vehicle_no': item_dict.vehicle_no,
            'name': item_dict.name,
            'ezn_no': item_dict.ezn_no,
            'fiscal_year': item_dict.fis_year,
            'car_in_date': item_dict.car_in_date,
            'car_out_date': item_dict.car_out_date,
        }
        result.append(data)
    return result