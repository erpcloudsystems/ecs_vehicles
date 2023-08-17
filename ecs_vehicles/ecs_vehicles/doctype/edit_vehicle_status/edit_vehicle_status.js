// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Edit Vehicle Status", 'refresh', function (frm) {
    frm.set_df_property("vehicles_status", "cannot_add_rows", true);

});

frappe.ui.form.on("Edit Vehicle Status", 'entity_name', function (frm) {
    frm.scroll_to_field('vehicle_no');
});

frappe.ui.form.on("Edit Vehicle Status", {
    refresh: function (frm, cdt, cdn) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("إصلاح / تعطيل جديد"), function () {
                frappe.new_doc("Edit Vehicle Status");
            },);
        }
    }
});
// frappe.ui.form.on("Edit Vehicle Status Table", "notes", function (frm, cdt, cdn) {
//     let d = locals[cdt][cdn];

//     if (d.vehicle_status_new == "صالحة") {
//         let result = d.notes.search("اعطال");
//         if (result) {

//             frappe.msgprint("الرجاء اختيار حالة السيارة بشكل صحيح");
//         }
//         result = text.search("أعطال");
//         if (result) {

//             frappe.msgprint("الرجاء اختيار حالة السيارة بشكل صحيح");
//         }
//     }
//     if (d.vehicle_status_new == "عاطلة") {
//         let result = d.notes.search("اصلاح");
//         if (result) {

//             frappe.msgprint("الرجاء اختيار حالة السيارة بشكل صحيح");
//         }
//         result = text.search("إصلاح");
//         if (result) {

//             frappe.msgprint("الرجاء اختيار حالة السيارة بشكل صحيح");
//         }
//     }
// });

frappe.ui.form.on("Edit Vehicle Status Table", "vehicle_status_new", function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    if (item.vehicle_status != "صالحة" || item.vehicle_status != "عاطلة") {
        frappe.msgprint(`المركبة رقم ${item.vehicle_no} الحالة الحالية (${item.vehicle_status}) والحالة الجديدة (${item.vehicle_status_new})`, "تنبيه")
    }
});
frappe.ui.form.on("Edit Vehicle Status", "get_vehicle", function (frm, cdt, cdn) {
    if (frm.doc.vehicle_no && frm.doc.entity_name) {
        frappe.call({
            doc: frm.doc,
            method: "get_searched_vehicles",
            freeze: 1,
            callback: function (r) {
                frm.set_value("vehicle_no", "");
                cur_frm.refresh_fields();
                frm.scroll_to_field('vehicle_no');
                if (r.message) {

                    cur_frm.set_value("status_table", []);
                    cur_frm.set_value("motor_no", r.message.motor_no);
                    cur_frm.set_value("chassie_no", r.message.chassis_no);
                    cur_frm.set_value("vehicle_type", r.message.vehicle_type);
                    // call with all options
                    frappe.call({
                        method: 'ecs_vehicles.ecs_vehicles.doctype.edit_vehicle_status.edit_vehicle_status.edit_vehicle_status',
                        args: {
                            name: r.message.name,
                        },
                        freeze: true,
                        callback: (r) => {
                            if (r.message) {
                                r.message.forEach((row, idx, array) => {
                                    let status_table = frm.add_child("status_table");
                                    status_table.value = row.value;
                                    status_table.date = row.date;
                                    status_table.remarks = row.remarks;
                                    status_table.edited_by = row.edited_by;
                                    status_table.old_transaction_no = row.old_transaction_no;
                                    cur_frm.refresh_field("status_table");
                                })
                            }
                        },

                    })
                }
            }
        });
        frm.refresh_fields();
    }
});