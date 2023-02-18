from __future__ import unicode_literals
from frappe import utils
import frappe
from frappe.utils import nowdate
from frappe import _

frappe.whitelist()
def daily():
    date = nowdate()

    frappe.db.sql(
        """ update `tabVehicles` set license_status = "منتهية" 
            where license_to_date < '{date}' 
        """.format(date=date)
    )