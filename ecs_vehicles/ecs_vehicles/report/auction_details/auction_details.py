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
    
    total_count = "<b> العدد الإجمالي: {0}<span style='margin-right:50px'></span></b> ".format(data[0]["total_count"])
    header = " "  + total_count

    message = [header]
    return columns, data, message


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
            "width": 120,
        },
        {
            "label": _("رقم اللوط"),
            "fieldname": "idx",
            "fieldtype": "Integer",
            "width": 100,
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
            "width": 120,
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("النوع"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("الموديل"),
            "fieldname": "vehicle_model",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("اللون"),
            "fieldname": "vehicle_color",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("الشاسيه"),
            "fieldname": "chassis_no",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("الموتور"),
            "fieldname": "motor_no",
            "fieldtype": "Data",
            "width": 120,
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
    result = []
    item_results = frappe.db.sql(
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
    counter = 0
    for item_dict in item_results:
        counter += 1
        data = {
            'name': item_dict.name,
            'auction_date': item_dict.auction_date,
            'idx': item_dict.idx,
            'accumulated_lot': item_dict.accumulated_lot,
            'vehicle': item_dict.vehicle,
            'police_id': item_dict.police_id,
            'entity': item_dict.entity,
            'vehicle_type': item_dict.vehicle_type,
            'vehicle_style': item_dict.vehicle_style,
            'vehicle_shape': item_dict.vehicle_shape,
            'vehicle_brand': item_dict.vehicle_brand,
            'vehicle_model': item_dict.vehicle_model,
            'vehicle_color': item_dict.vehicle_color,
            'chassis_no': item_dict.chassis_no,
            'motor_no': item_dict.motor_no,
        }
        result.append(data)
    try:
        result[0]["total_count"] = counter
    except:
        pass
    return result