

INSERT INTO `tabLiquids Issuing Table` ( parent ,car_num , issue_no, from_date, to_date,entity, voucher, vehicle_status,qty,parenttype, parentfield )
SELECT  `tabVehicles Issuing Table`.vehicle, `tabVehicles Issuing Table`.car_num, `tabVehicles Issuing Table`.parent, `tabVehicles Issuing Table`.last_issue_from_date, `tabVehicles Issuing Table`.last_issue_to_date , `tabVehicles Issuing Table`.entity_name, `tabVehicles Issuing Table`.bon_code, `tabVehicles Issuing Table`.vic_status, `tabVehicles Issuing Table`.tot_volume, 'Vehicles', 'liquid_table' 
FROM    `tabVehicles Issuing Table`
WHERE `tabVehicles Issuing Table`.oil_flag=1
AND `tabVehicles Issuing Table`.vehicle_boat = "Vehicles";

UPDATE `tabLiquids Issuing Table`
JOIN `tabLiquids Issuing` ON `tabLiquids Issuing Table`.issue_no = `tabLiquids Issuing`.name
SET `tabLiquids Issuing Table`.issue_type = `tabLiquids Issuing`.issue_type
WHERE `tabLiquids Issuing Table`.issue_type IS NULL
AND `tabLiquids Issuing`.oil_flag=1;

UPDATE `tabVehicles Issuing Table` 
JOIN `tabVehicles` ON `tabVehicles Issuing Table`.car_num = `tabVehicles`.vehicle_no
set `tabVehicles Issuing Table`.vehicle_boat = "Vehicles"
WHERE `tabVehicles Issuing Table`.vehicle_type IS NULL
AND `tabVehicles Issuing Table`.vehicle_boat IS NULL;

UPDATE `tabVehicles Issuing Table` 
JOIN `tabLiquids Issuing` ON `tabVehicles Issuing Table`.parent = `tabLiquids Issuing`.name
SET `tabVehicles Issuing Table`.last_issue_from_date = `tabLiquids Issuing`.from_date,
`tabVehicles Issuing Table`.last_issue_to_date = `tabLiquids Issuing`.to_date;
where `tabVehicles Issuing Table`.oil_flag = 1;

UPDATE `tabQty Per Liquid` 
set vehicles_count = on_vics,
qty = main_qty
where on_vics is not null
and oil_flag=1;


UPDATE `tabQty Per Liquid` 
JOIN `tabFuel Voucher` ON `tabQty Per Liquid`.bon_code = `tabFuel Voucher`.code
set `tabQty Per Liquid`.liquid = `tabFuel Voucher`.fuel_type
where `tabQty Per Liquid`.liquid is null;

UPDATE `tabQty Per Liquid` 
JOIN `tabOil Type` ON `tabQty Per Liquid`.bon_code = `tabOil Type`.code
set `tabQty Per Liquid`.liquid = `tabOil Type`.name
where `tabQty Per Liquid`.liquid is null
and `tabQty Per Liquid`.oil_flag=1;

-- datediff

UPDATE `tabLiquids Issuing` 
set issue_days = datediff(to_date, from_date)
WHERE oil_flag = 1;


UPDATE `tabLiquids Issuing` 
set issue_state = "جاري تحضير الصرفية ومراجعتها"
where issue_state is null
and tanfeez =0
and oil_flag=1;

UPDATE `tabLiquids Issuing` 
set issue_state = "تم صرف البونات من خزينة السوائل"
where issue_state is null
and tanfeez =200
and oil_flag=1;

