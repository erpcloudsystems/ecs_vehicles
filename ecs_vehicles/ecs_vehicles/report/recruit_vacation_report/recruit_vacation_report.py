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
            "fieldname": "name",
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
    conditions1 = ""
    conditions2 = ""
    conditions3 = ""
    if filters.get("recruit"):
        conditions1 += "and  `tabEmployee`.name = %(recruit)s"
    if filters.get("start_date"):
        conditions += " and  `tabRecruit Vacation`.start_date = %(start_date)s"
    if filters.get("end_date"):
        conditions += " and  `tabRecruit Vacation`.end_date = %(end_date)s"
    if filters.get("overnight")== "مبيت":
        conditions1 += " and  `tabEmployee`.overnight = %(overnight)s"
    if filters.get("overnight")== "اجازة دورية":
        conditions2 += " join  `tabRecruit Vacation` on `tabRecruit Vacation`.recruit = `tabEmployee`.name "
        #conditions3 += " and  `tabRecruit Vacation`.end_date = %(end_date)s"

    result = []

    item_result2 = frappe.db.sql("""
        select
            `tabEmployee`.employee_name, `tabEmployee`.name, `tabEmployee`.overnight
        from
           `tabEmployee`  {conditions2}
        where 
        `tabEmployee`.employment_type = "Recruit"
        {conditions1}
         
        """.format(conditions1=conditions1,conditions2=conditions2), filters, as_dict=1)
    for item_dict in item_result2:
        data = {
            'employee_name': item_dict.employee_name ,
            'name': item_dict.name ,
            'overnight': item_dict.overnight ,
        }
        item_results = frappe.db.sql("""
            select
                recruit, employee_name, start_date, start_time, end_date, end_time, notes
            from
                `tabRecruit Vacation`
            where
                `tabRecruit Vacation`.docstatus = 1
                and `tabRecruit Vacation`.recruit = '{recruit}'
                {conditions}
            """.format(conditions=conditions,recruit=item_dict.name), filters, as_dict=1)

        for x in item_results:
            data['start_date'] = x.start_date
            data['start_time'] = x.start_time
            data['end_date'] = x.end_date
            data['end_time'] = x.end_time
            data['notes'] = x.notes
        result.append(data)
    return result