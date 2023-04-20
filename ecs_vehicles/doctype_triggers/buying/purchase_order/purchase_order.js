/*
frappe.ui.form.on("Sales Invoice", "validate", function(frm) {
});
*/
frappe.ui.form.on('Material Request', {
    refresh(frm) {
    setTimeout(() => {
        frm.remove_custom_button('Stop');
        frm.remove_custom_button('Purchase Order','Create');
        frm.remove_custom_button('Supplier Quotation','Create');
        frm.remove_custom_button('Request for Quotation','Create');

        }, 10);
    }
})frappe.ui.form.on('Material Request', {
    refresh(frm) {
    setTimeout(() => {
        frm.remove_custom_button('Stop');
        frm.remove_custom_button('Purchase Order','Create');
        frm.remove_custom_button('Supplier Quotation','Create');
        frm.remove_custom_button('Request for Quotation','Create');

        }, 10);
    }
})