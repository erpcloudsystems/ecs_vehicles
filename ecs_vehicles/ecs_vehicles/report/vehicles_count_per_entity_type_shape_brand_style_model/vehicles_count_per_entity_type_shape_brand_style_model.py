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
            "label": _("النوع"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 140,
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
            "width": 140,
        },
		{
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 140,
        },
		{
            "label": _("الموديل"),
            "fieldname": "vehicle_model",
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
			t2.vehicle_type as vehicle_type,
			t2.vehicle_shape as vehicle_shape,
			t2.vehicle_brand as vehicle_brand,
			t2.vehicle_style as vehicle_style,
			t2.vehicle_model as vehicle_model,
            (select count(name) 
            from `tabVehicles`
            where vehicle_status in ('صالحة', 'عاطلة')
            and entity_name = t2.entity_name
            and vehicle_type = t2.vehicle_type
            and vehicle_shape = t2.vehicle_shape
            and vehicle_brand = t2.vehicle_brand
            and vehicle_style = t2.vehicle_style
            and vehicle_model = t2.vehicle_model) as total_count,
			(select count(name) 
            from `tabVehicles`
            where vehicle_status = 'صالحة'
            and entity_name = t2.entity_name
            and vehicle_type = t2.vehicle_type
            and vehicle_shape = t2.vehicle_shape
            and vehicle_brand = t2.vehicle_brand
            and vehicle_style = t2.vehicle_style
            and vehicle_model = t2.vehicle_model) as valid,
            (select count(name) 
            from `tabVehicles`
            where vehicle_status = 'عاطلة'
            and entity_name = t2.entity_name
            and vehicle_type = t2.vehicle_type
            and vehicle_shape = t2.vehicle_shape
            and vehicle_brand = t2.vehicle_brand
            and vehicle_style = t2.vehicle_style
            and vehicle_model = t2.vehicle_model) as broken
            
		from `tabVehicles` t2
		where t2.entity_name is not null
        and t2.vehicle_type is not null
		and t2.vehicle_shape is not null
		and t2.vehicle_brand is not null
		and t2.vehicle_style is not null
		and t2.vehicle_model is not null
		group by t2.entity_name, t2.vehicle_type, t2.vehicle_shape, t2.vehicle_brand, t2.vehicle_style, t2.vehicle_model
        )
		union

        (
        Select
			t2.entity_name as entity_name,
			'لانش' as vehicle_type,
            t2.body_type as vehicle_shape,
			t2.boat_brand as vehicle_brand,
			'-' as vehicle_style,
			t2.boat_model as vehicle_model,
            (select count(name) 
            from `tabBoats`
            where boat_validity in ('صالحة', 'عاطلة')
            and entity_name = t2.entity_name
			and body_type = t2.body_type
            and boat_brand = t2.boat_brand
            and boat_model = t2.boat_model) as total_count,
            (select count(name) 
            from `tabBoats`
            where boat_validity = 'صالحة'
            and entity_name = t2.entity_name
			and body_type = t2.body_type
            and boat_brand = t2.boat_brand
            and boat_model = t2.boat_model) as valid,
            (select count(name) 
            from `tabBoats`
            where boat_validity = 'عاطلة'
            and entity_name = t2.entity_name
			and body_type = t2.body_type
            and boat_brand = t2.boat_brand
            and boat_model = t2.boat_model) as broken
            
		from `tabBoats` t2
		where t2.entity_name is not null
        and t2.body_type is not null
		and t2.boat_brand is not null
		and t2.boat_model is not null
		group by t2.entity_name, t2.body_type, t2.boat_brand, t2.boat_model
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
                "vehicle_type": x.vehicle_type,
                "vehicle_shape": x.vehicle_shape,
                "vehicle_brand": x.vehicle_brand,
                "vehicle_style": x.vehicle_style,
                "vehicle_model": x.vehicle_model,
                "total_count": x.total_count,
                "valid": x.valid,
                "broken": x.broken,
            }
            result.append(data)
    return result
