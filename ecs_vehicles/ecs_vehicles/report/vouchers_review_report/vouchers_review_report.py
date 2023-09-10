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
            "label": _("تاريخ التسوية"),
            "fieldname": "revision_date",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("مستند التسوية"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Vouchers Review",
            "width": 150
        },
        {
            "label": _("اسم الشركة"),
            "fieldname": "company_name",
            "fieldtype": "Link",
            "options": "Gas Station",
            "width": 150
        },
        {
            "label": _("تاريخ الدفعة"),
            "fieldname": "batch_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("رقم الدفعة"),
            "fieldname": "batch_no",
            "fieldtype": "Integer",
            "width": 100
        },
        {
            "label": _("المجموعة"),
            "fieldname": "group_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("فئة البون"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("العدد"),
            "fieldname": "total_count",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("اسم المستخدم"),
            "fieldname": "user",
            "fieldtype": "Data",
            "width": 200
        },
    ]


def get_data(filters, columns):
    get_qty_per_liquid = []
    get_qty_per_liquid = get_qty_per_liquids(filters)
    return get_qty_per_liquid


def get_qty_per_liquids(filters):
    conditions = ""
    conditions2 = "" 
    if filters.get("company_name"):
        conditions += " and voucher_review.company_name ='%s'" % filters.get("company_name")
    if filters.get("fiscal_year"):
        conditions += " and voucher_review.fiscal_year ='%s'" % filters.get("fiscal_year")
    if filters.get("group_no"):
        conditions += " AND voucher_review.group_no ='%s'" % filters.get("group_no")
    if filters.get("user"):
        conditions += " AND voucher_review.owner ='%s'" % filters.get("user")
    if filters.get("entity"):
        conditions2 += " AND voucher_revie_table.entity ='%s'" % filters.get("entity")
    if filters.get("voucher_type"):
        conditions2 += " AND voucher_revie_table.voucher_type LIKE '%{0}%' ".format(filters.get("voucher_type"))

    if filters.get("batch_no"):
        conditions += " AND voucher_review.batch_no ='%s'" % filters.get("batch_no")

    if filters.get("batch_from_date"):
        conditions += " AND voucher_review.batch_date >='%s'" % filters.get("batch_from_date")

    if filters.get("batch_to_date"):
        conditions += " AND voucher_review.batch_date <='%s'" % filters.get("batch_to_date")
    if filters.get("revision_from_date"):
        conditions += " AND voucher_review.date >='%s'" % filters.get("revision_from_date")

    if filters.get("revision_to_date"):
        conditions += " AND voucher_review.date <='%s'" % filters.get("revision_to_date")
    item_results = frappe.db.sql("""
        Select
                voucher_review.name as name,
                voucher_review.owner as user,
                voucher_review.company_name as company_name,
                voucher_review.batch_no as batch_no,
                voucher_review.batch_date as batch_date,
                voucher_review.date as revision_date,
                voucher_review.group_no,
                voucher_review.counter
        from `tabVouchers Review` voucher_review
        where voucher_review.docstatus = 1        
        {conditions}
        ORDER BY user, batch_no, CONVERT(voucher_review.group_no, SIGNED)
        """.format(conditions=conditions), as_dict=1)
    def item_results_map(parent, conditions):
        return frappe.db.sql("""
        Select
                voucher_revie_table.voucher_type as voucher_type,
                COUNT(voucher_revie_table.voucher_type ) AS voucher_type_count
        from `tabVouchers Review` voucher_review 
        join `tabReview Vouchers Table` voucher_revie_table on voucher_revie_table.parent = voucher_review.name
        where voucher_review.docstatus = 1
        AND voucher_revie_table.parent = "{parent}"
        {conditions}
        GROUP BY voucher_type 
        """.format(parent=parent, conditions=conditions), as_dict=1)

    user_printed = frappe.session.user
    # frappe.msgprint(str(user_printed))
    result = []
    users = []
    users_dict = {}
    if item_results:
        for item_dict in item_results:
            result_map = item_results_map(item_dict.name, conditions)
            cur_user = frappe.db.get_value("User", {"name":item_dict.user}, ["full_name"])
            if not users_dict.get(cur_user):
                users_dict[cur_user] = cur_user
                users.append(cur_user)

            for row in result_map:
                data = {
                "name": item_dict.name,
                "user": cur_user,
                "company_name": item_dict.company_name,
                'batch_no': item_dict.batch_no,
                'batch_date': item_dict.batch_date,
                'revision_date': item_dict.revision_date,
                'group_no': str(item_dict.group_no),
                'voucher_type': row.voucher_type,
                'total_count': row.voucher_type_count,
                "cur_user":user_printed
                
            }
                result.append(data)
        result[-1]["users"] = users
        return result