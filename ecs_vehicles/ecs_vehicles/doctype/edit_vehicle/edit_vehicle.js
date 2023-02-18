frappe.ui.form.on("Edit Vehicle", "vehicle_no", function(){
    cur_frm.doc.edit = "";
    cur_frm.doc.current_police_plate = "";
    cur_frm.doc.new_police_plate = "";
    cur_frm.doc.current_private_plate = "";
    cur_frm.doc.new_private_plate = "";
    cur_frm.doc.current_entity = "";
    cur_frm.doc.new_entity = "";
    cur_frm.doc.current_color = "";
    cur_frm.doc.new_color = "";
    cur_frm.doc.current_motor_no = "";
    cur_frm.doc.new_motor_no = "";
    cur_frm.doc.current_maintenance_entity = "";
    cur_frm.doc.new_maintenance_entity = "";
    cur_frm.doc.current_status = "";
    cur_frm.doc.new_status = "";
    cur_frm.refresh_field('edit');
    cur_frm.refresh_field('current_police_plate');
    cur_frm.refresh_field('new_police_plate');
    cur_frm.refresh_field('current_private_plate');
    cur_frm.refresh_field('new_private_plate');
    cur_frm.refresh_field('current_entity');
    cur_frm.refresh_field('new_entity');
    cur_frm.refresh_field('current_color');
    cur_frm.refresh_field('new_color');
    cur_frm.refresh_field('current_chassis_no');
    cur_frm.refresh_field('current_motor_no');
    cur_frm.refresh_field('new_motor_no');
    cur_frm.refresh_field('current_motor_no');
    cur_frm.refresh_field('new_motor_no');
    cur_frm.refresh_field('current_maintenance_entity');
    cur_frm.refresh_field('new_maintenance_entity');
    cur_frm.refresh_field('current_status');
    cur_frm.refresh_field('new_status');
});


frappe.ui.form.on('Edit Vehicle', 'vehicle_no', function(frm) {
//    if (cur_frm.doc.edit == "رقم شرطة") {
//        frappe.call({ method: "frappe.client.get_value",
//	        args: {
//	            doctype: "Vehicles",
//                fieldname: "vehicle_no",
//	            filters: {'name': cur_frm.doc.vehicle_no},
//            },
//            callback: function(r){
//                cur_frm.set_value("current_police_plate", r.message.vehicle_no);
//            }
//        });
//    }
//
//    if (cur_frm.doc.edit == "رقم ملاكي") {
//        frappe.call({ method: "frappe.client.get_value",
//	        args: {
//	            doctype: "Vehicles",
//                fieldname: "private_no",
//	            filters: {'name': cur_frm.doc.vehicle_no},
//            },
//            callback: function(r){
//                cur_frm.set_value("current_private_plate", r.message.private_no);
//            }
//        });
//    }
//
//    if (cur_frm.doc.edit == "جهة") {
//        frappe.call({ method: "frappe.client.get_value",
//	        args: {
//	            doctype: "Vehicles",
//                fieldname: "entity_name",
//	            filters: {'name': cur_frm.doc.vehicle_no},
//            },
//            callback: function(r){
//                cur_frm.set_value("current_entity", r.message.entity_name);
//            }
//        });
//    }
//
//    if (cur_frm.doc.edit == "لون") {
//        frappe.call({ method: "frappe.client.get_value",
//	        args: {
//	            doctype: "Vehicles",
//                fieldname: "vehicle_color",
//	            filters: {'name': cur_frm.doc.vehicle_no},
//            },
//            callback: function(r){
//                cur_frm.set_value("current_color", r.message.vehicle_color);
//            }
//        });
//    }
//
//    if (cur_frm.doc.edit == "رقم الموتور") {
//        frappe.call({ method: "frappe.client.get_value",
//	        args: {
//	            doctype: "Vehicles",
//                fieldname: "motor_no",
//	            filters: {'name': cur_frm.doc.vehicle_no},
//            },
//            callback: function(r){
//                cur_frm.set_value("current_motor_no", r.message.motor_no);
//            }
//        });
//    }
//
//    if (cur_frm.doc.edit == "جهة الصيانة") {
//        frappe.call({ method: "frappe.client.get_value",
//	        args: {
//	            doctype: "Vehicles",
//                fieldname: "maintenance_entity",
//	            filters: {'name': cur_frm.doc.vehicle_no},
//            },
//            callback: function(r){
//                cur_frm.set_value("current_maintenance_entity", r.message.maintenance_entity);
//            }
//        });
//    }
    
//    if (cur_frm.doc.edit == "صلاحية المركبة") {
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
