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
			"label": _("إسم الجهة التابعة لها"),
			"fieldname": "entity",
			"fieldtype": "Data",
			"width": 220
		},
        {
            "label": _("حالة المركبة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("إسم البون"),
            "fieldname": "voucher",
            "fieldtype": "Data",
            "width": 200
        },
		{
			"label": _("الكمية بالعدد"),
			"fieldname": "qty",
			"fieldtype": "Int",
			"width": 110
		},
        {
            "label": _("بداية الفترة"),
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("نهاية الفترة"),
            "fieldname": "to_date",
            "fieldtype": "Date",
            "width": 100
        },

    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    result = []
    item_results = frappe.db.sql("""
        select
            `tabLiquids Issuing Table`.entity, 
            `tabLiquids Issuing Table`.vehicle_status,
            `tabLiquids Issuing Table`.voucher,
            `tabLiquids Issuing Table`.qty,
            `tabLiquids Issuing Table`.from_date,
        	`tabLiquids Issuing Table`.to_date
        from
            `tabLiquids Issuing Table`
        where
            `tabLiquids Issuing Table`.parent = '{name}'
            and `tabLiquids Issuing Table`.issue_type = "غسيل"
        order by
        	`tabLiquids Issuing Table`.from_date
        """.format(name=filters.get("name")), filters, as_dict=1)

    total = frappe.db.sql("""
        select
            SUM(`tabLiquids Issuing Table`.qty) as sum_qty
        from
            `tabLiquids Issuing Table`
        where
            `tabLiquids Issuing Table`.parent = '{name}'
            and `tabLiquids Issuing Table`.issue_type = "غسيل"
        """.format(name=filters.get("name")), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'entity': item_dict.entity,
            'vehicle_status': item_dict.vehicle_status,
            'voucher': item_dict.voucher,
            'qty': item_dict.qty,
            'from_date': item_dict.from_date,
            'to_date': item_dict.to_date,
            "plate_no": frappe.db.get_value("Vehicles", filters.get("name"), ["vehicle_no"]),
            "fuel_type": frappe.db.get_value("Vehicles", filters.get("name"), ["fuel_type"]),
            "entity_name": frappe.db.get_value("Vehicles", filters.get("name"), ["entity_name"]),
            "vehicle_type": frappe.db.get_value("Vehicles", filters.get("name"), ["vehicle_type"]),
            "vehicle_shape": frappe.db.get_value("Vehicles", filters.get("name"), ["vehicle_shape"]),
            "vehicle_brand": frappe.db.get_value("Vehicles", filters.get("name"), ["vehicle_brand"]),
            "vehicle_style": frappe.db.get_value("Vehicles", filters.get("name"), ["vehicle_style"]),
            "vehicle_model": frappe.db.get_value("Vehicles", filters.get("name"), ["vehicle_model"]),
            "possession_date": frappe.db.get_value("Vehicles", filters.get("name"), ["possession_date"]),
            "total_qty": "",
            "cur_user": frappe.session.user,

        }
        result.append(data)

    if result:
        result[0]["total_qty"] = total[0]["sum_qty"]
    return result