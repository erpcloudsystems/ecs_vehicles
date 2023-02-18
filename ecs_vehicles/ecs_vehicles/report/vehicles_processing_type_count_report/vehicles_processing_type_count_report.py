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
            "label": _("نوع التجهيز"),
            "fieldname": "processing_type",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("إجمالي"),
            "fieldname": "total_count",
            "fieldtype": "Integer",
            "width": 150
        },
        {
            "label": _("صالح"),
            "fieldname": "valid",
            "fieldtype": "Integer",
            "width": 150
        },
        {
            "label": _("عاطل"),
            "fieldname": "broken",
            "fieldtype": "Integer",
            "width": 150
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    vehicles_list = frappe.db.sql("""
        Select
			processing_type as processing_type,
			count(name) as total_count
		from `tabVehicles`
		where vehicle_status != "مخردة"
		and processing_type is not null
		group by processing_type
		order by count(name) desc
        """, as_dict=1)

    result = []
    if vehicles_list:
        for x in vehicles_list:
            data = {
                'processing_type': x.processing_type,
				'total_count': x.total_count,
            }
            item_results = frappe.db.sql("""
                select
                    (select count(name) from `tabVehicles`
                    where `tabVehicles`.vehicle_status = 'صالحة'
					and `tabVehicles`.processing_type = '{processing_type}') as valid
				from
                    `tabVehicles`
                where
                   `tabVehicles`.processing_type = '{processing_type}'
                """.format(processing_type=x.processing_type), filters, as_dict=1)


            for item_dict in item_results:
                data['valid'] = item_dict.valid
                data['broken'] = x.total_count - item_dict.valid

            result.append(data)
    return result



