# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.utils import flt
from frappe.utils import nowdate


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        {
            "label": _("كود المركبة"),
            "fieldname": "name",
            "options": "Vehicles",
            "fieldtype": "Link",
            "width": 100,
        },
        {
            "label": _("رقم الشرطة"),
            "fieldname": "police_no",
            "fieldtype": "Link",
            "options": "Police Plate",
            "width": 100,
        },
        {
            "label": _("حالة الرخصة"),
            "fieldname": "license_status",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("رقم كارت الرخصة"),
            "fieldname": "license_no",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("بداية الترخيص"),
            "fieldname": "license_from_date",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("نهاية الترخيص"),
            "fieldname": "license_to_date",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("مدة الترخيص"),
            "fieldname": "license_duration",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("نوع المركبة"),
            "fieldname": "vehicle_type",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("الشكل"),
            "fieldname": "vehicle_shape",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("رقم الشاسيه"),
            "fieldname": "chassis_no",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("بلد الصنع"),
            "fieldname": "vehicle_country",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("تاريخ الحيازة"),
            "fieldname": "possession_date",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("مخصص الصرف"),
            "fieldname": "exchange_allowance",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("الجهة"),
            "fieldname": "entity",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("حالة المركبة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 110,
        },
    ]
    return columns


def get_conditions(filters):
    conditions = ""
    if filters.get("name"):
        conditions += " AND vehicle.name=%s" % frappe.db.escape(
            filters.get("name")
        )

    if filters.get("police_no"):
        conditions += " AND vehicle.vehicle_no=%s" % frappe.db.escape(
            filters.get("police_no")
        )
    if filters.get("vehicle_type"):
        conditions += " AND vehicle.vehicle_type=%s" % frappe.db.escape(
            filters.get("vehicle_type")
        )
    if filters.get("vehicle_shape"):
        conditions += " AND vehicle.vehicle_shape=%s" % frappe.db.escape(
            filters.get("vehicle_shape")
        )
    if filters.get("vehicle_brand"):
        conditions += " AND vehicle.vehicle_brand=%s" % frappe.db.escape(
            filters.get("vehicle_brand")
        )
    if filters.get("chassis_no"):
        conditions += " AND vehicle.chassis_no=%s" % frappe.db.escape(
            filters.get("chassis_no")
        )
    if filters.get("vehicle_country"):
        conditions += " AND vehicle.vehicle_country=%s" % frappe.db.escape(
            filters.get("vehicle_country")
        )
    if filters.get("possession_date"):
        conditions += " AND vehicle.possession_date=%s" % frappe.db.escape(
            filters.get("possession_date")
        )
    if filters.get("exchange_allowance"):
        conditions += " AND vehicle.exchange_allowance=%s" % frappe.db.escape(
            filters.get("exchange_allowance")
        )
    if filters.get("entity"):
        conditions += " AND vehicle.entity_name=%s" % frappe.db.escape(
            filters.get("entity")
        )
    if filters.get("vehicle_status"):
        conditions += " AND vehicle.vehicle_status=%s" % frappe.db.escape(
            filters.get("vehicle_status")
        )
    if filters.get("license_status"):
        conditions += " AND vehicle_license.license_state=%s" % frappe.db.escape(
            filters.get("license_status")
        )
    if filters.get("license_no"):
        conditions += " AND vehicle_license.license_no=%s" % frappe.db.escape(
            filters.get("license_no")
        )

    if filters.get("license_from_date"):
        conditions += " AND vehicle_license.from_date>='%s'" % filters.get(
            "license_from_date"
        )

    if filters.get("license_to_date"):
        conditions += " AND vehicle_license.from_date<='%s'" % filters.get(
            "license_to_date"
        )

    if filters.get("license_duration"):
        conditions += " AND vehicle_license.license_duration='%s'" % filters.get(
            "license_duration"
        )
    return conditions


def get_data(filters):
    conditions = get_conditions(filters)
    query = get_query(conditions, filters)
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
            "police_no": record.police_no or record.police_id,
            "vehicle_type": record.vehicle_type,
            "vehicle_shape": record.vehicle_shape,
            "vehicle_brand": record.vehicle_brand,
            "chassis_no": record.chassis_no,
            "vehicle_country": record.vehicle_country,
            "possession_date": record.possession_date,
            "exchange_allowance": record.exchange_allowance,
            "entity": record.entity,
            "vehicle_status": record.vehicle_status,
            "license_status": record.license_status or "لم تستخرج رخصة بعد",
            "license_no": record.license_no or "----------",
            "car_code": record.car_code or "----------",
            "license_from_date": record.license_from_date or "----------",
            "license_to_date": record.license_to_date or "----------",
            "license_duration": record.license_duration or "----------",
            "renewal_type": record.renewal_type or "----------",
            # "delivery_note_name": delivery_note_entry.get(record.sales_order),
            # "delivery_grand_total": flt(
            #     frappe.db.get_value(
            #         "Delivery Note",
            #         delivery_note_entry.get(record.sales_order),
            #         "grand_total",
            #     )
            # ),
            # "license_sumar_name": license_summary_entry.get(record.sales_order),
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


def get_query(conditions, filters):
    new_cond = "  vehicle.vehicle_no = vehicle_license.police_no"
    if filters.get("license_on") == "المركبة":
            new_cond = "  vehicle.name = vehicle_license.vehicle " 
    return frappe.db.sql(
        """
        SELECT
            vehicle.name AS name,
            vehicle.vehicle_no AS police_no,
            vehicle.police_id AS police_id,
            vehicle.vehicle_type AS vehicle_type,
            vehicle.vehicle_shape AS vehicle_shape,
            vehicle.vehicle_brand AS vehicle_brand,
            vehicle.chassis_no AS chassis_no,
            vehicle.vehicle_country AS vehicle_country,
            vehicle.possession_date AS possession_date,
            vehicle.exchange_allowance AS exchange_allowance,
            vehicle.entity_name AS entity,
            vehicle.vehicle_status AS vehicle_status,
            vehicle_license.license_state AS license_status,
            vehicle_license.license_no AS license_no,
            vehicle_license.from_date AS license_from_date,
            vehicle_license.to_date AS license_to_date,
            vehicle_license.license_duration AS license_duration,
            vehicle_license.card_code AS card_code,
            vehicle_license.renewal_type AS renewal_type
        FROM `tabVehicle License Entries` vehicle_license 
        right JOIN `tabVehicles` vehicle ON {new_cond}
        WHERE vehicle_license.license_no IS NULL
        {conditions}
        """.format(
            conditions=conditions,new_cond=new_cond
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

