// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Vouchers Entry', {

		setup: function(frm) {
			frm.set_query("voucher", function() {
				return {
					filters: [
						["Voucher","duplicated", "=", 0],
					]
				};
			});
		}
});
