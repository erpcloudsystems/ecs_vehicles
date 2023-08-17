# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleInquiry(Document):
    @frappe.whitelist()
    def get_searched_vehicles(self):
        self.vehicle_inquiry_table = []
        condition = ""
        if self.entity_name:
            condition += " AND entity_name = '{entity_name}' ".format(
                entity_name=self.entity_name
            )
        if len(self.vehicle_no) < 5:
            vehicles_list = frappe.db.sql(
                """
                (
                SELECT `tabVehicles`.name as name, `tabVehicles`.vehicle_no as vehicle_no,
                  `tabVehicles`.police_id as police_id, `tabVehicles`.entity_name as entity, 
                `tabVehicles`.vehicle_status as status, 
                "Vehicles" as vehicle_boat, `tabVehicle Status`.code as code
                FROM `tabVehicles`
                JOIN `tabVehicle Status` ON `tabVehicles`.vehicle_status = `tabVehicle Status`.name
                WHERE (vehicle_no = '{vehicle_no}'
                OR police_id = '{vehicle_no}')
                {condition}
                )
                UNION
                (
                SELECT `tabBoats`.name as name, `tabBoats`.boat_no as vehicle_no, 
                `tabBoats`.boat_no as police_id, `tabBoats`.entity_name as entity, 
                boat_validity as status, "Boats" as vehicle_boat, `tabVehicle Status`.code as code
                FROM `tabBoats`
                JOIN `tabVehicle Status` ON `tabBoats`.boat_validity = `tabVehicle Status`.name
                WHERE (boat_no = '{vehicle_no}'
                OR boat_no = '{vehicle_no}')
                {condition}
                )
                ORDER BY code
                """.format(
                    condition=condition,
                    vehicle_no=self.vehicle_no,
                    entity_name=self.entity_name,
                ),
                as_dict=1,
            )
        else:
            vehicles_list = frappe.db.sql(
                """
                (
                SELECT `tabVehicles`.name as name, `tabVehicles`.vehicle_no as vehicle_no,
                  `tabVehicles`.police_id as police_id, `tabVehicles`.entity_name as entity, 
                `tabVehicles`.vehicle_status as status, 
                "Vehicles" as vehicle_boat, `tabVehicle Status`.code as code
                FROM `tabVehicles`
                JOIN `tabVehicle Status` ON `tabVehicles`.vehicle_status = `tabVehicle Status`.name
                WHERE (vehicle_no LIKE '%{vehicle_no}'
                OR police_id LIKE '%{vehicle_no}')
                {condition}
                )
                UNION
                (
                SELECT `tabBoats`.name as name, `tabBoats`.boat_no as vehicle_no, 
                `tabBoats`.boat_no as police_id, `tabBoats`.entity_name as entity, 
                boat_validity as status, "Boats" as vehicle_boat, `tabVehicle Status`.code as code
                FROM `tabBoats`
                JOIN `tabVehicle Status` ON `tabBoats`.boat_validity = `tabVehicle Status`.name
                WHERE (boat_no LIKE '%{vehicle_no}'
                OR boat_no LIKE '%{vehicle_no}')
                {condition}
                )
                ORDER BY code
                """.format(
                    condition=condition,
                    vehicle_no=self.vehicle_no,
                    entity_name=self.entity_name,
                ),
                as_dict=1,
            )
        if self.vehicle_no and not vehicles_list:
            self.vehicle = "-------"
            self.entity = "-------"
            self.chassis_no = "-------"
            self.motor_no = "-------"
            self.motor_no2 = "-------"
            self.vehicle_type = "-------"
            self.vehicle_country = "-------"
            self.vehicle_shape = "-------"
            self.current_status = "-------"
            self.vehicle_brand = "-------"
            self.vehicle_style = "-------"
            self.vehicle_model = "-------"
            self.fuel_type = "-------"
            self.cylinder_count = "-------"
            self.exchange_allowance = "-------"
            self.processing_type = "-------"
            self.vehicle_color = "-------"
            self.litre_capacity = "-------"
            self.feeding_type = "-------"
            self.ignition_type = "-------"
            self.wheel_drive_type = "-------"
            self.transmission = "-------"
            self.possession_date = "-------"
            self.maintenance_entity = "-------"
            self.private_no = "-------"

        if self.vehicle_no and vehicles_list:
            for r in vehicles_list:
                vehicle = self.append("vehicle_inquiry_table", {})
                vehicle.vehicle_boat = r.vehicle_boat
                vehicle.vic_serial = r.name
                vehicle.vehicle_no = r.vehicle_no or r.police_id
                vehicle.entity = r.entity

                if r.vehicle_boat == "Boats":
                    vehicle.motor_no = (
                        frappe.db.get_value(
                            "Engine Table", {"parent": r.name, "idx": 1}, "engine_no"
                        )
                        or "-------"
                    )
                    vehicle.motor_no2 = (
                        frappe.db.get_value(
                            "Engine Table", {"parent": r.name, "idx": 2}, "engine_no"
                        )
                        or "-------"
                    )

        if frappe.db.exists(
            "Vehicles", {"vehicle_no": self.vehicle_no, "entity_name": self.entity_name}
        ):
            vic = frappe.get_doc(
                "Vehicles",
                {"vehicle_no": self.vehicle_no, "entity_name": self.entity_name},
            )
            self.vehicle = vic.vehicle_no or "-------"
            if vic.attached_entity == "" or vic.attached_entity == None:
                self.entity = vic.entity_name or "-------"
            else:
                self.entity = vic.entity_name + "<br>" + "(" + vic.attached_entity + ")"
            self.chassis_no = vic.chassis_no or "-------"
            self.motor_no = vic.motor_no or "-------"
            self.motor_no2 = "-------"
            self.vehicle_type = vic.vehicle_type or "-------"
            self.vehicle_country = vic.vehicle_country or "-------"
            self.vehicle_shape = vic.vehicle_shape or "-------"
            self.current_status = vic.vehicle_status or "-------"
            self.vehicle_brand = vic.vehicle_brand or "-------"
            self.vehicle_style = vic.vehicle_style or "-------"
            self.vehicle_model = vic.vehicle_model or "-------"
            self.fuel_type = vic.fuel_type or "-------"
            self.cylinder_count = vic.cylinder_count or "-------"
            self.exchange_allowance = vic.exchange_allowance or "-------"
            self.processing_type = vic.processing_type or "-------"
            self.vehicle_color = vic.vehicle_color or "-------"
            self.litre_capacity = vic.litre_capacity or "-------"
            self.feeding_type = vic.feeding_type or "-------"
            self.ignition_type = vic.ignition_type or "-------"
            self.wheel_drive_type = vic.wheel_drive_type or "-------"
            self.transmission = vic.transmission or "-------"
            self.possession_date = vic.possession_date or "-------"
            self.maintenance_entity = vic.maintenance_entity or "-------"
            self.private_no = vic.private_no or "-------"

        elif frappe.db.exists(
            "Vehicles", {"police_id": self.vehicle_no, "entity_name": self.entity_name}
        ):
            vic = frappe.get_doc(
                "Vehicles",
                {"police_id": self.vehicle_no, "entity_name": self.entity_name},
            )
            self.vehicle = vic.police_id or "-------"
            if vic.attached_entity == "" or vic.attached_entity == None:
                self.entity = vic.entity_name or "-------"
            else:
                self.entity = vic.entity_name + "<br>" + "(" + vic.attached_entity + ")"
            self.chassis_no = vic.chassis_no or "-------"
            self.motor_no = vic.motor_no or "-------"
            self.motor_no2 = "-------"
            self.vehicle_type = vic.vehicle_type or "-------"
            self.vehicle_country = vic.vehicle_country or "-------"
            self.vehicle_shape = vic.vehicle_shape or "-------"
            self.current_status = vic.vehicle_status or "-------"
            self.vehicle_brand = vic.vehicle_brand or "-------"
            self.vehicle_style = vic.vehicle_style or "-------"
            self.vehicle_model = vic.vehicle_model or "-------"
            self.fuel_type = vic.fuel_type or "-------"
            self.cylinder_count = vic.cylinder_count or "-------"
            self.exchange_allowance = vic.exchange_allowance or "-------"
            self.processing_type = vic.processing_type or "-------"
            self.vehicle_color = vic.vehicle_color or "-------"
            self.litre_capacity = vic.litre_capacity or "-------"
            self.feeding_type = vic.feeding_type or "-------"
            self.ignition_type = vic.ignition_type or "-------"
            self.wheel_drive_type = vic.wheel_drive_type or "-------"
            self.transmission = vic.transmission or "-------"
            self.possession_date = vic.possession_date or "-------"
            self.maintenance_entity = vic.maintenance_entity or "-------"
            self.private_no = vic.private_no or "-------"

        elif frappe.db.exists(
            "Boats", {"boat_no": self.vehicle_no, "entity_name": self.entity_name}
        ):
            vic = frappe.get_doc(
                "Boats", {"boat_no": self.vehicle_no, "entity_name": self.entity_name}
            )
            self.vehicle = vic.boat_no or "-------"
            self.entity = vic.entity_name or "-------"
            self.chassis_no = vic.chassis_no or "-------"
            self.motor_no = (
                frappe.db.get_value(
                    "Engine Table", {"parent": vic.name, "idx": 1}, "engine_no"
                )
                or "-------"
            )
            self.motor_no2 = (
                frappe.db.get_value(
                    "Engine Table", {"parent": vic.name, "idx": 2}, "engine_no"
                )
                or "-------"
            )
            self.vehicle_type = "لانش"
            self.vehicle_shape = vic.body_type or "-------"
            self.current_status = vic.boat_validity or "-------"
            self.vehicle_brand = vic.boat_brand or "-------"
            self.vehicle_style = vic.boat_style or "-------"
            self.vehicle_model = vic.boat_model or "-------"
            self.vehicle_country = "-------"
            self.fuel_type = vic.fuel_type or "-------"
            self.cylinder_count = vic.cylinder_count or "-------"
            self.possession_date = vic.issue_date or "-------"
            self.exchange_allowance = "-------"
            self.processing_type = "-------"
            self.vehicle_color = "-------"
            self.litre_capacity = "-------"
            self.feeding_type = "-------"
            self.ignition_type = "-------"
            self.wheel_drive_type = "-------"
            self.transmission = "-------"
            self.possession_date = "-------"
            self.maintenance_entity = "-------"
            self.private_no = "-------"
        elif frappe.db.exists("Vehicles", {"vehicle_no": self.vehicle_no}):
            vic = frappe.get_doc(
                "Vehicles",
                {"vehicle_no": self.vehicle_no},
            )

            if self.entity_name and not (
                vic.entity_name == self.entity_name
                or vic.attached_entity == self.entity_name
            ):
                frappe.throw(
                    "المركبة رقم {0} في جهة {1}".format(
                        self.vehicle_no, vic.attached_entity or vic.entity_name
                    )
                )

            self.vehicle = vic.vehicle_no or "-------"
            if vic.attached_entity == "" or vic.attached_entity == None:
                self.entity = vic.entity_name or "-------"
            else:
                self.entity = vic.entity_name + "<br>" + "(" + vic.attached_entity + ")"
            self.chassis_no = vic.chassis_no or "-------"
            self.motor_no = vic.motor_no or "-------"
            self.motor_no2 = "-------"
            self.vehicle_type = vic.vehicle_type or "-------"
            self.vehicle_country = vic.vehicle_country or "-------"
            self.vehicle_shape = vic.vehicle_shape or "-------"
            self.current_status = vic.vehicle_status or "-------"
            self.vehicle_brand = vic.vehicle_brand or "-------"
            self.vehicle_style = vic.vehicle_style or "-------"
            self.vehicle_model = vic.vehicle_model or "-------"
            self.fuel_type = vic.fuel_type or "-------"
            self.cylinder_count = vic.cylinder_count or "-------"
            self.exchange_allowance = vic.exchange_allowance or "-------"
            self.processing_type = vic.processing_type or "-------"
            self.vehicle_color = vic.vehicle_color or "-------"
            self.litre_capacity = vic.litre_capacity or "-------"
            self.feeding_type = vic.feeding_type or "-------"
            self.ignition_type = vic.ignition_type or "-------"
            self.wheel_drive_type = vic.wheel_drive_type or "-------"
            self.transmission = vic.transmission or "-------"
            self.possession_date = vic.possession_date or "-------"
            self.maintenance_entity = vic.maintenance_entity or "-------"
            self.private_no = vic.private_no or "-------"

        elif frappe.db.exists("Vehicles", {"police_id": self.vehicle_no}):
            vic = frappe.get_doc(
                "Vehicles",
                {"police_id": self.vehicle_no},
            )

            self.vehicle = vic.police_id or "-------"
            if vic.attached_entity == "" or vic.attached_entity == None:
                self.entity = vic.entity_name or "-------"
            else:
                self.entity = vic.entity_name + "<br>" + "(" + vic.attached_entity + ")"
            self.chassis_no = vic.chassis_no or "-------"
            self.motor_no = vic.motor_no or "-------"
            self.motor_no2 = "-------"
            self.vehicle_type = vic.vehicle_type or "-------"
            self.vehicle_country = vic.vehicle_country or "-------"
            self.vehicle_shape = vic.vehicle_shape or "-------"
            self.current_status = vic.vehicle_status or "-------"
            self.vehicle_brand = vic.vehicle_brand or "-------"
            self.vehicle_style = vic.vehicle_style or "-------"
            self.vehicle_model = vic.vehicle_model or "-------"
            self.fuel_type = vic.fuel_type or "-------"
            self.cylinder_count = vic.cylinder_count or "-------"
            self.exchange_allowance = vic.exchange_allowance or "-------"
            self.processing_type = vic.processing_type or "-------"
            self.vehicle_color = vic.vehicle_color or "-------"
            self.litre_capacity = vic.litre_capacity or "-------"
            self.feeding_type = vic.feeding_type or "-------"
            self.ignition_type = vic.ignition_type or "-------"
            self.wheel_drive_type = vic.wheel_drive_type or "-------"
            self.transmission = vic.transmission or "-------"
            self.possession_date = vic.possession_date or "-------"
            self.maintenance_entity = vic.maintenance_entity or "-------"
            self.private_no = vic.private_no or "-------"

        elif frappe.db.exists("Boats", {"boat_no": self.vehicle_no}):
            vic = frappe.get_doc("Boats", {"boat_no": self.vehicle_no})
            if self.entity_name and not (vic.entity_name == self.entity_name):
                frappe.throw(
                    "لانش رقم {0} في جهة {1}".format(self.vehicle_no, vic.entity_name)
                )
            self.vehicle = vic.boat_no or "-------"
            self.entity = vic.entity_name or "-------"
            self.chassis_no = vic.chassis_no or "-------"
            self.motor_no = (
                frappe.db.get_value(
                    "Engine Table", {"parent": vic.name, "idx": 1}, "engine_no"
                )
                or "-------"
            )
            self.motor_no2 = (
                frappe.db.get_value(
                    "Engine Table", {"parent": vic.name, "idx": 2}, "engine_no"
                )
                or "-------"
            )
            self.vehicle_type = "لانش"
            self.vehicle_shape = vic.body_type or "-------"
            self.current_status = vic.boat_validity or "-------"
            self.vehicle_brand = vic.boat_brand or "-------"
            self.vehicle_style = vic.boat_style or "-------"
            self.vehicle_model = vic.boat_model or "-------"
            self.vehicle_country = "-------"
            self.fuel_type = vic.fuel_type or "-------"
            self.cylinder_count = vic.cylinder_count or "-------"
            self.possession_date = vic.issue_date or "-------"
            self.exchange_allowance = "-------"
            self.processing_type = "-------"
            self.vehicle_color = "-------"
            self.litre_capacity = "-------"
            self.feeding_type = "-------"
            self.ignition_type = "-------"
            self.wheel_drive_type = "-------"
            self.transmission = "-------"
            self.possession_date = "-------"
            self.maintenance_entity = "-------"
            self.private_no = "-------"
        for row in self.vehicle_inquiry_table:
            if row.vehicle_no == self.vehicle:
                row.preview_data = 1


@frappe.whitelist()
def get_vehicle_details(vehicle_boat, vic_serial):
    try:
        return frappe.get_doc(vehicle_boat, vic_serial)
    except Exception as e:
        frappe.msgprint(str(e))

        return e
