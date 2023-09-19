// Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Boat Motor', {
	refresh: function(frm) {
        frm.set_df_property("status_history", "cannot_add_rows", true);
    
	}
});
