frappe.ui.form.on("Edit Vehicle", "vehicle_no", function(){
    cur_frm.doc.current_status = "";
    cur_frm.doc.new_status = "";
    cur_frm.refresh_field('current_status');
    cur_frm.refresh_field('new_status');
});


frappe.ui.form.on('Edit Vehicle', 'vehicle_no', function(frm) {
        frappe.call({ method: "frappe.client.get_value",
	        args: {
	            doctype: "Vehicles",
                fieldname: "vehicle_status",
	            filters: {'name': cur_frm.doc.vehicle_no},
            },
            callback: function(r){
                cur_frm.set_value("current_status", r.message.vehicle_status);
            }
        });
//    }
});