SELECT  issue_state, tanfeez FROM `tabLiquids Issuing`;
Insert into `tabVehicles Issuing Table` (parent,entity_name,cel_num,vic_serial,car_num,bon_code,TOT_VOLUME,VIC_STATUS,SARFIA_FROM_DATE,SARFIA_TO_DATE,NOTES,SARFIA_TYPE,HAVING_CODE,OHDA_TYPE,ACTUAL_VOLUME,ACTUAL_DISTANCE) values (57168,113101000,4,26114,763112,14,750,-1,'01/07/23','31/07/23',null,0,5,null,0,0);
Insert into `tabVehicles Issuing Table` (parent,entity_name,CEL_NUM,VIC_SERIAL,CAR_NUM,BON_CODE,TOT_VOLUME,VIC_STATUS,SARFIA_FROM_DATE,SARFIA_TO_DATE,NOTES,SARFIA_TYPE,HAVING_CODE,OHDA_TYPE,ACTUAL_VOLUME,ACTUAL_DISTANCE,oil_flag, parenttype, parentfield) values (57051,120300000,1,69876,11843,122,3,0,'01/06/23','30/06/23','�����',1,5,null,0,0, 1, "Liquids Issuing", "vehicles_issuing_table");
Insert into `tabLiquids Issuing` (name,SARF_TO_ALL,entity,issue_date,issue_type,month_count,from_date,to_date,contact_person,tanfeez, oil_flag, parenttype, parentfield) values (57262,-1,101004000,'15/07/23',1,1,'01/07/23','31/07/23','عقيد/محمد عوض',0, 1, "Liquids Issuing", "vehicles_issuing_table");
Insert into `tabQty Per Liquid` (NAME,parent,BON_CODE,MAIN_QTY,RATIO_QTY,ADD_QTY,TOT_MONTH_QTY,NUMBER_OF_MONTHES,TOTAL_QTY,PREV_OVER_QTY,ACT_QTY,ON_VICS,NOTES,OFF_VICS,ACT_DATE,TANAZOL_QTY, oil_flag, parenttype,parentfield) values ('98216320',57099,122,3,0,0,3,1,null,21,null,3,null,13,null,null,1,"Liquids Issuing", "qty_per_liquid");
Insert into `tabVouchers Issued Per Liquid` (name,parent,BON_CODE,PRINT_NUM,from_serial,to_serial,notebook_count,TASWIA,ACT_QTY,ACT_DATE, voucher_flag, parenttype, parentfield) values (696055,57099,106,5,100413576,100413600,1,null,25,'19/06/23', 1, "Liquid Vouchers Issuing", "qty_per_liquid");


-- 

UPDATE `tabLiquids Issuing`
set docstatus = 1
where issue_type = "زيت"
and docstatus = 0
and oil_flag=1;




update `tabLiquid Vouchers Issuing`
JOIN `tabLiquids Issuing` ON `tabLiquid Vouchers Issuing`.name = `tabLiquids Issuing`.name
SET `tabLiquid Vouchers Issuing`.liquids_issuing = `tabLiquids Issuing`.name,
`tabLiquid Vouchers Issuing`.issue_type = `tabLiquids Issuing`.issue_type,
`tabLiquid Vouchers Issuing`.from_date = `tabLiquids Issuing`.from_date,
`tabLiquid Vouchers Issuing`.to_date = `tabLiquids Issuing`.to_date,
`tabLiquid Vouchers Issuing`.entity = `tabLiquids Issuing`.entity
WHERE `tabLiquid Vouchers Issuing`.voucher_flag = 1;


update `tabLiquid Vouchers Issuing`
JOIN `tabLiquids Issuing` ON `tabLiquid Vouchers Issuing`.name = `tabLiquids Issuing`.name
SET `tabLiquid Vouchers Issuing`.type = "صرفية شهرية"
WHERE `tabLiquid Vouchers Issuing`.voucher_flag = 1
AND `tabLiquids Issuing`.issue_to = "جهة";


update `tabVouchers Issued Per Liquid`
set voucher_qty = act_qty
where voucher_flag = 1
and qty = 0;


update `tabVouchers Issued Per Liquid`
JOIN `tabQty Per Liquid` ON `tabVouchers Issued Per Liquid`.parent = `tabQty Per Liquid`.parent
set `tabVouchers Issued Per Liquid`.liquid = `tabQty Per Liquid`.liquid,
`tabVouchers Issued Per Liquid`.vehicles_count = `tabQty Per Liquid`.vehicles_count,
`tabVouchers Issued Per Liquid`.qty = `tabQty Per Liquid`.qty
where `tabVouchers Issued Per Liquid`.voucher_flag = 1
and `tabQty Per Liquid`.bon_code = `tabVouchers Issued Per Liquid`.bon_code;

