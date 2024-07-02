create or replace procedure createRider(password in varchar2,name in varchar2,mail_id in varchar2,phone_num in varchar2, dob in date,address_user in varchar2) as
    ex exception;
    pragma exception_init(ex,-2290);
begin
    insert into rider values(seq_rider.nextval,password,name,mail_id,phone_num,dob,address_user,null);
exception
    when ex then
        dbms_output.put_line('!! Error - Phone Number Must be of exactly 10 digits !!');
end;
/