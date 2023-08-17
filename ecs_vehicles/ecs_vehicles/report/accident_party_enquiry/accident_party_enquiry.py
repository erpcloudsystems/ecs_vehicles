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
            "label": _("اسم الشخص"),
            "fieldname": "party_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("نوع البطاقة"),
            "fieldname": "party_id_type",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("رقم البطاقة"),
            "fieldname": "party_id",
            "fieldtype": "Data",
            "width": 170
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
            "label": _("قيمة الخصم"),
            "fieldname": "deduction_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("مصاريف إدارية"),
            "fieldname": "administrative_expenses",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("القيمة الإجمالية للخصم"),
            "fieldname": "total_deduction_amount",
            "fieldtype": "Currency",
            "width": 150
        },
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
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("party_id"):
        conditions += "and party_id = %(party_id)s"
    if filters.get("party_id_type"):
        conditions += "and party_id_type = %(party_id_type)s"
    if filters.get("police_no"):
        conditions += "and police_no = %(police_no)s"
    if filters.get("fiscal_year"):
        conditions += "and fiscal_year = %(fiscal_year)s"
    if filters.get("entity"):
        conditions += "and entity = %(entity)s"
    if filters.get("accident_type"):
        conditions += "and accident_type = %(accident_type)s"
    if filters.get("accident_no"):
        conditions += "and accident_no = %(accident_no)s"
    if filters.get("party_name"):
        conditions += "and party_name = %(party_name)s"

    result = []
    item_results = frappe.db.sql("""
        select
            name, police_no, fiscal_year, accident_no, accident_date, accident_type, entity, deduction_amount, 
            administrative_expenses, total_deduction_amount, party_name, party_id, party_id_type
        from
            `tabAccident`
        where
            `tabAccident`.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'party_name': item_dict.party_name,
            'party_id': item_dict.party_id,
            'party_id_type': item_dict.party_id_type,
            'police_no': item_dict.police_no,
            'entity': item_dict.entity,
            'accident_no': str(item_dict.accident_no),
            'name': item_dict.name,
            'fiscal_year': item_dict.fiscal_year,
            'accident_date': item_dict.accident_date,
            'accident_type': item_dict.accident_type,
            'deduction_amount': item_dict.deduction_amount,
            'administrative_expenses': item_dict.administrative_expenses,
            'total_deduction_amount': item_dict.total_deduction_amount,
        }
        result.append(data)
    return result