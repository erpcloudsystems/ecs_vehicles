# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": ("المجموعة"),
            "fieldname": "group",
            "fieldtype": "Int",
            "width": 150
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    from_group = filters.get("from_group")
    to_group = filters.get("to_group") + 1
    group_range_list = list(range(from_group, to_group))
    result = []
    data = {}
    reviewed_groups_list = []

    reviewed_groups_dict = frappe.db.sql(
        """ select CONVERT(group_no, SIGNED) as group_no
            from `tabVouchers Review` 
            where docstatus = 1
            and batch_no = '{batch_no}'
            and fiscal_year = '{fiscal_year}'
        """.format(batch_no=filters.get("batch_no"), fiscal_year=filters.get("fiscal_year")), filters, as_dict=1)
    
    for item in reviewed_groups_dict:
        reviewed_groups_list.append(item.group_no)
    
    if reviewed_groups_list:
        for x in group_range_list:
            if x not in reviewed_groups_list:
                data = {
                    "group": x
                }
                result.append(data)

    return result