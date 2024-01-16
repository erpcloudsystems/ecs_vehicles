from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters, columns)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("المستخدم"),
            "fieldname": "user",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("التاريخ"),
            "fieldname": "creation_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("الباركود"),
            "fieldname": "barcode_no",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("فئة البون"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("اسم الجهة"),
            "fieldname": "entity",
            "fieldtype": "Data",
            "width": 150
        },
                {
            "label": _("رقم الدفعة"),
            "fieldname": "batch_no",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": _("رقم المجموعة"),
            "fieldname": "group_no",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": _("رقم التسوية"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("إصدار"),
            "fieldname": "release_date",
            "fieldtype": "Data",
            "width": 110
        },
        
    ]

    return columns

def get_data(filters, columns):
    usr = get_usrs(filters)
    return usr

def get_usrs(filters):
    conditions = ""

    if filters.get("user"):
        conditions += f" AND VR.owner = '{filters.get('user')}'"
    
    if filters.get("name"):
        conditions += f" AND VR.name = '{filters.get('name')}'"
    
    if filters.get("group_no"):
        conditions += f" AND VR.group_no = '{filters.get('group_no')}'"
    
    if filters.get("batch_no"):
        conditions += f" AND VR.batch_no = '{filters.get('batch_no')}'"
    
    if filters.get("from_date"):
        conditions += f" AND DATE(VR.creation) >= '{filters.get('from_date')}'"
    
    if filters.get("to_date"):
        conditions += f" AND DATE(VR.creation) <= '{filters.get('to_date')}'"
    
    if filters.get("release_date"):
        conditions += f" AND VOC.release_date = '{filters.get('release_date')}'"

    result = []
    item_results = frappe.db.sql(f"""
        SELECT
            VR.name AS name,
            VR.group_no,
            VR.batch_no,
            VR.owner,
            DATE(VR.creation) AS creation_date,
            VRT.barcode_no,
            VRT.voucher_type,
            VRT.entity,
            usr.full_name as user,
            VOC.release_date     
        FROM
            `tabVouchers Review` VR
        JOIN 
            `tabReview Vouchers Table` VRT
        
        ON
            VRT.parent = VR.name
        JOIN 
            `tabUser` usr
        ON
            usr.name = VR.owner
        JOIN 
            `tabVoucher` VOC
        ON
            VOC.barcode_no = VRT.barcode_no
        WHERE
            VR.docstatus <= 2
            {conditions}
        ORDER BY creation_date DESC
            
            """, as_dict=1)

    for item_dict in item_results:
        data = {
            "user": item_dict.user,
            "creation_date": item_dict.creation_date,
            "barcode_no": item_dict.barcode_no,
            "group_no": item_dict.group_no,
            "name": item_dict.name,
            "batch_no": item_dict.batch_no,
            "voucher_type": item_dict.voucher_type,
            "entity": item_dict.entity,
            "release_date":item_dict.release_date
        }
        result.append(data)

    return result