update `tabVouchers Issued Per Liquid`
join `tabLiquid Vouchers Issuing` on `tabVouchers Issued Per Liquid`.parent = `tabLiquid Vouchers Issuing`.name
JOIN `tabQty Per Liquid` ON `tabVouchers Issued Per Liquid`.parent = `tabQty Per Liquid`.parent
set `tabVouchers Issued Per Liquid`.liquid = `tabQty Per Liquid`.liquid,
`tabVouchers Issued Per Liquid`.vehicles_count = `tabQty Per Liquid`.vehicles_count,
`tabVouchers Issued Per Liquid`.qty = `tabQty Per Liquid`.qty
where `tabVouchers Issued Per Liquid`.voucher_flag = 0
and `tabQty Per Liquid`.bon_code = `tabVouchers Issued Per Liquid`.bon_code
and `tabLiquid Vouchers Issuing`.voucher_flag = 0;


update `tabVouchers Issued Per Liquid`
JOIN `tabOil Type` ON `tabVouchers Issued Per Liquid`.bon_code = `tabOil Type`.code
JOIN `tabLiquid Vouchers Issuing` ON `tabVouchers Issued Per Liquid`.parent = `tabLiquid Vouchers Issuing`.name
set `tabVouchers Issued Per Liquid`.liquid = `tabOil Type`.name
where `tabVouchers Issued Per Liquid`.voucher_flag = 1
and `tabLiquid Vouchers Issuing`.name = 57273;

update `tabVouchers Issued Per Liquid`
JOIN `tabQty Per Liquid` ON `tabVouchers Issued Per Liquid`.parent = `tabQty Per Liquid`.parent
set `tabVouchers Issued Per Liquid`.vehicles_count = `tabQty Per Liquid`.vehicles_count,
`tabVouchers Issued Per Liquid`.qty = `tabQty Per Liquid`.qty
where `tabVouchers Issued Per Liquid`.voucher_flag = 1
and `tabQty Per Liquid`.liquid = `tabVouchers Issued Per Liquid`.liquid
and `tabVouchers Issued Per Liquid`.parent = 57273;


update `tabVoucher`
JOIN `tabVouchers Issued Per Liquid` ON `tabVoucher`.issue_no = `tabVouchers Issued Per Liquid`.parent
join `tabLiquid Vouchers Issuing` ON `tabLiquid Vouchers Issuing`.name = `tabVouchers Issued Per Liquid`.parent
set `tabVoucher`.issue_no = `tabLiquid Vouchers Issuing`.name,
`tabVoucher`.issue_date = `tabLiquid Vouchers Issuing`.issue_date,
`tabVoucher`.entity = `tabLiquid Vouchers Issuing`.entity
where `tabVouchers Issued Per Liquid`.liquid = `tabVoucher`.voucher_type
and `tabVoucher`.issue_no is not null
and `tabVoucher`.entity is null
and `tabVoucher`.voucher_type = "زيت سي ـ اف فئة 8 لتر";

SELECT `tabVoucher`.issue_no,  `tabLiquid Vouchers Issuing`.name,  `tabVoucher`.issue_date,`tabLiquid Vouchers Issuing`.issue_date, `tabVoucher`.entity, `tabLiquid Vouchers Issuing`.entity, `tabVoucher`.serial_no, `tabVouchers Issued Per Liquid`.from_serial
FROM `tabVoucher`
JOIN `tabVouchers Issued Per Liquid` ON `tabVoucher`.issue_no = `tabVouchers Issued Per Liquid`.parent
join `tabLiquid Vouchers Issuing` ON `tabLiquid Vouchers Issuing`.name = `tabVouchers Issued Per Liquid`.parent
where `tabVouchers Issued Per Liquid`.liquid = `tabVoucher`.voucher_type
and `tabVoucher`.issue_no is not null
and `tabVoucher`.entity is null
and `tabVoucher`.voucher_type = "زيت سي ـ اف فئة 8 لتر";


----Vehicles
UPDATE `tabVehicles`
set oil_type = null
where exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
and oil_type is not null
and vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
and vehicle_type != "مقطورة";

SELECT count(*)
FROM `tabVehicles`
where exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
and oil_type is not null
and vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
and vehicle_type != "مقطورة";

