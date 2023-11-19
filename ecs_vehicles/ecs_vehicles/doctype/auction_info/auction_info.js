// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt


frappe.ui.form.on("Auction Info", {
	refresh: (frm) => {
		frm.set_query("vehicle", "auction_sales_slips", () => {
			const added_vehicles = frm.doc.auction_sales_slips.map((r) => r.vehicle);
			return {
				filters: [
				    ["name", "not in", added_vehicles],
                    ["Vehicles","vehicle_status", "=", "مخردة"]
                ],
			};
		});
	},
});

frappe.ui.form.on("Auction Info", "get_vehicle", function (frm, cdt, cdn) {
    if (frm.doc.vehicle_no) {
		$.each(frm.doc.auction_sales_slips || [], function (i, d) {
			if (d.police_id == cur_frm.doc.vehicle_no && !cur_frm.doc.vehicle_type2) {
				frappe.throw(" المركبة " + d.police_id + " تم إضافتها من قبل في الصف رقم " + d.idx);
			}
		})

        frappe.call({
            doc: frm.doc,
            method: "get_searched_vehicles",
            freeze: 1,
            callback: function (r) {
                frm.set_value("vehicle_no", "");
                cur_frm.refresh_fields();
                frm.scroll_to_field('vehicle_no');
            }
        });
        frm.refresh_fields();
    }
});
frappe.ui.form.on("Auction Info", "print_auction", function(frm){
	var myWin = window.open('/printview?doctype=Auction Info&name='+ cur_frm.doc.name +'&trigger_print=1&format=Auctions&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
	
});