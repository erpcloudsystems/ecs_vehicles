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
            "label": _("إسم البون"),
            "fieldname": "voucher_type",
            "fieldtype": "Link",
            "options": "Oil Type",
            "width": 150
        },
        {
            "label": _("من مسلسل"),
            "fieldname": "from_serial",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("إلى مسلسل"),
            "fieldname": "to_serial",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("عدد البونات"),
            "fieldname": "count_voucher",
            "fieldtype": "Integer",
            "width": 120
        },
        {
            "label": _("عدد الدفاتر"),
            "fieldname": "count_notebook",
            "fieldtype": "Integer",
            "width": 120
        },
        {
            "label": _("سعر الوحدة"),
            "fieldname": "unit_price",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": _("إجمالي السعر"),
            "fieldname": "total_price",
            "fieldtype": "Currency",
            "width": 160
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    voucher_type_list = frappe.db.sql("""
        select distinct `tabVoucher`.voucher_type as voucher_type
        from `tabVoucher` where `tabVoucher`.liquid_type = "غسيل" 
        group by `tabVoucher`.voucher_type
        """, as_dict=1)

    result = []
    if voucher_type_list:
        for x in voucher_type_list:
            data = {
                'voucher_type': x.voucher_type
            }
            item_results = frappe.db.sql("""
                select
                    ifnull(max(`tabVoucher`.serial_no),0) as max,
                    ifnull(min(`tabVoucher`.serial_no),0) as min,
                    (select `tabWashing Vouchers`.rate from `tabWashing Vouchers` 
                    where `tabWashing Vouchers`.name = '{voucher_type}') as rate

                from
                    `tabVoucher`
                where
                    `tabVoucher`.voucher_type = '{voucher_type}'
                    and `tabVoucher`.disabled = 0
                    and `tabVoucher`.serial_no > 0
                    and `tabVoucher`.liquid_type = "غسيل"
                    and `tabVoucher`.issue_no is null

                """.format(voucher_type=x.voucher_type), filters, as_dict=1)

            for item_dict in item_results:
                data['from_serial'] = item_dict.min
                data['to_serial'] = item_dict.max
                data['count_voucher'] = frappe.db.count("Voucher", filters=[
                    ['serial_no', 'between', [int(item_dict.min), int(item_dict.max)]], ['voucher_type', '=', x.voucher_type]]) if int(item_dict.max) - int(
                    item_dict.min) != 0 else 0
                data['count_notebook'] = frappe.db.count("Voucher", filters=[
                    ['serial_no', 'between', [int(item_dict.min), int(item_dict.max)]], ['voucher_type', '=', x.voucher_type]]) / 25 if int(
                    item_dict.max) - int(item_dict.min) != 0 else 0
                data['unit_price'] = item_dict.rate
                data['total_price'] = frappe.db.count("Voucher", filters=[
                    ['serial_no', 'between', [int(item_dict.min), int(item_dict.max)]], ['voucher_type', '=', x.voucher_type]]) * item_dict.rate if int(item_dict.max) - int(item_dict.min) != 0 else 0
                data["cur_user"] = frappe.session.user

            result.append(data)
    return result



