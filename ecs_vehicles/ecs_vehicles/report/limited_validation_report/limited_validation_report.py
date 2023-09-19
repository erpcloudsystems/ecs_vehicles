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
            "label": _("رقم الشرطة"),
            "fieldname": "police_no",
            "fieldtype": "Data",
            "width": 90,
        },
                {
            "label": _("رقم الرخصة"),
            "fieldname": "license_no",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("كود الكارت"),
            "fieldname": "card_code",
            "fieldtype": "Data",
            "width": 60,
        },
        {
            "label": _("حالة الكارت"),
            "fieldname": "license_status",
            "fieldtype": "Data",
            "width": 65,
        },
        {
            "label": _("نوع المركبة"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 80,
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity",
            "fieldtype": "Data",

            "width": 200,
        },
        {
            "label": _("رقم الملاكي"),
            "fieldname": "private_no",
            "fieldtype": "Data",
            "width": 100,
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
            "label": _("نوع التجديد"),
            "fieldname": "renewal_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("بواسطة"),
            "fieldname": "user",
            "fieldtype": "Data",
            "width": 100,
        },
    ]
    return columns


def get_conditions(filters):
    conditions = ""
    # if filters.get("license_on") == "المركبة" and not filters.get("police_no"):
    #     frappe.throw("برجاء ادخال رقم الشرطة للمركبة المراد البحث عنها")
    if filters.get("name"):
        conditions += " AND vehicle_license.name=%s" % frappe.db.escape(filters.get("name"))
    if filters.get("police_no"):
        conditions += " AND license_summary.police_no=%s" % frappe.db.escape(
            filters.get("police_no")
        )
        # if filters.get("license_on") == "المركبة":
        #     conditions += " AND license_summary.vehicle=%s" % frappe.db.escape(frappe.db.get_value("Vehicles", {"vehicle_no":filters.get("police_no")}, "name") if  frappe.db.exists("Vehicles", {"vehicle_no":filters.get("police_no")}) else frappe.db.get_value("Vehicles", {"police_id":filters.get("police_no")}, "name") )
    if filters.get("vehicle_type"):
        conditions += " AND license_summary.vehicle_type=%s" % frappe.db.escape(
            filters.get("vehicle_type")
        )
    if filters.get("entity"):
        conditions += " AND license_summary.entity=%s" % frappe.db.escape(filters.get("entity"))
    if filters.get("from_date"):
        conditions += " AND license_summary.from_date>='%s'" % filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND license_summary.from_date<='%s'" % filters.get("to_date")
    if filters.get("license_no"):
        conditions += " AND license_summary.license_no=%s" % frappe.db.escape(
            filters.get("license_no")
        )
    if filters.get("issue_status"):
        conditions += " AND license_summary.issue_status=%s" % frappe.db.escape(
            filters.get("issue_status")
        )
    
    conditions += " AND license_summary.renewal_type = 'تصريح مؤقت'" 
    if filters.get("user"):
        conditions += " AND license_summary.user=%s" % frappe.db.escape(filters.get("user"))
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
            "vehicle_code": record.vehicle_code,
            "police_no": record.police_no,
            "vehicle_type": record.vehicle_type,
            "entity": record.entity,
            "private_no": record.private_no if record.private_no else "----------",
            "from_date": record.from_date,
            "to_date": record.to_date,
            "license_no": record.license_no,
            "license_status": record.license_status,
            "issue_status": record.issue_status,
            "renewal_type": record.renewal_type,
            "user": record.user,
            "card_code": record.card_code,
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
    try:

        ingaze_row[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
    except:
        pass
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT 
            license_summary.name AS name,
            license_summary.vehicle AS vehicle_code,
            license_summary.police_no AS police_no,
            license_summary.private_no AS private_no,
            license_summary.vehicle_type AS vehicle_type,
            license_summary.entity AS entity,
            license_summary.from_date AS from_date,
            license_summary.to_date AS to_date,
            license_summary.license_no AS license_no,
            license_summary.license_status AS license_status,
            license_summary.issue_status AS issue_status,
            license_summary.renewal_type AS renewal_type,
            license_summary.user AS user,
            license_summary.card_code AS card_code
        FROM `tabVehicle License Entries` license_summary
        WHERE 1 =  1
        {conditions}
        ORDER BY license_summary.license_no, card_code DESC
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

