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
            "width": 120
        },
		{
			"label": _("تاريخ النقل"),
			"fieldname": "transfer_date",
			"fieldtype": "Date",
			"width": 120
		},
        {
            "label": _("رقم القرار"),
            "fieldname": "decision_number",
            "fieldtype": "Data",
            "width": 120
        },
		{
			"label": _("من جهة"),
			"fieldname": "transfer_from",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("الي جهة"),
			"fieldname": "transfer_to",
			"fieldtype": "Data",
			"width": 200
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
        conditions += " and transfer_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and transfer_date <= %(to_date)s"
    if filters.get("decision_number"):
        conditions += "and decision_number = %(decision_number)s"
    if filters.get("transfer_from"):
        conditions += "and transfer_from = %(transfer_from)s"
    if filters.get("transfer_to"):
        conditions += "and transfer_to = %(transfer_to)s"

    result = []
    item_results = frappe.db.sql("""
        select
            recruit, employee_name, military_date, transfer_date, decision_number, transfer_from, transfer_to
        from
            `tabTransfer For Recruit`
        where
            `tabTransfer For Recruit`.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'recruit': item_dict.recruit,
            'employee_name': item_dict.employee_name,
            'military_date': item_dict.military_date,
            'transfer_date': item_dict.transfer_date,
            'decision_number': item_dict.decision_number,
            'transfer_from': item_dict.transfer_from,
            'transfer_to': item_dict.transfer_to,
        }
        result.append(data)
    return result