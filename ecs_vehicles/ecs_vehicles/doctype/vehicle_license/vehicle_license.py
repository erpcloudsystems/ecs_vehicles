# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, getdate
from frappe.model.document import Document
import itertools

class VehicleLicense(Document):
    def before_insert(self):
        if self.license_no:
            if not frappe.db.exists("License Card", self.license_no) and self.license_no:
                license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no), str.isalpha)]
                code = license_no[0]
                serial = license_no[1]
                doc = frappe.get_doc({
                    "doctype": "License Card",
                    "code": code,
                    "serial": str(serial),
                })
                doc.insert()
        if self.license_no2:
            if not frappe.db.exists("License Card", self.license_no2):
                        license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no2), str.isalpha)]
                        code = license_no[0]
                        serial = license_no[1]
                        doc = frappe.get_doc({
                            "doctype": "License Card",
                            "code": code,
                            "serial": str(serial),
                        })
                        doc.insert()
        if self.license_no3:
            if not frappe.db.exists("License Card", self.license_no3):
                license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no3), str.isalpha)]
                code = license_no[0]
                serial = license_no[1]
                doc = frappe.get_doc({
                    "doctype": "License Card",
                    "code": code,
                    "serial": str(serial),
                })
                doc.insert()
        if self.license_no4:

            if not frappe.db.exists("License Card", self.license_no4):
                    license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no4), str.isalpha)]
                    code = license_no[0]
                    serial = license_no[1]
                    doc = frappe.get_doc({
                        "doctype": "License Card",
                        "code": code,
                        "serial": str(serial),
                    })
                    doc.insert()
    def after_insert(self):
        min_code_list = frappe.db.sql("""
                                 select 
                                card_code, 
                                from_serial,
                                to_serial
                                from `tabAdd License Cards`
                                WHERE `tabAdd License Cards`.default = 1""", as_dict=1)
        only_alpha= ""
        before_current = frappe.db.sql("""select license_no4 as name from `tabVehicle License` License order by name DESC LIMIT 1""", as_dict=1)
        for char in before_current[0].name:
            if char.isalpha():
                only_alpha += char
    # if only_alpha == min_code_list[0]["card_code"]:
        serial_1 = min_code_list[0]["card_code"] +  str(int( before_current[0].name.strip(only_alpha)) +1)
        serial_2 =  min_code_list[0]["card_code"] +  str(int( before_current[0].name.strip(only_alpha)) +2)
        serial_3 =  min_code_list[0]["card_code"] +  str(int( before_current[0].name.strip(only_alpha)) +3)
        serial_4 =  min_code_list[0]["card_code"] +  str(int( before_current[0].name.strip(only_alpha)) +4)
        self.license_no = serial_1
        self.license_no2 = serial_2
        self.license_no3 = serial_3
        self.license_no4 = serial_4
        

        # license_doc = frappe.get_doc = frappe.get_doc("Vehicle License", )
        # for x in min_code_list:
        #     if frappe.db.exists("License Card", {'serial': x.min}):
        #         serial_1 = int(x.min)
        #         serial_2 = int(x.min) + 1
        #         serial_3 = int(x.min) + 2
        #         serial_4 = int(x.min) + 3

        #         if frappe.db.exists("License Card", {'serial': serial_1}):
        #             min_code1 = frappe.get_doc("License Card", {'serial': serial_1})
        #             self.license_no = min_code1.name
        #         else:
        #             frappe.throw(" برجاء إضافة كروت جديدة ")


        #         if frappe.db.exists("License Card", {'serial': serial_2}):
        #             min_code2 = frappe.get_doc("License Card", {'serial': serial_2})
        #             self.license_no2 = min_code2.name
        #         else:
        #             frappe.throw(" برجاء إضافة كروت جديدة ")


        #         if frappe.db.exists("License Card", {'serial': serial_3}):
        #             min_code3 = frappe.get_doc("License Card", {'serial': serial_3})
        #             self.license_no3 = min_code3.name
        #         else:
        #             frappe.throw(" برجاء إضافة كروت جديدة ")


        #         if frappe.db.exists("License Card", {'serial': serial_4}):
        #             min_code4 = frappe.get_doc("License Card", {'serial': serial_4})
        #             self.license_no4 = min_code4.name
        #         else:
        #             frappe.throw(" برجاء إضافة كروت جديدة ")

        #     else:
        #         frappe.throw(" برجاء إضافة كروت جديدة ")

    def validate(self):
        if self.license_no:
            if not frappe.db.exists("License Card", self.license_no) and self.license_no:
                license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no), str.isalpha)]
                code = license_no[0]
                serial = license_no[1]
                doc = frappe.get_doc({
                    "doctype": "License Card",
                    "code": code,
                    "serial": str(serial),
                })
                doc.insert()
        if self.license_no2:
            if not frappe.db.exists("License Card", self.license_no2):
                        license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no2), str.isalpha)]
                        code = license_no[0]
                        serial = license_no[1]
                        doc = frappe.get_doc({
                            "doctype": "License Card",
                            "code": code,
                            "serial": str(serial),
                        })
                        doc.insert()
        if self.license_no3:
            if not frappe.db.exists("License Card", self.license_no3):
                license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no3), str.isalpha)]
                code = license_no[0]
                serial = license_no[1]
                doc = frappe.get_doc({
                    "doctype": "License Card",
                    "code": code,
                    "serial": str(serial),
                })
                doc.insert()
        if self.license_no4:

            if not frappe.db.exists("License Card", self.license_no4):
                    license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no4), str.isalpha)]
                    code = license_no[0]
                    serial = license_no[1]
                    doc = frappe.get_doc({
                        "doctype": "License Card",
                        "code": code,
                        "serial": str(serial),
                    })
                    doc.insert()


        if self.vehicle == self.vehicle2:
            frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (2) ")

        if self.vehicle == self.vehicle3:
            frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (3) ")

        if self.vehicle == self.vehicle4:
            frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (4) ")

        if self.vehicle2 == self.vehicle3:
            frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (2) والمركبة (3) ")

        if self.vehicle2 == self.vehicle4:
            frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (2) والمركبة (4) ")

        if self.vehicle3 == self.vehicle4:
            frappe.throw(" برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (3) والمركبة (4) ")


        user = frappe.session.user
        user_name = frappe.db.get_value("User", user, "full_name")

        self.set("license_entry_summary", [])
        license_entry_summary = self.append("license_entry_summary", {})
        license_entry_summary.vehicle = self.vehicle
        license_entry_summary.police_no = self.police_no
        license_entry_summary.private_no = self.private_no
        license_entry_summary.vehicle_type = self.vehicle_type
        license_entry_summary.entity = self.entity
        license_entry_summary.from_date = self.from_date
        license_entry_summary.to_date = self.to_date
        license_entry_summary.license_no = self.license_no
        license_entry_summary.issue_status = self.issue_status
        license_entry_summary.user = user_name
        if self.issue_status == "تجديد":
            license_entry_summary.renewal_type = self.renewal_type
        else:
            license_entry_summary.renewal_type = "ترخيص أول مرة"

        license_entry_summary = self.append("license_entry_summary", {})
        license_entry_summary.vehicle = self.vehicle2
        license_entry_summary.police_no = self.police_no2
        license_entry_summary.private_no = self.private_no2
        license_entry_summary.vehicle_type = self.vehicle_type2
        license_entry_summary.entity = self.entity2
        license_entry_summary.from_date = self.from_date2
        license_entry_summary.to_date = self.to_date2
        license_entry_summary.license_no = self.license_no2
        license_entry_summary.issue_status = self.issue_status2
        license_entry_summary.user = user_name
        if self.issue_status2 == "تجديد":
            license_entry_summary.renewal_type = self.renewal_type2
        else:
            license_entry_summary.renewal_type = "ترخيص أول مرة"

        license_entry_summary = self.append("license_entry_summary", {})
        license_entry_summary.vehicle = self.vehicle3
        license_entry_summary.police_no = self.police_no3
        license_entry_summary.private_no = self.private_no3
        license_entry_summary.vehicle_type = self.vehicle_type3
        license_entry_summary.entity = self.entity3
        license_entry_summary.from_date = self.from_date3
        license_entry_summary.to_date = self.to_date3
        license_entry_summary.license_no = self.license_no3
        license_entry_summary.issue_status = self.issue_status3
        license_entry_summary.user = user_name
        if self.issue_status3 == "تجديد":
            license_entry_summary.renewal_type = self.renewal_type3
        else:
            license_entry_summary.renewal_type = "ترخيص أول مرة"

        license_entry_summary = self.append("license_entry_summary", {})
        license_entry_summary.vehicle = self.vehicle4
        license_entry_summary.police_no = self.police_no4
        license_entry_summary.private_no = self.private_no4
        license_entry_summary.vehicle_type = self.vehicle_type4
        license_entry_summary.entity = self.entity4
        license_entry_summary.from_date = self.from_date4
        license_entry_summary.to_date = self.to_date4
        license_entry_summary.license_no = self.license_no4
        license_entry_summary.issue_status = self.issue_status4
        license_entry_summary.user = user_name
        if self.issue_status4 == "تجديد":
            license_entry_summary.renewal_type = self.renewal_type4
        else:
            license_entry_summary.renewal_type = "ترخيص أول مرة"


    def on_submit(self):
        user = frappe.session.user
        user_name = frappe.db.get_value("User", user, "full_name")
        vehicle = frappe.get_doc('Vehicles', self.vehicle)
        vehicle.license_no = self.license_no
        vehicle.license_status = "سارية"
        vehicle.license_duration = self.license_duration
        vehicle.license_from_date = self.from_date
        vehicle.license_to_date = self.to_date
        license_no = vehicle.append("vehicle_license_logs", {})
        license_no.license_no = self.license_no
        license_no.issue_status = self.issue_status
        if self.issue_status == "تجديد":
            license_no.renewal_type = self.renewal_type
        else:
            license_no.renewal_type = "ترخيص أول مرة"
        license_no.license_duration = self.license_duration
        license_no.license_from_date = self.from_date
        license_no.license_to_date = self.to_date
        license_no.license_status = self.license_status
        license_no.user = user_name
        license_no.save()
        vehicle.save()
        vehicle2 = frappe.get_doc('Vehicles', self.vehicle2)
        vehicle2.license_no = self.license_no2
        vehicle2.license_status = "سارية"
        vehicle2.license_duration = self.license_duration2
        vehicle2.license_from_date = self.from_date2
        vehicle2.license_to_date = self.to_date2
        license_no2 = vehicle2.append("vehicle_license_logs", {})
        license_no2.license_no = self.license_no2
        license_no2.issue_status = self.issue_status2
        if self.issue_status2 == "تجديد":
            license_no2.renewal_type = self.renewal_type2
        else:
            license_no2.renewal_type = "ترخيص أول مرة"
        license_no2.license_duration = self.license_duration2
        license_no2.license_from_date = self.from_date2
        license_no2.license_to_date = self.to_date2
        license_no2.license_status = self.license_status2
        license_no2.user = user_name
        license_no2.save()
        vehicle2.save()
        vehicle3 = frappe.get_doc('Vehicles', self.vehicle3)
        vehicle3.license_no = self.license_no3
        vehicle3.license_status = "سارية"
        vehicle3.license_duration = self.license_duration3
        vehicle3.license_from_date = self.from_date3
        vehicle3.license_to_date = self.to_date3
        license_no3 = vehicle3.append("vehicle_license_logs", {})
        license_no3.license_no = self.license_no3
        license_no3.issue_status = self.issue_status3
        if self.issue_status3 == "تجديد":
            license_no3.renewal_type = self.renewal_type3
        else:
            license_no3.renewal_type = "ترخيص أول مرة"
        license_no3.license_duration = self.license_duration3
        license_no3.license_from_date = self.from_date3
        license_no3.license_to_date = self.to_date3
        license_no3.license_status = self.license_status3
        license_no3.user = user_name
        license_no3.save()
        vehicle3.save()
        vehicle4 = frappe.get_doc('Vehicles', self.vehicle4)
        vehicle4.license_no = self.license_no4
        vehicle4.license_status = "سارية"
        vehicle4.license_duration = self.license_duration4
        vehicle4.license_from_date = self.from_date4
        vehicle4.license_to_date = self.to_date4
        license_no4 = vehicle4.append("vehicle_license_logs", {})
        license_no4.license_no = self.license_no4
        license_no4.issue_status = self.issue_status4
        if self.issue_status4 == "تجديد":
            license_no4.renewal_type = self.renewal_type4
        else:
            license_no4.renewal_type = "ترخيص أول مرة"
        license_no4.license_duration = self.license_duration4
        license_no4.license_from_date = self.from_date4
        license_no4.license_to_date = self.to_date4
        license_no4.license_status = self.license_status4
        license_no4.user = user_name
        license_no4.save()
        vehicle4.save()
        license_card = frappe.get_doc('License Card', self.license_no)
        license_card.vehicle = self.vehicle
        license_card.vehicle_license = self.name
        license_card.license_status = self.license_status
        license_card.issue_status = self.issue_status
        license_card.renewal_type = self.renewal_type
        license_card.license_duration = self.license_duration
        license_card.from_date = self.from_date
        license_card.to_date = self.to_date
        license_card.letter = self.letter
        license_card.police_no = self.police_no
        license_card.private_no = self.private_no
        license_card.vehicle_type = self.vehicle_type
        license_card.entity = self.entity
        license_card.vehicle_shape = self.vehicle_shape
        license_card.vehicle_brand = self.vehicle_brand
        license_card.vehicle_style = self.vehicle_style
        license_card.vehicle_model = self.vehicle_model
        license_card.vehicle_color = self.vehicle_color
        license_card.motor_no = self.motor_no
        license_card.chassis_no = self.chassis_no
        license_card.cylinder_count = self.cylinder_count
        license_card.litre_capacity = self.litre_capacity
        license_card.fuel_type = self.fuel_type
        license_card.possession_date = self.possession_date
        license_card.processing_type = self.processing_type
        license_card.save()
        license_card2 = frappe.get_doc('License Card', self.license_no2)
        license_card2.vehicle = self.vehicle2
        license_card2.vehicle_license = self.name
        license_card2.license_status = self.license_status2
        license_card2.issue_status = self.issue_status2
        license_card2.renewal_type = self.renewal_type2
        license_card2.license_duration = self.license_duration2
        license_card2.from_date = self.from_date2
        license_card2.to_date = self.to_date2
        license_card2.letter = self.letter2
        license_card2.police_no = self.police_no2
        license_card2.private_no = self.private_no2
        license_card2.vehicle_type = self.vehicle_type2
        license_card2.entity = self.entity2
        license_card2.vehicle_shape = self.vehicle_shape2
        license_card2.vehicle_brand = self.vehicle_brand2
        license_card2.vehicle_style = self.vehicle_style2
        license_card2.vehicle_model = self.vehicle_model2
        license_card2.vehicle_color = self.vehicle_color2
        license_card2.motor_no = self.motor_no2
        license_card2.chassis_no = self.chassis_no2
        license_card2.cylinder_count = self.cylinder_count2
        license_card2.litre_capacity = self.litre_capacity2
        license_card2.fuel_type = self.fuel_type2
        license_card2.possession_date = self.possession_date2
        license_card2.processing_type = self.processing_type2
        license_card2.save()
        license_card3 = frappe.get_doc('License Card', self.license_no3)
        license_card3.vehicle = self.vehicle3
        license_card3.vehicle_license = self.name
        license_card3.license_status = self.license_status3
        license_card3.issue_status = self.issue_status3
        license_card3.renewal_type = self.renewal_type3
        license_card3.license_duration = self.license_duration3
        license_card3.from_date = self.from_date3
        license_card3.to_date = self.to_date3
        license_card3.letter = self.letter3
        license_card3.police_no = self.police_no3
        license_card3.private_no = self.private_no3
        license_card3.vehicle_type = self.vehicle_type3
        license_card3.entity = self.entity3
        license_card3.vehicle_shape = self.vehicle_shape3
        license_card3.vehicle_brand = self.vehicle_brand3
        license_card3.vehicle_style = self.vehicle_style3
        license_card3.vehicle_model = self.vehicle_model3
        license_card3.vehicle_color = self.vehicle_color3
        license_card3.motor_no = self.motor_no3
        license_card3.chassis_no = self.chassis_no3
        license_card3.cylinder_count = self.cylinder_count3
        license_card3.litre_capacity = self.litre_capacity3
        license_card3.fuel_type = self.fuel_type3
        license_card3.possession_date = self.possession_date3
        license_card3.processing_type = self.processing_type3
        license_card3.save()
        license_card4 = frappe.get_doc('License Card', self.license_no4)
        license_card4.vehicle = self.vehicle4
        license_card4.vehicle_license = self.name
        license_card4.license_status = self.license_status4
        license_card4.issue_status = self.issue_status4
        license_card4.renewal_type = self.renewal_type4
        license_card4.license_duration = self.license_duration4
        license_card4.from_date = self.from_date4
        license_card4.to_date = self.to_date4
        license_card4.letter = self.letter4
        license_card4.police_no = self.police_no4
        license_card4.private_no = self.private_no4
        license_card4.vehicle_type = self.vehicle_type4
        license_card4.entity = self.entity4
        license_card4.vehicle_shape = self.vehicle_shape4
        license_card4.vehicle_brand = self.vehicle_brand4
        license_card4.vehicle_style = self.vehicle_style4
        license_card4.vehicle_model = self.vehicle_model4
        license_card4.vehicle_color = self.vehicle_color4
        license_card4.motor_no = self.motor_no4
        license_card4.chassis_no = self.chassis_no4
        license_card4.cylinder_count = self.cylinder_count4
        license_card4.litre_capacity = self.litre_capacity4
        license_card4.fuel_type = self.fuel_type4
        license_card4.possession_date = self.possession_date4
        license_card4.processing_type = self.processing_type4
        license_card4.save()

    def on_update_after_submit(self):
        license_card = frappe.get_doc('License Card', self.license_no)
        license_card.license_status = self.license_status
        license_card.save()
        license_record = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle, "license_no": self.license_no})
        license_record.license_status = self.license_status
        license_record.save()

        license_card2 = frappe.get_doc('License Card', self.license_no2)
        license_card2.license_status = self.license_status2
        license_card2.save()
        license_record2 = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle2, "license_no": self.license_no2})
        license_record2.license_status = self.license_status2
        license_record2.save()

        license_card3 = frappe.get_doc('License Card', self.license_no3)
        license_card3.license_status = self.license_status3
        license_card3.save()
        license_record3 = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle3, "license_no": self.license_no3})
        license_record3.license_status = self.license_status3
        license_record3.save()

        license_card4 = frappe.get_doc('License Card', self.license_no4)
        license_card4.license_status = self.license_status4
        license_card4.save()
        license_record4 = frappe.get_doc('Vehicle License Logs', {"parent": self.vehicle4, "license_no": self.license_no4})
        license_record4.license_status = self.license_status4
        license_record4.save()

