
// frappe.ui.form.on('Stock Entry', {
//  maintenance_order: function(frm) {
// 			frappe.call({
// 				doc: frm.doc,
//                 method: "ecs_vehicles.ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.get_item_table",
// 				callback: function(r) {
// 					frm.refresh_fields();
// 					frm.refresh();
// 				}
// 			});
// 	}
// });
// maintenance_order: function(frm){   // I have used refresh you can use any trigger
//     frm.clear_table('items');
//     frappe.call({
//         method:"ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.get_item_table",
//         freeze: true,
//         args:{
//             doc:frm.doc.maintenance_order,
//            },
//             callback: function (response) {
//             if (response.message) {
//                 $.each(response.message, function(i,row) {   // row can be anything, it is merely a name


//                         var child_add = cur_frm.add_child("items");  // child_add can be anything
//                         child_add.item_group = row.item_group;
//                         child_add.item_code = row.item_code; // you can add as many fields as you want
//                         child_add.item_name = row.item_name; // you can add as many fields as you want
//                         child_add.uom = row.default_unit_of_measure; // you can add as many fields as you want
//                         child_add.qty = row.qty; // you can add as many fields as you want
//                         child_add.description = row.description; // you can add as many fields as you want
                      

//                             });
//           frm.refresh_fields("items");
//             }
//             }
//             });
//         }


