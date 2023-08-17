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
            "label": _("الجهة"),
            "fieldname": "entity",
            "fieldtype": "Data",
            "width": 230,
        },
        {
            "label": _("عدد الرخص المستخرجة"),
            "fieldname": "entity_count",
            "fieldtype": "Data",
            "width": 150,
        },


    ]
    return columns


def get_conditions(filters):
    conditions = ""


    if filters.get("entity"):
        conditions += " AND license_summary.entity=%s" % frappe.db.escape(filters.get("entity"))
    if filters.get("from_date"):
        conditions += " AND vehicle_license.creation >='%s'" % filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND vehicle_license.creation <='%s'" % filters.get("to_date")

    return conditions


def get_data(filters):
    conditions = get_conditions(filters)
    query = get_query(conditions)
    license_details_query = license_details()
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
            "entity": record.entity,
            "entity_count": record.entity_count,

            # "delivery_note_name": delivery_note_entry.get(record.sales_order),
            # "delivery_grand_total": flt(
            #     frappe.db.get_value(
            #         "Delivery Note",
            #         delivery_note_entry.get(record.sales_order),
            #         "grand_total",
            #     )
            # ),
            # "license_summary_name": license_summary_entry.get(record.sales_order),
            # "invoice_grand_total": flt(
            #     frappe.db.get_value(
            #         "Sales Invoice",
            #         license_summary_entry.get(record.sales_order),
            #         "grand_total",
            #     )
            # ),
            # "note": "note",
        }
        ingaze_row.append(row_detail)
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT

            license_summary.entity AS entity,
            COUNT(license_summary.entity) AS entity_count


        FROM `tabVehicle License Entries` license_summary
        WHERE license_summary.is_current =  "1"
        AND license_summary.entity is not null
        {conditions}
        GROUP BY license_summary.entity

		ORDER BY COUNT(license_summary.entity) DESC

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
