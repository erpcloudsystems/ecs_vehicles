# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, getdate
from frappe.model.document import Document


@frappe.whitelist()
def get_cards_no():
    response = {}
    min_code_list = frappe.db.sql(
        """
                                 select 
                                card_code, 
                                from_serial,
                                to_serial
                                from `tabAdd License Cards`
                                WHERE `tabAdd License Cards`.default = 1""",
        as_dict=1,
    )
    try:
        license_no4 = get_max_no(min_code_list[0].card_code)
        response["card_code"] = min_code_list[0].card_code
        response["card_no"] = license_no4 + 1
        response["card_no2"] = license_no4 + 2
        response["card_no3"] = license_no4 + 3
        response["card_no4"] = license_no4 + 4
    except IndexError:
        response["card_code"] = ""
        response["card_no"] = ""
        response["card_no2"] = ""
        response["card_no3"] = ""
        response["card_no4"] = ""

    return response


# @frappe.whitelist()
# def get_cards_no ():
#         response = {}
#         min_code_list = frappe.db.sql("""
#                                  select
#                                 card_code,
#                                 from_serial,
#                                 to_serial
#                                 from `tabAdd License Cards`
#                                 WHERE `tabAdd License Cards`.default = 1""", as_dict=1)
#         try:
#             license_no4 = get_max_no(min_code_list[0].card_code)
#             response["card_code"] = min_code_list[0].card_code
#             response["card_no"] = license_no4 +1
#             response["card_no2"] = license_no4 +2
#             response["card_no3"] = license_no4 +3
#             response["card_no4"] = license_no4 +4
#         except IndexError:
#             response["card_code"] = ""
#             response["card_no"] = ""
#             response["card_no2"] = ""
#             response["card_no3"] = ""
#             response["card_no4"] = ""


#         return response
def get_max_no(card_code):
    before_current = frappe.db.sql(
        """select license_no4 as license_no4 from `tabVehicle License` 
        where license_no4 !="" 
        and license_no4 IS NOT NULL 
        and card_code4 = "{card_code}"
        and docstatus = 1 """.format(
            card_code=card_code
        ),
        as_dict=1,
    )
    last_card = 1
    import re

    if before_current:
        for row in before_current:
            numbers = re.sub("[^0-9]", "", str(row.license_no4))
            if int(numbers) > last_card:
                last_card = int(numbers)

    return last_card


