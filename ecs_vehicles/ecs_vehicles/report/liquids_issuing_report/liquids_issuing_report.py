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
    header = ""
    print = "<b> <a style = 'color:blue;' href='/app/print/Liquids%20Issuing/{0}'>{1}</a> </b> <br>".format(
        filters.get("liquids_issuing"), "طباعة الصرفية"
    )
    
    # print2 = "<b> <a style = 'color:green;' href='/printpreview?doctype=Liquid+Vouchers+Issuing&name={0}&trigger_print=1&print_format=Vouchers+Issuing&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar'>{1}</a> </b> <br>".format(
    #     data[0]["lvi"], "طباعة صرفية البونات"
    # )
    entity = "<b> الصرفية إلى: </b>{0}  <br>".format(data[0]["issue_to"])
    date = "<b> تاريخ الصرفية: </b> {0} <br>".format(data[0]["issue_date"])
    from_date = "<b>  الصرفية عن الفترة من: </b> {0} <br>".format(data[0]["from_date"])
    to_date = "<b>  الصرفية عن الفترة إلى: </b> {0} <br>".format(data[0]["to_date"])

    issue_state = """<b > موقف الصرفية: </b> <span style="color:red; font-weight:bold;">{0}</span> <br>""".format(
        data[0]["issue_state"]
    )
    if data[0]["issue_state"] == "جاري تحضير الصرفية ومراجعتها":
        issue_state = """<b > موقف الصرفية: </b> <span style="color:green; font-weight:bold;">{0}</span> <br>""".format(
            data[0]["issue_state"]
        )
    if data[0]["issue_state"]:
        header = (
            " "
            + print
            + " "
            # + print2
            # + " "
            + entity
            + " "
            + date
            + " "
            + from_date
            + " "
            + to_date
            + " "
            + issue_state
        )
    else:
        header = (
            " " + print + " " + entity + " " + date + " " + from_date + " " + to_date
        )

    message = [header]
    return columns, data, message


def get_columns():
    return [
        {
            "label": _("السائل"),
            "fieldname": "liquid",
            "fieldtype": "Data",
            "width": 250,
        },
         {
            "label": _("عدد المركبات"),
            "fieldname": "vehicles_count",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("الكمية المقررة"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 150,
        },
    ]


def get_data(filters, columns):
    get_qty_per_liquid = []
    get_qty_per_liquid = get_qty_per_liquids(filters)
    return get_qty_per_liquid


def get_qty_per_liquids(filters):
    conditions = ""
    if filters.get("liquids_issuing"):
        conditions += " and liquid_issuing.name = %(liquids_issuing)s"
    item_results = frappe.db.sql(
        """
        Select
            qty_per_liquid.name as name,
            qty_per_liquid.liquid as liquid,
            qty_per_liquid.qty as qty,
            qty_per_liquid.vehicles_count as vehicles_count,
            liquid_issuing.issue_to as issue_to,
            liquid_issuing.issue_date as issue_date,
            liquid_issuing.from_date as from_date,
            liquid_issuing.to_date as to_date,
            liquid_issuing.issue_state as issue_state
        from `tabLiquids Issuing` liquid_issuing join `tabQty Per Liquid` qty_per_liquid
        on qty_per_liquid.parent = liquid_issuing.name
        where liquid_issuing.submitted = 1
        AND qty != 0
        {conditions}
        order by liquid
        """.format(
            conditions=conditions
        ),
        filters,
        as_dict=1,
    )
    result = []
    lvi = ""
    if item_results:
        for item_dict in item_results:
            # if frappe.db.exists("Liquid Vouchers Issuing", {'issue_no': filters.get("liquids_issuing")}):
            #     lvi = frappe.db.get_value("Liquid Vouchers Issuing", {'liquids_issuing': filters.get("liquids_issuing")}, "name")
            data = {
                "liquid": item_dict.liquid,
                "qty": item_dict.qty,
                "vehicles_count": item_dict.vehicles_count,
                "issue_to": item_dict.issue_to,
                "issue_date": item_dict.issue_date,
                "from_date": item_dict.from_date,
                "to_date": item_dict.to_date,
                "issue_state": item_dict.issue_state,
                # "lvi": lvi
            }
            result.append(data)
        return result
