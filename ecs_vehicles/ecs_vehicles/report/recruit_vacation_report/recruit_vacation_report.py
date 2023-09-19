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
            "label": _("تاريخ بداية الاجازة"),
            "fieldname": "start_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("وقت بداية الاجازة"),
            "fieldname": "start_time",
            "fieldtype": "Time",
            "width": 150
        },
		{
			"label": _("تاريخ نهاية الاجازة"),
			"fieldname": "end_date",
			"fieldtype": "Date",
			"width": 150
		},
        {
            "label": _("وقت نهاية الاجازة"),
            "fieldname": "end_time",
            "fieldtype": "Time",
            "width": 150
        },
        {
            "label": _("نوع الاجازة"),
            "fieldname": "types_of_vacations",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("الملاحظات"),
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
        conditions += "and  `tabRecruit Vacation`.recruit = %(recruit)s"
    if filters.get("start_date"):
        conditions += " and  `tabRecruit Vacation`.end_date >= %(start_date)s"
    if filters.get("end_date"):
        conditions += " and  `tabRecruit Vacation`.end_date <= %(end_date)s"
    if filters.get("overnight")== "مبيت":
        conditions += " and  `tabRecruit Vacation`.types_of_vacations = %(overnight)s"
    if filters.get("overnight")== "أجازة دورية":
        conditions += "  and `tabRecruit Vacation`.types_of_vacations = %(overnight)s"

    result = []
    item_results = frappe.db.sql("""
            select
                recruit, employee_name,  start_date, start_time, end_date, end_time, types_of_vacations, notes
            from
                `tabRecruit Vacation`
            where
                `tabRecruit Vacation`.docstatus = 1
                {conditions}
            order by end_date desc
            """.format(conditions=conditions), filters, as_dict=1)

    for x in item_results:
        data = {}
        data['recruit'] = x.recruit
        data['employee_name'] = x.employee_name
        data['start_date'] = x.start_date
        data['start_time'] = x.start_time
        data['end_date'] = x.end_date
        data['end_time'] = x.end_time
        data['types_of_vacations'] = x.types_of_vacations
        data['notes'] = x.notes
        result.append(data)
    return result