class VehicleLicense(Document):
    # def before_insert(self):
    #     if self.license_no:
    #         if not frappe.db.exists("License Card", self.license_no) and self.license_no:
    #             license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no), str.isalpha)]
    #             code = license_no[0]
    #             serial = license_no[1]
    #             doc = frappe.get_doc({
    #                 "doctype": "License Card",
    #                 "code": code,
    #                 "serial": str(serial),
    #             })
    #             doc.insert()
    #     if self.license_no2:
    #         if not frappe.db.exists("License Card", self.license_no2):
    #                     license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no2), str.isalpha)]
    #                     code = license_no[0]
    #                     serial = license_no[1]
    #                     doc = frappe.get_doc({
    #                         "doctype": "License Card",
    #                         "code": code,
    #                         "serial": str(serial),
    #                     })
    #                     doc.insert()
    #     if self.license_no3:
    #         if not frappe.db.exists("License Card", self.license_no3):
    #             license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no3), str.isalpha)]
    #             code = license_no[0]
    #             serial = license_no[1]
    #             doc = frappe.get_doc({
    #                 "doctype": "License Card",
    #                 "code": code,
    #                 "serial": str(serial),
    #             })
    #             doc.insert()
    #     if self.license_no4:

    #         if not frappe.db.exists("License Card", self.license_no4):
    #                 license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no4), str.isalpha)]
    #                 code = license_no[0]
    #                 serial = license_no[1]
    #                 doc = frappe.get_doc({
    #                     "doctype": "License Card",
    #                     "code": code,
    #                     "serial": str(serial),
    #                 })
    #                 doc.insert()

    # serial_1 = min_code_list[0]["card_code"] +  str(last_card +1)
    # serial_2 =  min_code_list[0]["card_code"] +  str(last_card +2)
    # serial_3 =  min_code_list[0]["card_code"] +  str(last_card +3)
    # serial_4 =  min_code_list[0]["card_code"] +  str(last_card +4)
    # self.license_no = serial_1
    # self.license_no2 = serial_2
    # self.license_no3 = serial_3
    # self.license_no4 = serial_4

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
        # if self.license_no:
        #     if not frappe.db.exists("License Card", self.license_no) and self.license_no:
        #         license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no), str.isalpha)]
        #         code = license_no[0]
        #         # serial = license_no[1]
        #         doc = frappe.get_doc({
        #             "doctype": "License Card",
        #             "code": code,
        #             "serial": str(serial),
        #         })
        #         doc.insert()
        # if self.license_no2:
        #     if not frappe.db.exists("License Card", self.license_no2):
        #                 license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no2), str.isalpha)]
        #                 code = license_no[0]
        #                 serial = license_no[1]
        #                 doc = frappe.get_doc({
        #                     "doctype": "License Card",
        #                     "code": code,
        #                     "serial": str(serial),
        #                 })
        #                 doc.insert()
        # if self.license_no3:
        #     if not frappe.db.exists("License Card", self.license_no3):
        #         license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no3), str.isalpha)]
        #         code = license_no[0]
        #         serial = license_no[1]
        #         doc = frappe.get_doc({
        #             "doctype": "License Card",
        #             "code": code,
        #             "serial": str(serial),
        #         })
        #         doc.insert()
        # if self.license_no4:

        #     if not frappe.db.exists("License Card", self.license_no4):
        #             license_no  = [''.join(g) for k, g in itertools.groupby(str(self.license_no4), str.isalpha)]
        #             code = license_no[0]
        #             serial = license_no[1]
        #             doc = frappe.get_doc({
        #                 "doctype": "License Card",
        #                 "code": code,
        #                 "serial": str(serial),
        #             })
        #             doc.insert()

        if self.vehicle == self.vehicle2:
            frappe.throw(
                " برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (2) "
            )

        if self.vehicle == self.vehicle3:
            frappe.throw(
                " برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (3) "
            )

        if self.vehicle == self.vehicle4:
            frappe.throw(
                " برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (1) والمركبة (4) "
            )

        if self.vehicle2 == self.vehicle3:
            frappe.throw(
                " برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (2) والمركبة (3) "
            )

        if self.vehicle2 == self.vehicle4:
            frappe.throw(
                " برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (2) والمركبة (4) "
            )

        if self.vehicle3 == self.vehicle4:
            frappe.throw(
                " برجاء إختيار مركبة مختلفة حيث أنك قمت بإختيار نفس المركبة في المركبة (3) والمركبة (4) "
            )

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
        record_name = 1
        max_id = frappe.db.sql(
            """
                    SELECT MAX(name) as max_name
                    FROM `tabVehicle License Logs`
                    """,
            as_dict=1,
        )
        if frappe.db.exists("Vehicle License Logs", 1):
            record_name = int(max_id[0]["max_name"]) + 1
        user = frappe.session.user
        user_name = frappe.db.get_value("User", user, "full_name")
        renewal_type = self.renewal_type
        if self.validation:
            renewal_type = "تصريح مؤقت"
        vehicle_entry1 = frappe.get_doc(
            {
                "doctype": "Vehicle License Entries",
                "vehicle": self.vehicle,
                "police_no": self.police_no,
                "private_no": self.private_no,
                "issue_status": self.issue_status,
                "renewal_type": renewal_type,
                "license_duration": self.license_duration,
                "entity": self.entity,
                "from_date": self.from_date,
                "to_date": self.to_date,
                "license_no": self.license_no,
                "card_code": self.card_code,
                "license_status": self.license_status,
                "letter": self.letter,
                "license_state": "سارية",
                "vehicle_type": self.vehicle_shape,
                "user": user_name,
                "vehicle_license": self.name,
                "validation": self.validation,
            }
        )
        vehicle_entry1.save()
        vehlicense_entries = frappe.db.sql(
            """
                SELECT * FROM `tabVehicle License Entries`
                WHERE police_no="{vehicle_no}"
                """.format(
                vehicle_no=self.police_no
            ),
            as_dict=1,
        )
        if vehlicense_entries:
            for entry in vehlicense_entries:
                frappe.db.sql(
                    """
                UPDATE `tabVehicle License Entries`
                set is_current = "0"
                WHERE name = "{name}"
                """.format(
                        name=entry.name
                    )
                )
            frappe.db.sql(
                """
            UPDATE `tabVehicle License Entries`
            set is_current = "1"
            WHERE name = "{name}"
            """.format(
                    name=vehicle_entry1.name
                )
            )
            frappe.db.commit()
        renewal_type2 = self.renewal_type2
        if self.validation2:
            renewal_type2 = "تصريح مؤقت"
        vehicle_entry2 = frappe.get_doc(
            {
                "doctype": "Vehicle License Entries",
                "vehicle": self.vehicle2,
                "police_no": self.police_no2,
                "private_no": self.private_no2,
                "issue_status": self.issue_status2,
                "renewal_type": renewal_type2,
                "license_duration": self.license_duration2,
                "entity": self.entity2,
                "from_date": self.from_date2,
                "to_date": self.to_date2,
                "license_no": self.license_no2,
                "card_code": self.card_code2,
                "license_state": "سارية",
                "license_status": self.license_status2,
                "letter": self.letter2,
                "vehicle_type": self.vehicle_shape2,
                "user": user_name,
                "vehicle_license": self.name,
                "validation": self.validation2,
            }
        )
        vehicle_entry2.save()
        vehlicense_entries2 = frappe.db.sql(
            """
                SELECT * FROM `tabVehicle License Entries`
                WHERE police_no="{vehicle_no}"
                """.format(
                vehicle_no=self.police_no2
            ),
            as_dict=1,
        )
        if vehlicense_entries2:
            for entry in vehlicense_entries2:
                frappe.db.sql(
                    """
                UPDATE `tabVehicle License Entries`
                set is_current = "0"
                WHERE name = "{name}"
                """.format(
                        name=entry.name
                    )
                )
            frappe.db.sql(
                """
            UPDATE `tabVehicle License Entries`
            set is_current = "1"
            WHERE name = "{name}"
            """.format(
                    name=vehicle_entry2.name
                )
            )
            frappe.db.commit()
        renewal_type3 = self.renewal_type3
        if self.validation3:
            renewal_type3 = "تصريح مؤقت"
        vehicle_entry3 = frappe.get_doc(
            {
                "doctype": "Vehicle License Entries",
                "vehicle": self.vehicle3,
                "police_no": self.police_no3,
                "private_no": self.private_no3,
                "issue_status": self.issue_status3,
                "renewal_type": renewal_type3,
                "license_duration": self.license_duration3,
                "entity": self.entity3,
                "from_date": self.from_date3,
                "to_date": self.to_date3,
                "license_no": self.license_no3,
                "card_code": self.card_code3,
                "license_state": "سارية",
                "license_status": self.license_status3,
                "letter": self.letter3,
                "vehicle_type": self.vehicle_shape3,
                "user": user_name,
                "vehicle_license": self.name,
                "validation": self.validation3,
            }
        )
        vehicle_entry3.save()
        vehlicense_entries3 = frappe.db.sql(
            """
                SELECT * FROM `tabVehicle License Entries`
                WHERE police_no="{vehicle_no}"
                """.format(
                vehicle_no=self.police_no3
            ),
            as_dict=1,
        )
        if vehlicense_entries3:
            for entry in vehlicense_entries3:
                frappe.db.sql(
                    """
                UPDATE `tabVehicle License Entries`
                set is_current = "0"
                WHERE name = "{name}"
                """.format(
                        name=entry.name
                    )
                )
            frappe.db.sql(
                """
            UPDATE `tabVehicle License Entries`
            set is_current = "1"
            WHERE name = "{name}"
            """.format(
                    name=vehicle_entry3.name
                )
            )
            frappe.db.commit()
        renewal_type4 = self.renewal_type4
        if self.validation4:
            renewal_type4 = "تصريح مؤقت"
        vehicle_entry4 = frappe.get_doc(
            {
                "doctype": "Vehicle License Entries",
                "vehicle": self.vehicle4,
                "police_no": self.police_no4,
                "private_no": self.private_no4,
                "issue_status": self.issue_status4,
                "renewal_type": renewal_type4,
                "license_duration": self.license_duration4,
                "entity": self.entity4,
                "from_date": self.from_date4,
                "to_date": self.to_date4,
                "license_no": self.license_no4,
                "card_code": self.card_code4,
                "license_status": self.license_status4,
                "letter": self.letter4,
                "license_state": "سارية",
                "vehicle_type": self.vehicle_shape4,
                "user": user_name,
                "vehicle_license": self.name,
                "validation": self.validation4,
            }
        )
        vehicle_entry4.save()
        vehlicense_entries4 = frappe.db.sql(
            """
                SELECT * FROM `tabVehicle License Entries`
                WHERE police_no="{vehicle_no}"
                """.format(
                vehicle_no=self.police_no4
            ),
            as_dict=1,
        )
        if vehlicense_entries4:
            for entry in vehlicense_entries4:
                frappe.db.sql(
                    """
                UPDATE `tabVehicle License Entries`
                set is_current = "0"
                WHERE name = "{name}"
                """.format(
                        name=entry.name
                    )
                )
            frappe.db.sql(
                """
            UPDATE `tabVehicle License Entries`
            set is_current = "1"
            WHERE name = "{name}"
            """.format(
                    name=vehicle_entry4.name
                )
            )
            frappe.db.commit()
        # vehicle = frappe.get_doc('Vehicles', self.vehicle)
        # vehicle.license_no = self.license_no
        # vehicle.card_code = self.card_code
        # vehicle.license_status = "سارية"
        # vehicle.license_duration = self.license_duration
        # vehicle.license_from_date = self.from_date
        # vehicle.license_to_date = self.to_date
        # vehicle.save()

        # vehicle2 = frappe.get_doc('Vehicles', self.vehicle2)
        # vehicle2.license_no = self.license_no2
        # vehicle2.card_code = self.card_code2
        # vehicle2.license_status = "سارية"
        # vehicle2.license_duration = self.license_duration2
        # vehicle2.license_from_date = self.from_date2
        # vehicle2.license_to_date = self.to_date2
        # admin2020
        # mgdemd
        # vehicle2.save()
        # vehicle3 = frappe.get_doc('Vehicles', self.vehicle3)
        # vehicle3.license_no = self.license_no3
        # vehicle3.card_code = self.card_code3
        # vehicle3.license_status = "سارية"
        # vehicle3.license_duration = self.license_duration3
        # vehicle3.license_from_date = self.from_date3
        # vehicle3.license_to_date = self.to_date3

        # vehicle3.save()
        # vehicle4 = frappe.get_doc('Vehicles', self.vehicle4)
        # vehicle4.license_no = self.license_no4
        # vehicle4.card_code = self.card_code4
        # vehicle4.license_status = "سارية"
        # vehicle4.license_duration = self.license_duration4
        # vehicle4.license_from_date = self.from_date4
        # vehicle4.license_to_date = self.to_date4

        # vehicle4.save()
        # license_card = frappe.get_doc('License Card', self.license_no)
        # license_card.vehicle = self.vehicle
        # license_card.vehicle_license = self.name
        # license_card.license_status = self.license_status
        # license_card.issue_status = self.issue_status
        # license_card.renewal_type = self.renewal_type
        # license_card.license_duration = self.license_duration
        # license_card.from_date = self.from_date
        # license_card.to_date = self.to_date
        # license_card.letter = self.letter
        # license_card.police_no = self.police_no
        # license_card.private_no = self.private_no
        # license_card.vehicle_type = self.vehicle_type
        # license_card.entity = self.entity
        # license_card.vehicle_shape = self.vehicle_shape
        # license_card.vehicle_brand = self.vehicle_brand
        # license_card.vehicle_style = self.vehicle_style
        # license_card.vehicle_model = self.vehicle_model
        # license_card.vehicle_color = self.vehicle_color
        # license_card.motor_no = self.motor_no
        # license_card.chassis_no = self.chassis_no
        # license_card.cylinder_count = self.cylinder_count
        # license_card.litre_capacity = self.litre_capacity
        # license_card.fuel_type = self.fuel_type
        # license_card.possession_date = self.possession_date
        # license_card.processing_type = self.processing_type
        # license_card.save()
        # license_card2 = frappe.get_doc('License Card', self.license_no2)
        # license_card2.vehicle = self.vehicle2
        # license_card2.vehicle_license = self.name
        # license_card2.license_status = self.license_status2
        # license_card2.issue_status = self.issue_status2
        # license_card2.renewal_type = self.renewal_type2
        # license_card2.license_duration = self.license_duration2
        # license_card2.from_date = self.from_date2
        # license_card2.to_date = self.to_date2
        # license_card2.letter = self.letter2
        # license_card2.police_no = self.police_no2
        # license_card2.private_no = self.private_no2
        # license_card2.vehicle_type = self.vehicle_type2
        # license_card2.entity = self.entity2
        # license_card2.vehicle_shape = self.vehicle_shape2
        # license_card2.vehicle_brand = self.vehicle_brand2
        # license_card2.vehicle_style = self.vehicle_style2
        # license_card2.vehicle_model = self.vehicle_model2
        # license_card2.vehicle_color = self.vehicle_color2
        # license_card2.motor_no = self.motor_no2
        # license_card2.chassis_no = self.chassis_no2
        # license_card2.cylinder_count = self.cylinder_count2
        # license_card2.litre_capacity = self.litre_capacity2
        # license_card2.fuel_type = self.fuel_type2
        # license_card2.possession_date = self.possession_date2
        # license_card2.processing_type = self.processing_type2
        # license_card2.save()
        # license_card3 = frappe.get_doc('License Card', self.license_no3)
        # license_card3.vehicle = self.vehicle3
        # license_card3.vehicle_license = self.name
        # license_card3.license_status = self.license_status3
        # license_card3.issue_status = self.issue_status3
        # license_card3.renewal_type = self.renewal_type3
        # license_card3.license_duration = self.license_duration3
        # license_card3.from_date = self.from_date3
        # license_card3.to_date = self.to_date3
        # license_card3.letter = self.letter3
        # license_card3.police_no = self.police_no3
        # license_card3.private_no = self.private_no3
        # license_card3.vehicle_type = self.vehicle_type3
        # license_card3.entity = self.entity3
        # license_card3.vehicle_shape = self.vehicle_shape3
        # license_card3.vehicle_brand = self.vehicle_brand3
        # license_card3.vehicle_style = self.vehicle_style3
        # license_card3.vehicle_model = self.vehicle_model3
        # license_card3.vehicle_color = self.vehicle_color3
        # license_card3.motor_no = self.motor_no3
        # license_card3.chassis_no = self.chassis_no3
        # license_card3.cylinder_count = self.cylinder_count3
        # license_card3.litre_capacity = self.litre_capacity3
        # license_card3.fuel_type = self.fuel_type3
        # license_card3.possession_date = self.possession_date3
        # license_card3.processing_type = self.processing_type3
        # license_card3.save()
        # license_card4 = frappe.get_doc('License Card', self.license_no4)
        # license_card4.vehicle = self.vehicle4
        # license_card4.vehicle_license = self.name
        # license_card4.license_status = self.license_status4
        # license_card4.issue_status = self.issue_status4
        # license_card4.renewal_type = self.renewal_type4
        # license_card4.license_duration = self.license_duration4
        # license_card4.from_date = self.from_date4
        # license_card4.to_date = self.to_date4
        # license_card4.letter = self.letter4
        # license_card4.police_no = self.police_no4
        # license_card4.private_no = self.private_no4
        # license_card4.vehicle_type = self.vehicle_type4
        # license_card4.entity = self.entity4
        # license_card4.vehicle_shape = self.vehicle_shape4
        # license_card4.vehicle_brand = self.vehicle_brand4
        # license_card4.vehicle_style = self.vehicle_style4
        # license_card4.vehicle_model = self.vehicle_model4
        # license_card4.vehicle_color = self.vehicle_color4
        # license_card4.motor_no = self.motor_no4
        # license_card4.chassis_no = self.chassis_no4
        # license_card4.cylinder_count = self.cylinder_count4
        # license_card4.litre_capacity = self.litre_capacity4
        # license_card4.fuel_type = self.fuel_type4
        # license_card4.possession_date = self.possession_date4
        # license_card4.processing_type = self.processing_type4
        # license_card4.save()

    def on_cancel(self):
        for row in frappe.db.sql(
            """
        SELECT name 
        FROM `tabVehicle License Entries`
        WHERE vehicle_license= "{vehicle_license}"
        """.format(
                vehicle_license=self.name
            ),
            as_dict=1,
        ):
            delete_doc = frappe.db.sql(
                """
            DELETE FROM `tabVehicle License Entries` WHERE name="{name}"
            """.format(
                    name=row.name
                )
            )
        delete_logs = frappe.db.sql(
            """
        DELETE FROM `tabVehicle License Logs` WHERE license_doc="{name}"
        """.format(
                name=self.name
            )
        )
        frappe.db.commit()

    def on_update_after_submit(self):
        # license_card = frappe.get_doc('License Card', self.license_no)
        # license_card.license_status = self.license_status
        # license_card.save()
        try:
            license_record = frappe.get_doc(
                "Vehicle License Entries",
                {"vehicle_license": self.name, "police_no": self.police_no},
            )
            license_record.license_status = self.license_status
            license_record.save()
        except:
            pass
        # license_card2 = frappe.get_doc('License Card', self.license_no2)
        # license_card2.license_status = self.license_status2
        # license_card2.save()
        try:
            license_record2 = frappe.get_doc(
                "Vehicle License Entries",
                {"vehicle_license": self.name, "police_no2": self.police_no2},
            )
            license_record2.license_status = self.license_status2
            license_record2.save()
        except:
            pass
        # license_card3 = frappe.get_doc('License Card', self.license_no3)
        # license_card3.license_status = self.license_status3
        # license_card3.save()
        try:
            license_record3 = frappe.get_doc(
                "Vehicle License Entries",
                {"vehicle_license": self.name, "police_no3": self.police_no3},
            )
            license_record3.license_status = self.license_status3
            license_record3.save()
        except:
            pass
        # license_card4 = frappe.get_doc('License Card', self.license_no4)
        # license_card4.license_status = self.license_status4
        # license_card4.save()
        try:
            license_record4 = frappe.get_doc(
                "Vehicle License Entries",
                {"vehicle_license": self.name, "police_no4": self.police_no3},
            )
            license_record4.license_status = self.license_status4
            license_record4.save()
        except:
            pass


