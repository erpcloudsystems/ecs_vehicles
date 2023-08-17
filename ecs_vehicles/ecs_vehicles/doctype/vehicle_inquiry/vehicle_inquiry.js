frappe.ui.form.on("Vehicle Inquiry", 'refresh', function(frm){
	frm.disable_save();
	frm.set_df_property("vehicle_inquiry_table", "cannot_add_rows", true);
	frm.set_df_property("vehicle_inquiry_table", "cannot_delete_rows", true);

});


frappe.ui.form.on("Vehicle Inquiry", "get_vehicle_data", function(frm, cdt, cdn) {
	frappe.call({
		doc: frm.doc,
		method: "get_searched_vehicles",
		freeze:1,
		callback: function(r) {
			cur_frm.refresh_fields();
			frm.set_value("vehicle_no", "");
			frm.scroll_to_field('vehicle_no');
		}
	});
});


frappe.ui.form.on("Vehicle Inquiry Table", "preview_data", function(frm, cdt, cdn) {
    let item = locals[cdt][cdn]; 
	frappe.call({
		method: "ecs_vehicles.ecs_vehicles.doctype.vehicle_inquiry.vehicle_inquiry.get_vehicle_details",
		args:{
			"vehicle_boat":item.vehicle_boat,
			"vic_serial":item.vic_serial,
		},
		freeze:1,
		callback: function(r) {
			console.log(r)

			if (r.message) {
				console.log(r.message)
				if (item.vehicle_boat === "Vehicles"){
					frm.doc.vehicle = r.message.vehicle_no || r.message.police_id
					if (r.message.attached_entity == "" || r.message.attached_entity == null){
						frm.doc.entity = r.message.entity_name  || "-------"
						
					}else{
						
						frm.doc.entity = r.message.entity_name + "<br>" + "(" + r.message.attached_entity + ")"
					}
					frm.doc.chassis_no = r.message.chassis_no || "------"
					frm.doc.motor_no = r.message.motor_no || "------"
					frm.doc.vehicle_type = r.message.vehicle_type || "------"
					frm.doc.vehicle_country = r.message.vehicle_country || "------"
					frm.doc.vehicle_shape = r.message.vehicle_shape || "------"
					frm.doc.current_status = r.message.vehicle_status || "------"
					frm.doc.vehicle_brand = r.message.vehicle_brand || "------"
					frm.doc.vehicle_style = r.message.vehicle_style || "------"
					frm.doc.vehicle_model = r.message.vehicle_model || "------"
					frm.doc.fuel_type = r.message.fuel_type || "------"
					frm.doc.cylinder_count = r.message.cylinder_count || "------"
					frm.doc.exchange_allowance = r.message.exchange_allowance || "------"
					frm.doc.processing_type = r.message.processing_type || "------"
					frm.doc.vehicle_color = r.message.vehicle_color || "------"
					frm.doc.litre_capacity = r.message.litre_capacity || "------"
					frm.doc.feeding_type = r.message.feeding_type || "------"
					frm.doc.ignition_type = r.message.ignition_type || "------"
					frm.doc.wheel_drive_type = r.message.wheel_drive_type || "------"
					frm.doc.transmission = r.message.transmission || "------"
					frm.doc.possession_date = r.message.possession_date || "------"
					frm.doc.maintenance_entity = r.message.maintenance_entity || "------"
					frm.doc.private_no = r.message.private_no || "------"
				} else {
					frm.doc.vehicle = r.message.boat_no  || "-------"
					
					frm.doc.entity = r.message.entity_name  || "-------"
					frm.doc.chassis_no = r.message.chassis_no  || "-------"
					frm.doc.motor_no = item.motor_no || "------"
					frm.doc.motor_no2 = item.motor_no2 || "------"
					frm.doc.vehicle_type = "لانش" 
					frm.doc.vehicle_shape = r.message.body_type  || "-------"
					frm.doc.current_status = r.message.boat_validity  || "-------"
					frm.doc.vehicle_brand = r.message.boat_brand  || "-------"
					frm.doc.vehicle_style = r.message.boat_style  || "-------"
					frm.doc.vehicle_model = r.message.boat_model  || "-------"
					frm.doc.vehicle_country = "-------"
					frm.doc.fuel_type = r.message.fuel_type  || "-------"
					frm.doc.cylinder_count = r.message.cylinder_count  || "-------"
					frm.doc.possession_date = r.message.issue_date  || "-------"
					frm.doc.exchange_allowance = "-------"
					frm.doc.processing_type = "-------"
					frm.doc.vehicle_color = "-------"
					frm.doc.litre_capacity = "-------"
					frm.doc.feeding_type = "-------"
					frm.doc.ignition_type = "-------"
					frm.doc.wheel_drive_type = "-------"
					frm.doc.transmission = "-------"
					frm.doc.possession_date = "-------"
					frm.doc.maintenance_entity = "-------"
					frm.doc.private_no = "-------"
				}
				
			}
			frm.refresh_fields();
		}
	});
	frm.scroll_to_field('vehicle_no');
	let new_inquiry =[]
	frm.doc.vehicle_inquiry_table.forEach((row,idx,array)=>{
		if (!(row.name === item.name) ) {
			row.preview_data = 0
			new_inquiry.push(row)
		} else {
			new_inquiry.push(row)

		}
	})
	frm.doc.vehicle_inquiry_table = new_inquiry
	frm.refresh_field("vehicle_inquiry_table")

});
