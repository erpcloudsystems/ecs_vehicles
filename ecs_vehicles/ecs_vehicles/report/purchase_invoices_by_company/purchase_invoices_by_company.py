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
            "label": ("المورد"),
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 100
        },
        {
            "label": ("رقم الإستمارة"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": ("تاريخ الإستمارة"),
            "fieldname": "date",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": ("نوع الاستمارة"),
            "fieldname": "finance_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": ("السنة المالية"),
            "fieldname": "fiscal_year",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": (" اجمالي الفواتير "),
            "fieldname": "total",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": (" إجمالي الغرامات "),
            "fieldname": "total_fine",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": (" إجمالي الخصم الفني "),
            "fieldname": "total_deduct",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": (" إجمالي خصم القانوني "),
            "fieldname": "total_legatl_deduct",
            "fieldtype": "Data",
            "width": 100
        }, 
        {
            "label": (" إجمالي فرق السعر "),
            "fieldname": "total_price_difference",
            "fieldtype": "Data",
            "width": 100
        }, 
        {
            "label": (" اجمالي الضرائب "),
            "fieldname": "total_taxes",
            "fieldtype": "Data",
            "width": 100
        }, 
        {
            "label": ("إجمالي الأستقطاعات "),
            "fieldname": "total_deductions",
            "fieldtype": "Data",
            "width": 100
        }, 
        {
            "label": ("الاجمالي النهائي"),
            "fieldname": "grand_total",
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
    if filters.get("supplier"):
        conditions += "and finance.supplier = %(supplier)s"
    if filters.get("from_date"):
        conditions += " and finance.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and finance.date <= %(to_date)s"
    result = []
    item_results = frappe.db.sql("""
        Select
            finance.supplier as supplier,
            finance.series_no as name,
            finance.date as date,	
            finance.form_type as finance_type,	
            finance.year as fiscal_year,	
            finance.total_invoices as total,	
            finance.total_a_fine as total_fine,	
            finance.total_technical_a_fine as total_deduct,	
            finance.total_legal_a_fine as total_legatl_deduct,	
            finance.tota_price_difference as total_price_difference,	
            finance.total_taxes as total_taxes,	
            finance.total_deductions as total_deductions,	
            finance.total as grand_total
        from `tabFinance Form` finance
        where finance.docstatus = 1
        {conditions}
        order by finance.date desc
        """.format(conditions=conditions), filters, as_dict=1)
    return item_results
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