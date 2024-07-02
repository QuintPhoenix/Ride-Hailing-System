create table rider(user_id int,password varchar(20) NOT NULL,name varchar(20) NOT NULL,mail_id varchar(20) NOT NULL,phone_num varchar(10) NOT NULL,DOB date NOT NULL,address varchar(20) NOT NULL,avg_rating float);

create table driver(user_id int,password varchar(20) NOT NULL,name varchar(20) NOT NULL,mail_id varchar(20) NOT NULL,phone_num varchar(10) NOT NULL,DOB date NOT NULL,address varchar(20) NOT NULL,avg_rating float,vehicle_id int NOT NULL,cut int NOT NULL,current_loc varchar(20),shift_id int);

create table shift(shift_id int,start_time timestamp,end_time timestamp);

create table vehicle(vehicle_id int NOT NULL,seating_capacity int NOT NULL,type varchar(10) NOT NULL,color varchar(20) NOT NULL,status varchar(20),model varchar(20) NOT NULL,plate_num varchar(20) NOT NULL);

create table pays_for(user_id int, trip_id int ,payment_id int,event_timestamp timestamp,payment_mode int);

create table trip(trip_id int,pickup_loc varchar(20),drop_loc varchar(20),start_time timestamp,end_time timestamp,dist int,driver_id int,rider_id int,status varchar(20),rating float,fare int,tarcking_id int NOT NULL);