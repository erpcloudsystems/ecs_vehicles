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
