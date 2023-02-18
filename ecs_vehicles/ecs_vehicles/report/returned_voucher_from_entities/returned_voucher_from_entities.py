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
        {"label": _("الجهة"), "fieldname": "entity", "fieldtype": "Link", "options":"Entity","width": 300},
        {
            "label": _("بنزين 95"),
            "fieldname": "fuel_95",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("بنزين 92"),
            "fieldname": "fuel_92",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("بنزين 80"),
            "fieldname": "fuel_80",
            "fieldtype": "Data",
            "width": 100,
        },
        {"label": _("سولار"), "fieldname": "solar", "fieldtype": "Data", "width": 100},
        {"label": _("غاز"), "fieldname": "gas", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters, columns):
    get_qty_per_liquid = []
    get_qty_per_liquid = get_qty_per_liquids(filters)
    return get_qty_per_liquid

def get_qty_per_liquids(filters):
    conditions = ""
    conditions1 = ""
    if filters.get("from_date"):
        conditions += " AND write_off.posting_date >='%s'" % filters.get("from_date")
    if filters.get("to_date")   :
        conditions += " AND write_off.posting_date <='%s'" % filters.get("to_date")
    if filters.get("release_date"):
        conditions += " AND write_off.release_date ='%s'" % filters.get("release_date")
    if filters.get("entity"):
        conditions1 += " AND write_off.entity ='%s'" % filters.get("entity")

    types = frappe.db.sql(
        """
        Select
                    entity
        from `tabLiquids Write Off` write_off
        where write_off.docstatus = 1
        {conditions1}
        group by write_off.entity
        """.format(conditions1=conditions1),
        as_dict=1,
    )

    result = []
    for type in types:
        fuel_95 = frappe.db.sql(
            """
        Select SUM(if (write_off_table.uom = "دفتر", write_off_table.remaining_qty * 25 , write_off_table.remaining_qty) ) as remaining_qty
        from `tabLiquids Write Off` write_off
        JOIN `tabLiquids Write Off Table` write_off_table ON write_off.name = write_off_table.parent
        where write_off.docstatus = 1
        AND write_off_table.liquid_voucher = 'بنزين 95 فئة 30 لتر' 
        AND write_off.entity = "{type}"
        {conditions}
        """.format(type=type.entity, conditions=conditions),
            as_dict=1,
        )
        fuel_92 = frappe.db.sql(
            """
        Select SUM(if (write_off_table.uom = "دفتر", write_off_table.remaining_qty * 25 , write_off_table.remaining_qty) ) as remaining_qty
        from `tabLiquids Write Off` write_off
        JOIN `tabLiquids Write Off Table` write_off_table ON write_off.name = write_off_table.parent
        where write_off.docstatus = 1
        AND write_off_table.liquid_voucher = 'بنزين 92 فئة 20 لتر' 
        AND write_off.entity = "{type}"
        {conditions}
        """.format(type=type.entity,conditions=conditions),
            as_dict=1,
        )
        fuel_80 = frappe.db.sql(
            """
        Select SUM(if (write_off_table.uom = "دفتر", write_off_table.remaining_qty * 25 , write_off_table.remaining_qty) ) as remaining_qty
        from `tabLiquids Write Off` write_off
        JOIN `tabLiquids Write Off Table` write_off_table ON write_off.name = write_off_table.parent
        where write_off.docstatus = 1
        AND write_off_table.liquid_voucher = 'بنزين 80 فئة 20 لتر' 
        AND write_off.entity = "{type}"
        {conditions}
        """.format(type=type.entity,conditions=conditions),
            as_dict=1,
        )
        solar = frappe.db.sql(
            """
        Select SUM(if (write_off_table.uom = "دفتر", write_off_table.remaining_qty * 25 , write_off_table.remaining_qty) ) as remaining_qty
        from `tabLiquids Write Off` write_off
        JOIN `tabLiquids Write Off Table` write_off_table ON write_off.name = write_off_table.parent
        where write_off.docstatus = 1
        AND write_off_table.liquid_voucher = 'سولار فئة 40 لتر' 
        AND write_off.entity = "{type}"
        {conditions}
        """.format(type=type.entity,conditions=conditions),
            as_dict=1,
        )
        gas = frappe.db.sql(
            """
        Select SUM(if (write_off_table.uom = "دفتر", write_off_table.remaining_qty * 25 , write_off_table.remaining_qty) ) as remaining_qty
        from `tabLiquids Write Off` write_off
        JOIN `tabLiquids Write Off Table` write_off_table ON write_off.name = write_off_table.parent
        where write_off.docstatus = 1
        AND write_off_table.liquid_voucher = 'غاز طبيعي فئة 15 متر مكعب' 
        AND write_off.entity = "{type}"
        {conditions}
        """.format(type=type.entity,conditions=conditions),
            as_dict=1,
        )
        if fuel_95[0].remaining_qty and fuel_92[0].remaining_qty and fuel_80[0].remaining_qty and gas[0].remaining_qty and solar[0].remaining_qty :
            data = {
                "entity": type.entity,
                "fuel_95": fuel_95[0].remaining_qty or "0",
                "fuel_92": fuel_92[0].remaining_qty or "0",
                "fuel_80": fuel_80[0].remaining_qty or "0",
                "solar": solar[0].remaining_qty or "0",
                "gas": gas[0].remaining_qty or "0",
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
                "qty": item_dict.qty,
                "in_words": item_dict.in_words,
                "issue_to": item_dict.issue_to,
                "issue_date": item_dict.issue_date,
                "from_date": item_dict.from_date,
                "to_date": item_dict.to_date,
                "issue_state": item_dict.issue_state,
            }
            result.append(data)
        return result

