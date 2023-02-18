// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Auction Invoice', {
    setup: function(frm) {
        frm.set_query("sales_info_payment", function() {
            return {
                filters: [
                    ["Sales Info Payment","docstatus", "=", 1]
                ]
            };
        });
    }
});

frappe.ui.form.on("Auction Invoice", "sales_info_payment", function(frm){
    frappe.model.with_doc("Sales Info Payment", frm.doc.sales_info_payment, function() {
        var tabletransfer= frappe.model.get_doc("Sales Info Payment", frm.doc.sales_info_payment);
        cur_frm.clear_table("auction_sales_slips");
        $.each(tabletransfer.auction_sales_slips, function(d, row){
            d = frm.add_child("auction_sales_slips");
            d.lot_no = row.lot_no;
			d.accumulated_lot = row.accumulated_lot;
			d.vehicle = row.vehicle;
			d.police_id = row.police_id;
			d.entity = row.entity;
			d.vehicle_type = row.vehicle_type;
			d.vehicle_shape = row.vehicle_shape;
			d.vehicle_brand = row.vehicle_brand;
			d.vehicle_model = row.vehicle_model;
			d.vehicle_style = row.vehicle_style;
			d.vehicle_color = row.vehicle_color;
			d.chassis_no = row.chassis_no;
			d.motor_no = row.motor_no;
			d.estimated_price = row.estimated_price;
			d.selling_price = row.selling_price;
			d.tax_percent = 0;

            cur_frm.refresh_field("auction_sales_slips");
        });
    });
});

frappe.ui.form.on('Auction Invoice', {
    refresh:function(frm){
        frm.set_df_property("auction_sales_slips", "cannot_add_rows", true);
        frm.set_df_property("auction_sales_slips", "cannot_delete_rows", true);
    }
 });


