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
    refresh:function(frm){
        frm.set_df_property("engine_table", "cannot_delete_rows", true);
        //frm.set_df_property("engine_table", "cannot_add_rows", true);
    }
});
