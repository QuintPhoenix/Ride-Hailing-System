/* Primary Keys and Checks */
alter table rider add constraint rider_pk primary key (user_id);
alter table rider add constraint rider_phone_num_check check (length(phone_num)=10); 
alter table driver add constraint driver_pk primary key (user_id);
alter table driver add constraint driver_phone_num_check check (length(phone_num)=10);
alter table shift add constraint shift_pk primary key (shift_id);
alter table shift add constraint shift_timing_check check (start_time<=end_time);
alter table vehicle add constraint vehicle_pk primary key (vehicle_id);
alter table vehicle add constraint vehicle_status_check check (status = 'Free' or status ='Booked');
alter table pays_for add constraint pays_for_pk primary key (payment_id);
alter table pays_for add constraint payment_mode_check check (payment_mode='Cash' or payment_mode='Online');
alter table trip add constraint trip_pk primary key (trip_id);
alter table trip add constraint trip_timing_check check (start_time<=end_time);

/*foreign keys */
alter table driver add constraint driver_shift_fk foreign key (shift_id) references shift(shift_id) on delete cascade;
alter table driver add constraint driver_vehicle_fk foreign key (vehicle_id) references vehicle(vehicle_id) on delete cascade;
alter table pays_for add constraint pays_for_rider_fk foreign key (user_id) references rider(user_id) on delete cascade;
alter table pays_for add constraint pays_for_trip_fk foreign key (trip_id) references trip(trip_id) on delete cascade;
alter table trip add constraint trip_rider_fk foreign key (rider_id) references rider(user_id) on delete cascade;
alter table trip add constraint trip_driver_fk foreign key (driver_id) references driver(user_id) on delete cascade;