# @frappe.whitelist()
# def update_vehicles_logs ():
#     veh_license = frappe.db.sql("""
#         SELECT license.name, license.vehicle4 as vehicle, license.police_no4 as police_no ,
#         license.vehicle_type4 as vehicle_type, license.entity4 as entity, license.issue_status4 as issue_status, license.renewal_type4 as renewal_type,
#         license.last_end_date4 as last_end_date, license.license_duration4 as license_duration, license.from_date4 as from_date, license.to_date4 as to_date,
#         license.license_no4 as license_no, license.license_status4 as license_status
#         FROM `tabVehicle License` license
#         ORDER BY license.name
#     """, as_dict=1)
#     import random
#     import string
#     import datetime
#     # printing lowercase
#     letters = string.digits
#     counter=0
#     veh= ""
#     lic=""
#     try:
#         for row in veh_license:
#             counter+=1
#             # print(row)
#             # print(row.from_date)
#             # print(row.to_date)
#             veh=row.vehicle
#             lic=row.name
#             if not int(row.name.split("-")[1]) >= 71456:

#                 try:
#                     from_date = datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
#                 except ValueError:
#                     try:
#                         from_date = datetime.datetime.strptime(row.from_date, '%Y-%m-%d').date()
#                     except:
#                         from_date = datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
#                         try:
#                             from_date = datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
#                         except:
#                             from_date = datetime.datetime.strptime(row.from_date[0], '%Y-%m-%d').date()


