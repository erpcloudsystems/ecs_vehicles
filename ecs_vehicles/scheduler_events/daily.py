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




# def rename_documents():
#     documents_list = frappe.db.get_list("Maintenance Order")
#     counter = 1
#     for x in documents_list:
#         new_name = "MO-" + ("0" * (5 - len(str(counter)))) + str(counter)
#         frappe.db.sql(
#         """ update `tabMaintenance Order` set name = '{new_name}' where name='{old_name}'
#         """.format(new_name=new_name, old_name=x.name)
#         )
#         counter += 1
#         break
#     print(counter)