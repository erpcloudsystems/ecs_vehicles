// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt


frappe.ui.form.on('Request for Quotations', {
	maintenance_order: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "get_data",
				   callback: function(r) {
					//    frm.save();
					//    frm.refresh_fields();
					//    frm.refresh();
					cur_frm.doc.maintenance_order = "";
					frm.refresh_fields();

				   }
			   });
	   }
   });
frappe.ui.form.on('Request for Quotations',{
    refresh: (frm) => {
        frm.set_query("maintenance_order", () => {
			let added_invoices = []
			let unique = []
			if (frm.doc.request_for_quotations_item){

				added_invoices = frm.doc.request_for_quotations_item.map((r) => r.maintenance_order);
				unique = added_invoices.filter((value, index, array) => added_invoices.indexOf(value) === index);
			}

            return {
                filters:[
                    ["name", "not in", unique],
                ],
			};
		});
	},
});