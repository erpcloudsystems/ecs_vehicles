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
    
    total_count = "<b> عدد المركبات : {0}<span style='margin-right:50px'></span></b> ".format(data[0]["total_count"])
    header = " "  + total_count

    message = [header]
    return columns, data, message


def get_columns():
    return [
        {
            "label": _("كود المركبة"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Vehicles",
            "width": 110,
        },
        {
            "label": _("رقم الشرطة"),
            "fieldname": "vehicle_no",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("النوع"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 80,
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الموديل"),
            "fieldname": "vehicle_model",
            "fieldtype": "Data",
            "width": 80,
        },
        {
            "label": _("الحالة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("اللون"),
            "fieldname": "vehicle_color",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": _("رقم الموتور"),
            "fieldname": "motor_no",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("رقم الشاسيه"),
            "fieldname": "chassis_no",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("رقم الملاكي"),
            "fieldname": "private_no",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("جهة الصيانة"),
            "fieldname": "maintenance_entity",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": _("نوع التجهيز"),
            "fieldname": "processing_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("مخصص الصرف"),
            "fieldname": "exchange_allowance",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("نوع الحيازة"),
            "fieldname": "possession_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("تاريخ الحيازة"),
            "fieldname": "possession_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("نوع الوقود"),
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("السعة اللترية"),
            "fieldname": "litre_capacity",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("عدد السلندرات"),
            "fieldname": "cylinder_count",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("بون الوقود"),
            "fieldname": "fuel_voucher",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("مقرر الوقود"),
            "fieldname": "litre_count",
            "fieldtype": "Data",
            "width": 90,
        },
        {
            "label": _("نوع الزيت"),
            "fieldname": "oil_type",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("مقرر الزيت"),
            "fieldname": "oil_count",
            "fieldtype": "Data",
            "width": 90,
        },
        {
            "label": _("بون الغاز"),
            "fieldname": "gas_voucher",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("مقرر الغاز"),
            "fieldname": "gas_count",
            "fieldtype": "Data",
            "width": 90,
        },
        {
            "label": _("بون الغسيل"),
            "fieldname": "washing_voucher",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("مقرر الغسيل"),
            "fieldname": "washing_count",
            "fieldtype": "Data",
            "width": 95,
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
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
    if filters.get("vehicle_color"):
        conditions1 += "and vehicle_color = %(vehicle_color)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
    if filters.get("entity"):
        conditions1 += "and entity_name = %(entity)s"
        conditions2 += "and entity_name = %(entity)s"
    if filters.get("motor_no"):
        conditions1 += "and motor_no = %(motor_no)s"
        conditions2 += "and engine_no = %(motor_no)s"
    if filters.get("chassis_no"):
        conditions1 += "and chassis_no = %(chassis_no)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
    if filters.get("private_no"):
        conditions1 += "and private_no = %(private_no)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
    if filters.get("maintenance_entity"):
        conditions1 += "and maintenance_entity = %(maintenance_entity)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
    if filters.get("processing_type"):
        conditions1 += "and processing_type = %(processing_type)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
    if filters.get("exchange_allowance"):
        conditions1 += "and exchange_allowance = %(exchange_allowance)s"
        conditions2 += "and body_type not in ('مطاطي','فيبر جلاس','خشبي','صلب','موتوسيكل مائى','معدنى')"
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
            vehicle_color as vehicle_color,
            entity_name as entity_name,
            motor_no as motor_no,
            chassis_no as chassis_no,
            private_no as private_no,
            vehicle_status as vehicle_status,
            maintenance_entity as maintenance_entity,
            processing_type as processing_type,
            exchange_allowance as exchange_allowance,
            possession_date as possession_date,
            possession_type as possession_type,
            fuel_type as fuel_type,
            litre_capacity as litre_capacity,
            cylinder_count as cylinder_count,
            fuel_voucher as fuel_voucher,
            litre_count as litre_count,
            oil_type as oil_type,
            oil_count as oil_count,
            gas_voucher as gas_voucher,
            gas_count as gas_count,
            washing_voucher as washing_voucher,
            washing_count as washing_count
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
            '-----------' as vehicle_color,
            entity_name as entity_name,
            engine_no as motor_no,
            '-----------' as chassis_no,
            '-----------' as private_no,
            boat_validity as vehicle_status,
            '-----------' as maintenance_entity,
            '-----------' as processing_type,
            '-----------' as exchange_allowance,
            '-----------' as possession_type,
            issue_date as possession_date,
            fuel_type as fuel_type,
            motor_capacity as litre_capacity,
            motor_cylinder_count as cylinder_count,
            fuel_voucher as fuel_voucher,
            qty as litre_count,
            '-----------' as oil_type,
            '-----------' as oil_count,
            '-----------' as gas_voucher,
            '-----------' as gas_count,
            '-----------' as washing_voucher,
            '-----------' as washing_count
        FROM `tabBoats`
        WHERE 1=1
        {conditions2}
        )
    ORDER BY entity_name desc, vehicle_type
        """.format(conditions1=conditions1, conditions2=conditions2), filters, as_dict=1)

    result = []
    counter = 0
    if item_results:
        for item_dict in item_results:
            counter += 1
            data = {
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
                'possession_type': item_dict.possession_type if item_dict.possession_type else "-----------",
                'fuel_type': item_dict.fuel_type if item_dict.fuel_type else "-----------",
                'litre_capacity': item_dict.litre_capacity if item_dict.litre_capacity else "-----------",
                'cylinder_count': item_dict.cylinder_count if item_dict.cylinder_count else "-----------",
                'fuel_voucher': item_dict.fuel_voucher if item_dict.fuel_voucher else "-----------",
                'litre_count': item_dict.litre_count if item_dict.litre_count else "-----------",
                'oil_type': item_dict.oil_type if item_dict.oil_type else "-----------",
                'oil_count': item_dict.oil_count if item_dict.oil_count else "-----------",
                'gas_voucher': item_dict.gas_voucher if item_dict.gas_voucher else "-----------",
                'gas_count': item_dict.gas_count if item_dict.gas_count else "-----------",
                'washing_voucher': item_dict.washing_voucher if item_dict.washing_voucher else "-----------",
                'washing_count': item_dict.washing_count if item_dict.washing_count else "-----------",
            }
            result.append(data)
    try:
        result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
        result[0]["total_count"] = counter
    except:
        pass
    return result