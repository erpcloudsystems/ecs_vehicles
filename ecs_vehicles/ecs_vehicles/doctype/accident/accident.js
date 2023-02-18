// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Accident", "deduction_party", function() {
    cur_frm.doc.party_name = cur_frm.doc.ministry_party_name;
});