#                 try:
#                     to_date = datetime.datetime.strptime(row.to_date, '%d/%m/%Y').date()
#                 except ValueError:
#                     try:
#                         to_date = datetime.datetime.strptime(row.to_date, '%d-%m-%Y').date()
#                     except:
#                         to_date = datetime.datetime.strptime(row.to_date, '%d/%m/%Y').date()
#                         try:
#                             to_date = datetime.datetime.strptime(row.to_date, '%d/%m/%Y').date()
#                         except:
#                             to_date = datetime.datetime.strptime(row.to_date[0], '%Y-%m-%d').date()
#             veh_license_logs = frappe.db.sql("""
#                 INSERT INTO `tabVehicle License Logs` (name, parent, parenttype, parentfield, license_no, entity,license_doc,
#                 issue_status, renewal_type, license_duration, license_from_date, license_to_date, license_status)
#                 VALUES ("{name}", "{parent}", "{parenttype}", "{parentfield}",  "{license_no}", "{entity}","{license_doc}",
#                 "{issue_status}", "{renewal_type}", "{license_duration}", "{license_from_date}", "{license_to_date}", "{license_status}")
#             """.format(name= ''.join(random.choice(letters) for i in range(15)),parent=row.vehicle,parenttype="Vehicles",  parentfield="vehicle_license_logs"
#                     , license_no=row.license_no, entity=row.entity,issue_status=row.issue_status
#                     , renewal_type=row.renewal_type, license_duration=row.license_duration, license_from_date=from_date.strftime("%Y/%m/%d"),
#             license_to_date=to_date.strftime("%Y/%m/%d"),license_status=row.license_status, license_doc=row.name
#             ))
#             # print(veh_license_logs)
#             # break
#             # DELETE FROM `tabVehicle License Logs` where parenttype="Vehicles" and parentfield="vehicle_license_logs"
#     except Exception as e:
#         print(e)
#         print(counter)
#         print(veh)
#         print(lic)


