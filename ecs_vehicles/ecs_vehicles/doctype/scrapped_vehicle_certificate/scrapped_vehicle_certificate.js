frappe.ui.form.on('Scrapped Vehicle Certificate', {
	onload: function(frm) {
		frm.set_query("vehicle", function() {
			return {
				filters: {
					"vehicle_status": "مخردة"
				}
			}
		});
		cur_frm.refresh_field('option');
	}
});

frappe.ui.form.on('Scrapped Vehicle Certificate', 'vehicle', function(frm,cdt,cdn){
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Vehicles',
			'filters': { 'name': frm.doc.vehicle},
			'fieldname': [
				'vehicle_no',
				'police_id'
			]
		},
		callback: function (r) {
			if (r.message.vehicle_no) {
				frm.set_value("police_no", r.message.vehicle_no);
			}
			else {
				frm.set_value("police_no", r.message.police_id);
			}
		}
	});
	frm.refresh();
});


frappe.ui.form.on("Scrapped Vehicle Certificate", "print_certificate_data", function(frm){
	var myWin = window.open('/printview?doctype=Scrapped%20Vehicle%20Certificate&name='+ cur_frm.doc.name +'&trigger_print=1&format=%D8%B4%D9%87%D8%A7%D8%AF%D8%A9%20%D8%A8%D9%8A%D8%A7%D9%86%D8%A7%D8%AA%20%D9%85%D8%B1%D9%83%D8%A8%D8%A9%20%D8%B4%D8%B1%D8%B7%D8%A9%20%D9%85%D9%84%D8%BA%D8%A7%D8%A1%20%D9%88%20%D9%85%D8%A8%D8%A7%D8%B9%D8%A9%20%D9%84%D9%88%D8%B7&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Scrapped Vehicle Certificate", "print_correction_data", function(frm){
	var myWin = window.open('/printview?doctype=Scrapped%20Vehicle%20Certificate&name='+ cur_frm.doc.name +'&trigger_print=1&format=%D8%B5%D8%AD%D8%A9%20%D8%A8%D9%8A%D8%A7%D9%86%D8%A7%D8%AA%20%D9%85%D8%B1%D9%83%D8%A8%D8%A9%20%D8%B4%D8%B1%D8%B7%D8%A9%20%D9%85%D9%84%D8%BA%D8%A7%D8%A9%20%D9%85%D8%A8%D8%A7%D8%B9%D8%A9%20%D9%84%D9%88%D8%B7&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});