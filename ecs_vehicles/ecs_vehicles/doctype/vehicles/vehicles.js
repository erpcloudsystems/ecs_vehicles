// Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
// For license information, please see license.txt


frappe.ui.form.on('Vehicles', {
	check_police_no: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "check_police_no",
            callback: function(r) {
            }
        });
    }
});

frappe.ui.form.on('Vehicles', {
	check_chassis_no: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "check_chassis_no",
            callback: function(r) {
            }
        });
    }
});


//frappe.ui.form.on('Vehicles', {
//    setup: function(frm) {
//        frm.set_query("vehicle_no", function() {
//            return {
//                filters: [
//                    ["Police Plate","current_vehicle", "=", "إحتياطي مخزن"],
//                    ["Police Plate","status", "=", "صالحة"]
//                ]
//            };
//        });
//    }
//});
//
//frappe.ui.form.on('Vehicles', {
//    setup: function(frm) {
//        frm.set_query("new_vehicle_no", function() {
//            return {
//                filters: [
//                    ["Police Plate","current_vehicle", "=", "إحتياطي مخزن"],
//                    ["Police Plate","status", "=", "صالحة"]
//                ]
//            };
//        });
//    }
//});

frappe.ui.form.on('Vehicles', {
    setup: function(frm) {
        frm.set_query("private_no", function() {
            return {
                filters: [
                    ["Private Plate","current_vehicle", "=", ""],
                    ["Private Plate","status", "=", "صالحة"]
                ]
            };
        });
    }
});

frappe.ui.form.on('Vehicles', {
    setup: function(frm) {
        frm.set_query("new_private_no", function() {
            return {
                filters: [
                    ["Private Plate","current_vehicle", "=", ""],
                    ["Private Plate","status", "=", "صالحة"]
                ]
            };
        });
    }
});


frappe.ui.form.on('Vehicles', {
    setup: function(frm) {
        frm.set_query("motor_no", function() {
            return {
                filters: [
                    ["Vehicle Motor","current_vehicle", "=", "إحتياطي مخزن"]
                ]
            };
        });
    }
});

frappe.ui.form.on('Vehicles', {
    setup: function(frm) {
        frm.set_query("new_motor_no", function() {
            return {
                filters: [
                    ["Vehicle Motor","current_vehicle", "=", "إحتياطي مخزن"]
                ]
            };
        });
    }
});