def updatedate():
    import datetime

    veh_license = frappe.db.sql(
        """
    SELECT attgehadate, name
    FROM `tabAttached Entity Logs`
    """,
        as_dict=1,
    )
    counter = 0
    for row in veh_license:
        counter += 1
        try:
            # print(row)
            veh_rec_date = datetime.datetime.strptime(
                row.veh_rec_date, "%d/%m/%y"
            ).date()
            veh_license_date = frappe.db.sql(
                """
                UPDATE `tabJob Order` SET veh_rec_date="{veh_rec_date}" where name="{name}"
                """.format(
                    veh_rec_date=veh_rec_date.strftime("%Y-%m-%d"), name=row.name
                )
            )
            print(row)
            print(veh_rec_date)
        except Exception as e:
            print(e)


@frappe.whitelist()
def history_vehicle1(police_no):
    return frappe.db.sql(
        """
    SELECT vehicle, police_no, private_no, entity, from_date, to_date,
    issue_status, license_no, renewal_type, license_status,
    license_duration,letter,vehicle_type, user
    FROM `tabVehicle License Entries` entry
    WHERE police_no = "{police_no}"
    ORDER BY from_date 
    """.format(
            police_no=police_no
        ),
        as_dict=1,
    )


def updatedate2():
    import datetime

    veh_license = frappe.db.sql(
        """
    SELECT ass_date, name
    FROM `tabEditing Table`
    where ass_date is not null
    """,
        as_dict=1,
    )
    counter = 0
    for row in veh_license:
        try:
            # print(row)
            # day = row.sarfia_from_date.split("-")[0][2:]
            # date = datetime.datetime.strptime(str(day) +"-"+ str(row.sarfia_from_date.split("-")[1]) +"-"+ str(row.sarfia_from_date.split("-")[2]), '%d-%m-%y').date()
            # print(date)
            ass_date = datetime.datetime.strptime(
                row.ass_date, "%d/%m/%y"
            ).date()
            print(ass_date)
            veh_license_date = frappe.db.sql(
                """
                UPDATE `tabEditing Table` SET date="{ass_date}" where name="{name}"
                """.format(
                    ass_date=ass_date.strftime("%Y-%m-%d"),
                    name=row.name,
                )
            )
            print(row)

            frappe.db.commit()
        except Exception as e:
            print(e)


