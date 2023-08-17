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
            "label": _("رقم المركبة"),
			"fieldname": "vehicle_no",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("الماركة / الطراز"),
			"fieldname": "brand_style",
			"fieldtype": "Data",
			"width": 160
		},
        {
			"label": _("الموديل"),
			"fieldname": "vehicle_model",
			"fieldtype": "Data",
			"width": 80
		},
        {
            "label": _("الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Data",
            "width": 280
        },
        {
            "label": _("المتعهد"),
            "fieldname": "supplier",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("أمر الشغل"),
            "fieldname": "job_order_no",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("تاريخه"),
            "fieldname": "job_order_date",
            "fieldtype": "Date",
            "width": 100
        },
		{
            "label": _("قيمته"),
            "fieldname": "job_order_amount",
            "fieldtype": "Float",
            "width": 120
        },
                {
            "label": _("الفحص"),
            "fieldname": "checkup",
            "fieldtype": "Data",
            "width": 100
        },

    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("vehicle_no"):
        conditions += "and a.vehicle_no = %(vehicle_no)s"
    if filters.get("entity_name"):
        conditions += "and a.entity_name = %(entity_name)s"
    if filters.get("vehicle_brand"):
        conditions += "and a.vehicle_brand = %(vehicle_brand)s"
    if filters.get("vehicle_style"):
        conditions += "and a.vehicle_style = %(vehicle_style)s"
    if filters.get("vehicle_model"):
        conditions += "and a.vehicle_model = %(vehicle_model)s"
    if filters.get("supplier"):
        conditions += "and a.supplier2 = %(supplier)s"
    if filters.get("from_date"):
        conditions += " and a.job_order_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and a.job_order_date <= %(to_date)s"
    if filters.get("job_order_no"):
        conditions += "and a.job_order_no = %(job_order_no)s"
    if filters.get("checkup") == "مسدد":
        conditions += "and a.purchase_invoices is not null"
    if filters.get("checkup") == "غير مسدد":
        conditions += "and a.purchase_invoices is null"

    result = []
    item_results = frappe.db.sql("""
        select
            a.vehicle_no, 
            a.vehicle_model, 
            a.vehicle_brand, 
            a.vehicle_style, 
			a.entity_name, 
			a.supplier2,
            a.job_order_no, 
            a.job_order_date, 
            a.aamr_shoghl_total_amount, 
            a.purchase_invoices
        from
            `tabVehicle Maintenance Process` a
        where
           	a.job_order_no is not null
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        checkup = ""
        if item_dict.purchase_invoices:
            checkup = "مسدد"
        if not item_dict.purchase_invoices:
            checkup = "غير مسدد"
        data = {
            'entity_name': item_dict.entity_name,
            'brand_style': str(item_dict.vehicle_brand) + " / " + str(item_dict.vehicle_style),
            'vehicle_no': item_dict.vehicle_no,
            'vehicle_model': item_dict.vehicle_model,
            'supplier': item_dict.supplier2,
            'job_order_no': item_dict.job_order_no,
            'job_order_date': item_dict.job_order_date,
            'job_order_amount': item_dict.aamr_shoghl_total_amount,
            'checkup': checkup,
        }
        result.append(data)
    return result