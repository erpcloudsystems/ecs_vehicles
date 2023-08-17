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
			"label": _("اسم المجند"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 200
		},
        {
            "label": _("رقم المجند"),
            "fieldname": "recruit",
            "fieldtype": "Link",
			"options": "Employee",
            "width": 150
        },
        {
            "label": _("تاريخ الغياب"),
            "fieldname": "absent_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("ملاحظات"),
            "fieldname": "notes",
            "fieldtype": "Data",
            "width": 300
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("recruit"):
        conditions += "and recruit = %(recruit)s"
    if filters.get("from_date"):
        conditions += " and absent_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and absent_date <= %(to_date)s"
    if filters.get("notes"):
        conditions += "and notes = %(notes)s"

    result = []
    item_results = frappe.db.sql("""
        select
            recruit, employee_name, military_date, absent_date, notes
        from
            `tabRecruit Absent`
        where
            `tabRecruit Absent`.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'recruit': item_dict.recruit,
            'employee_name': item_dict.employee_name,
            'military_date': item_dict.military_date,
            'absent_date': item_dict.absent_date,
            'notes': item_dict.notes,
        }
        result.append(data)
    return result