def updatedate33():
    import datetime

    veh_license = frappe.db.sql(
        """
    SELECT from_date as from_date, to_date as to_date, name
    FROM `tabAuction Invoice`
    where oil_flag=1
    """,
        as_dict=1,
    )
    for row in veh_license:
        try:
            current_issue = " من " + str(row.from_date) + " إلى " + str(row.to_date)
            veh_license_date = frappe.db.sql(
                """
                UPDATE `tabLiquids Issuing` SET current_issue="{current_issue}" where name="{name}"
                """.format(
                    current_issue=current_issue,
                    name=row.name,
                )
            )
            frappe.db.commit()
        except Exception as e:
            print(e)


def updatedate222():
    import datetime

    veh_license = frappe.db.sql(
        """
    SELECT invoice_date as invoice_date, name
    FROM `tabAuction Invoice`
    where docstatus = 1
    """,
        as_dict=1,
    )
    counter = 0
    for row in veh_license:
        try:
            print(row)
            day = str(row.invoice_date).split("-")[0][2:]
            invoice_date = datetime.datetime.strptime(
                str(day)
                + "-"
                + str(str(row.invoice_date).split("-")[1])
                + "-"
                + str(str(row.invoice_date).split("-")[2]),
                "%d-%m-%y",
            ).date()
            print(day)
            print(invoice_date)
            # date = datetime.datetime.strptime(row.date, "%d/%m/%y").date()
            veh_license_date = frappe.db.sql(
                """
                UPDATE `tabAuction Invoice` SET invoice_date="{invoice_date}" where name="{name}"
                """.format(
                    invoice_date=invoice_date, name=row.name
                )
            )
            frappe.db.commit()
        except Exception as e:
            print(e)


def updatedate3():
    import datetime

    veh_license = frappe.db.sql(
        """
    SELECT name
    FROM `tabVehicles` vehicles
    WHERE vehicles.vehicle_status in ("صالحة", "عاطلة")

    """,
        as_dict=1,
    )
    counter = 0
    for row in veh_license:
        try:
            # print(row)
            # day = row.date.split("-")[0][2:]
            # date = datetime.datetime.strptime(str(day) +"-"+ str(row.date.split("-")[1]) +"-"+ str(row.date.split("-")[2]), '%d-%m-%y').date()
            frappe.db.sql(
                """
        SELECT
            license_entries.from_date AS license_from_date,
            license_entries.to_date AS to_date,
            license_entries.card_code AS card_code,
            license_entries.license_no AS license_no,
            license_entries.renewal_type AS renewal_type,
            license_entries.entity AS entity_name

        FROM `tabVehicle License Entries` license_entries
        WHERE vehicle_license.vehicle_status in ("صالحة", "عاطلة")
        AND vehicle_license.name = "{vehicles}"
        ORDER BY to_date DESC LIMIT 1

        """.format(
                    vehicles=row.name, today=nowdate()
                ),
                as_dict=1,
            )  # nosec
            date = datetime.datetime.strptime(row.date, "%d/%m/%y").date()
            veh_license_date = frappe.db.sql(
                """
                UPDATE `tabForm Invoices` SET date="{date}" where name="{name}"
                """.format(
                    date=date.strftime("%Y-%m-%d"), name=row.name
                )
            )
            # print(date)
            frappe.db.commit()
        except Exception as e:
            print(e)


def update_license_state():
    from frappe.utils import nowdate

    date = nowdate()
    frappe.db.sql(
        """ update `tabVehicle License Entries` set license_state = "سارية" 
            where to_date > '{date}' 
        """.format(
            date=date
        )
    )


