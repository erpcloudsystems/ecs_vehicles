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
            "label": _("اسم الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Link",
            "options": "Entity",
            "width": 200,
        },
        {
            "label": _("شكل المركبة"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("إجمالي"),
            "fieldname": "total_count",
            "fieldtype": "Integer",
            "width": 70,
        },
        {
            "label": _("صالح"),
            "fieldname": "valid",
            "fieldtype": "Integer",
            "width": 70,
        },
        {
            "label": _("عاطل"),
            "fieldname": "broken",
            "fieldtype": "Integer",
            "width": 70,
        },
        {
            "label": _("تحت التخريد"),
            "fieldname": "under_scrap",
            "fieldtype": "Integer",
            "width": 90,
        },
        {
            "label": _("مخردة"),
            "fieldname": "scrap",
            "fieldtype": "Integer",
            "width": 70,
        },
        {
            "label": _("تحت البيع بالمزاد"),
            "fieldname": "under_auction",
            "fieldtype": "Integer",
            "width": 120,
        },
        {
            "label": _("بيعت بالمزاد"),
            "fieldname": "auctioned",
            "fieldtype": "Integer",
            "width": 100,
        },
        {
            "label": _("تحت الفحص"),
            "fieldname": "under_inspection",
            "fieldtype": "Integer",
            "width": 100,
        },
        {
            "label": _("مسروقة"),
            "fieldname": "stolen",
            "fieldtype": "Integer",
            "width": 80,
        },
        {
            "label": _("محترقة"),
            "fieldname": "burned",
            "fieldtype": "Integer",
            "width": 80,
        },
        {
            "label": _("ارتجاع للجهة المالكة"),
            "fieldname": "returned",
            "fieldtype": "Integer",
            "width": 130,
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    vehicles_list = frappe.db.sql(
        """
        (
        Select
			t2.entity_name as entity_name,
			t2.vehicle_shape as vehicle_shape,
			count(t2.name) as total_count,
            (select count(name) 
            from `tabVehicles`
            where vehicle_status = 'صالحة'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as valid,
            (select count(name) 
            from `tabVehicles`
            where vehicle_status = 'عاطلة'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as broken,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'تحت التخريد'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as under_scrap,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'مخردة'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as scrap,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'تحت البيع بالمزاد'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as under_auction,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'بيعت بالمزاد'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as auctioned,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'تحت الفحص'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as under_inspection,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'مسروقة'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as stolen,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'محترقة'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as burned,
            (select count(name)
            from `tabVehicles`
            where vehicle_status = 'ارتجاع للجهة المالكة'
            and vehicle_shape = t2.vehicle_shape
            and entity_name = t2.entity_name) as returned

		from `tabVehicles` t2
		where t2.vehicle_shape is not null
        and t2.entity_name is not null
		group by t2.entity_name, t2.vehicle_shape
        )
		union

        (
        Select
			t2.entity_name as entity_name,
			t2.body_type as vehicle_shape,
			count(t2.name) as total_count,
            (select count(name) 
            from `tabBoats`
            where boat_validity = 'صالحة'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as valid,
            (select count(name) 
            from `tabBoats`
            where boat_validity = 'عاطلة'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as broken,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'تحت التخريد'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as under_scrap,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'مخردة'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as scrap,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'تحت البيع بالمزاد'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as under_auction,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'بيعت بالمزاد'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as auctioned,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'تحت الفحص'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as under_inspection,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'مسروقة'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as stolen,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'محترقة'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as burned,
            (select count(name)
            from `tabBoats`
            where boat_validity = 'ارتجاع للجهة المالكة'
            and body_type = t2.body_type
            and entity_name = t2.entity_name) as returned

		from `tabBoats` t2
		where t2.body_type is not null
        and t2.entity_name is not null
		group by t2.entity_name, t2.body_type
        )

		order by entity_name , total_count desc

        """,
        as_dict=1,
    )

    result = []
    if vehicles_list:
        for x in vehicles_list:
            data = {
                "entity_name": x.entity_name,
                "vehicle_shape": x.vehicle_shape,
                "total_count": x.total_count,
                "valid": x.valid,
                "broken": x.broken,
                "under_scrap": x.under_scrap,
                "scrap": x.scrap,
                "under_auction": x.under_auction,
                "auctioned": x.auctioned,
                "under_inspection": x.under_inspection,
                "stolen": x.stolen,
                "burned": x.burned,
                "returned": x.returned,
            }
            result.append(data)
    return result
