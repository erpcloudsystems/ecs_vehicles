// Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Edit Boat", "boat_no", function(){
    cur_frm.doc.edit = "";
    cur_frm.doc.current_entity = "";
    cur_frm.doc.new_entity = "";
    cur_frm.doc.current_status = "";
    cur_frm.doc.new_status = "";
    cur_frm.refresh_field('edit');
    cur_frm.refresh_field('current_entity');
    cur_frm.refresh_field('new_entity');
    cur_frm.refresh_field('current_status');
    cur_frm.refresh_field('new_status');
});


frappe.ui.form.on('Edit Boat', 'edit', function(frm) {
    if (cur_frm.doc.edit == "جهة") {
        frappe.call({ method: "frappe.client.get_value",
	        args: {
	            doctype: "Boats",
                fieldname: "entity_name",
	            filters: {'boat_no': cur_frm.doc.boat_no},
            },
            callback: function(r){
                cur_frm.set_value("current_entity", r.message.entity_name);
            }
        });
    }

    if (cur_frm.doc.edit == "صلاحية اللانش") {
        frappe.call({ method: "frappe.client.get_value",
	        args: {
	            doctype: "Boats",
                fieldname: "boat_validity",
	            filters: {'boat_no': cur_frm.doc.boat_no},
            },
            callback: function(r){
                cur_frm.set_value("current_status", r.message.boat_validity);
            }
        });
    }
});
