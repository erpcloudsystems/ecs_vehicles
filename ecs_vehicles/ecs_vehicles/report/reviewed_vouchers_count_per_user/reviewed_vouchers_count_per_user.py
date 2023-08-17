# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("إسم المستخدم"),
            "fieldname": "username",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("عدد البونات التي تم تسويتها"),
            "fieldname": "vouchers_count",
            "fieldtype": "Int",
            "width": 300
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabVoucher`.review_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabVoucher`.review_date <= %(to_date)s"

    user_list = frappe.db.sql(
        """ select distinct `tabVoucher`.username as username
            from `tabVoucher` 
            where `tabVoucher`.reviewed = 1
            {conditions}
            group by `tabVoucher`.username
        """.format(conditions=conditions), filters, as_dict=1)

    result = []
    if user_list:
        for x in user_list:
            data = {
                'username': x.username
            }
            item_results = frappe.db.sql(
				""" select count(`tabVoucher`.name) as vouchers_count
					from `tabVoucher` 
					where `tabVoucher`.reviewed = 1
					{conditions}
					and `tabVoucher`.username = '{username}'
				""".format(conditions=conditions, username=x.username), filters, as_dict=1)

            for item_dict in item_results:
                data['vouchers_count'] = item_dict.vouchers_count
            result.append(data)
    return result