# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class EditVehicleStatus(Document):
    @frappe.whitelist()
    def get_searched_vehicles(self):
        # check if vehicle exists
        # for vehicle in self.vehicles_status:
        #     if vehicle.vehicle_no == self.vehicle_no:
        #         frappe.throw(
        #             "المركبة رقم {vehicle_no} موجودة بالفعل".format(
        #                 vehicle_no=vehicle.vehicle_no
        #             )
        #         )

        if frappe.db.exists("Vehicles", {"vehicle_no": self.vehicle_no}):
            if frappe.db.exists(
                "Vehicles",
                {"vehicle_no": self.vehicle_no, "attached_entity": self.entity_name},
            ):
                if self.vehicle_type2:
                    vic = frappe.get_doc(
                        "Vehicles",
                        {
                            "vehicle_no": self.vehicle_no,
                            "attached_entity": self.entity_name,
                            "vehicle_type": self.vehicle_type2,
                        },
                    )
                    get_list_count = frappe.db.get_list(
                        "Vehicles",
                        filters={
                            "vehicle_no": self.vehicle_no,
                            "attached_entity": self.entity_name,
                            "vehicle_type": self.vehicle_type2,
                        },
                        fields=["vehicle_no", "vehicle_type"],
                    )
                else:
                    vic = frappe.get_doc(
                        "Vehicles",
                        {
                            "vehicle_no": self.vehicle_no,
                            "attached_entity": self.entity_name,
                        },
                    )
                    get_list_count = frappe.db.get_list(
                        "Vehicles",
                        filters={
                            "vehicle_no": self.vehicle_no,
                            "attached_entity": self.entity_name,
                            "vehicle_type": self.vehicle_type2,
                        },
                        fields=["vehicle_no", "vehicle_type"],
                    )

                if len(get_list_count) > 1:
                    vehicle_types = " <br> "
                    for row in get_list_count:
                        vehicle_types = vehicle_types + " <br> " + row.vehicle_type
                    vehicle_no = "يوجد عدد {count} مركبة بنفس رقم الشرطة {vehicle_no} وتابعة لجهة {entity_name}. <br> \
                    برجاء تحديد نوع المركبة : {vehicle_types}".format(
                        count=len(get_list_count),
                        vehicle_no=self.vehicle_no,
                        entity_name=self.entity_name,
                        vehicle_types=vehicle_types,
                    )
                    frappe.throw(vehicle_no)
            elif frappe.db.exists(
                "Vehicles",
                {"vehicle_no": self.vehicle_no, "entity_name": self.entity_name},
            ):
                if self.vehicle_type2:
                    vic = frappe.get_doc(
                        "Vehicles",
                        {
                            "vehicle_no": self.vehicle_no,
                            "entity_name": self.entity_name,
                            "vehicle_type": self.vehicle_type2,
                        },
                    )
                    get_list_count = frappe.db.get_list(
                        "Vehicles",
                        filters={
                            "vehicle_no": self.vehicle_no,
                            "entity_name": self.entity_name,
                            "vehicle_type": self.vehicle_type2,
                        },
                        fields=["vehicle_no", "vehicle_type"],
                    )
                else:
                    vic = frappe.get_doc(
                        "Vehicles",
                        {
                            "vehicle_no": self.vehicle_no,
                            "entity_name": self.entity_name,
                        },
                    )
                    get_list_count = frappe.db.get_list(
                        "Vehicles",
                        filters={
                            "vehicle_no": self.vehicle_no,
                            "entity_name": self.entity_name,
                        },
                        fields=["vehicle_no", "vehicle_type"],
                    )

                if len(get_list_count) > 1:
                    vehicle_types = " <br> "
                    for row in get_list_count:
                        vehicle_types = vehicle_types + " <br> " + row.vehicle_type
                    vehicle_no = "يوجد عدد {count} مركبة بنفس رقم الشرطة {vehicle_no} وتابعة لجهة {entity_name}. <br> \
                    برجاء تحديد نوع المركبة : {vehicle_types}".format(
                        count=len(get_list_count),
                        vehicle_no=self.vehicle_no,
                        entity_name=self.entity_name,
                        vehicle_types=vehicle_types,
                    )
                    frappe.throw(vehicle_no)
            else:
                vic = frappe.get_doc("Vehicles", {"vehicle_no": self.vehicle_no})

            if (
                vic.entity_name != self.entity_name
                and vic.attached_entity != self.entity_name
            ):
                frappe.throw(
                    "المركبة رقم {vehicle_no} تابعة لجهة {entity_name}".format(
                        vehicle_no=vic.vehicle_no, entity_name=vic.entity_name
                    )
                )
            # if vic.attached_entity == self.entity_name:
            #     vic = frappe.get_doc(
            #         "Vehicles",
            #         {
            #             "vehicle_no": self.vehicle_no,
            #             "attached_entity": self.entity_name,
            #         },
            #     )
            # elif vic.entity_name == self.entity_name:
            #     vic = frappe.get_doc(
            #         "Vehicles",
            #         {
            #             "vehicle_no": self.vehicle_no,
            #             "entity_name": self.entity_name,
            #         },
            #     )

            last_status = frappe.db.sql(
                """
                SELECT `tabVehicle Status Logs`.value as status, 
                        `tabVehicle Status Logs`.date as date, 
                        `tabVehicle Status Logs`.remarks as remarks
                FROM `tabVehicle Status Logs`
                WHERE `tabVehicle Status Logs`.parent = "{parent}"
                ORDER BY `tabVehicle Status Logs`.date DESC LIMIT 1 
            """.format(
                    parent=vic.name,
                ),
                as_dict=1,
            )

            vehicle = self.append("vehicles_status", {})
            vehicle.vehicle_no = vic.vehicle_no
            vehicle.vehicle_type = vic.vehicle_type
            vehicle.vehicle_status = vic.vehicle_status
            if vic.vehicle_status == "صالحة":
                vehicle.vehicle_status_new = "عاطلة"
            if vic.vehicle_status == "عاطلة":
                vehicle.vehicle_status_new = "صالحة"
            vehicle.document_type = "Vehicles"
            vehicle.vehicle = vic.name
            # vehicle.cur_date = nowdate()

            if last_status:
                if last_status[0].status == vic.vehicle_status:
                    vehicle.current_status = (
                        str(last_status[0].status)
                        + " بتاريخ "
                        + str(last_status[0].date)
                    )
                    vehicle.old_remarks = str(last_status[0].remarks)

                else:
                    vehicle.current_status = vic.vehicle_status
                    vehicle.old_remarks = " - "

            else:
                vehicle.current_status = vic.vehicle_status
                vehicle.old_remarks = " - "

        elif frappe.db.exists("Boats", {"boat_no": self.vehicle_no}):
            vic = frappe.get_doc("Boats", {"boat_no": self.vehicle_no})
            if vic.entity_name != self.entity_name:
                frappe.throw(
                    "المركبة رقم {boat_no} تابعة لجهة {entity_name}".format(
                        boat_no=vic.boat_no, entity_name=vic.entity_name
                    )
                )

            vic = frappe.get_doc("Boats", {"boat_no": self.vehicle_no})
            vehicle = self.append("vehicles_status", {})
            vehicle.vehicle_no = vic.boat_no
            vehicle.vehicle_type = "لانش"
            vehicle.vehicle_status = vic.boat_validity
            vehicle.current_status = vic.boat_validity
            vehicle.old_remarks = " - "
            if vic.boat_validity == "صالحة":
                vehicle.vehicle_status_new = "عاطلة"
            if vic.boat_validity == "عاطلة":
                vehicle.vehicle_status_new = "صالحة"
            vehicle.document_type = "Boats"
            vehicle.vehicle = vic.name
            # vehicle.cur_date = nowdate()
        else:
            vehicle_no = self.vehicle_no

            frappe.throw(
                "لا يوجد مركبة برقم {vehicle_no}".format(vehicle_no=vehicle_no)
            )

        if vic.name.startswith("BOAT-"):
            motors_no = ""
            for motor in vic.engine_table:
                motors_no = motors_no + motor.engine_no + "<br>"
            return {
                "name": vic.name,
                "motor_no": motors_no,
                "chassis_no": vic.chassis_no,
                "vehicle_type": vic.body_type,
            }
        self.vehicle_type2 = None
        return {
            "name": vic.name,
            "motor_no": vic.motor_no,
            "chassis_no": vic.chassis_no,
            "vehicle_type": vic.vehicle_type,
        }

    def validate(self):
        self.motor_no = None
        self.chassie_no = None
        self.vehicle_type = None
        self.status_table = []
        for vehicle in self.vehicles_status:
            if not vehicle.updated:
                if frappe.db.exists("Vehicles", {"name": vehicle.vehicle}):
                    vehicle.updated = 1
                    vic = frappe.get_doc("Vehicles", {"name": vehicle.vehicle})
                    vic.vehicle_status = vehicle.vehicle_status_new
                    row = vic.append("status_table", {})
                    row.date = vehicle.cur_date
                    row.value = vehicle.vehicle_status_new
                    row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
                    row.old_transaction_no = self.name
                    row.remarks = vehicle.notes
                    vic.save()
                elif frappe.db.exists("Boats", {"name": vehicle.vehicle}):
                    vehicle.updated = 1
                    boat = frappe.get_doc("Boats", {"name": vehicle.vehicle})
                    # frappe.db.sql(
                    #     """
                    #     UPDATE `tabBoats` SET boat_validity = "{vehicle_status_new}" WHERE name = "{name}"
                    #     """.format(
                    #         name=boat.name,
                    #         vehicle_status_new=vehicle.vehicle_status_new,
                    #     )
                    # )
                    boat.boat_validity = vehicle.vehicle_status_new
                    row = boat.append("validity_table", {})
                    row.date = vehicle.cur_date
                    row.value = vehicle.vehicle_status_new
                    row.edited_by = frappe.db.get_value("User", self.owner, "full_name")
                    row.old_transaction_no = self.name
                    row.remarks = vehicle.notes
                    boat.save()

    def on_trash(self):
        logs = frappe.db.get_all(
            "Vehicle Status Logs", {"old_transaction_no": self.name}
        )
        for log in logs:
            # delete log
            # frappe.delete_doc("Vehicle Status Logs", log.name)
            frappe.db.sql(
                """
                DELETE FROM `tabVehicle Status Logs` WHERE name="{name}" 
                """.format(
                    name=log.name
                )
            )

        for vehicle in self.vehicles_status:
            if frappe.db.exists("Vehicles", {"name": vehicle.vehicle}):
                vic = frappe.get_doc("Vehicles", {"name": vehicle.vehicle})
                vic.vehicle_status = vehicle.vehicle_status
                vic.save()

            elif frappe.db.exists("Boats", {"name": vehicle.vehicle}):
                vic = frappe.get_doc("Boats", {"name": vehicle.vehicle})
                vic.boat_validity = vehicle.vehicle_status
                vic.save()


@frappe.whitelist()
def edit_vehicle_status(name):
    return frappe.db.sql(
        """
    SELECT value, date, edited_by, remarks, old_transaction_no
    FROM `tabVehicle Status Logs` logs
    WHERE parent = "{vehicle_no}"
    ORDER BY date 
    """.format(
            vehicle_no=name
        ),
        as_dict=1,
    )
