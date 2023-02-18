from __future__ import unicode_literals
from frappe import utils
import frappe
from frappe.utils import nowdate
from frappe import _

frappe.whitelist()
def hourly():
    pass
    '''
    date = nowdate()
    frappe.db.sql(
        """ update `tabVehicle License` set license_status = "منتهية" 
            where to_date <= '{date}' 
        """.format(date=date)
    )
    '''