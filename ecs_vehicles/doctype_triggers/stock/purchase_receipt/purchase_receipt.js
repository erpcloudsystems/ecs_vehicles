
frappe.ui.form.on("Purchase Receipt", "onload", function (frm) {
    console.log("here")
	var myWin = window.open('/printview?doctype=Purchase%20Receipt&name=' + cur_frm.doc.name + '&trigger_print=1&format=vehicle_check&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});
