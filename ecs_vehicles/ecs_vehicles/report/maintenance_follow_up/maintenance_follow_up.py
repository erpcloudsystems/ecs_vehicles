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
            "label": _("رقم الإذن"),
            "fieldname": "ezn_no",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("تاريخ الإذن"),
            "fieldname": "ezn_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("السنة المالية"),
            "fieldname": "fiscal_year",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("إذن الإصلاح"),
            "fieldname": "custody_report",
            "fieldtype": "Link",
            "options": "Custody Report",
            "width": 130
        },
        {
            "label": _("رقم الشرطة"),
            "fieldname": "vehicle_no",
            "fieldtype": "Data",
            "width": 90,
        },
        {
            "label": _("الماركة / الطراز"),
            "fieldname": "brand_style",
            "fieldtype": "Data",
            "width": 160
        },
        {
            "label": _("إسم الجهة"),
            "fieldname": "entity_name",
            "fieldtype": "Data",
            "width": 280
        },
        {
            "label": _("إجراء الإصلاح"),
            "fieldname": "maintenance_order",
            "fieldtype": "Link",
            "options": "Maintenance Order",
            "width": 150
        },
        {
            "label": _("حالة إجراء الإصلاح"),
            "fieldname": "maintenance_order_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("طلب عرض أسعار"),
            "fieldname": "maintenance_rfq",
            "fieldtype": "Link",
            "options": "Maintenance Order",
            "width": 150
        },
        {
            "label": _("حالة طلب عرض أسعار"),
            "fieldname": "maintenance_rfq_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("مذكرة العرض"),
            "fieldname": "presentation_note",
            "fieldtype": "Link",
            "options": "Presentation Note Out",
            "width": 150
        },
        {
            "label": _("حالة مذكرة العرض"),
            "fieldname": "presentation_note_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("أمر الشغل"),
            "fieldname": "job_order",
            "fieldtype": "Link",
            "options": "Job Order",
            "width": 150
        },
        {
            "label": _("حالة أمر الشغل"),
            "fieldname": "job_order_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("فاتورة الصيانة"),
            "fieldname": "purchase_invoices",
            "fieldtype": "Link",
            "options": "Purchase Invoices",
            "width": 150
        },
        {
            "label": _("حالة الفاتورة"),
            "fieldname": "purchase_invoices_status",
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
    if filters.get("vehicle_no"):
        conditions += "and custody_report.vehicle_no = %(vehicle_no)s"
    if filters.get("entity_name"):
        conditions += "and custody_report.entity_name = %(entity_name)s"
    if filters.get("from_date"):
        conditions += " and custody_report.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and custody_report.date <= %(to_date)s"
    if filters.get("fiscal_year"):
        conditions += "and custody_report.fiscal_year = %(fiscal_year)s"
    if filters.get("ezn_no"):
        conditions += "and custody_report.ezn_no = %(ezn_no)s"


    result = []
    custody_report = frappe.db.sql("""
        SELECT
            custody_report.name as custody_report_name, 
            custody_report.entity_name, 
            custody_report.vehicle_brand, 
            custody_report.vehicle_style, 
            custody_report.vehicle_no, 
            custody_report.ezn_no,
            custody_report.date, 
            custody_report.fiscal_year, 
            maintenance_order.name as maintenance_order_name, 
            maintenance_order.docstatus as maintenance_order_status,
            maintenance_request_for_quotations.name as maintenance_request_for_quotations_name, 
            maintenance_request_for_quotations.docstatus as maintenance_request_for_quotations_status,
            presentation_note_out.name as presentation_note_out_name, 
            presentation_note_out.docstatus as presentation_note_out_status,
            job_order.name as job_order_name, 
            job_order.docstatus as job_order_status,
            purchase_invoices.name as purchase_invoices_name, 
            purchase_invoices.docstatus as purchase_invoices_status

        FROM
            `tabCustody Report` custody_report
                LEFT JOIN `tabMaintenance Order` maintenance_order
                ON custody_report.name = maintenance_order.custody_report
                
                LEFT JOIN `tabMaintenance Request for Quotations` maintenance_request_for_quotations
                ON maintenance_request_for_quotations.maintenance_order = maintenance_order.name

                LEFT JOIN `tabPresentation Note Out` presentation_note_out
                ON presentation_note_out.maintenance_order = maintenance_order.name

                LEFT JOIN `tabJob Order` job_order
                ON job_order.maintenance_order = maintenance_order.name

                LEFT JOIN `tabPurchase Invoices` purchase_invoices
                ON purchase_invoices.maintenance_order = maintenance_order.name

        WHERE
            custody_report.docstatus = 1
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)

    if custody_report:
        for cr in custody_report:
            maintenance_order_status = " ---------- "
            maintenance_request_for_quotations_status = " ---------- "
            presentation_note_out_status = " ---------- "
            job_order_status = " ---------- "
            purchase_invoices_status = " ---------- "

            if cr.maintenance_order_status == 0:
                maintenance_order_status = "مسودة"
            if cr.maintenance_order_status == 1:
                maintenance_order_status = "مسجل"
            if cr.maintenance_order_status == 2:
                maintenance_order_status = "ملغى"

            if cr.maintenance_request_for_quotations_status == 0:
                maintenance_request_for_quotations_status = "مسودة"
            if cr.maintenance_request_for_quotations_status == 1:
                maintenance_request_for_quotations_status = "مسجل"
            if cr.maintenance_request_for_quotations_status == 2:
                maintenance_request_for_quotations_status = "ملغى"

            if cr.presentation_note_out_status == 0:
                presentation_note_out_status = "مسودة"
            if cr.presentation_note_out_status == 1:
                presentation_note_out_status = "مسجل"
            if cr.presentation_note_out_status == 2:
                presentation_note_out_status = "ملغى"

            if cr.job_order_status == 0:
                job_order_status = "مسودة"
            if cr.job_order_status == 1:
                job_order_status = "مسجل"
            if cr.job_order_status == 2:
                job_order_status = "ملغى"

            if cr.purchase_invoices_status == 0:
                purchase_invoices_status = "مسودة"
            if cr.purchase_invoices_status == 1:
                purchase_invoices_status = "مسجل"
            if cr.purchase_invoices_status == 2:
                purchase_invoices_status = "ملغى"

            data = {
                'ezn_no': cr.ezn_no,
                'ezn_date': cr.date,
                'fiscal_year': cr.fiscal_year,
                'vehicle_no': cr.vehicle_no,
                'brand_style': str(cr.vehicle_brand) + " / " + str(cr.vehicle_style),
                'entity_name': cr.entity_name,
                'custody_report': cr.custody_report_name,
                'maintenance_order': cr.maintenance_order_name or " ---------- ",
                'maintenance_order_status': maintenance_order_status,
                'maintenance_rfq': cr.maintenance_request_for_quotations_name or " ---------- ",
                'maintenance_rfq_status': maintenance_request_for_quotations_status,
                'presentation_note': cr.presentation_note_out_name or " ---------- ",
                'presentation_note_status': presentation_note_out_status,
                'job_order': cr.job_order_name or " ---------- ",
                'job_order_status': job_order_status,
                'purchase_invoices': cr.purchase_invoices_name or " ---------- ",
                'purchase_invoices_status': purchase_invoices_status,
            }

            result.append(data)
    return result