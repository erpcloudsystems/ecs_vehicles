# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import in_words, money_in_words


class FinanceForm(Document):
    def __init__(self, *args, **kwargs):
        super(FinanceForm, self).__init__(*args, **kwargs)
        if self.old_flag == 0:
            self.total_of_invoices = 0
            self.a_fine = 0
            self.technical_a_fine = 0
            self.legal_a_fine = 0
            self.price_difference = 0

    def get_total_of_invoices(self):
        if self.old_flag == 0:
            for invoice in self.form_invoices:
                self.total_of_invoices += invoice.total
                self.a_fine += invoice.late_fees
                self.technical_a_fine += invoice.technical_fees
                self.legal_a_fine += invoice.legal_fees
                self.price_difference += invoice.price_difference
            self.total_invoices = self.total_of_invoices
            self.total_a_fine = self.a_fine
            self.total_technical_a_fine = self.technical_a_fine
            self.total_legal_a_fine = self.legal_a_fine
            self.tota_price_difference = self.price_difference

    def get_bank_details(self):
        # if self.old_flag == 0:
        # bank = frappe.db.get_all("Banks Table", {"parent":self.supplier, "parenttype":"Supplier", "default":"1"}, ["bank", "account_no"])
        bank = frappe.db.get_all(
            "Banks Table",
            {"parent": self.supplier, "parenttype": "Supplier"},
            ["bank", "account_no"],
        )
        if bank:
            self.bank_name = bank[0].bank
            self.bank_account_no = bank[0].account_no
        elif frappe.db.exists(
            "Banks Table", {"parent": self.supplier, "parenttype": "Supplier"}
        ):
            bank_name, account_no = frappe.db.get_value(
                "Banks Table",
                {"parent": self.supplier, "parenttype": "Supplier"},
                ["bank", "account_no"],
            )
            self.bank_name = bank_name
            self.bank_account_no = account_no
        else:
            frappe.throw("لا يوجد بنك في بيانات المورد")

    def get_deduction_values(self):
        if self.old_flag == 0:
            self.development = 0
            self.disabled = 0
            self.martyrs = 0
            for deduction in self.deduction_data:
                if deduction.type == "تنمية":
                    self.development = deduction.value
                if deduction.type == "معاقين":
                    self.disabled = deduction.value * len(self.form_invoices)
                if deduction.type == "شهداء":
                    self.martyrs = deduction.value * len(self.form_invoices)

    def get_taxes(self):
        if self.old_flag == 0:
            self.total_taxes = 0
            if self.include_taxes and self.taxes:
                self.total_taxes = (
                    int(self.taxes[0].tax_percent) * self.total_invoices / 100
                )

    def calculate_imprints(self):
        if self.old_flag == 0:
            self.normal_imprint = 0
            self.extra_imprint = 0
            self.total_of_imprints = 0
            if 50 <= self.total_invoices <= 300 and self.include_imprints:
                self.normal_imprint = (self.total_invoices - 50) * 12 / 1000
                self.extra_imprint = self.normal_imprint * 3
                self.total_of_imprints = self.normal_imprint + self.extra_imprint
            if 300 <= self.total_invoices <= 550 and self.include_imprints:
                self.normal_imprint = (self.total_invoices - 50) * 13 / 1000
                self.extra_imprint = self.normal_imprint * 3
                self.total_of_imprints = self.normal_imprint + self.extra_imprint
            if 550 <= self.total_invoices <= 1050 and self.include_imprints:
                self.normal_imprint = (self.total_invoices - 50) * 14 / 1000
                self.extra_imprint = self.normal_imprint * 3
                self.total_of_imprints = self.normal_imprint + self.extra_imprint
            if 1050 <= self.total_invoices <= 5050 and self.include_imprints:
                self.normal_imprint = (self.total_invoices - 50) * 15 / 1000
                self.extra_imprint = self.normal_imprint * 3
                self.total_of_imprints = self.normal_imprint + self.extra_imprint
            if 5050 <= self.total_invoices <= 10050 and self.include_imprints:
                self.normal_imprint = (self.total_invoices - 50) * 16 / 1000
                self.extra_imprint = self.normal_imprint * 3
                self.total_of_imprints = self.normal_imprint + self.extra_imprint
            if self.total_invoices > 10050 and self.include_imprints:
                self.normal_imprint = ((self.total_invoices - 10050) * 6 * 0.001) + 160
                self.extra_imprint = self.normal_imprint * 3
                self.total_of_imprints = self.normal_imprint + self.extra_imprint

    def get_totals(self):
        if self.old_flag == 0:
            self.total_deductions = (
                self.development
                + self.disabled
                + self.martyrs
                + self.total_taxes
                + self.total_a_fine
                + self.total_of_imprints
                + self.tota_price_difference
                + self.total_legal_a_fine
                + self.total_technical_a_fine
            )
            self.total = self.total_invoices - self.total_deductions

    def get_in_words(self):
        real_no = str(round(self.total, 2)).split(".")[0]
        piasters = str(round(self.total, 2)).split(".")[1]
        if int(piasters) > 0:
            if int(piasters) > 10:
                self.no_to_words = (
                    in_words(int(real_no))
                    + " جنيها و "
                    + in_words(int(piasters))
                    + " قرشا فقط"
                )
            else:
                self.no_to_words = (
                    in_words(int(real_no))
                    + " جنيها و "
                    + in_words(int(piasters + "0"))
                    + " قرشا فقط"
                )

        else:
            self.no_to_words = in_words(int(real_no)) + " جنيها فقط"

        # if self.old_flag == 0:

    def validate(self):
        # if self.old_flag == 0:
        if frappe.db.exists(
            "Finance Form",
            {
                "series_no": self.series_no,
                "year": self.year,
                "form_type": self.form_type,
                "name": ["!=", self.name],
            },
        ):
            frappe.throw("رقم الأستمارة مستعمل من قبل في نفس السنة المالية")
        if not self.form_invoices:
            frappe.throw("من فضلك اضف فاتوره ")
        self.get_bank_details()
        self.get_total_of_invoices()
        self.get_deduction_values()
        self.get_taxes()
        self.calculate_imprints()
        self.get_totals()
        self.get_in_words()
