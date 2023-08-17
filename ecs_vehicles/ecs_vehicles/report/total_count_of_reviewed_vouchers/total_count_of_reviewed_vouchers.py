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
            "label": ("فئة البون"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 230
        },
        {
            "label": ("عدد البونات التي تم تسويتها"),
            "fieldname": "vouchers_count",
            "fieldtype": "Int",
            "width": 200
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    voucher_type_list = frappe.db.sql(
        """ select `tabVoucher`.voucher_type as voucher_type
            from `tabVoucher` 
            where `tabVoucher`.reviewed = 1
            and `tabVoucher`.batch_no = '{batch_no}'
            and `tabVoucher`.fiscal_year = '{fiscal_year}'
            group by `tabVoucher`.voucher_type
        """.format(batch_no=filters.get("batch_no"), fiscal_year=filters.get("fiscal_year")), filters, as_dict=1)

    result = []
    if voucher_type_list:
        for x in voucher_type_list:
            data = {
                'voucher_type': x.voucher_type
            }
            item_results = frappe.db.sql(
				""" select count(`tabVoucher`.name) as vouchers_count
					from `tabVoucher` 
					where `tabVoucher`.reviewed = 1
                    and `tabVoucher`.batch_no = '{batch_no}'
                    and `tabVoucher`.fiscal_year = '{fiscal_year}'
					and `tabVoucher`.voucher_type = '{voucher_type}'
				""".format(voucher_type=x.voucher_type, batch_no=filters.get("batch_no"), 
							fiscal_year=filters.get("fiscal_year")), filters, as_dict=1)

            for item_dict in item_results:
                data['vouchers_count'] = item_dict.vouchers_count
            result.append(data)
    return result
