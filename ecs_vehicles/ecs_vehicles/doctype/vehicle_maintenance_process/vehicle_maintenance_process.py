# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date
from frappe.utils import flt, rounded, add_months, nowdate, getdate, now_datetime
from datetime import date
import json
from frappe.utils import in_words


@frappe.whitelist()
def get_last_sarf_detail(vehicles, item_code):
    last_sarf_date = frappe.db.sql(
        """ select
                                                stock_ledger.action_date, stock_ledger.part_qty
                                                from `tabKarta Ledger Entry` stock_ledger 
                                                where stock_ledger.vic_serial = '{vehicles}'
                                                and stock_ledger.part_universal_code = '{item_code}'
                                                and stock_ledger.del_flag = "0"
                                                order by stock_ledger.action_date desc limit 1
                                                """.format(
            vehicles=vehicles, item_code=item_code
        ),
        as_dict=1,
    )
    try:
        return last_sarf_date[0].action_date, last_sarf_date[0].part_qty
    except:
        return "لم يسبق"


@frappe.whitelist()
def create_karta_ledger_entry_method(
    item, vehicles, ezn_no, date, entity_name, fis_year
):
    # frappe.msgprint(str(item))
    item = json.loads(item)
    # frappe.msgprint(str(item))

    if item["maintenance_method"] == "إذن صرف وإرتجاع" and not item.get("kle"):
        new_doc = frappe.get_doc(
            {
                "doctype": "Karta Ledger Entry",
                "ord_serial": item["parent"],
                "detail_serial": item["name"],
                "vic_serial": vehicles,
                "part_universal_code": item["item_code"],
                "action_date": nowdate(),
                "part_unit": item.get("default_unit_of_measure"),
                "part_status_ratio": item.get("quality"),
                "part_country": item.get("brand", ""),
                "workshop_type": "ورش داخلية",
                "workshop_name": frappe.db.get_value(
                    "Item", item["item_code"], "warehouse"
                ),
                "ezn_no": ezn_no,
                "ezn_date": date,
                "doc_type": "Vehicle Maintenance Process",
                "geha_code": entity_name,
                "year": fis_year,
                "trans_type": "كارتة عهد",
                "part_qty": item.get("qty"),
                "del_flag": 0,
            }
        )
        new_doc.insert(ignore_permissions=True)
        return new_doc.name


