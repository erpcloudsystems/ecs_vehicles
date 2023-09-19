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
            "label": _("كود المزاد"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Auction Info",
            "width": 140,
        },
        {
            "label": _("تاريخ المزاد"),
            "fieldname": "auction_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": _("رقم اللوط"),
            "fieldname": "idx",
            "fieldtype": "Integer",
            "width": 150,
        },
        {
            "label": _("عدد البونات"),
            "fieldname": "count_voucher",
            "fieldtype": "Integer",
            "width": 120,
        },
        {
            "label": _("رقم اللوط المجمع"),
            "fieldname": "accumulated_lot",
            "fieldtype": "Integer",
            "width": 120,
        },
        {
            "label": _("رقم الشرطة"),
            "fieldname": "police_id",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("النوع"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("الموديل"),
            "fieldname": "vehicle_model",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("اللون"),
            "fieldname": "vehicle_color",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("الشاسيه"),
            "fieldname": "chassis_no",
            "fieldtype": "Data",
            "width": 160,
        },
        {
            "label": _("الموتور"),
            "fieldname": "motor_no",
            "fieldtype": "Data",
            "width": 160,
        },
    ]


def get_data(filters, columns):
    conditions = get_conditions(filters)
    item_price_qty_data = get_item_price_qty_data(conditions)
    return item_price_qty_data

def get_conditions(filters):
    conditions = ""
    if filters.get("name"):
        conditions += " AND auction.name=%s" % frappe.db.escape(filters.get("name"))
    if filters.get("police_no"):
        conditions += " AND auction_slips.police_id=%s" % frappe.db.escape(
            filters.get("police_no")
        )
    if filters.get("lot_no"):
        conditions += " AND auction_slips.idx=%s" % frappe.db.escape(
            filters.get("lot_no")
        )
    if filters.get("grouped_lot_no"):
        conditions += " AND auction_slips.accumulated_lot=%s" % frappe.db.escape(filters.get("grouped_lot_no"))
    if filters.get("from_date"):
        conditions += " AND auction.auction_date>='%s'" % filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND auction.auction_date<='%s'" % filters.get("to_date")
    return conditions


def get_item_price_qty_data(conditions):
    voucher_type_list = frappe.db.sql(
        """
        select  
			auction.name,
            auction.auction_date,
            auction_slips.idx,
            auction_slips.accumulated_lot,
            auction_slips.vehicle,
            auction_slips.police_id,
            auction_slips.entity,
            auction_slips.vehicle_type,
            auction_slips.vehicle_style,
            auction_slips.vehicle_shape,
            auction_slips.vehicle_brand,
            auction_slips.vehicle_model,
            auction_slips.vehicle_color,
            auction_slips.chassis_no,
            auction_slips.motor_no            
        from `tabAuction Info` auction
        join `tabAuction Sales Slips` auction_slips on auction_slips.parent = auction.name
        where auction.docstatus = 1
        {conditions}

        ORDER BY 
            auction.auction_date DESC
        
        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )
    if voucher_type_list:
        return voucher_type_list
