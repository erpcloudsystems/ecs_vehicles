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
            "label": _("الكود"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 120,
            "hidden": 1
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("رقم الشرطة"),
            "fieldname": "vehicle_no",
            "fieldtype": "Data",
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
            "label": _("الحالة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("عدد السلندرات"),
            "fieldname": "cylinder_count",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("نوع الوقود"),
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("مقرر الوقود"),
            "fieldname": "litre_count",
            "fieldtype": "Integer",
            "width": 90
        },
        {
            "label": _("نوع الزيت"),
            "fieldname": "oil_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("مقرر الغاز"),
            "fieldname": "gas_count",
            "fieldtype": "Integer",
            "width": 90
        },
        {
            "label": _("بون الغسيل"),
            "fieldname": "washing_voucher",
            "fieldtype": "Data",
            "width": 150
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    conditions1 = ""
    conditions2 = ""
    if filters.get("name"):
        conditions1 += "and (vehicle_no = %(name)s or police_id = %(name)s) "
        conditions2 += "and boat_no = %(name)s "
    if filters.get("vehicle_type"):
        conditions1 += "and vehicle_type = %(vehicle_type)s"
    if filters.get("vehicle_type") and (filters.get("vehicle_type") != "لانش"):
        conditions2 += "and body_type = %(vehicle_type)s "
    if filters.get("vehicle_shape"):
        conditions1 += "and vehicle_shape = %(vehicle_shape)s"
        conditions2 += "and body_type = %(vehicle_shape)s"
    if filters.get("vehicle_brand"):
        conditions1 += "and vehicle_brand = %(vehicle_brand)s"
        conditions2 += "and boat_brand = %(vehicle_brand)s"
    if filters.get("vehicle_style"):
        conditions1 += "and vehicle_style = %(vehicle_style)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
    if filters.get("vehicle_model"):
        conditions1 += "and vehicle_model = %(vehicle_model)s"
        conditions2 += "and boat_model = %(vehicle_model)s"
    if filters.get("entity"):
        conditions1 += "and entity_name = %(entity)s"
        conditions2 += "and entity_name = %(entity)s"
    if filters.get("vehicle_status"):
        conditions1 += "and vehicle_status = %(vehicle_status)s"
        conditions2 += "and boat_validity = %(vehicle_status)s"
    if filters.get("fuel_type"):
        conditions1 += "and fuel_type = %(fuel_type)s"
        conditions2 += "and fuel_type = %(fuel_type)s"
    if filters.get("cylinder_count"):
        conditions1 += "and cylinder_count = %(cylinder_count)s"
        conditions2 += "and cylinder_count = %(cylinder_count)s"


    item_results = frappe.db.sql("""
        (
        SELECT
            name as name,
            vehicle_no as vehicle_no,
            police_id as police_id,
            vehicle_type as vehicle_type,
            vehicle_shape as vehicle_shape,
            vehicle_brand as vehicle_brand,
            vehicle_style as vehicle_style,
            vehicle_model as vehicle_model,
            entity_name as entity_name,
            vehicle_status as vehicle_status,
            fuel_type as fuel_type,
            cylinder_count as cylinder_count,
            litre_count as litre_count,
            oil_type as oil_type,
            gas_count as gas_count,
            washing_voucher as washing_voucher
        FROM `tabVehicles`
        WHERE 1=1
        {conditions1}
        )
    UNION
        (
        SELECT
            name as name,
            boat_no as vehicle_no,
            boat_no as police_id,
            'لانش' as vehicle_type,
            body_type as vehicle_shape,
            boat_brand as vehicle_brand,
            '-----------' as vehicle_style,
            boat_model as vehicle_model,
            entity_name as entity_name,
            boat_validity as vehicle_status,
            fuel_type as fuel_type,
            cylinder_count as cylinder_count,
            qty as litre_count,
            '-----------' as oil_type,
            '-----------' as gas_count,
            '-----------' as washing_voucher
        FROM `tabBoats`
        WHERE 1=1
        {conditions2}
        )
    ORDER BY entity_name desc, vehicle_type
        """.format(conditions1=conditions1, conditions2=conditions2), filters, as_dict=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'vehicle_no': item_dict.vehicle_no if item_dict.vehicle_no else item_dict.police_id,
                'entity_name': item_dict.entity_name if item_dict.entity_name else "-----------",
                'vehicle_type': item_dict.vehicle_type if item_dict.vehicle_type else "-----------",
                'vehicle_shape': item_dict.vehicle_shape if item_dict.vehicle_shape else "-----------",
                'vehicle_brand': item_dict.vehicle_brand if item_dict.vehicle_brand else "-----------",
                'vehicle_style': item_dict.vehicle_style if item_dict.vehicle_style else "-----------",
                'vehicle_model': item_dict.vehicle_model if item_dict.vehicle_model else "-----------",
                'vehicle_status': item_dict.vehicle_status if item_dict.vehicle_status else "-----------",
                'fuel_type': item_dict.fuel_type if item_dict.fuel_type else "-----------",
                'litre_capacity': item_dict.litre_capacity if item_dict.litre_capacity else "-----------",
                'cylinder_count': item_dict.cylinder_count if item_dict.cylinder_count else "-----------",
                'litre_count': item_dict.litre_count if item_dict.litre_count else "-----------",
                'oil_type': item_dict.oil_type if item_dict.oil_type else "-----------",
                'gas_count': item_dict.gas_count if item_dict.gas_count else "-----------",
                'washing_voucher': item_dict.washing_voucher if item_dict.washing_voucher else "-----------",
            }
            result.append(data)
    try:

        result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
    except:
        pass
        return result