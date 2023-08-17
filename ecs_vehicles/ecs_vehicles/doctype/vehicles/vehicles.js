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

frappe.ui.form.on('Vehicles', {
	delete_vehicle: function(frm) {
        frappe.confirm('هل أنت متأكد من حذف المركبة؟',
    () => {
        frappe.call({
            doc: frm.doc,
            method: "delete_vehicle",
            freeze: 1,
            callback: function(r) {
            }
        });
        frappe.set_route('app/vehicles')
    }, () => {
        // action to perform if No is selected
    })
        
    }
});

frappe.ui.form.on('Vehicles', {
	search: function(frm) {
        frappe.call({ method: "frappe.client.get_value", args: {
            doctype: "Vehicles",
            fieldname: ["name"],
            filters: {'vehicle_no': cur_frm.doc.search_vehicle,}},
            callback: function(r) {
                if (r.message.name) {
                    frappe.set_route('app/vehicles/'+ r.message.name);
                    frm.set_value("search_vehicle", null);
			        frm.refresh();

                }
                else{
                    frappe.set_route('app/vehicles/');
                    frm.set_value("search_vehicle", null);
			        frm.refresh();
                }
            },
            freeze: 1,
            freeze_message: "جاري البحث عن رقم الشرطة ...",
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

// frappe.ui.form.on('Vehicles', {
//     setup: function(frm) {
//         frm.set_query("private_no", function() {
//             return {
//                 filters: [
//                     ["Private Plate","current_vehicle", "=", ""],
//                     ["Private Plate","status", "=", "صالحة"]
//                 ]
//             };
//         });
//     }
// });

// frappe.ui.form.on('Vehicles', {
//     setup: function(frm) {
//         frm.set_query("new_private_no", function() {
//             return {
//                 filters: [
//                     ["Private Plate","current_vehicle", "=", ""],
//                     ["Private Plate","status", "=", "صالحة"]
//                 ]
//             };
//         });
//     }
// });


// frappe.ui.form.on('Vehicles', {
//     setup: function(frm) {
//         frm.set_query("motor_no", function() {
//             return {
//                 filters: [
//                     ["Vehicle Motor","current_vehicle", "=", "إحتياطي مخزن"]
//                 ]
//             };
//         });
//     }
// });

// frappe.ui.form.on('Vehicles', {
//     setup: function(frm) {
//         frm.set_query("new_motor_no", function() {
//             return {
//                 filters: [
//                     ["Vehicle Motor","current_vehicle", "=", "إحتياطي مخزن"]
//                 ]
//             };
//         });
//     }
// });


frappe.ui.form.on('Vehicles', {
    refresh:function(frm){
        frm.set_df_property("vehicle_no_table", "cannot_add_rows", true);
        frm.set_df_property("entity_table", "cannot_add_rows", true);
        frm.set_df_property("attached_entity_logs", "cannot_add_rows", true);
        frm.set_df_property("status_table", "cannot_add_rows", true);
        frm.set_df_property("motor_table", "cannot_add_rows", true);
        frm.set_df_property("processing_type_table", "cannot_add_rows", true);
        frm.set_df_property("color_table", "cannot_add_rows", true);
        frm.set_df_property("maintenance_entity_table", "cannot_add_rows", true);
        frm.set_df_property("private_no_table", "cannot_add_rows", true);
        frm.set_df_property("chassis_no_table", "cannot_add_rows", true);
        frm.set_df_property("group_shape_table", "cannot_add_rows", true);
        frm.set_df_property("shape_table", "cannot_add_rows", true);
        frm.set_df_property("brand_table", "cannot_add_rows", true);
        frm.set_df_property("style_table", "cannot_add_rows", true);
        frm.set_df_property("model_table", "cannot_add_rows", true);
        frm.set_df_property("country_table", "cannot_add_rows", true);
        frm.set_df_property("exchange_allowance_table", "cannot_add_rows", true);
    }
 });

frappe.ui.form.on('Vehicles', {
    after_save:function(frm){
        frm.scroll_to_field('search_vehicle');
    }
});