@frappe.whitelist()
def update_vehicles_logs ():
    veh_license = frappe.db.sql("""
        SELECT license.name, license.vehicle4 as vehicle, license.police_no4 as police_no ,
        license.vehicle_type4 as vehicle_type, license.entity4 as entity, license.issue_status4 as issue_status, license.renewal_type4 as renewal_type, 
        license.last_end_date4 as last_end_date, license.license_duration4 as license_duration, license.from_date4 as from_date, license.to_date4 as to_date, 
        license.license_no4 as license_no, license.license_status4 as license_status
        FROM `tabVehicle License` license
        ORDER BY license.name
    """, as_dict=1)
    import random
    import string
    import datetime
    # printing lowercase
    letters = string.digits
    counter=0
    veh= ""
    lic=""
    try:
        for row in veh_license:
            counter+=1
            # print(row)
            # print(row.from_date)
            # print(row.to_date)
            veh=row.vehicle
            lic=row.name
            if not int(row.name.split("-")[1]) >= 71456:

                try:
                    from_date = datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
                except ValueError:
                    try:
                        from_date = datetime.datetime.strptime(row.from_date, '%Y-%m-%d').date()
                    except:
                        from_date = datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
                        try:
                            from_date = datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
                        except:
                            from_date = datetime.datetime.strptime(row.from_date[0], '%Y-%m-%d').date()



                try:
                    to_date = datetime.datetime.strptime(row.to_date, '%d/%m/%Y').date()
                except ValueError:
                    try:
                        to_date = datetime.datetime.strptime(row.to_date, '%d-%m-%Y').date()
                    except:
                        to_date = datetime.datetime.strptime(row.to_date, '%d/%m/%Y').date()
                        try:
                            to_date = datetime.datetime.strptime(row.to_date, '%d/%m/%Y').date()
                        except:
                            to_date = datetime.datetime.strptime(row.to_date[0], '%Y-%m-%d').date()
            veh_license_logs = frappe.db.sql("""
                INSERT INTO `tabVehicle License Logs` (name, parent, parenttype, parentfield, license_no, entity,license_doc,
                issue_status, renewal_type, license_duration, license_from_date, license_to_date, license_status)
                VALUES ("{name}", "{parent}", "{parenttype}", "{parentfield}",  "{license_no}", "{entity}","{license_doc}",
                "{issue_status}", "{renewal_type}", "{license_duration}", "{license_from_date}", "{license_to_date}", "{license_status}")
            """.format(name= ''.join(random.choice(letters) for i in range(15)),parent=row.vehicle,parenttype="Vehicles",  parentfield="vehicle_license_logs"
                    , license_no=row.license_no, entity=row.entity,issue_status=row.issue_status
                    , renewal_type=row.renewal_type, license_duration=row.license_duration, license_from_date=from_date.strftime("%Y/%m/%d"),
            license_to_date=to_date.strftime("%Y/%m/%d"),license_status=row.license_status, license_doc=row.name
            ))
            # print(veh_license_logs)
            # break
            # DELETE FROM `tabVehicle License Logs` where parenttype="Vehicles" and parentfield="vehicle_license_logs"
    except Exception as e:
        print(e)
        print(counter)
        print(veh)
        print(lic)

def updatedate():
    import datetime
    veh_license = frappe.db.sql("""
    SELECT from_date3, to_date4, name
    FROM `tabVehicle License`
    """, as_dict=1)
    counter = 0
    for row in veh_license:
        counter +=1
        try:
            # print(row.from_date)
            from_date3 = datetime.datetime.strptime(row.from_date3, '%d/%m/%Y').date()
            # print(from_date)

            veh_license_date = frappe.db.sql("""
                UPDATE `tabVehicle License` SET from_date="{from_date}" where name="{name}"
                """.format(from_date=from_date3.strftime("%Y-%m-%d"), name=row.name))
        except Exception as e:

            # print(veh_license[counter])
            print(e)
            