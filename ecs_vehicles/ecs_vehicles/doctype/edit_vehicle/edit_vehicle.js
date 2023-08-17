frappe.ui.form.on("Edit Vehicle", "vehicle_no", function(){
    cur_frm.doc.current_status = "";
    cur_frm.doc.new_status = "";
    cur_frm.refresh_field('current_status');
    cur_frm.refresh_field('new_status');
});


frappe.ui.form.on('Edit Vehicle', 'vehicle_no', function(frm) {
        frappe.call({ 
            method: "frappe.client.get_value",
	        args: {
	            doctype: "Vehicles",
                fieldname: "vehicle_status",
	            filters: {'name': cur_frm.doc.vehicle_no},
            },
            callback: function(r){
                cur_frm.set_value("current_status", r.message.vehicle_status);
            }
        });
//    }
});



frappe.ui.form.on('Edit Vehicle', 'vehicle_no', function(frm) {
    cur_frm.set_value("status_table", []);
    // call with all options
    frappe.call({
    method: 'ecs_vehicles.ecs_vehicles.doctype.edit_vehicle.edit_vehicle.edit_vehicle',
    args: {
        vehicle_no: frm.doc.vehicle_no
    },
    freeze: true,
    callback: (r) => {
        if(r.message){
            console.log(r)
            r.message.forEach((row, idx, array)=>{
                let status_table = frm.add_child("status_table");
                status_table.value = row.value;
                status_table.date = row.date;
                status_table.remarks = row.remarks;
                status_table.edited_by = row.edited_by;
                status_table.old_transaction_no = row.old_transaction_no;
                cur_frm.refresh_field("status_table");
            })
        }
    },

})
 
});
