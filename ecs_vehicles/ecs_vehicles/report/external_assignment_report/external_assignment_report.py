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
			"label": _("تاريخ التجنيد"),
			"fieldname": "military_date",
			"fieldtype": "Date",
			"width": 150
		},
        {
            "label": _("تاريخ الانتداب"),
            "fieldname": "assignment_date",
            "fieldtype": "Date",
            "width": 150
        },
		{
			"label": _("جهات الانتداب"),
			"fieldname": "assignment_entities",
			"fieldtype": "Data",
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
    if filters.get("military_date"):
        conditions += "and military_date = %(military_date)s"
    if filters.get("from_date"):
        conditions += " and assignment_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and assignment_date <= %(to_date)s"
    if filters.get("assignment_entities"):
        conditions += "and assignment_entities = %(assignment_entities)s"
    if filters.get("notes"):
        conditions += "and notes = %(notes)s"

    result = []
    item_results = frappe.db.sql("""
        select
            recruit, employee_name, military_date, assignment_date, assignment_entities, notes
        from
            `tabExternal Assignment`
        where
            `tabExternal Assignment`.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'recruit': item_dict.recruit,
            'employee_name': item_dict.employee_name,
            'military_date': item_dict.military_date,
            'assignment_date': item_dict.assignment_date,
            'assignment_entities': item_dict.assignment_entities,
            'notes': item_dict.notes,
        }
        result.append(data)
    return result