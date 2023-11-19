// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Accident", "deduction_party", function() {
    cur_frm.doc.party_name = cur_frm.doc.ministry_party_name;
});

frappe.ui.form.on("Accident", "onload", function(frm) {
    if(!cur_frm.doc.fiscal_year){
        frappe.call({ method: "frappe.client.get_value", 
            args: {
                doctype: "System Defaults",
                fieldname: "default_fiscal_year",
            },
            callback: function(r) { cur_frm.set_value("fiscal_year", r.message.default_fiscal_year); }
        });
    }
});