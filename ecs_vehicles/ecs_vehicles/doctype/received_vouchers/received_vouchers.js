// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt


frappe.ui.form.on('Received Vouchers', "validate", function(frm){
    frappe.set_route('app/received-vouchers/' + frm.doc.name);
});

frappe.ui.form.on('Received Vouchers', {
    refresh:function(frm){
        frm.set_df_property("vouchers_count_table", "cannot_add_rows", true);
        //frm.set_df_property("vouchers_count_table", "cannot_delete_rows", true);
    }
 });

frappe.ui.form.on('Received Vouchers', {
	liquid_type: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "append_vouchers",
            callback: function(r) {
            }
        });
    }
});

frappe.ui.form.on('Received Vouchers', {
	fiscal_year: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_max_batch",
            callback: function(r) {
                console.log(r);
                frm.doc.batch_no = r.message;
                frm.refresh();
            }
        });
    }
});