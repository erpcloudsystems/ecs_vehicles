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
            "label": _("فئة البون"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("عدد البونات المصروفة"),
            "fieldname": "voucher_count",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("سعر البونات المصروفة"),
            "fieldname": "cost_voucher_count",
            "fieldtype": "Currency",
            "width": 250
        },
        {
            "label": _("عدد البونات التي تم تسويتها"),
            "fieldname": "voucher_count_reconceled",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("سعر البونات التي تم تسويتها"),
            "fieldname": "cost_voucher_count_reconceled",
            "fieldtype": "Currency",
            "width": 250
        },
        {
            "label": _("عدد البونات التي لم يتم تسويتها"),
            "fieldname": "voucher_count_not_reconceled",
            "fieldtype": "Data",
            "width": 350
        },
        {
            "label": _("سعر البونات التي لم يتم تسويتها"),
            "fieldname": "cost_voucher_count_not_reconceled",
            "fieldtype": "Currency",
            "width": 350
        },

        
    ]


def get_data(filters, columns):
    get_qty_per_liquid = []
    get_qty_per_liquid = get_qty_per_liquids(filters)
    return get_qty_per_liquid


def get_qty_per_liquids(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND issue_date >='%s'" % filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND issue_date <='%s'" % filters.get("to_date")
    if filters.get("release_date"):
        conditions += " AND release_date <='%s'" % filters.get("release_date")
    if filters.get("fuel") or filters.get("oil") or filters.get("gas") or filters.get("washing"):
        fuel = filters.get("fuel", 0)
        oil = filters.get("oil", 0)
        gas = filters.get("gas", 0)
        washing = filters.get("washing", 0)
        first = ""
        firsts = ""
        oils = ""
        gass = ""
        washings = ""
        if fuel:
            firsts = "وقود"
            first = "وقود"
        if oil:
            oils = "زيت"
            first = "زيت"
        if gas:
            gass = "غاز"
            first = "غاز"
        if washing:
            washings = "غسيل"
            first = "غسيل"
        conditions += " AND (liquid_type = '{0}' OR liquid_type = '{1}' OR liquid_type = '{2}' OR liquid_type = '{3}' OR liquid_type = '{4}' )".format(first ,firsts, oils , gass , washings)
    try:
        types = frappe.db.sql("""
        Select
        voucher_type as voucher_type
        from `tabVoucher` voucher
        where (voucher.liquid_type = '{0}' OR voucher.liquid_type = '{1}' OR voucher.liquid_type = '{2}' OR voucher.liquid_type = '{3}' OR voucher.liquid_type = '{4}' )
        group by voucher_type
        order by liquid_type desc
        """.format(first ,firsts, oils , gass , washings), as_dict=1)
    except:
        frappe.throw("برجاء تحديد نوع السائل")
    result = []
    for type in types:
        item_results = frappe.db.sql("""
        Select
            COUNT(name) as name_count
        from `tabVoucher` voucher
        where issue_date is NOT NULL
        AND voucher_type = '{type}'
        {conditions}
        """.format(conditions=conditions, type=type.voucher_type), as_dict=1)
        cost_item_results = frappe.db.sql("""
        Select
            SUM(voucher_price) as voucher_price
        from `tabVoucher` voucher
        where issue_date is NOT NULL
        AND voucher_type = '{type}'
        {conditions}
        """.format(conditions=conditions, type=type.voucher_type), as_dict=1)
        reconceled = frappe.db.sql("""
        Select
            COUNT(name) as name_count
        from `tabVoucher` voucher
        where issue_date is NOT NULL
        AND reviewed =1
        AND voucher_type = '{type}'
        {conditions}
        """.format(conditions=conditions, type=type.voucher_type), as_dict=1)
        cost_reconceled = frappe.db.sql("""
        Select
            SUM(voucher_price) as voucher_price
        from `tabVoucher` voucher
        where issue_date is NOT NULL
        AND reviewed =1
        AND voucher_type = '{type}'
        {conditions}
        """.format(conditions=conditions, type=type.voucher_type), as_dict=1)
        count_not_reconceled = frappe.db.sql("""
        Select
            COUNT(name) as name_count
        from `tabVoucher` voucher
        where issue_date is NOT NULL
        AND reviewed = 0
        AND voucher_type = '{type}'
        {conditions}
        """.format(conditions=conditions, type=type.voucher_type), as_dict=1)
        cost_count_not_reconceled = frappe.db.sql("""
        Select
            SUM(voucher_price) as voucher_price
        from `tabVoucher` voucher
        where issue_date is NOT NULL
        AND reviewed = 0
        AND voucher_type = '{type}'
        {conditions}
        """.format(conditions=conditions, type=type.voucher_type), as_dict=1)
        
        data = {
                "voucher_type":type.voucher_type,
                "voucher_count":item_results[0].name_count,
                "cost_voucher_count":cost_item_results[0].voucher_price,
                "voucher_count_reconceled":reconceled[0].name_count,
                "cost_voucher_count_reconceled":cost_reconceled[0].voucher_price,
                "voucher_count_not_reconceled":count_not_reconceled[0].name_count,
                "cost_voucher_count_not_reconceled":cost_count_not_reconceled[0].voucher_price,
            }
        result.append(data)
    return result
    # return [{
    #     "voucher_count":item_results[0].name_count,
    #     "voucher_count_reconceled":reconceled[0].name_count,
    #     "voucher_count_not_reconceled":count_not_reconceled[0].name_count,
    # }]
    result = []
    if item_results:
        for item_dict in item_results:
            item_dict
            data = {
                "voucher_count": len(item_results),
                'qty': item_dict.qty,
                'in_words': item_dict.in_words,
                'issue_to': item_dict.issue_to,
                'issue_date': item_dict.issue_date,
                'from_date': item_dict.from_date,
                'to_date': item_dict.to_date,
                'issue_state': item_dict.issue_state,
            }
            result.append(data)
        return result