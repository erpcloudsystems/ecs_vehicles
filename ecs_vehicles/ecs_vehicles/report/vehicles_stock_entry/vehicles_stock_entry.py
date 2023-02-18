
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
            "label": _("كود الصنف"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options":"Item",
            "width": 150
        },
        {
            "label": _("اسم الصنف"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("الكمية"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("وحدة القياس"),
            "fieldname": "uom",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("التسعير الاساسي استنادأ لوحدة القياس"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 250
        },
        {
            "label": _("المبلغ الأساسي"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 150
        },
    ]


def get_data(filters, columns):
    get_qty_per_liquid = []
    get_qty_per_liquid = get_qty_per_liquids(filters)
    return get_qty_per_liquid


def get_qty_per_liquids(filters):
    conditions = ""
    if filters.get("vehicle"):
        conditions += " AND vehicles ='%s'" % filters.get("vehicle")
    if filters.get("maintenance_order"):
        conditions += " AND maintenance_order ='%s'" % filters.get("maintenance_order")
    if filters.get("from_date"):
        conditions += " AND issue_date>='%s'" % filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND issue_date<='%s'" % filters.get("to_date")
    item_results = frappe.db.sql("""
        Select
            stock_entry_detail.item_code,
            stock_entry_detail.item_name,
            stock_entry_detail.qty,
            stock_entry_detail.uom,
            stock_entry_detail.basic_rate,
            stock_entry_detail.amount
        from `tabStock Entry` stock_entry
        join `tabStock Entry Detail` stock_entry_detail ON stock_entry.name = stock_entry_detail.parent
        where stock_entry.stock_entry_type = "صرف مواد"
        {conditions}
        """.format(conditions=conditions), as_dict=1)
    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                "item_code": item_dict.item_code,
                "item_name": item_dict.item_name,
                'qty': item_dict.qty,
                'uom': item_dict.uom,
                'rate': item_dict.basic_rate,
                'amount': item_dict.amount,
            }
            result.append(data)
        return result