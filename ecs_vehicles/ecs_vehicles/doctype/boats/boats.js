// Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
// For license information, please see license.txt

//frappe.ui.form.on('Boats', {
//refresh(frm) {
// // your code here
//$('*[data-fieldname="engine_table"]').find('.grid-remove-rows').hide();
// },
// });

//frappe.ui.form.on('Engine Table', {
//refresh(frm) {
// // your code here
//},
//form_render(frm, cdt, cdn){
// frm.fields_dict.engine_table.grid.wrapper.find('.grid-delete-row').hide();
// frm.fields_dict.engine_table.grid.wrapper.find('.grid-duplicate-row').hide();
// frm.fields_dict.engine_table.grid.wrapper.find('.grid-move-row').hide();
// frm.fields_dict.engine_table.grid.wrapper.find('.grid-append-row').hide();
// frm.fields_dict.engine_table.grid.wrapper.find('.grid-insert-row-below').hide();
// frm.fields_dict.engine_table.grid.wrapper.find('.grid-insert-row').hide();
// }
// });


frappe.ui.form.on('Boats', {
    refresh: function (frm) {
        // frm.set_df_property("engine_table", "cannot_delete_rows", true);
        //frm.set_df_property("engine_table", "cannot_add_rows", true);
        frm.set_df_property("validity_table", "cannot_add_rows", true);
        frm.set_df_property("entity_table", "cannot_add_rows", true);
        frm.set_df_property("engine_table", "cannot_add_rows", true);
        frm.set_df_property("engines_table", "cannot_add_rows", true);
    },
    motor_add: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "motor_add",
            callback: function (r) {
                frm.refresh();
            }
        });
    },
    get_lanch_entity: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_lanch_entity",
            callback: function (r) {
                frm.refresh();
            }
        });
    },
    motor_transport: function (frm) {
        frappe.call({
            doc: frm.doc,
            freeze: 1,
            method: "motor_transport",
            callback: function (r) {
                frm.doc.engin_transaction = ""
                frm.doc.lanch_no = ""
                frm.doc.entity_lable = ""
                frm.doc.spare_warehouse = 0
                frm.refresh();
            }
        });
    },
    setup: function (frm) {
        frm.set_query("body_type", function () {
            return {
                filters: [
                    ["Vehicle Shape", "name", "in", ["مطاطي", "فيبر جلاس", "خشبي", "صلب", "موتوسيكل مائى", "معدنى"]],
                ]
            }

        });
    }
});
