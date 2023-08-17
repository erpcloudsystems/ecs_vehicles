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
            "width": 120
        },
        {
            "label": _("تاريخ الاصابة"),
            "fieldname": "injury_date",
            "fieldtype": "Date",
            "width": 120
        },
		{
			"label": _("تاريخ العرض"),
			"fieldname": "presentation_date",
			"fieldtype": "Date",
			"width": 120
		},
        {
            "label": _("مكان العرض"),
            "fieldname": "presentation_place",
            "fieldtype": "Data",
            "width": 180
        },
		{
			"label": _("تاريخ اللجنة"),
			"fieldname": "the_committees_date",
			"fieldtype": "Date",
			"width": 120
		},
        {
            "label": _("قرار اللجنة"),
            "fieldname": "the_committees_decision",
            "fieldtype": "Data",
            "width": 150
        },
		{
			"label": _("ما تم اتخاذه حيال القرار"),
			"fieldname": "about_the_decision",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("حالة العرض"),
			"fieldname": "presentation_case",
			"fieldtype": "Data",
			"width": 120
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
        conditions += " and presentation_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and presentation_date <= %(to_date)s"
    if filters.get("presentation_place"):
        conditions += "and presentation_place = %(presentation_place)s"
    if filters.get("the_committees_date"):
        conditions += "and the_committees_date = %(the_committees_date)s"
    if filters.get("the_committees_decision"):
        conditions += "and the_committees_decision = %(the_committees_decision)s"
    if filters.get("about_the_decision"):
        conditions += "and about_the_decision = %(about_the_decision)s"
    if filters.get("presentation_case"):
        conditions += "and presentation_case = %(presentation_case)s"


    result = []
    item_results = frappe.db.sql("""
        select
            recruit, employee_name, injury_date, presentation_place, presentation_date, the_committees_date, the_committees_decision, about_the_decision, presentation_case
        from
            `tabPresentation To Medical Commission For Recruit`
        where
            `tabPresentation To Medical Commission For Recruit`.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'recruit': item_dict.recruit,
            'employee_name': item_dict.employee_name,
            'injury_date': item_dict.injury_date,
            'presentation_place': item_dict.presentation_place,
            'presentation_date': item_dict.presentation_date,
            'the_committees_date': item_dict.the_committees_date,
            'the_committees_decision': item_dict.the_committees_decision,
            'about_the_decision': item_dict.about_the_decision,
            'presentation_case': item_dict.presentation_case,
        }
        result.append(data)
    return result