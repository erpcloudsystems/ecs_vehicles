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
            "label": _("الرخصة"),
            "fieldname": "name",
            "options": "Vehicle License Entries",
            "fieldtype": "Link",
            "width": 140,
        },
        {
            "label": _("المسلسل"),
            "fieldname": "serial",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("الكود"),
            "fieldname": "code",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("حالة كارت الرخصة"),
            "fieldname": "license_status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("نوع المركبة"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("بداية الترخيص"),
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "label": _("نهاية الترخيص"),
            "fieldname": "to_date",
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "label": _("رقم الرخصة"),
            "fieldname": "vehicle_license",
            "fieldtype": "Link",
            "options": "Vehicle License",
            "width": 120,
        },
        {
            "label": _("المركبة"),
            "fieldname": "vehicle",
            "fieldtype": "Link",
            "options": "Vehicles",
            "width": 100,
        },
        {
            "label": _("حالة الإصدار"),
            "fieldname": "issue_status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("نوع التجديد"),
            "fieldname": "renewal_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("مدة الترخيص"),
            "fieldname": "license_duration",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("بواسطة"),
            "fieldname": "owner",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("تعديل بواسة"),
            "fieldname": "modified_by",
            "fieldtype": "Data",
            "width": 120,
        },
    ]
    return columns


def get_conditions(filters):
    conditions = ""
    if filters.get("name"):
        conditions += " AND license_summary.name=%s" % frappe.db.escape(
            filters.get("name")
        )
    if filters.get("serial"):
        conditions += " AND license_summary.serial=%s" % frappe.db.escape(
            filters.get("serial")
        )
    if filters.get("vehicle_type"):
        conditions += " AND license_summary.vehicle_type=%s" % frappe.db.escape(
            filters.get("vehicle_type")
        )
    if filters.get("code"):
        conditions += " AND license_summary.code=%s" % frappe.db.escape(
            filters.get("code")
        )
    if filters.get("vehicle_license"):
        conditions += " AND license_summary.vehicle_license=%s" % frappe.db.escape(
            filters.get("vehicle_license")
        )
    if filters.get("vehicle"):
        conditions += " AND license_summary.vehicle=%s" % frappe.db.escape(
            filters.get("vehicle")
        )
    if filters.get("license_status"):
        conditions += " AND license_summary.license_status=%s" % frappe.db.escape(
            filters.get("license_status")
        )
    if filters.get("issue_status"):
        conditions += " AND license_summary.issue_status=%s" % frappe.db.escape(
            filters.get("issue_status")
        )
    if filters.get("owner"):
        conditions += " AND license_summary.owner=%s" % frappe.db.escape(
            filters.get("owner")
        )
    if filters.get("modified_by"):
        conditions += " AND license_summary.modified_by=%s" % frappe.db.escape(
            filters.get("modified_by")
        )
    if filters.get("from_date"):
        conditions += " AND license_summary.from_date>='%s'" % filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND license_summary.from_date<='%s'" % filters.get("to_date")
    return conditions


def get_data(filters):
    conditions = get_conditions(filters)
    query = get_query(conditions)
    # license_details_query = license_details()
    # license_summary_entry = license_summary()
    # license_summary_entry = get_license_summary_entry(conditions)
    # projects_entry = get_projects_entry(conditions)
    # pr_records = get_mapped_pr_records()
    # pi_records = get_mapped_pi_records()

    ingaze_row = []

    for record in query:
        # fetch material records linked to the purchase order item
        # mr_record = mr_records.get(records.material_request_item, [{}])[0]
        row_detail = {
            "name": record.name,
            "serial": record.serial,
            "vehicle_type": record.vehicle_type,
            "code": record.code,
            "vehicle_license": record.vehicle_license,
            "vehicle": record.vehicle,
            "license_status": record.license_status,
            "issue_status": record.issue_status,
            "renewal_type": record.renewal_type,
            "license_duration": record.license_duration,
            "owner": record.owner,
            "modified_by": record.modified_by,
            "from_date": record.from_date,
            "to_date": record.to_date,
            "letter": record.letter,
            "police_no": record.police_no,
        }
        ingaze_row.append(row_detail)
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT
             license_summary.name AS name,
            license_summary.license_no AS serial,
            license_summary.card_code AS code,
            license_summary.vehicle_license AS vehicle_license,
            license_summary.vehicle AS vehicle,
            license_summary.license_status AS license_status,
            license_summary.vehicle_type AS vehicle_type,
            license_summary.issue_status AS issue_status,
            license_summary.renewal_type AS renewal_type,
            license_summary.license_duration AS license_duration,
            license_summary.from_date AS from_date,
            license_summary.to_date AS to_date,
            license_summary.letter AS letter,
            license_summary.police_no AS police_no,
            license_summary.owner AS owner,
            license_summary.modified_by AS modified_by
        FROM `tabVehicle License Entries` license_summary
        WHERE license_summary.docstatus =  0
        AND license_summary.license_status = "تالف"
        {conditions}
		ORDER BY license_summary.license_no DESC

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

