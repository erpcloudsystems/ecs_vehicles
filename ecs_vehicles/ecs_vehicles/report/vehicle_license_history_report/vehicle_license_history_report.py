# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.utils import flt


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        {
            "label": _("المركبة"),
            "fieldname": "name",
            "options": "Vehicles",
            "fieldtype": "Link",
            "width": 140,
        },
        {
            "label": _("رقم الرخصة"),
            "fieldname": "license_no",
            "fieldtype": "Link",
            "options": "License Card",
            "width": 120,
        },
        {
            "label": _("حالة الإصدار"),
            "fieldname": "issue_status",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("مدة الترخيص"),
            "fieldname": "license_duration",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("بداية الترخيص"),
            "fieldname": "license_from_date",
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "label": _("نهاية الترخيص"),
            "fieldname": "license_to_date",
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "label": _("نوع التجديد"),
            "fieldname": "renewal_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("الحالة"),
            "fieldname": "license_status",
            "fieldtype": "Data",
            "width": 120,
        },
    ]
    return columns


def get_conditions(filters):
    conditions = ""
    if filters.get("name"):
        conditions += " AND license_summary.police_no=%s" % frappe.db.escape(filters.get("name"))
    if filters.get("license_no"):
        conditions += " AND license_summary.license_no=%s" % frappe.db.escape(
            filters.get("license_no")
        )
    if filters.get("issue_status"):
        conditions += " AND license_summary.issue_status=%s" % frappe.db.escape(
            filters.get("issue_status")
        )
    if filters.get("renewal_type"):
        conditions += " AND license_summary.renewal_type=%s" % frappe.db.escape(
            filters.get("renewal_type")
        )
    if filters.get("license_duration"):
        conditions += " AND license_summary.license_duration=%s" % frappe.db.escape(
            filters.get("license_duration")
        )
    if filters.get("license_status"):
        conditions += " AND license_summary.license_status=%s" % frappe.db.escape(
            filters.get("license_status")
        )

    if filters.get("from_date"):
        conditions += " AND license_summary.from_date>='%s'" % filters.get(
            "from_date"
        )

    if filters.get("to_date"):
        conditions += " AND license_summary.from_date<='%s'" % filters.get(
            "to_date"
        )

    return conditions


def get_data(filters):
    conditions = get_conditions(filters)
    query = get_query(conditions)

    ingaze_row = []

    for record in query:
        # fetch material records linked to the purchase order item
        # mr_record = mr_records.get(records.material_request_item, [{}])[0]
        row_detail = {
            "name": record.name,
            "license_no": record.license_no,
            "issue_status": record.issue_status,
            "renewal_type": record.renewal_type,
            "license_duration": record.license_duration,
            "license_from_date": record.license_from_date,
            "license_to_date": record.license_to_date,
            "license_status": record.license_status,
        }
        ingaze_row.append(row_detail)
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT 
             license_summary.name AS name,
            license_summary.license_no AS license_no,
            license_summary.issue_status AS issue_status,
            license_summary.renewal_type AS renewal_type,
            license_summary.license_duration AS license_duration,
            license_summary.from_date AS license_from_date,
            license_summary.to_date AS license_to_date,
            license_summary.license_status AS license_status

        FROM `tabVehicle License Entries` license_summary
        WHERE license_summary.is_current = 1
        {conditions}
        ORDER BY license_summary.from_date DESC

        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )  # nosec


def license_details():
    return frappe._dict(
        frappe.db.sql(
            """
        SELECT 
            license_summary.parent AS license_summary_parent,
             vehicle_license.name AS vehicle_license_name

        FROM `tabLicense Entry Summary` license_summary
        JOIN `tabVehicle License` vehicle_license ON vehicle_license.name = license_summary.parent
        WHERE vehicle_license.docstatus =  1
        """
        )
    )  # nosec


def license_summary():
    return frappe._dict(
        frappe.db.sql(
            """
        SELECT 
            license_summary_item.sales_order AS against_sales_order,
             license_summary.name AS license_summary_name

        FROM `tabSales Invoice` license_summary
        JOIN `tabSales Invoice Item` license_summary_item ON license_summary.name = license_summary_item.parent
        WHERE license_summary.status != "Cancelled"
        """
        )
    )  # nosec

