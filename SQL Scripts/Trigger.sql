CREATE OR REPLACE TRIGGER validate_phone_number
AFTER INSERT OR UPDATE ON rider
FOR EACH ROW
DECLARE
    v_phone_length NUMBER := 0;
    v_phone_num CHAR(10);
BEGIN
    v_phone_num := :new.phone_num;
    
    FOR i IN 1..10 LOOP
        IF SUBSTR(v_phone_num, i, 1) IS NOT NULL THEN
            v_phone_length := v_phone_length + 1;
        END IF;
    END LOOP;
    
    IF v_phone_length != 10 THEN
        dbms_output.put_line('Not valid');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER calculate_fare_and_cut
AFTER UPDATE ON trip
FOR EACH ROW
DECLARE
    v_distance trip.dist%TYPE;
    v_fare trip.fare%TYPE;
    v_cut driver.cut%TYPE;
    v_last_driver_id driver.user_id%TYPE;
BEGIN
    IF :new.status = 'Completed' THEN

        v_distance := :new.dist;
        v_fare := v_distance * 2;
        v_cut := v_fare * 0.2;

        SELECT driver_id INTO v_last_driver_id
        FROM trip
        WHERE trip_id = :new.trip_id;

        UPDATE trip
        SET fare = v_fare, tarcking_id = :new.tarcking_id
        WHERE trip_id = :new.trip_id;

        UPDATE driver
        SET cut = cut + v_cut
        WHERE user_id = v_last_driver_id;

        DBMS_OUTPUT.PUT_LINE('Fare and cut calculated and updated successfully.');
    END IF;
END;
/

