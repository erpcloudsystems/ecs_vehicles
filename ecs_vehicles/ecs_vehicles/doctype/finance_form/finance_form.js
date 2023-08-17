// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Finance Form',{
    refresh: (frm) => {
        frm.set_query("purchase_invoices", "form_invoices", () => {
			const added_invoices = frm.doc.form_invoices.map((r) => r.purchase_invoices);
            return {
                filters:[
                    ["name", "not in", added_invoices],
                    ["Purchase Invoices","supplier", "=", frm.doc.supplier],
                    //["Purchase Invoices","docstatus", "=", 1]
                ],
			};
		});
	},
    supplier: (frm) => {
        function frappe_call(doctype_name, filters,fieldnames) {
            let status = 0
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    'doctype': doctype_name,
                    'filters': filters,
                    'fields': fieldnames,
                },
                
                callback: function(r) {
                    console.log(r.message)
                    if (r.message) {
                        if (!frm.doc.deduction_data){
                            let child = r.message
                            child.forEach((item, idx, arr) => {
                                let deduction_data = frm.add_child("deduction_data");
                                deduction_data.type = item.type_name
                                deduction_data.value = item.value_name
                            });

                        }
                        frm.refresh_field('deduction_data');           
                    }
                }
            });
            return status
          }
        console.log(frm.doc.creation)
        // cur_frm.clear_table("form_invoices");
        frm.refresh_field('form_invoices');           

        if (frm.doc.creation === undefined) {
            frappe_call("Deduction Type" , {}  ,["type_name", "value_name"])
        }
        else {
            
            frm.refresh_field('deduction_data');           

        }

	},
    include_taxes: (frm) => {
        function frappe_call(doctype_name, filters,fieldnames) {
            let status = 0
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    'doctype': doctype_name,
                    'filters': filters,
                    'fieldname': fieldnames,
                },
        
                callback: function(r) {
                    if (r.message) {
                        let include_taxes = frm.add_child("taxes");
                        include_taxes.taxes = r.message.tax_name
                        include_taxes.tax_percent = r.message.tax_percent
                        frm.refresh_field('taxes');           
                    }
                }
            });
            return status
          }
        if (frm.doc.include_taxes == 1) {
            frappe_call("Taxes" , {"tax_name": "1% ضرائب"}  ,["tax_name", "tax_percent"])
        }
        else {
            cur_frm.clear_table("taxes");
        }

	},
});



frappe.ui.form.on("Finance Form", "print_format1", function(frm){
	var myWin = window.open('/printview?doctype=Finance%20Form&name='+ cur_frm.doc.name +'&trigger_print=1&format=%D8%A7%D8%B3%D8%AA%D9%85%D8%A7%D8%B1%D9%87%20%D8%B5%D8%B1%D9%81&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
});

frappe.ui.form.on("Finance Form", "print_format2", function(frm){
	var myWin = window.open('/printview?doctype=Finance%20Form&name='+ cur_frm.doc.name +'&trigger_print=1&format=%D8%A8%D9%8A%D8%A7%D9%86%20%D8%A8%D8%A7%D9%84%D9%85%D8%B9%D8%A7%D9%85%D9%84%D8%A7%D8%AA%20%D9%85%D8%B9%20%D9%85%D9%85%D9%88%D9%84%D9%8A%20%D8%A7%D9%84%D9%82%D8%B7%D8%A7%D8%B9%20%D8%A7%D9%84%D8%AE%D8%A7%D8%B5%20%D9%88%20%D9%82%D8%B7%D8%A7%D8%B9%20%D8%A7%D9%84%D8%A3%D8%B9%D9%85%D8%A7%D9%84&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
});

frappe.ui.form.on("Finance Form", "print_format3", function(frm){
	var myWin = window.open('/printview?doctype=Finance%20Form&name='+ cur_frm.doc.name +'&trigger_print=1&format=%D8%A5%D8%B3%D8%AA%D9%85%D8%A7%D8%B1%D8%A9&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
});
