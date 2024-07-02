CREATE SEQUENCE TRIP_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE PROCEDURE insert_rider1(
    p_user_id IN rider.user_id%TYPE,
    p_password IN rider.password%TYPE,
    p_name IN rider.name%TYPE,
        p_mail_id IN rider.mail_id%TYPE,
    p_phone_num IN rider.phone_num%TYPE
)
AS
BEGIN
    INSERT INTO rider VALUES (p_user_id, p_password, p_name, p_mail_id, p_phone_num, NULL, NULL, 0);
    DBMS_OUTPUT.PUT_LINE('Data inserted successfully.');
END
/

CREATE OR REPLACE PROCEDURE insert_driver(
    p_user_id IN driver.user_id%TYPE,
    p_password IN driver.password%TYPE,
    p_name IN driver.name%TYPE,
    p_mail_id IN driver.mail_id%TYPE,
    p_phone_num IN driver.phone_num%TYPE,
    p_vehicle_id IN driver.vehicle_id%TYPE,
    p_shift_id IN driver.shift_id%TYPE
)
AS
BEGIN
    INSERT INTO driver VALUES (
        p_user_id, p_password, p_name, p_mail_id, p_phone_num,
        NULL, NULL, 0, p_vehicle_id, 0,
        NULL, p_shift_id
    );
    DBMS_OUTPUT.PUT_LINE('Data inserted successfully.');
END;
/

CREATE OR REPLACE PROCEDURE insert_trip(
    p_trip_id IN trip.trip_id%TYPE,
    p_pickup_loc IN trip.pickup_loc%TYPE,
    p_drop_loc IN trip.drop_loc%TYPE,
    p_rider_id IN trip.rider_id%TYPE,
    p_tarcking_id IN trip.tarcking_id%TYPE
)
AS
BEGIN
    INSERT INTO trip VALUES (
        TRIP_SEQ.NEXTVAL, p_pickup_loc, p_drop_loc, SYSTIMESTAMP, SYSTIMESTAMP,
        0, NULL, p_rider_id, 'Searching', 0, 0, TRIP_SEQ.NEXTVAL
    );
    DBMS_OUTPUT.PUT_LINE('Data inserted successfully.');
END;
/

CREATE OR REPLACE PROCEDURE update_trip_end_time(
    p_trip_id IN trip.trip_id%TYPE
)
AS
BEGIN
    UPDATE trip
    SET end_time = SYSTIMESTAMP
    WHERE trip_id = p_trip_id;

    DBMS_OUTPUT.PUT_LINE('End time updated successfully.');
END;
/
CREATE OR REPLACE PROCEDURE assign_driver(trip_id1 in trip.trip_id%TYPE)
AS
    D_ID NUMBER;
BEGIN
    SELECT USER_ID INTO D_ID FROM DRIVER ORDER BY AVG_RATING DESC;
    UPDATE TRIP SET TRIP.DRIVER_ID = D_ID,STATUS='Alloted' WHERE TRIP.TRIP_ID = TRIP_ID1;
END;
/

