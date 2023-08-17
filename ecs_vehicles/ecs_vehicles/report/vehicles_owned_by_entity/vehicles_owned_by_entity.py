# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("المستند"),
            "fieldname": "document_type",
            "fieldtype": "Link",
            "options": "DocType",
            "width": 100,
            "hidden": 1
        },
        {
            "label": _("كود المركبة"),
            "fieldname": "vehicle_name",
            "fieldtype": "Dynamic Link",
            "options": "document_type",
            "width": 120
        },
        {
            "label": _("رقم الشرطة"),
            "fieldname": "vehicle_no",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الطراز"),
            "fieldname": "vehicle_style",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("الحالة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("الملحوظات"),
            "fieldname": "notes",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("ملحقة"),
            "fieldname": "attached",
            "fieldtype": "Data",
            "width": 120,
            "hidden": 1
        }
    ]
    return columns

def get_conditions(filters):
    conditions1 =""
    conditions2 =""
    conditions3 =""
    if filters.get("entity"):
        conditions1 += " AND (vehicles.entity_name = '{0}' and (vehicles.attached_entity is null or vehicles.attached_entity = ''))".format(filters.get("entity"))
        conditions2 += " AND ((vehicles.entity_name != '{0}' and vehicles.attached_entity = '{0}'))".format(filters.get("entity"))
        conditions3 += " AND boats.entity_name = '{}'".format(filters.get("entity"))

    return conditions1, conditions2, conditions3

def get_data(filters):
    conditions1, conditions2, conditions3 = get_conditions(filters)
    query = get_query(conditions1, conditions2, conditions3)
    response = []
    for row in query:
        row= {
                "document_type":row.document_type,
                "vehicle_name":row.name,
                "vehicle_date":row.date,
                "vehicle_no": row.vehicle_no if row.vehicle_no else row.police_id ,
                "vehicle_shape": row.shape,
                "vehicle_brand": row.brand,
                "vehicle_style": row.style,
                "cur_user": frappe.db.get_value("User", frappe.session.user, "full_name"),
                "vehicle_status": "{0}".format("عاطلة" if row.vehicle_status in ["عاطلة", "تحت التخريد"] else " "),
                "notes": "{0}".format(row.exchange_allowance if row.exchange_allowance in ["لوحة فقط", "لوحة وخدمة كاملة فقط"] else " "),
                "attached": row.attached,
            }
        response.append(row)
    return response

def get_query(conditions1, conditions2, conditions3):
    return frappe.db.sql(
        """
            SELECT vehicles.vehicle_no vehicle_no, vehicles.vehicle_shape shape, vehicles.vehicle_brand brand, 
                vehicles.vehicle_status as vehicle_status, vehicles.vehicle_style style , vehicles.name as name, 
                vehicles.exchange_allowance as exchange_allowance, "Vehicles" as document_type, "غير ملحقة" as attached
            FROM `tabVehicles` vehicles
            WHERE vehicles.vehicle_status IN ("عاطلة","صالحة", "تحت التخريد")
            {conditions1}
        UNION
            SELECT vehicles.vehicle_no vehicle_no, vehicles.vehicle_shape shape, vehicles.vehicle_brand brand, 
                vehicles.vehicle_status as vehicle_status, vehicles.vehicle_style style , vehicles.name as name, 
                vehicles.exchange_allowance as exchange_allowance, "Vehicles" as document_type, "ملحقة" as attached
            FROM `tabVehicles` vehicles
            WHERE vehicles.vehicle_status IN ("عاطلة","صالحة", "تحت التخريد")
            {conditions2}
        UNION
            SELECT boats.boat_no as vehicle_no, boats.body_type as shape, boats.boat_brand as brand, 
                boats.boat_validity as vehicle_status, boats.boat_style as style , boats.name as name, 
                "لوحة وسوائل" as exchange_allowance, "Boats" as document_type, "غير ملحقة" as attached
            FROM `tabBoats` boats
            WHERE boats.boat_validity IN ("عاطلة","صالحة", "تحت التخريد")
            {conditions3}
        ORDER By shape, brand, style, vehicle_no
    """.format(conditions1=conditions1, conditions2=conditions2, conditions3=conditions3), as_dict=1)