def update_veh_card_license():
    vehicles = frappe.db.sql(
        """
    SELECT  name, vehicle_no
    FROM `tabVehicles`
    """,
        as_dict=1,
    )

    for row in vehicles:
        vehlicense_entries = frappe.db.sql(
            """
                SELECT * FROM `tabVehicle License Entries` 
                WHERE police_no="{name}"
                ORDER BY to_date
                """.format(
                name=row.vehicle_no
            ),
            as_dict=1,
        )
        if vehlicense_entries:
            vehlicense = frappe.db.sql(
                """
                SELECT * FROM `tabVehicle License Entries` 
                WHERE police_no="{name}"
                ORDER BY to_date DESC
                LIMIT 1
                """.format(
                    name=row.vehicle_no
                ),
                as_dict=1,
            )
            frappe.db.sql(
                """
            UPDATE `tabVehicles`
            set license_no = "{license_no}",
                card_code = "{card_code}",
                license_status= "{license_status}",
                license_from_date= "{license_from_date}",
                license_to_date="{license_to_date}"
            WHERE vehicle_no = "{name}"
            """.format(
                    license_no=vehlicense[0].license_no,
                    card_code=vehlicense[0].card_code,
                    license_status="سارية",
                    license_from_date=vehlicense[0].from_date,
                    license_to_date=vehlicense[0].to_date,
                    name=vehlicense[0].police_no,
                )
            )
        for entry in vehlicense_entries:
            record_name = 1
            max_id = frappe.db.sql(
                """
                    SELECT MAX(name) as max_name
                    FROM `tabVehicle License Logs`
                    """,
                as_dict=1,
            )
            if frappe.db.exists("Vehicle License Logs", 1):
                record_name = int(max_id[0]["max_name"]) + 1
            frappe.db.sql(
                """
            INSERT INTO `tabVehicle License Logs`(
                issue_status,renewal_type,license_duration,entity,license_from_date,
                license_to_date,card_code,license_no,license_status,letter,user,
                license_doc,parent,parenttype,parentfield, name)
                    VALUES ("{issue_status}", "{renewal_type}", "{license_duration}", "{entity}",
                    "{license_from_date}", "{license_to_date}", "{card_code}", "{license_no}",
                    "{license_status}", "{letter}", "{user}", "{license_doc}",
                    "{parent}", "{parenttype}", "{parentfield}", "{name}")
                    """.format(
                    issue_status=entry.issue_status,
                    renewal_type=entry.renewal_type,
                    license_duration=entry.license_duration,
                    entity=entry.entity,
                    license_from_date=entry.from_date,
                    license_to_date=entry.to_date,
                    card_code=entry.card_code,
                    license_no=entry.license_no,
                    license_status=entry.license_status,
                    letter=entry.letter,
                    user=entry.user,
                    license_doc=entry.license_doc,
                    parent=entry.vehicle,
                    parenttype="Vehicles",
                    parentfield="vehicle_license_logs",
                    name=record_name,
                )
            )
            frappe.db.commit()


def current_license():
    vehicles = frappe.db.sql(
        """
    SELECT  name, vehicle_no
    FROM `tabVehicles`
    """,
        as_dict=1,
    )

    for row in vehicles:
        vehlicense_entries = frappe.db.sql(
            """
                SELECT * FROM `tabVehicle License Entries`
                WHERE police_no="{vehicle_no}"
                """.format(
                vehicle_no=row.vehicle_no
            ),
            as_dict=1,
        )
        if vehlicense_entries:
            for entry in vehlicense_entries:
                frappe.db.sql(
                    """
                UPDATE `tabVehicle License Entries`
                set is_current = "0"
                WHERE name = "{name}"
                """.format(
                        name=entry.name
                    )
                )
            vehlicense = frappe.db.sql(
                """
                SELECT * FROM `tabVehicle License Entries` 
                WHERE police_no="{vehicle_no}"
                ORDER BY to_date DESC
                LIMIT 1
                """.format(
                    vehicle_no=row.vehicle_no
                ),
                as_dict=1,
            )
            frappe.db.sql(
                """
            UPDATE `tabVehicle License Entries`
            set is_current = "1"
            WHERE name = "{name}"
            """.format(
                    name=vehlicense[0].name
                )
            )
            frappe.db.commit()

        # for entry in vehlicense_entries:
        #     record_name = 1
        #     max_id = frappe.db.sql("""
        #             SELECT MAX(name) as max_name
        #             FROM `tabVehicle License Logs`
        #             """, as_dict=1)
        #     if frappe.db.exists("Vehicle License Logs", 1):
        #         record_name = int(max_id[0]["max_name"]) + 1
        #     frappe.db.sql("""
        #     INSERT INTO `tabVehicle License Logs`(
        #         issue_status,renewal_type,license_duration,entity,license_from_date,
        #         license_to_date,card_code,license_no,license_status,letter,user,
        #         license_doc,parent,parenttype,parentfield, name)
        #             VALUES ("{issue_status}", "{renewal_type}", "{license_duration}", "{entity}",
        #             "{license_from_date}", "{license_to_date}", "{card_code}", "{license_no}",
        #             "{license_status}", "{letter}", "{user}", "{license_doc}",
        #             "{parent}", "{parenttype}", "{parentfield}", "{name}")
        #             """.format(issue_status=entry.issue_status,renewal_type=entry.renewal_type,
        #                        license_duration=entry.license_duration,entity=entry.entity,
        #                        license_from_date=entry.from_date,license_to_date=entry.to_date,
        #                        card_code=entry.card_code,license_no=entry.license_no,
        #                        license_status=entry.license_status,letter=entry.letter,
        #                        user=entry.user,license_doc=entry.license_doc,
        #                        parent=entry.vehicle,parenttype="Vehicles",
        #                        parentfield="vehicle_license_logs",name=record_name))


