from __future__ import unicode_literals
from frappe import utils
import frappe
from frappe.utils import nowdate
from frappe import _

frappe.whitelist()
def hourly():
    date = nowdate()

    # frappe.db.sql(
    #     """ update `tabVehicles` set license_status = "منتهية" 
    #         where license_to_date < '{date}' 
    #     """.format(date=date)
    # )
    frappe.db.sql(
        """ update `tabVehicle License Entries` set license_state = "منتهية" 
            where to_date < '{date}' 
        """.format(date=date)
    )
    frappe.db.sql(
        """ update `tabVehicle License Entries` set license_state = "سارية" 
            where to_date >= '{date}' 
        """.format(date=date)
    )
    
    '''
    date = nowdate()
    frappe.db.sql(
        """ update `tabVehicle License` set license_status = "منتهية" 
            where to_date <= '{date}' 
        """.format(date=date)
    )
    '''