UPDATE `tabVehicles`
set `tabVehicles`.oil_type = (
    SELECT `tabLiquids Issuing Table`.voucher
    FROM `tabLiquids Issuing Table`
    WHERE `tabLiquids Issuing Table`.parent = `tabVehicles`.name
    and `tabLiquids Issuing Table`.issue_type = "زيت"
    order by `tabLiquids Issuing Table`.from_date desc
    limit 1
)
where `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
and `tabVehicles`.vehicle_type != "مقطورة";


SELECT distinct oil_type
FROM `tabVehicles`
where oil_type  not in (
    SELECT name FROM `tabOil Type`
    
)
and vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
and vehicle_type != "مقطورة";


SELECT count(*)
FROM `tabLiquids Issuing Table` 
where voucher= "زيت  اس ام  فئة 4 لتر";

UPDATE `tabQty Per Liquid`
SET liquid = "زيت اس ام فئة 4 لتر"
WHERE liquid= "زيت  اس ام  فئة 4 لتر";

INSERT INTO `tabLiquids Issuing Table` ( parent ,car_num , issue_no, from_date, to_date,entity, voucher, vehicle_status,qty,parenttype, parentfield )
SELECT  `tabVehicles Issuing Table`.vehicle, `tabVehicles Issuing Table`.car_num, `tabVehicles Issuing Table`.parent, `tabVehicles Issuing Table`.last_issue_from_date, `tabVehicles Issuing Table`.last_issue_to_date , `tabVehicles Issuing Table`.entity_name, `tabVehicles Issuing Table`.bon_code, `tabVehicles Issuing Table`.vic_status, `tabVehicles Issuing Table`.tot_volume, 'Vehicles', 'liquid_table' 
FROM    `tabVehicles Issuing Table`
WHERE `tabVehicles Issuing Table`.oil_flag=1
AND `tabVehicles Issuing Table`.vehicle_boat = "Vehicles";


INSERT INTO `tabSold Lots Table` ( parent ,police_id , lot_no,
 accumulated_lot, vehicle,entity, vehicle_type,
  vehicle_shape,vehicle_brand,vehicle_model,vehicle_style,vehicle_color,chassis_no,
  motor_no,estimated_price,selling_price,parenttype, parentfield )
SELECT   `tabSales Info Payment`.name, `tabScrapped Vehicles Table`.police_id, `tabScrapped Vehicles Table`.lot_no,
`tabScrapped Vehicles Table`.accumulated_lot, `tabScrapped Vehicles Table`.vehicle,  `tabScrapped Vehicles Table`.entity,
`tabScrapped Vehicles Table`.vehicle_type,  `tabScrapped Vehicles Table`.vehicle_shape,`tabScrapped Vehicles Table`.vehicle_brand,
`tabScrapped Vehicles Table`.vehicle_model,`tabScrapped Vehicles Table`.vehicle_style,`tabScrapped Vehicles Table`.vehicle_color,
`tabScrapped Vehicles Table`.chassis_no,`tabScrapped Vehicles Table`.motor_no,`tabScrapped Vehicles Table`.estimated_price,
`tabScrapped Vehicles Table`.selling_price, "Sales Info Payment", "auction_sales_slips" 
FROM `tabScrapped Vehicles Table`
join `tabAuction Invoice` on `tabScrapped Vehicles Table`.parent = `tabAuction Invoice`.name
join `tabSales Info Payment` on `tabSales Info Payment`.auction_info = `tabAuction Invoice`.auction_info
where `tabSales Info Payment`.customer = `tabAuction Invoice`.customer;


update  `tabScrapped Vehicles Table`
join `tabAuction Invoice` on `tabScrapped Vehicles Table`.parent = `tabAuction Invoice`.invoice_number
set parenttype = "Auction Invoice",
parentfield = "auction_sales_slips",
parent = `tabAuction Invoice`.name;


UPDATE `tabScrapped Vehicles Table`
join `tabVehicles` ON `tabVehicles`.vic_serial = `tabScrapped Vehicles Table`.vehicle 
set `tabScrapped Vehicles Table`.vehicle = `tabVehicles`.name,
`tabScrapped Vehicles Table`.police_id = `tabVehicles`.vehicle_no,
`tabScrapped Vehicles Table`.entity = `tabVehicles`.entity_name,
`tabScrapped Vehicles Table`.vehicle_type = `tabVehicles`.vehicle_type,
`tabScrapped Vehicles Table`.vehicle_shape = `tabVehicles`.vehicle_shape,
`tabScrapped Vehicles Table`.vehicle_brand = `tabVehicles`.vehicle_brand,
`tabScrapped Vehicles Table`.vehicle_model = `tabVehicles`.vehicle_model,
`tabScrapped Vehicles Table`.vehicle_style = `tabVehicles`.vehicle_style,
`tabScrapped Vehicles Table`.vehicle_color = `tabVehicles`.vehicle_color,
`tabScrapped Vehicles Table`.chassis_no = `tabVehicles`.chassis_no,
`tabScrapped Vehicles Table`.motor_no = `tabVehicles`.motor_no;

UPDATE `tabBoats` 
JOIN `tabEngine Table` ON `tabEngine Table`.parent = `tabBoats`.name
set `tabBoats`.engine_no2 = `tabEngine Table`.engine_no,
`tabBoats`.engine_brand2 = `tabEngine Table`.engine_brand,
`tabBoats`.engine_power2 = `tabEngine Table`.engine_power,
`tabBoats`.motor_cylinder_count2 = `tabEngine Table`.cylinder_count,
`tabBoats`.feeding_type2 = `tabEngine Table`.feeding_type,
`tabBoats`.motor_fuel_type2 = `tabEngine Table`.fuel_type,
`tabBoats`.entity2 = `tabEngine Table`.entity,
`tabBoats`.motor_capacity2 = `tabEngine Table`.motor_capacity,
`tabBoats`.current_validity2 = `tabEngine Table`.current_validity
WHERE `tabEngine Table`.parenttype = "Boats"
AND `tabEngine Table`.parentfield = "engine_table"
and `tabEngine Table`.idx =2;

-- GET ALL VEHICLES HAS DUPLICAT private_no
SELECT `tabVehicles`.name, `tabVehicles`.private_no, count(`tabVehicles`.private_no)
FROM `tabVehicles`
GROUP BY `tabVehicles`.private_no
HAVING count(`tabVehicles`.private_no) > 1;


SELECT `tabVehicles`.name, `tabVehicles`.private_no, `tabPrivate Plate Logs`.date
From `tabVehicles`
JOIN `tabPrivate Plate Logs` ON `tabVehicles`.name = `tabPrivate Plate Logs`.parent
where `tabVehicles`.private_no = `tabPrivate Plate Logs`.value
and `tabPrivate Plate Logs`.idx = (select max(idx) from `tabPrivate Plate Logs` where `tabPrivate Plate Logs`.parent = `tabVehicles`.name);

[{'222300': [{'VEH-00765': datetime.date(2004, 10, 23)}, {'VEH-13794': datetime.date(2004, 6, 5)}]}]


UPDATE `tabPolice Plate`
SET current_vehicle = "إحتياطي مخزن لوحات"
WHERE current_vehicle != "إحتياطي مخزن لوحات"
AND current_vehicle not in (
    SELECT name 
    FROM `tabVehicles`
);
---- Attached Entity Logs
update `tabAttached Entity Logs`
Join `tabVehicles` ON `tabVehicles`.vic_serial = `tabAttached Entity Logs`.vic_serial
set  `tabAttached Entity Logs`.parent = `tabVehicles`.name
where  `tabAttached Entity Logs`.vic_serial is not  null;

update `tabAttached Entity Logs`
JOIN `tabEntity` On `tabEntity`.code = `tabAttached Entity Logs`.attgehacode
set `tabAttached Entity Logs`.value = `tabEntity`.name
where `tabAttached Entity Logs`.attgehacode is not null;

--- `tabEntity Logs`

update `tabEntity Logs`
join `tabBoats` ON `tabBoats`.boat_no = `tabEntity Logs`.LAUNCH_NO
set `tabEntity Logs`.parent = `tabBoats`.name
where `tabEntity Logs`.LAUNCH_NO is not null;

update `tabEntity Logs`
join `tabEntity` ON `tabEntity`.code = `tabEntity Logs`.VALUE
set `tabEntity Logs`.value = `tabEntity`.name
where `tabEntity Logs`.LAUNCH_NO is not null;

-- `tabVehicle Status Logs`

update `tabVehicle Status Logs`
join `tabVehicle Status` ON `tabVehicle Status`.code = `tabVehicle Status Logs`.motorcase_code
set value = `tabVehicle Status`.name
where `tabVehicle Status Logs`.motorcase_code is not null;

-- Editing Table
update `tabEditing Table`
JOIN `tabBoats` ON `tabBoats`.boat_no = `tabEditing Table`.old_transaction_no
set `tabEditing Table`.old_transaction_no = `tabBoats`.name
where `tabEditing Table`.ass_date is not null;
