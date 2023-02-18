// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Info Payment', {
    setup: function(frm) {
        frm.set_query("auction_info", function() {
            return {
                filters: [
                    ["Auction Info","docstatus", "=", 1]
                ]
            };
        });
    }
});

frappe.ui.form.on('Sales Info Payment', {
    refresh:function(frm){
        frm.set_df_property("auction_sales_slips", "cannot_add_rows", true);
        frm.set_df_property("auction_sales_slips", "cannot_delete_rows", true);
    }
 });

frappe.ui.form.on('Sales Info Payment', {
	accumulated_lot: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_accumulated_lot_vehicles",
            callback: function(r) {
            }
        });
        cur_frm.refresh_field("auction_sales_slips");
    }
});