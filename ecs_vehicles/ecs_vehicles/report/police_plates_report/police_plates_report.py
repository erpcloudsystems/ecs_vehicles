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
            "label": _("التاريخ"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": _("كود المركبة"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Vehicles",
            "width": 110
        },
        {
            "label": _("النوع"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("الموديل"),
            "fieldname": "vehicle_model",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("اللون"),
            "fieldname": "vehicle_color",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("رقم الموتور"),
            "fieldname": "motor_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("رقم الشاسيه"),
            "fieldname": "chassis_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("رقم الملاكي"),
            "fieldname": "private_no",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الحالة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("جهة الصيانة"),
            "fieldname": "maintenance_entity",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("نوع التجهيز"),
            "fieldname": "processing_type",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("مخصص الصرف"),
            "fieldname": "exchange_allowance",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("تاريخ الحيازة"),
            "fieldname": "possession_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("نوع الوقود"),
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("السعة اللترية"),
            "fieldname": "litre_capacity",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("عدد السلندرات"),
            "fieldname": "cylinder_count",
            "fieldtype": "Data",
            "width": 110
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("plate_no"):
        conditions += " and logs.value = %(plate_no)s"

    item_results = frappe.db.sql("""
        Select
            logs.date as date,
            vehicle.name as name,
            vehicle.vehicle_no as vehicle_no,
            vehicle.police_id as police_id,
            vehicle.vehicle_type as vehicle_type,
            vehicle.vehicle_shape as vehicle_shape,
            vehicle.vehicle_brand as vehicle_brand,
            vehicle.vehicle_style as vehicle_style,
            vehicle.vehicle_model as vehicle_model,
            vehicle.vehicle_color as vehicle_color,
            vehicle.entity_name as entity_name,
            vehicle.motor_no as motor_no,
            vehicle.chassis_no as chassis_no,
            vehicle.private_no as private_no,
            vehicle.vehicle_status as vehicle_status,
            vehicle.maintenance_entity as maintenance_entity,
            vehicle.processing_type as processing_type,
            vehicle.exchange_allowance as exchange_allowance,
            vehicle.possession_date as possession_date,
            vehicle.fuel_type as fuel_type,
            vehicle.litre_capacity as litre_capacity,
            vehicle.cylinder_count as cylinder_count
        from `tabVehicles` vehicle join `tabPolice Plate Logs` logs
        on logs.parent = vehicle.name
        where 1 = 1
        {conditions}
        order by date DESC
        """.format(conditions=conditions), filters, as_dict=1)
    # return item_results
    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                "date": item_dict.date,
                'name': item_dict.name,
                'vehicle_no': item_dict.vehicle_no if item_dict.vehicle_no else item_dict.police_id,
                'vehicle_type': item_dict.vehicle_type if item_dict.vehicle_type else "-----------",
                'vehicle_shape': item_dict.vehicle_shape if item_dict.vehicle_shape else "-----------",
                'vehicle_brand': item_dict.vehicle_brand if item_dict.vehicle_brand else "-----------",
                'vehicle_style': item_dict.vehicle_style if item_dict.vehicle_style else "-----------",
                'vehicle_model': item_dict.vehicle_model if item_dict.vehicle_model else "-----------",
                'vehicle_color': item_dict.vehicle_color if item_dict.vehicle_color else "-----------",
                'entity_name': item_dict.entity_name if item_dict.entity_name else "-----------",
                'motor_no': item_dict.motor_no if item_dict.motor_no else "-----------",
                'chassis_no': item_dict.chassis_no if item_dict.chassis_no else "-----------",
                'private_no': item_dict.private_no if item_dict.private_no else "-----------",
                'vehicle_status': item_dict.vehicle_status if item_dict.vehicle_status else "-----------",
                'maintenance_entity': item_dict.maintenance_entity if item_dict.maintenance_entity else "-----------",
                'processing_type': item_dict.processing_type if item_dict.processing_type else "-----------",
                'exchange_allowance': item_dict.exchange_allowance if item_dict.exchange_allowance else "-----------",
                'possession_date': item_dict.possession_date if item_dict.possession_date else "-----------",
                'fuel_type': item_dict.fuel_type if item_dict.fuel_type else "-----------",
                'litre_capacity': item_dict.litre_capacity if item_dict.litre_capacity else "-----------",
                'cylinder_count': item_dict.cylinder_count if item_dict.cylinder_count else "-----------",
            }
            result.append(data)
        return result