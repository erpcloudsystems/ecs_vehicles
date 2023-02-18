# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt
import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
               {
            "label": ("كود المستند"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Maintenance Order",
            "width": 100
        },
         {
            "label": ("رقم الاذن"),
            "fieldname": "ezn_no",
            "fieldtype": "Data",

            "width": 100
        },
         {
            "label": ("كود المركبة"),
            "fieldname": "vehicles",
            "fieldtype": "Link",
            "options": "Vehicles",
            "width": 120
        },
        {
            "label": ("رقم الشرطة"),
            "fieldname": "vehicle_no",
            "fieldtype": "Data",
            "width": 90
        },
        {
            "label": ("الجهة التابع لها "),
            "fieldname": "maintenance_entity",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": (" كود الصنف"),
            "fieldname": "item_code",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": ("اسم الصنف"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": ("مجموعه الصنف"),
            "fieldname": "item_group",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": ("الكمية "),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": ("تاريخ الصيانة"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120
        },

    ]

def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("name"):
        conditions += "and a.vehicle_no = %(name)s"
    if filters.get("from_date"):
        conditions += " and a.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and a.date <= %(to_date)s"
    result = []
    item_results = frappe.db.sql("""
        Select
            a.name as name,
			a.vehicle_no as vehicle_no,
			a.vehicles as vehicles,	
			a.date as date,
            a.ezn_no as ezn_no,
            a.entity_name as maintenance_entity,
			b.item_code as item_code,
			b.item_name as item_name,
			b.qty as qty,
			b.item_group

        from `tabMaintenance Order` a join `tabMaintenance Order Item`b on a.name = b.parent
        where a.docstatus = 1

        {conditions}
        order by a.name desc, a.date desc
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            'name': item_dict.name,
            'vehicle_no': item_dict.vehicle_no,
            'vehicles': item_dict.vehicles,
            'date': item_dict.date,
            'maintenance_entity': item_dict.maintenance_entity,
			'item_code': item_dict.item_code,
			'item_name': item_dict.item_name,
			'qty': item_dict.qty,
			'item_group': item_dict.item_group,
            'ezn_no': item_dict.ezn_no,
        }
        result.append(data)
    return result