class VehicleMaintenanceProcess(Document):
    def get_in_words(self):
        real_no = str(round(float(self.mozakira_total_amount), 2)).split(".")[0]
        piasters = str(round(float(self.mozakira_total_amount), 2)).split(".")[1]
        if int(piasters) > 0:
            if int(piasters) > 10:
                self.total_in_words = (
                    in_words(int(real_no))
                    + " جنيها و "
                    + in_words(int(piasters))
                    + " قرشا فقط"
                )
            else:
                self.total_in_words = (
                    in_words(int(real_no))
                    + " جنيها و "
                    + in_words(int(piasters + "0"))
                    + " قرشا فقط"
                )

        else:
            self.total_in_words = in_words(int(real_no)) + " جنيها فقط"

    def get_in_words2(self):
        real_no = str(round(float(self.aamr_shoghl_total_amount), 2)).split(".")[0]
        piasters = str(round(float(self.aamr_shoghl_total_amount), 2)).split(".")[1]
        if int(piasters) > 0:
            if int(piasters) > 10:
                self.aamr_shoghl_total_in_words = (
                    in_words(int(real_no))
                    + " جنيها و "
                    + in_words(int(piasters))
                    + " قرشا فقط"
                )
            else:
                self.aamr_shoghl_total_in_words = (
                    in_words(int(real_no))
                    + " جنيها و "
                    + in_words(int(piasters + "0"))
                    + " قرشا فقط"
                )

        else:
            self.aamr_shoghl_total_in_words = in_words(int(real_no)) + " جنيها فقط"

    @frappe.whitelist()
    def opened_job_order(self):
        opended_job = 0
        for x in self.kashf_ohda_item:
            if (
                x.maintenance_method == "إصلاح خارجي"
                and x.include_in_maintenance_order == 1
            ):
                opended_job = 1
        # job_order_list = frappe.db.get_list("Vehicle Maintenance Process", filters=[["vehicles","=", self.vehicles], ["fiscal_year","=",self.fiscal_year], ["name","!=", self.name], ["job_order_no", "!=", None]], fields={"name", "job_order_no", "job_order_date", "fiscal_year", "purchase_invoices"})
        if opended_job == 1:
            job_order_list = frappe.db.sql(
                """
            SELECT name, job_order_no, job_order_date, fiscal_year, purchase_invoices
            FROM `tabVehicle Maintenance Process` vehicle_maintenance_process
            WHERE vehicle_maintenance_process.vehicles = "{vehicles}"
            AND vehicle_maintenance_process.fiscal_year = "{fiscal_year}"
            AND vehicle_maintenance_process.name != "{name}"
            AND vehicle_maintenance_process.job_order_no  is not NULL
            AND vehicle_maintenance_process.cancel_ezn  = 0
            """.format(
                    vehicles=self.vehicles, fiscal_year=self.fiscal_year, name=self.name
                ),
                as_dict=1,
            )

            if job_order_list:
                for y in job_order_list:
                    # purchase_invoices_list = frappe.db.exists("Vehicle Maintenance Process", filters={"vehicles": self.vehicles, "job_order_no":y.job_order_no}, fields={"name"})
                    if not y.purchase_invoices and self.pass_order == 0:
                        # if not purchase_invoices_list and not self.pass_order:
                        return (
                            " لا يجوز إضافة إجراء إصلاح خارجي للمركبة وذلك لوجود أمر شغل ساري رقم "
                            + str(y.job_order_no)
                            + " بتاريخ "
                            + str(y.ezn_date or y.fiscal_year)
                        )
                        # frappe.throw(" لا يجوز إضافة إجراء إصلاح خارجي للمركبة وذلك لوجود أمر شغل ساري رقم " + str(y.job_order_no) + " بتاريخ " + str(y.ezn_date or y.fiscal_year))

    def validate_for_duplicate_items(self):
        check_list = []
        for d in self.get("kashf_ohda_item"):
            kashf_items = [d.item_code, d.item_name, d.maintenance_method]
            duplicate_items_msg = ("الصنف {0} تم إضافته أكثر من مرة").format(
                frappe.bold(d.item_name)
            )
            duplicate_items_msg += "<br><br>"
            if kashf_items in check_list:
                frappe.throw(duplicate_items_msg)
            else:
                check_list.append(kashf_items)

    def karta_new_function(self):
        detailed_karta_list = frappe.db.sql(
            """
            select part_universal_code, part_qty, maintenance_method
            from `tabKarta Ledger Entry`
            where ord_serial = '{ord_serial}' and del_flag = "0"
            and maintenance_method = "إذن صرف وإرتجاع"
            """.format(
                ord_serial=self.name
            ),
            as_dict=1,
        )

        # frappe.msgprint(str(detailed_karta_list))

        karta_items_list = []
        if detailed_karta_list:
            for u in detailed_karta_list:
                karta_items_list.append(u.part_universal_code)

        # frappe.msgprint(str(karta_items_list))

        kashf_items_list = []
        for z in self.kashf_ohda_item:
            if (
                z.maintenance_method == "إذن صرف وإرتجاع"
                and z.include_in_maintenance_order
            ):
                kashf_items_list.append(z.item_code)

        # frappe.msgprint(str(kashf_items_list))

        if not detailed_karta_list:
            for row in self.kashf_ohda_item:
                if (
                    row.maintenance_method == "إذن صرف وإرتجاع"
                    and row.include_in_maintenance_order
                ):
                    new_doc = frappe.get_doc(
                        {
                            "doctype": "Karta Ledger Entry",
                            "ord_serial": self.name,
                            "detail_serial": row.name,
                            "vic_serial": self.vehicles,
                            "part_universal_code": row.item_code,
                            "action_date": nowdate(),
                            "part_unit": row.default_unit_of_measure,
                            "part_status_ratio": row.quality,
                            "part_country": row.brand,
                            "workshop_type": "ورش داخلية",
                            "workshop_name": frappe.db.get_value(
                                "Item", row.item_code, "warehouse"
                            ),
                            "ezn_no": self.ezn_no,
                            "ezn_date": self.ezn_date,
                            "doc_type": "Vehicle Maintenance Process",
                            "geha_code": self.entity_name,
                            "year": self.fiscal_year,
                            "trans_type": "كارتة عهد",
                            "part_qty": row.qty,
                            "maintenance_method": row.maintenance_method,
                            "del_flag": "0",
                        }
                    )
                    new_doc.insert(ignore_permissions=True)
                    row.kle = new_doc.name

        if detailed_karta_list:
            for item in karta_items_list:
                if item not in kashf_items_list:
                    frappe.db.sql(
                        """ 
                        UPDATE `tabKarta Ledger Entry` set del_flag = "1"
                        WHERE part_universal_code='{part_universal_code}' and ord_serial='{ord_serial}'
                    """.format(
                            part_universal_code=item, ord_serial=self.name
                        )
                    )

                if item in kashf_items_list:
                    for row in self.kashf_ohda_item:
                        if row.include_in_maintenance_order and row.item_code == item:
                            for k in detailed_karta_list:
                                if (
                                    row.item_code == k.part_universal_code
                                    and row.qty == k.part_qty
                                    and row.maintenance_method == k.maintenance_method
                                ):
                                    pass

                                elif (
                                    row.item_code == k.part_universal_code
                                    and row.qty != k.part_qty
                                    and row.maintenance_method == k.maintenance_method
                                ):
                                    frappe.db.sql(
                                        """ 
                                        UPDATE `tabKarta Ledger Entry` set action_date = '{action_date}',
                                        part_universal_code = '{item_code}', part_qty = '{part_qty}',
                                        maintenance_method = '{maintenance_method}'
                                        WHERE del_flag = "0" and part_universal_code='{part_universal_code}' and ord_serial='{ord_serial}'
                                    """.format(
                                            action_date=nowdate(),
                                            item_code=k.part_universal_code,
                                            part_qty=row.qty,
                                            maintenance_method=row.maintenance_method,
                                            part_universal_code=k.part_universal_code,
                                            ord_serial=self.name,
                                        )
                                    )

                                elif (
                                    row.item_code == k.part_universal_code
                                    and row.maintenance_method != k.maintenance_method
                                ):
                                    frappe.db.sql(
                                        """ 
                                        UPDATE `tabKarta Ledger Entry` set del_flag = "1"
                                        WHERE del_flag = "0" and part_universal_code='{part_universal_code}' and ord_serial='{ord_serial}'
                                        AND name = "{kle}"
                                    """.format(
                                            action_date=nowdate(),
                                            item_code=k.part_universal_code,
                                            part_qty=row.qty,
                                            maintenance_method=row.maintenance_method,
                                            part_universal_code=k.part_universal_code,
                                            ord_serial=self.name,
                                            kle=row.kle,
                                        )
                                    )

                        elif (
                            not row.include_in_maintenance_order
                            and row.item_code == item
                        ):
                            frappe.db.sql(
                                """ 
                                UPDATE `tabKarta Ledger Entry` set del_flag = "1"
                                WHERE part_universal_code='{part_universal_code}' and ord_serial='{ord_serial}'
                            """.format(
                                    part_universal_code=item, ord_serial=self.name
                                )
                            )

            for kashf in kashf_items_list:
                if kashf not in karta_items_list:
                    for row in self.kashf_ohda_item:
                        if (
                            row.maintenance_method == "إذن صرف وإرتجاع"
                            and row.include_in_maintenance_order
                            and row.item_code == kashf
                        ):
                            new_doc = frappe.get_doc(
                                {
                                    "doctype": "Karta Ledger Entry",
                                    "ord_serial": self.name,
                                    "detail_serial": row.name,
                                    "vic_serial": self.vehicles,
                                    "part_universal_code": row.item_code,
                                    "action_date": nowdate(),
                                    "part_unit": row.default_unit_of_measure,
                                    "part_status_ratio": row.quality,
                                    "part_country": row.brand,
                                    "workshop_type": "ورش داخلية",
                                    "workshop_name": frappe.db.get_value(
                                        "Item", row.item_code, "warehouse"
                                    ),
                                    "ezn_no": self.ezn_no,
                                    "ezn_date": self.ezn_date,
                                    "doc_type": "Vehicle Maintenance Process",
                                    "geha_code": self.entity_name,
                                    "year": self.fiscal_year,
                                    "trans_type": "كارتة عهد",
                                    "part_qty": row.qty,
                                    "maintenance_method": row.maintenance_method,
                                    "del_flag": "0",
                                }
                            )
                            new_doc.insert(ignore_permissions=True)
                            row.kle = new_doc.name

    def assign_shadow(self):
        # if item.maintenance_method == "حافظة مشتريات" self.shadow = 1
        for row in self.kashf_ohda_item:
            # check if this item found before in the same fiscal year for the same vehicle in Vehicle Maintenance Process
            # if found then update the shadow field to 1
            check_shadow = frappe.db.sql(
                """
                select kashf_item.item_code
                from `tabVehicle Maintenance Process` vmp
                join `tabKashf Ohda Item` kashf_item on kashf_item.parent = vmp.name
                where vmp.vehicles = '{vehicles}' 
                and vmp.fiscal_year = '{fiscal_year}'
                and vmp.name != '{name}'
                and kashf_item.item_code = '{item_code}'
                and kashf_item.maintenance_method in ("حافظة مشتريات", "إصلاح خارجي")
                and kashf_item.include_in_maintenance_order = 1
                """.format(
                    vehicles=self.vehicles,
                    fiscal_year=self.fiscal_year,
                    name=self.name,
                    item_code=row.item_code,
                ),
                as_dict=1,
            )
            if check_shadow:
                for x in check_shadow:
                    row.shadow = 1
            else:
                row.shadow = 0

    def validate(self):
        self.validate_for_duplicate_items()

        if not self.kashf_ohda_item:
            frappe.throw(" برجاء إضافة قطع الغيار داخل كشف العهدة ")

        if self.ezn_no:
            ezn_no_list = frappe.db.sql(
                """ Select ezn_no, name from `tabVehicle Maintenance Process`
            where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(
                    name=self.name, fiscal_year=self.fiscal_year
                ),
                as_dict=1,
            )

            for x in ezn_no_list:
                if self.ezn_no == x.ezn_no:
                    frappe.throw(
                        " لا يمكن تكرار رقم الإذن "
                        + str(x.ezn_no)
                        + " أكثر من مرة قي نفس السنة المالية حيث أنه مستخدم في المستند "
                        + x.name
                    )

        if self.mozakira_no:
            mozakira_no_list = frappe.db.sql(
                """ Select mozakira_no, name from `tabVehicle Maintenance Process`
            where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(
                    name=self.name, fiscal_year=self.fiscal_year
                ),
                as_dict=1,
            )

            for x in mozakira_no_list:
                if self.mozakira_no == x.mozakira_no:
                    frappe.throw(
                        " لا يمكن تكرار رقم المذكرة "
                        + str(x.mozakira_no)
                        + " أكثر من مرة قي نفس السنة المالية حيث أنه مستخدم في المستند "
                        + x.name
                    )

        if self.job_order_no:
            job_order_no_list = frappe.db.sql(
                """ Select job_order_no, name from `tabVehicle Maintenance Process`
            where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(
                    name=self.name, fiscal_year=self.fiscal_year
                ),
                as_dict=1,
            )

            for x in job_order_no_list:
                if self.job_order_no == x.job_order_no:
                    frappe.throw(
                        " لا يمكن تكرار رقم المذكرة "
                        + str(x.job_order_no)
                        + " أكثر من مرة قي نفس السنة المالية حيث أنه مستخدم في المستند "
                        + x.name
                    )

        for row in self.kashf_ohda_item:
            if row.maintenance_method == "إصلاح خارجي" and not row.maintenance_type:
                frappe.throw(" برجاء تحديد طبيعة الإصلاح للإصلاح الخارجي ")
        #                                                and (stock_ledger.doc_type = "Vehicle Maintenance Process" and stock_ledger.maintenance_method != "إصلاح خارجي")

        # if(item.include_in_maintenance_order && emdad2023emdad_2023 !ezn_egraa_item2.includes(item.name.toString()) && item.maintenance_method === "إذن صرف وإرتجاع" && !item.kle) {
        for item in self.kashf_ohda_item:
            last_sarf_date = frappe.db.sql(
                """ select
                        stock_ledger.action_date, stock_ledger.part_qty
                        from `tabKarta Ledger Entry` stock_ledger 
                        where stock_ledger.vic_serial = '{vehicles}'
                        and stock_ledger.part_universal_code = '{item_code}'
                        and stock_ledger.del_flag = "0"
                        and (
                        (stock_ledger.maintenance_method = "إذن صرف وإرتجاع"
                        and doc_type = "Vehicle Maintenance Process" ) 
                        or 
                        (stock_ledger.maintenance_method = "إصلاح خارجي"
                        and doc_type = "Purchase Invoices" ) 
                        or 
                        (stock_ledger.maintenance_method = "خطاب جهة"
                        and doc_type = "Add To Karta" )
                        )
                        order by stock_ledger.action_date desc limit 1
                """.format(
                    vehicles=self.vehicles, item_code=item.item_code
                ),
                as_dict=1,
            )

            try:
                if not item.last_issue_detail:
                    item.last_sarf_qty = last_sarf_date[0].part_qty
                    item.last_issue_detail = last_sarf_date[0].action_date
            except:
                if not item.last_issue_detail:
                    item.last_issue_detail = "لم يسبق"
        self.assign_shadow()
        self.ezn_egraa_item = []
        for item in self.kashf_ohda_item:
            if not item.qty and item.include_in_maintenance_order:
                frappe.throw("برجاء اضافة كمية كل صنف")
            if item.include_in_maintenance_order and not item.maintenance_method:
                frappe.throw("برجاء إضافة طريقة الإصلاح")
            if item.maintenance_method != "إصلاح خارجي":
                item.maintenance_type = ""
            if item.include_in_maintenance_order:
                table = self.append("ezn_egraa_item", {})
                table.action_date = nowdate()
                table.maintenance_method = item.maintenance_method
                table.maintenance_type = item.maintenance_type
                table.consumption_type = item.consumption_type
                table.scrapped_vehicle = item.scrapped_vehicle
                table.item_code = item.item_code
                table.item_name = item.item_name
                table.item_group = item.item_group
                table.description = item.description
                table.brand = item.brand
                table.qty = item.qty
                table.default_unit_of_measure = item.default_unit_of_measure
                table.disc = item.disc
                table.quality = item.quality
                table.store_code = item.store_code
                table.last_issue_detail = item.last_issue_detail
                table.last_sarf_qty = item.last_sarf_qty
                table.namozg_no2 = item.namozag_no
                table.is_printed = item.egraa_printed
                table.custody_report_item = item.name

                # if item.maintenance_method == "إذن صرف وإرتجاع":
                #     new_doc = frappe.get_doc({
                #                 "doctype": "Karta Ledger Entry",
                #                 "ord_serial" : item.parent,
                #                 "detail_serial" : item.name,
                #                 "vic_serial" : self.vehicles,
                #                 "part_universal_code" : item.item_code,
                #                 # "action_date" : nowdate(),
                #                 "action_date" : self.ezn_date,
                #                 "part_unit" : item.default_unit_of_measure,
                #                 "part_status_ratio" : item.quality,
                #                 "part_country" : item.brand,
                #                 "workshop_type" : "ورش داخلية",
                #                 "workshop_name" : frappe.db.get_value("Item", item.item_code, "warehouse"),
                #                 "ezn_no" : self.ezn_no,
                #                 "ezn_date" : self.ezn_date,
                #                 "doc_type" : "Vehicle Maintenance Process",
                #                 "geha_code" : self.entity_name,
                #                 "year" : self.fiscal_year,
                #                 "trans_type" : "كارتة عهد",
                #                 "part_qty" : item.qty,
                #                 "del_flag": 0
                #             })
                #     new_doc.insert(ignore_permissions=True)
                #     item.kle = new_doc.name
                #     table.kle= new_doc.name

        if self.talb_total_amount:
            if self.edit_in_words == 0:
                self.talab_total_in_words = in_words(
                    self.talb_total_amount, "جنيها مصريا فقط لا غير"
                )

        if self.mozakira_total_amount:
            if self.edit_in_words2 == 0:
                self.get_in_words()
                # self.total_in_words = in_words(self.mozakira_total_amount, "جنيها مصريا فقط لا غير")

        if self.aamr_shoghl_total_amount:
            if self.edit_in_words3 == 0:
                self.get_in_words2()
                # self.aamr_shoghl_total_in_words = in_words(self.aamr_shoghl_total_amount, "جنيها مصريا فقط لا غير")

        # if self.total:
        #     self.purchase_inwords = in_words(self.total, "جنيها مصريا فقط لا غير")

        if self.job_order_date:
            self.work_end_date = add_to_date(self.job_order_date, days=10)

        self.edit_ezn = 0
        self.karta_new_function()

    def on_trash(self):
        frappe.db.sql(
            """ update `tabKarta Ledger Entry` set del_flag = "1"
                where ord_serial ='{ord_serial}'
            """.format(
                ord_serial=self.name
            )
        )

    @frappe.whitelist()
    def wheels_update_table(doc, method=None):
        today = date.today()
        past_date = add_months(today, -32)
        last_sarf_date = frappe.db.sql(
            """ select  item.item_code, item.item_name, item.item_group, item.description,
                                                karta_ledger.action_date, karta_ledger.part_qty
                                                from `tabKarta Ledger Entry` karta_ledger
                                                JOIN  `tabItem` item ON item.item_code = part_universal_code
                                                where karta_ledger.vic_serial = '{vehicles}'
                                                and item.item_name Like '%اطار%'
                                                and karta_ledger.del_flag = "0"
                                                and karta_ledger.action_date > "{past_date}"
                                                """.format(
                vehicles=doc.vehicles,
                item_group="اطارات داخلية و خارجية",
                past_date=past_date,
            ),
            as_dict=1,
        )
        for row in last_sarf_date:
            table = doc.append("kashf_ohda_item", {})
            table.item_code = row.item_code
            table.item_name = row.item_name
            table.item_group = row.item_group
            table.default_unit_of_measure = "بالعدد"
            table.include_in_maintenance_order = 0
            table.namozag_no = "1"
            table.qty = 1
            table.last_issue_detail = row.action_date
            table.last_sarf_qty = row.part_qty
            
    @frappe.whitelist()
    def battaries_update_table(doc, method=None):
        today = date.today()
        past_date = add_months(today, -32)
        last_sarf_date = frappe.db.sql(
            """ select  item.item_code, item.item_name, item.item_group, item.description,
                                                karta_ledger.action_date, karta_ledger.part_qty
                                                from `tabKarta Ledger Entry` karta_ledger
                                                JOIN  `tabItem` item ON item.item_code = part_universal_code
                                                where karta_ledger.vic_serial = '{vehicles}'
                                                and item.item_name Like '%بطاريه%'
                                                and karta_ledger.del_flag = "0"
                                                and karta_ledger.action_date > "{past_date}"
                                                """.format(
                vehicles=doc.vehicles,
                item_group="اطارات داخلية و خارجية",
                past_date=past_date,
            ),
            as_dict=1,
        )
        for row in last_sarf_date:
            table = doc.append("kashf_ohda_item", {})
            table.item_code = row.item_code
            table.item_name = row.item_name
            table.item_group = row.item_group
            table.default_unit_of_measure = "بالعدد"
            table.qty = 1
            table.include_in_maintenance_order = 0
            table.namozag_no = "1"

    @frappe.whitelist()
    def update_table(doc, method=None):
        if doc.select_type == "مجموعات متوافقة":
            first_list = frappe.db.sql(
                """ select  a.item_code, c.item_name, c.item_group, c.description
                                            from `tabProduct Bundle Item` a join `tabProduct Bundle` b 
                                            on a.parent = b.name join `tabItem` c on a.item_code = c.name
                                            where b.new_item_code = '{new_item_code}'
                                            """.format(
                    new_item_code=doc.bundle
                ),
                as_dict=1,
            )

            for z in first_list:
                table = doc.append("kashf_ohda_item", {})
                table.item_code = z.item_code
                table.item_name = z.item_name
                table.item_group = z.item_group
                table.default_unit_of_measure = "بالعدد"
                table.qty = 1
                table.include_in_maintenance_order = 0
                table.namozag_no = "1"
                # table.last_issue_detail = last_sarf_date.get(str(z.item_code) + str(doc.vehicles), "لم يسبق").split("$")[0] if last_sarf_date.get(str(z.item_code) + str(doc.vehicles), "لم يسبق") != "لم يسبق" else "لم يسبق"
                # table.last_sarf_qty = last_sarf_date.get(str(z.item_code) + str(doc.vehicles), "لم يسبق").split("$")[1] if last_sarf_date.get(str(z.item_code) + str(doc.vehicles), "لم يسبق") != "لم يسبق" else "لم يسبق"

    @frappe.whitelist()
    def add_maintenance_rfq(doc, method=None):
        if not doc.ezn_egraa_item:
            frappe.throw(
                " لم يتم إضافة أى قطعة غيار بطبيعة إصلاح خارجي داخل جدول قطع الغيار بإذن الإجراء "
            )
        external_fix_list = []
        for row in doc.ezn_egraa_item:
            if row.maintenance_method == "إصلاح خارجي":
                external_fix_list.append(row)
        if not external_fix_list:
            frappe.throw(
                " لم يتم إضافة أى قطعة غيار بطبيعة إصلاح خارجي داخل جدول قطع الغيار بإذن الإجراء "
            )

        doc.talb_date = date.today()
        doc.talb_oroud_asaar_item = []
        for row in doc.ezn_egraa_item:
            if row.maintenance_method == "إصلاح خارجي":
                table = doc.append("talb_oroud_asaar_item", {})
                table.item_group = row.item_group
                table.maintenance_type = row.maintenance_type
                table.consumption_type = row.consumption_type
                table.item_code = row.item_code
                table.item_name = row.item_name
                table.description = row.description
                table.brand = row.brand
                table.default_unit_of_measure = row.default_unit_of_measure
                table.qty = row.qty
                table.discount_ratio = row.disc
                table.rate = 0
                table.amount = 0
        doc.save()
        frappe.msgprint(
            " تم إنشاء طلب عروض أسعار لقطع الغيار الموجودة بإذن الإجراء بنجاح "
        )

    @frappe.whitelist()
    def add_presentation_note_out(doc, method=None):
        # if not doc.accepted_supplier:
        #     frappe.throw(" برجاء تحديد المورد المقبول في طلب عروض الأسعار")
        # if not doc.talb_total_amount:
        #     frappe.throw(" برجاء تحديد السعر الإجمالي في طلب عروض الأسعار")
        doc.mozakira_date = date.today()
        # doc.supplier = doc.accepted_supplier
        doc.check_byname = doc.accepted_supplier
        doc.contract_term = "7"
        doc.fix_period = 10
        # doc.mozakira_total_amount = doc.talb_total_amount
        doc.total_in_words = in_words(doc.talb_total_amount, "جنيها مصريا فقط لا غير")
        doc.mozakira_item = []
        for row in doc.talb_oroud_asaar_item:
            table = doc.append("mozakira_item", {})
            table.maintenance_type = row.maintenance_type
            table.consumption_type = row.consumption_type
            table.item_code = row.item_code
            table.item_name = row.item_name
            table.item_group = row.item_group
            table.description = row.description
            table.brand = row.brand
            table.default_unit_of_measure = row.default_unit_of_measure
            table.qty = row.qty
            table.discount_amount = row.discount_ratio
            table.rate = row.rate
            table.amount = row.amount
        doc.save()
        frappe.msgprint(" تم إنشاء مذكرة عرض بنجاح ")

    @frappe.whitelist()
    def add_job_order(doc, method=None):
        if not doc.mozakira_no:
            frappe.throw(" برجاء تحديد رقم المذكرة في مذكرة العرض ")
        if not doc.supplier:
            frappe.throw(" برجاء تحديد المورد في مذكرة العرض ")
        if not doc.mozakira_total_amount:
            frappe.throw(" برجاء تحديد السعر الإجمالي في مذكرة العرض ")
        # if frappe.db.sql("""SELECT
        #     name
        #     FROM `tabVehicle Maintenance Process` vehicle_maintenance_process
        #     WHERE job_order_no = "{job_order_no}"
        #     AND fiscal_year= "{fiscal_year}"
        #     AND vehicles="{vehicles}"
        #     AND name != "{name}"
        #     """.format(job_order_no=doc.mozakira_no, fiscal_year=doc.fiscal_year,vehicles=doc.vehicles, name=doc.name),as_dict=1):
        #     # frappe.msg_print("أمر شغل موجود من قبل على نفس المركبة ")
        #     aamr_shoghl_status = 'معـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــاد'
        #     vehicle_maintenance_process = doc.name
        # else:
        #     aamr_shoghl_status = ""
        #     vehicle_maintenance_process = ""
        doc.job_order_date = date.today()
        doc.work_end_date = add_to_date(doc.job_order_date, days=10)
        doc.job_order_no = doc.mozakira_no
        doc.fix_perod = "10"
        doc.supplier2 = doc.supplier
        # doc.aamr_shoghl_status = aamr_shoghl_status
        # doc.vehicle_maintenance_process = vehicle_maintenance_process
        doc.aamr_shoghl_total_amount = doc.mozakira_total_amount
        doc.aamr_shoghl_total_in_words = in_words(
            doc.mozakira_total_amount, "جنيها مصريا فقط لا غير"
        )
        doc.aamr_shoghl_item = []
        for row in doc.mozakira_item:
            table = doc.append("aamr_shoghl_item", {})
            table.maintenance_type = row.maintenance_type
            table.consumption_type = row.consumption_type
            table.item_code = row.item_code
            table.item_name = row.item_name
            table.item_group = row.item_group
            table.description = row.description
            table.brand = row.brand
            table.default_unit_of_measure = row.default_unit_of_measure
            table.qty = row.qty
            table.discount_amount = row.discount_amount
            table.rate = row.rate
            table.amount = row.amount
        doc.save()
        frappe.msgprint(" تم إنشاء أمر شغل بنجاح ")

    @frappe.whitelist()
    def add_maintenance_invoice(doc, method=None):
        if not doc.job_order_no:
            frappe.throw(" برجاء إضافة رقم الشغل ")
        if frappe.db.exists(
            "Purchase Invoices",
            {"year": doc.fiscal_year, "order_no": doc.job_order_no},
            ["name"],
        ):
            purchase_invoices_status = (
                "معـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــاد"
            )
        else:
            purchase_invoices_status = ""
        new_doc = frappe.get_doc(
            {
                "doctype": "Purchase Invoices",
                "year": doc.fiscal_year,
                "date": nowdate(),
                "ezn_no": doc.ezn_no,
                "purchase_invoices_status": purchase_invoices_status,
                "vehicle_maintenance_process": doc.name,
                "jop_order": doc.name,
                "order_no": doc.job_order_no,
                "order_date": doc.job_order_date,
                "pre_no_type": doc.fix_type,
                "supplier": doc.supplier2,
                "vehicles": doc.vehicles,
                "total": doc.aamr_shoghl_total_amount,
                "vehicle_no": doc.vehicle_no,
                "vehicle_brand": doc.vehicle_brand,
                "group_shape": doc.group_shape,
                "vehicle_model": doc.vehicle_model,
                "chassis_no": doc.chassis_no,
                "entity_name": doc.entity_name,
                "possession_type": doc.possession_type,
                "vehicle_shape": doc.vehicle_shape,
                "vehicle_style": doc.vehicle_style,
                "maintenance_entity": doc.maintenance_entity,
            }
        )

        for x in doc.aamr_shoghl_item:
            table = new_doc.append("purchase_invoices_table", {})
            table.item_group = x.item_group
            table.maintenance_type = x.maintenance_type
            table.dis_cause = x.consumption_type
            table.item_code = x.item_code
            table.item_name = x.item_name
            table.description = x.description
            table.default_unit_of_measure = x.default_unit_of_measure
            table.brand = x.brand
            table.part_qty = x.qty
            table.part_price = x.rate
            table.amount = x.amount
            table.dis_rate = x.discount_amount

        new_doc.insert(ignore_permissions=True)
        doc.purchase_invoices = new_doc.name
        doc.save()
        frappe.msgprint(
            " تم إنشاء فاتورة صيانة <a href=/app/purchase-invoices/{0}>{1}</a>".format(
                new_doc.name, new_doc.name
            )
        )

    # @frappe.whitelist()
    # def create_purchase_order_request(doc, method=None):
    #     doc.order_request_items = []
    #     for row in doc.ezn_egraa_item:
    #         if row.maintenance_method == "حافظة مشتريات":
    #             table = doc.append("order_request_items", {})
    #             table.item_code = row.item_code
    #             table.item_name = row.item_name
    #             table.item_group = row.item_group
    #             table.description = row.description
    #             table.brand = row.brand
    #             table.default_unit_of_measure = row.default_unit_of_measure
    #             table.qty = row.qty
    #             table.disc = row.disc
    #             table.prt_prc = 0
    #             table.amount = 0
    #     doc.save()
    #     frappe.msgprint(" تم إنشاء طلب عرض أسعار مشتريات بنجاح ")

    @frappe.whitelist()
    def print_internal_ezn(doc, method=None):
        doc.print_internal_ezn_count += 1
        doc.last_print_internal_ezn_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "كشف عهدة"
        table.format_no = doc.print_templete1
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

        # item_to_be_printed = 0
        # for x in doc.kashf_ohda_item:
        #     if x.is_printed == 0 and x.namozag_no == doc.print_templete1:
        #         item_to_be_printed = 1
        # if item_to_be_printed == 1:
        #     for row in doc.kashf_ohda_item:
        #         if row.namozag_no == doc.print_templete1:
        #             row.is_printed = 1
        #     doc.print_internal_ezn_count += 1
        #     doc.last_print_internal_ezn_date = nowdate()
        #     doc.save()
        #     doc.reload()

        # elif item_to_be_printed == 0 and doc.enable_print == 1:
        #     doc.print_internal_ezn_count += 1
        #     doc.last_print_internal_ezn_date = nowdate()
        #     doc.save()
        #     doc.reload()

        # else:
        #     return " لقد تم طباعة جميع الأصناف بنموذج رقم " + str(doc.print_templete1) + " من قبل ولا يمكن طباعتها مرة أخرى ... برجاء الرجوع للإدارة "

    @frappe.whitelist()
    def print_external_ezn(doc, method=None):
        doc.print_external_ezn_count += 1
        doc.last_print_external_ezn_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "إذن إصلاح خارجي"
        table.format_no = doc.print_templete2
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

        # items_to_be_printed = 0
        # for x in doc.ezn_egraa_item:
        #     if x.is_printed == 0 and x.namozg_no2 == doc.print_templete2 and x.maintenance_method == "إصلاح خارجي":
        #         items_to_be_printed = 1
        # if items_to_be_printed == 1:
        #     for row in doc.ezn_egraa_item:
        #         if row.namozg_no2 == doc.print_templete2 and row.maintenance_method == "إصلاح خارجي":
        #             row.is_printed = 1
        #             frappe.db.sql(""" UPDATE `tabKashf Ohda Item`
        #                             SET egraa_printed = 1 WHERE name = '{name}' and parent='{parent}'
        #                         """.format(name=row.custody_report_item, parent=doc.name))
        #             frappe.db.commit()
        #             # row.is_printed = 1
        #             # frappe.db.set_value("Kashf Ohda Item", row.custody_report_item, "egraa_printed", 1)
        #             # item = frappe.get_doc("Kashf Ohda Item", row.custody_report_item)
        #             # item.egraa_printed = 1
        #             # item.save()
        #     doc.print_external_ezn_count += 1
        #     doc.last_print_external_ezn_date = nowdate()
        #     doc.save()
        #     doc.reload()

        # elif items_to_be_printed == 0 and doc.enable_print == 1:
        #     doc.print_external_ezn_count += 1
        #     doc.last_print_external_ezn_date = nowdate()
        #     doc.save()
        #     doc.reload()

        # else:
        #     return " لقد تم طباعة جميع الأصناف بنموذج رقم " + str(doc.print_templete2) + " من قبل ولا يمكن طباعتها مرة أخرى ... برجاء الرجوع للإدارة "

    @frappe.whitelist()
    def print_external_ezn_on_entity(doc, method=None):
        doc.print_external_ezn_on_entity_count += 1
        doc.last_print_external_ezn_on_entity_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "إصلاح خارجي على الجهة"
        table.format_no = doc.print_templete2
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_purchase_wallet(doc, method=None):
        doc.print_purchase_wallet_count += 1
        doc.last_print_purchase_wallet_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "حافظة مشتريات"
        table.format_no = doc.print_templete2
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_issue_return(doc, method=None):
        doc.print_issue_return_count += 1
        doc.last_print_issue_return_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "إذن صرف وإرتجاع"
        table.format_no = doc.print_templete2
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_certificate(doc, method=None):
        doc.print_certificate_count += 1
        doc.last_print_certificate_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "شهادة إدارية"
        table.format_no = doc.print_templete2
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_exchange_certificate(doc, method=None):
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "شهادة إستبدال"
        table.format_no = doc.print_templete2
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_maintenance_rfq(doc, method=None):
        doc.print_maintenance_rfq_count += 1
        doc.last_print_maintenance_rfq_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "طلب عروض أسعار"
        table.format_no = "-"
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_mozakira(doc, method=None):
        doc.print_mozakira_count += 1
        doc.last_print_mozakira_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "مذكرة عرض"
        table.format_no = "-"
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()

    @frappe.whitelist()
    def print_job_order(doc, method=None):
        doc.print_job_order_count += 1
        doc.last_print_job_order_date = nowdate()
        table = doc.append("maintenance_print_logs", {})
        table.format_name = "أمر شغل"
        table.format_no = "-"
        table.print_date = nowdate()
        table.printed_by = frappe.db.get_value("User", frappe.session.user, "full_name")
        doc.save()
        doc.reload()


@frappe.whitelist()
def delete_flag_karta_ledger_entry_method(kle):
    frappe.db.sql(
        """ update `tabKarta Ledger Entry` set del_flag = 1
                where name ='{name}'
            """.format(
            name=kle
        )
    )


@frappe.whitelist()
def delete_fkarta_ledger_entry_method(ord_serial):
    frappe.db.sql(
        """ update `tabKarta Ledger Entry` set del_flag = 1
                where ord_serial ='{ord_serial}'
            """.format(
            ord_serial=ord_serial
        )
    )


@frappe.whitelist()
def update_karta_method(kle, part_universal_code, qty):
    frappe.db.sql(
        """ update `tabKarta Ledger Entry` set part_universal_code = "{part_universal_code}", part_qty= "{part_qty}"
                where name ='{name}'
            """.format(
            name=kle, part_universal_code=part_universal_code, part_qty=qty
        )
    )


def after_doctype_insert():
    frappe.db.add_unique("Vehicle Maintenance Process", ("ezn_no", "fiscal_year"))


@frappe.whitelist()
def fix_karta_ledger_entry():
    veh_maintenance = frappe.db.sql(
        """
    SELECT veh_maintenance_process.name, veh_maintenance_process.vehicles, veh_maintenance_process.ezn_date,
    veh_maintenance_process.ezn_no, 
    veh_maintenance_process.fiscal_year
    FROM `tabVehicle Maintenance Process` veh_maintenance_process
    WHERE veh_maintenance_process.mono IS NOT NULL

    LIMIT 1
    """,
        as_dict=1,
    )
    for row in veh_maintenance:
        its_karta = frappe.db.sql(
            """
        SELECT name, ord_serial, vic_serial, part_universal_code,part_qty, action_date, part_unit, ezn_no, 
        year, maintenance_method, doc_type
        FROM `tabKarta Ledger Entry`
        WHERE ezn_no="39651"
        AND year="2023/2022"
        AND del_flag=0
        AND creation IS NOT NULL
        """.format(
                ezn_no=row.ezn_no, year=row.fiscal_year
            ),
            as_dict=1,
        )
        # print(its_karta)
        # for idx, row in enumerate(its_karta):

        #     # for karta in row:
        #     #     print(karta)
        #     print(row)
        #     print(idx)
        #     print(len(row))
        #     if row.part_universal_code == its_karta[idx + 1 ].part_universal_code:
        #         return True
        pointer = 0
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                # print(len(its_karta))
                # print(row)
                # print(pointer)
                # print(its_karta[pointer].part_universal_code)
                if (
                    its_karta[pointer].part_universal_code
                    == its_karta[row].part_universal_code
                    and its_karta[pointer].vic_serial == its_karta[row].vic_serial
                    # and its_karta[pointer].part_qty == its_karta[row].part_qty
                    and its_karta[pointer].ezn_no == its_karta[row].ezn_no
                    and its_karta[pointer].year == its_karta[row].year
                    and its_karta[pointer].maintenance_method
                    == its_karta[row].maintenance_method
                    and (
                        its_karta[pointer].doc_type == "Maintenance Order"
                        or its_karta[row].doc_type == "Maintenance Order"
                    )
                ):
                    print("he1" + str(pointer))
                    print(its_karta[pointer].name)
                    print(its_karta[row].name)
                    print(its_karta[pointer].ord_serial)
                    print(its_karta[row].ord_serial)
                    print(its_karta[pointer].action_date)
                    print(its_karta[row].action_date)
                    if its_karta[pointer].ord_serial.startswith("VMP-"):
                        frappe.db.sql(
                            """ update `tabKarta Ledger Entry` set del_flag = "1"
                                where name ='{name}'
                            """.format(
                                name=its_karta[pointer].name
                            )
                        )
                        frappe.db.commit()
                    if its_karta[row].ord_serial.startswith("VMP-"):
                        frappe.db.sql(
                            """ update `tabKarta Ledger Entry` set del_flag = "1"
                                where name ='{name}'
                            """.format(
                                name=its_karta[row].name
                            )
                        )
                        frappe.db.commit()
            pointer += 1


def adjust_license_seial():
    licens_entries = frappe.db.sql(
        """
    SELECT * 
    FROM `tabVehicle License Entries`
    WHERE license_no > "7214968"
    AND card_code = "AFA"
    ORDER BY license_no 
    """,
        as_dict=1,
    )
    license_no = 7214968
    for entry in licens_entries:
        print(entry.name)
        print(entry.license_no)
        license_no += 1
        # frappe.db.sql(
        #                     """ update `tabVehicle License Entries` set license_no = "{license_no}"
        #                         where name ='{name}'
        #                     """.format(name=entry.name, license_no=license_no)
        #                 )
        # frappe.db.commit()


import datetime


@frappe.whitelist()
def fix_karta_ledger_entry1():
    veh_maintenance = frappe.db.sql(
        """
    SELECT name, bon_serial, bon_code, bon_version, sarfia_no, i_date
    FROM `tabVoucher` voucher
    WHERE  bon_serial IS NOT NULL
    AND bon_code IS NOT NULL
    AND bon_version IS NOT NULL
    AND sarfia_no IS NOT NULL
    AND i_date IS NOT NULL
    ORDER BY name
    """,
        as_dict=1,
    )
    updated = 0
    counter = 0
    for row in veh_maintenance:
        if counter % 100000 == 0:
            print("reached row " + str(counter) + "name " + str(row.name))
        counter += 1

        its_karta = frappe.db.sql(
            """
        SELECT name, bon_serial, bon_code,
        bon_version, sarfia_no, i_date
        FROM `tabVoucher`
        WHERE bon_serial="{bon_serial}"
        AND bon_code = "{bon_code}"
        AND bon_version = "{bon_version}"
        AND sarfia_no = "{sarfia_no}"
        AND i_date = "{i_date}"
        """.format(
                bon_serial=row.bon_serial,
                bon_code=row.bon_code,
                bon_version=row.bon_version,
                sarfia_no=row.sarfia_no,
                i_date=row.i_date,
            ),
            as_dict=1,
        )
        pointer = 0
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                if (
                    its_karta[pointer].bon_serial == its_karta[row].bon_serial
                    and its_karta[pointer].bon_code == its_karta[row].bon_code
                    and its_karta[pointer].bon_version == its_karta[row].bon_version
                    and its_karta[pointer].sarfia_no == its_karta[row].sarfia_no
                    and its_karta[pointer].i_date == its_karta[row].i_date
                ):
                    frappe.db.sql(
                        """ delete from `tabVoucher` 
                                where name ='{name}'
                            """.format(
                            name=its_karta[row].name
                        )
                    )
                    frappe.db.commit()
                    # print("updated" + str(its_karta[row].name))

                    updated += 1

            pointer += 1
    print(updated)


import datetime


@frappe.whitelist()
def remove_duplicated_logs_lqd_issue_table():
    lqd_issue_table = frappe.db.sql(
        """
    SELECT * FROM `tabLiquids Issuing Table`
    ORDER BY name desc
    """,
        as_dict=1,
    )
    updated = 0
    for row in lqd_issue_table:
        its_karta = frappe.db.sql(
            """
        SELECT * FROM `tabLiquids Issuing Table`
        WHERE parent="{parent}"
        AND issue_no = "{issue_no}"
        AND issue_type = "{issue_type}"
        AND voucher = "{voucher}"
        AND qty = "{qty}"
        AND from_date = "{from_date}"
        AND to_date = "{to_date}"
        AND entity = "{entity}"
        AND vehicle_status = "{vehicle_status}"
        """.format(
                parent=row.parent,
                issue_no=row.issue_no,
                issue_type=row.issue_type,
                entity=row.entity,
                vehicle_status=row.vehicle_status,
                voucher=row.voucher,
                qty=row.qty,
                from_date=row.from_date,
                to_date=row.to_date,
            ),
            as_dict=1,
        )
        pointer = 0
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                if (
                    its_karta[pointer].parent == its_karta[row].parent
                    and its_karta[pointer].issue_no == its_karta[row].issue_no
                    and its_karta[pointer].issue_type == its_karta[row].issue_type
                    and its_karta[pointer].voucher == its_karta[row].voucher
                    and its_karta[pointer].qty == its_karta[row].qty
                    and its_karta[pointer].from_date == its_karta[row].from_date
                    and its_karta[pointer].to_date == its_karta[row].to_date
                    and its_karta[pointer].entity == its_karta[row].entity
                    and its_karta[pointer].vehicle_status
                    == its_karta[row].vehicle_status
                ):
                    frappe.db.sql(
                        """ delete from `tabLiquids Issuing Table`
                                where name ='{name}'
                            """.format(
                            name=its_karta[row].name
                        )
                    )
                    frappe.db.commit()
                    # print("updated" + str(its_karta[row].name))

                    updated += 1

            pointer += 1
    print(updated)


import datetime


@frappe.whitelist()
def fix_karta_ledger_entry21():
    veh_maintenance = frappe.db.sql(
        """
    SELECT name, veh_maintenance_process.name, veh_maintenance_process.vehicles, veh_maintenance_process.ezn_date,
    veh_maintenance_process.ezn_no, 
    veh_maintenance_process.fiscal_year
    FROM `tabVehicle Maintenance Process` veh_maintenance_process
    """,
        as_dict=1,
    )
    updated = 0
    for row in veh_maintenance:
        its_karta = frappe.db.sql(
            """
        SELECT name, ord_serial, vic_serial, part_universal_code,part_qty, action_date, part_unit, ezn_no, 
        year, maintenance_method, doc_type
        FROM `tabKarta Ledger Entry`
        WHERE ezn_no="{ezn_no}"
        AND year="{year}"
        AND del_flag=0
        """.format(
                ezn_no=row.ezn_no, year=row.fiscal_year
            ),
            as_dict=1,
        )
        pointer = 0
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                # print(len(its_karta))
                # print(row)
                # print(pointer)
                # print(its_karta[pointer].part_universal_code)
                if (
                    its_karta[pointer].part_universal_code
                    == its_karta[row].part_universal_code
                    and its_karta[pointer].vic_serial == its_karta[row].vic_serial
                    and its_karta[pointer].ord_serial == its_karta[row].ord_serial
                    and its_karta[pointer].part_qty == its_karta[row].part_qty
                    and its_karta[pointer].ezn_no == its_karta[row].ezn_no
                    and its_karta[pointer].year == its_karta[row].year
                    # and its_karta[pointer].part_unit == its_karta[row].part_unit
                    and its_karta[pointer].doc_type == its_karta[row].doc_type
                    and its_karta[pointer].maintenance_method
                    == its_karta[row].maintenance_method
                    # and (its_karta[pointer].doc_type == "Maintenance Order" or its_karta[row].doc_type == "Maintenance Order")
                ):
                    # print("he1"+ str(pointer))
                    # print(its_karta[pointer].name)
                    # print(its_karta[row].name)
                    # print(its_karta[pointer].ord_serial)
                    # print(its_karta[row].ord_serial)
                    # print(its_karta[pointer].action_date)
                    # print(its_karta[row].action_date)
                    # datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
                    if its_karta[pointer].action_date > its_karta[row].action_date:
                        frappe.db.sql(
                            """ update `tabKarta Ledger Entry` set del_flag = "1"
                                where name ='{name}'
                            """.format(
                                name=its_karta[pointer].name
                            )
                        )
                        frappe.db.commit()
                        # print("updated" + str(its_karta[pointer].name))

                        updated += 1
                    else:
                        frappe.db.sql(
                            """ update `tabKarta Ledger Entry` set del_flag = "1"
                                where name ='{name}'
                            """.format(
                                name=its_karta[row].name
                            )
                        )
                        frappe.db.commit()
                        # print("updated" + str(its_karta[row].name))
                        updated += 1

            pointer += 1
    print(updated)


@frappe.whitelist()
def fix_karta_ledger_entry2():
    veh_maintenance = frappe.db.sql(
        """
    SELECT veh_maintenance_process.name
    FROM `tabVehicles` veh_maintenance_process    
    """,
        as_dict=1,
    )
    updated = 0
    for row in veh_maintenance:
        its_karta = frappe.db.sql(
            """
        SELECT *
        FROM `tabMaintenance Entity Logs`
        WHERE parent="{name}"
        AND parenttype="Vehicles"
        AND parentfield="maintenance_entity_table"
        """.format(
                name=row.name
            ),
            as_dict=1,
        )

        pointer = 0
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                # print(len(its_karta))
                # print(row)
                # print(pointer)
                # print(its_karta[pointer].part_universal_code)
                if (
                    its_karta[pointer].value == its_karta[row].value
                    and its_karta[pointer].date == its_karta[row].date
                    and its_karta[pointer].edited_by == its_karta[row].edited_by
                    and its_karta[pointer].remarks == its_karta[row].remarks
                    and its_karta[pointer].old_transaction_no
                    == its_karta[row].old_transaction_no
                    # and its_karta[pointer].vic_serial == its_karta[row].vic_serial
                    # and its_karta[pointer].ass_code == its_karta[row].ass_code
                    # and its_karta[pointer].ass_date == its_karta[row].ass_date
                    # and its_karta[pointer].ass_note == its_karta[row].ass_note
                ):
                    # print("he1"+ str(pointer))
                    # print(its_karta[pointer].name)
                    # print(its_karta[row].name)
                    # print(its_karta[pointer].ord_serial)
                    # print(its_karta[row].ord_serial)
                    # print(its_karta[pointer].action_date)
                    # print(its_karta[row].action_date)
                    # datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
                    frappe.db.sql(
                        """ delete from `tabMaintenance Entity Logs` 
                                where name ='{name}'
                            """.format(
                            name=its_karta[row].name
                        )
                    )
                    frappe.db.commit()
                    # print("updated" + str(its_karta[row].date))
                    updated += 1

            pointer += 1
    print(updated)


import datetime


@frappe.whitelist()
def create_print_logs():
    veh_maintenance = frappe.db.sql(
        """
    SELECT name, veh_maintenance_process.name, veh_maintenance_process.vehicles, veh_maintenance_process.ezn_date,
    veh_maintenance_process.ezn_no, 
    veh_maintenance_process.fiscal_year
    FROM `tabVehicle Maintenance Process` veh_maintenance_process
    """,
        as_dict=1,
    )
    updated = 0
    for veh_row in veh_maintenance:
        its_karta = frappe.db.sql(
            """
        SELECT  name, namozag_no,parent
        FROM `tabKashf Ohda Item`
        WHERE parent="{name}"
        AND parenttype= "Vehicle Maintenance Process"
        AND parentfield="kashf_ohda_item"
        """.format(
                name=veh_row.name
            ),
            as_dict=1,
        )
        pointer = 0
        # print(str(its_karta))
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                if its_karta[pointer].namozag_no == its_karta[row].namozag_no:
                    # print("he1"+ str(pointer))
                    # print(its_karta[pointer].name)
                    # print(its_karta[row].parent)
                    # print(its_karta[row].name)
                    # print(its_karta[row].idx)
                    # print(its_karta[row].item_name)
                    # print(its_karta[row].item_code)
                    # print(its_karta[pointer].ord_serial)
                    # print(its_karta[row].ord_serial)
                    # print(its_karta[pointer].action_date)
                    # print(its_karta[row].action_date)
                    # datetime.datetime.strptime(row.from_date, '%d/%m/%Y').date()
                    if not frappe.db.sql(
                        """
                    SELECT  name, format_name,format_no,parent
                    FROM `tabMaintenance Print Logs`
                    WHERE parent="{name}"
                    AND parenttype= "Vehicle Maintenance Process"
                    AND parentfield="maintenance_print_logs"
                    AND format_name = "كشف عهدة"
                    AND format_no = "{namozag_no}"
                    """.format(
                            name=veh_row.name,
                            namozag_no=its_karta[pointer].namozag_no,
                        ),
                        as_dict=1,
                    ):
                        record_name = 1
                        import random
                        import string

                        s = 10
                        ran = "".join(
                            random.choices(string.ascii_lowercase + string.digits, k=s)
                        )
                        frappe.db.sql(
                            """ INSERT INTO  `tabMaintenance Print Logs`(format_name,format_no,parent,parenttype,parentfield,name) 
                                    VALUES("كشف عهدة", "{namozag_no}","{parent}","Vehicle Maintenance Process","maintenance_print_logs","{name}")
                                """.format(
                                namozag_no=its_karta[pointer].namozag_no,
                                parent=its_karta[pointer].parent,
                                name=ran,
                            )
                        )
                        frappe.db.commit()
                        # print("updated" + str(its_karta[pointer].name))

                        updated += 1

            pointer += 1
    print(updated)


import datetime


@frappe.whitelist()
def create_print_logs2():
    veh_maintenance = frappe.db.sql(
        """
    SELECT name, veh_maintenance_process.name, veh_maintenance_process.vehicles, veh_maintenance_process.ezn_date,
    veh_maintenance_process.ezn_no, 
    veh_maintenance_process.fiscal_year
    FROM `tabVehicle Maintenance Process` veh_maintenance_process
    """,
        as_dict=1,
    )
    updated = 0
    for veh_row in veh_maintenance:
        its_karta = frappe.db.sql(
            """
        SELECT  name, namozg_no2, parent, maintenance_method
        FROM `tabEzn Egraa Item`
        WHERE parent="{name}"
        AND parenttype= "Vehicle Maintenance Process"
        AND parentfield="ezn_egraa_item"
        """.format(
                name=veh_row.name
            ),
            as_dict=1,
        )
        pointer = 0
        # print(str(its_karta))
        while pointer <= len(its_karta):
            for row in range(pointer + 1, len(its_karta)):
                if (
                    its_karta[pointer].namozg_no2 == its_karta[row].namozg_no2
                    and its_karta[pointer].maintenance_method
                    == its_karta[row].maintenance_method
                ):
                    if not frappe.db.sql(
                        """
                    SELECT  name, format_name,format_no,parent
                    FROM `tabMaintenance Print Logs`
                    WHERE parent="{name}"
                    AND parenttype= "Vehicle Maintenance Process"
                    AND parentfield="maintenance_print_logs"
                    AND format_name = "{maintenance_method}"
                    AND format_no = "{namozag_no}"
                    """.format(
                            name=veh_row.name,
                            namozag_no=its_karta[pointer].namozg_no2,
                            maintenance_method=its_karta[pointer].maintenance_method,
                        ),
                        as_dict=1,
                    ):
                        record_name = 1
                        import random
                        import string

                        s = 10
                        ran = "".join(
                            random.choices(string.ascii_lowercase + string.digits, k=s)
                        )
                        frappe.db.sql(
                            """ INSERT INTO  `tabMaintenance Print Logs`(format_name,format_no,parent,parenttype,parentfield,name) 
                                    VALUES("{maintenance_method}", "{namozag_no}","{parent}","Vehicle Maintenance Process","maintenance_print_logs","{name}")
                                """.format(
                                namozag_no=its_karta[pointer].namozg_no2,
                                parent=its_karta[pointer].parent,
                                name=ran,
                                maintenance_method=its_karta[
                                    pointer
                                ].maintenance_method,
                            )
                        )
                        frappe.db.commit()
                        # print("updated" + str(its_karta[pointer].name))

                        updated += 1

            pointer += 1
    print(updated)
