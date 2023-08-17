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
    # header = ""
    # print = "<b> <a style = 'color:blue;' href='/app/print/Liquids%20Issuing/{0}'>{1}</a> </b> <br>".format(filters.get("liquids_issuing"), "طباعة الصرفية")
    # entity = "<b> الصرفية إلى: </b>{0}  <br>".format(data[0]["issue_to"])
    # date = "<b> تاريخ الصرفية: </b> {0} <br>".format(data[0]["issue_date"])
    # from_date = "<b>  الصرفية عن الفترة من: </b> {0} <br>".format(data[0]["from_date"])
    # to_date = "<b>  الصرفية عن الفترة إلى: </b> {0} <br>".format(data[0]["to_date"])

    # issue_state = """<b > موقف الصرفية: </b> <span style="color:red; font-weight:bold;">{0}</span> <br>""".format(data[0]["issue_state"])
    # if data[0]["issue_state"] == "جاري تحضير الصرفية ومراجعتها":
    #     issue_state = """<b > موقف الصرفية: </b> <span style="color:green; font-weight:bold;">{0}</span> <br>""".format(data[0]["issue_state"])
    # if data[0]["issue_state"]:
    #     header = " " + print + " " + entity + " " + date + " " + from_date + " " + to_date + " " + issue_state
    # else:
    #     header = " "  + print + " " + entity + " " + date + " " + from_date + " " + to_date

    # message = [header]
    return columns, data


def get_columns():
    return [
        {
            "label": _("السائل"),
            "fieldname": "liquid",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("الكمية المنصرفة"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("عدد الدفاتر"),
            "fieldname": "coupon_count",
            "fieldtype": "Data",
            "width": 350
        },

    ]


def get_data(filters, columns):
    get_qty_per_liquid = []
    get_qty_per_liquid = get_qty_per_liquids(filters)
    return get_qty_per_liquid


def get_qty_per_liquids(filters):
    conditions = ""
    if filters.get("issue_type"):
        conditions += " and liquid_voucher_issuing.issue_type ='%s'" % filters.get("issue_type")
    if filters.get("entity"):
        conditions += " and liquid_voucher_issuing.entity ='%s'" % filters.get("entity")

    if filters.get("from_date"):
        conditions += " AND liquid_voucher_issuing.issue_date >='%s'" % filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND liquid_voucher_issuing.issue_date <='%s'" % filters.get("to_date")
    # if filters.get("liquids_issuing"):
    #     conditions += " AND liquid_voucher_issuing.name ='%s'" % filters.get("liquids_issuing")
    item_results = frappe.db.sql("""
        Select
            vouchers_issued_per_liquid.liquid as liquid,
            SUM(vouchers_issued_per_liquid.voucher_qty) as qty,
            SUM(vouchers_issued_per_liquid.notebook_count)as notebook_count
        from `tabLiquid Vouchers Issuing` liquid_voucher_issuing join `tabVouchers Issued Per Liquid` vouchers_issued_per_liquid
        on vouchers_issued_per_liquid.parent = liquid_voucher_issuing.name
        where liquid_voucher_issuing.docstatus = 1
        and vouchers_issued_per_liquid.docstatus = 1
        AND (vouchers_issued_per_liquid.voucher_qty > 0 or vouchers_issued_per_liquid.voucher_qty is not null)
        {conditions}
        GROUP BY vouchers_issued_per_liquid.liquid
        ORDER BY liquid 
        """.format(conditions=conditions), as_dict=1)
    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                "liquid": item_dict.liquid,
                'qty': item_dict.qty,
                'coupon_count': item_dict.notebook_count,
            }
            result.append(data)
        return result