def split_license_no():
    import itertools

    entries = frappe.db.sql(
        """
    SELECT  name, license_no, card_code
    FROM `tabVehicle License Entries`

    """,
        as_dict=1,
    )
    for row in entries:
        license_no = [
            "".join(g) for k, g in itertools.groupby(str(row.license_no), str.isalpha)
        ]
        # print(license_no)
        if row.license_no == 0:
            continue
        elif len(license_no) > 1:
            # print(license_no[0])
            # print(license_no[1])
            # print(row.name)
            frappe.db.sql(
                """
                UPDATE `tabVehicle License Entries`
                set license_no = "{license_no}",
                card_code = "{card_code}"
                WHERE name = "{name}"
                """.format(
                    name=row.name, license_no=license_no[0], card_code=license_no[1]
                )
            )
            frappe.db.commit()
        # elif len(license_no) == 1:
        #     # print(license_no[0])
        #     # print(row.name)
        #     frappe.db.sql("""
        #         UPDATE `tabVehicle License Entries`
        #         set license_no = "{license_no}",
        #         card_code = "{card_code}"
        #         WHERE name = "{name}"
        #         """.format(name=row.name, license_no=license_no[0]))


"""
    UPDATE `tabVehicle License Entries` JOIN `tabVehicle License`
    ON `tabVehicle License Entries`.vehicle =  `tabVehicle License`.vehicle
    set `tabVehicle License Entries`.license_no = `tabVehicle License`.license_no,
        `tabVehicle License Entries`.card_code = `tabVehicle License`.card_code,
        `tabVehicle License Entries`.license_status = `tabVehicle License`.license_status,
        `tabVehicle License Entries`.vehicle_license = `tabVehicle License`.name
    WHERE `tabVehicle License`.docstatus =1
    AND `tabVehicle License Entries`.from_date =  `tabVehicle License`.from_date;
    """

"""
    UPDATE `tabForm Invoices` form_invoice JOIN `tabPurchase Invoices` purchase_invoices
    ON purchase_invoices.vehicle_no =  form_invoice.vic_no
    set form_invoice.purchase_invoices = purchase_invoices.name,
        purchase_invoices.total = form_invoice.contract_price
    WHERE purchase_invoices.inv_no =  form_invoice.add_no
    AND purchase_invoices.order_no =  form_invoice.p_no;
    """


"""
    UPDATE `tabForm Invoices` form_invoice JOIN `tabFinance Form` finance_form
    ON form_invoice.vehicle =  purchase_invoices.vehicles
    set form_invoice.purchase_invoices = purchase_invoices.name,
        purchase_invoices.total = form_invoice.contract_price
    WHERE purchase_invoices.inv_no =  form_invoice.add_no
    AND purchase_invoices.order_no =  form_invoice.p_no;
    """


"""
    UPDATE `tabForm Invoices` form_invoice JOIN `tabFinance Form` finance_form
    ON form_invoice.doc_id =  finance_form.doc_id
    set form_invoice.parent = finance_form.name,
        form_invoice.parentfield = "form_invoices",
        form_invoice.parenttype = "Finance Form";
    """

"""
    UPDATE `tabForm Invoices` form_invoice JOIN `tabEntity` entity
    ON form_invoice.geha_code =  entity.code
    set form_invoice.entity_name = entity.name;    """

"""
    UPDATE `tabVehicle License Entries` entry JOIN `tabVehicles` vehicle
    ON entry.vehicle = vehicle.name
    set entry.vehicle_type = vehicle.vehicle_shape;
"""

"""
INSERT INTO `tabVehicle License Logs`(issue_status,renewal_type,license_duration,entity,license_from_date,
                        license_to_date,card_code,license_no,license_status,letter,user,
                        license_doc,parent,parenttype,parentfield, name
) 
"""
"""
    UPDATE `tabVehicle License Logs` 
    set `tabVehicle License Logs`.issue_status = `tabVehicle License Entries`.issue_status,
     `tabVehicle License Logs`.renewal_type = `tabVehicle License Entries`.renewal_type,
     `tabVehicle License Logs`.license_duration = `tabVehicle License Entries`.license_duration,
     `tabVehicle License Logs`.entity = `tabVehicle License Entries`.entity,
     `tabVehicle License Logs`.license_from_date = `tabVehicle License Entries`.from_date,
     `tabVehicle License Logs`.license_to_date = `tabVehicle License Entries`.to_date,
     `tabVehicle License Logs`.card_code = `tabVehicle License Entries`.card_code,
     `tabVehicle License Logs`.license_no = `tabVehicle License Entries`.license_no,
     `tabVehicle License Logs`.license_status = `tabVehicle License Entries`.license_status,
     `tabVehicle License Logs`.letter = `tabVehicle License Entries`.letter,
     `tabVehicle License Logs`.user = `tabVehicle License Entries`.user,
     `tabVehicle License Logs`.license_doc = `tabVehicle License Entries`.vehicle_license,
     `tabVehicle License Logs`.parent = `tabVehicle License Entries`.vehicle,
     `tabVehicle License Logs`.parenttype = "Vehicles",
     `tabVehicle License Logs`.parentfield = "vehicle_license_logs"
    WHERE `tabVehicle License Entries`.vehicle = "VEH-63062"
    ORDER BY `tabVehicle License Entries`.to_date;
        """

"""
UPDATE `tabMaintenance Entity Logs` logs 
set logs.remarks = logs.ass_note
WHERE logs.remarks IS NULL
and logs.ass_note  IS NOT NULL
"""
"""
UPDATE `tabMaintenance Entity Logs` logs 
set logs.date = logs.ass_date
WHERE logs.date IS NULL
and logs.ass_date  IS NOT NULL
"""
"""
UPDATE `tabMaintenance Entity Logs`  JOIN `tabVehicles` 
ON `tabMaintenance Entity Logs`.vic_serial = `tabVehicles`.vic_serial
set `tabMaintenance Entity Logs`.parent = `tabVehicles`.name,
`tabMaintenance Entity Logs`.parentfield = "maintenance_entity_table",
`tabMaintenance Entity Logs`.parenttype = "Vehicles";
 
"""
