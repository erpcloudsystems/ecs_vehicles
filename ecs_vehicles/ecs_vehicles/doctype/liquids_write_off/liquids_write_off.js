// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Liquids Write Off', {
    refresh:function(frm){
        frm.set_df_property("liquids_write_off_table", "cannot_add_rows", true);
        //frm.set_df_property("liquids_write_off_table", "cannot_delete_rows", true);
    }
 });
