
CREATE VIEW get_payments_view AS
SELECT DISTINCT 
    a.id,
    CONCAT(b.firstname, ' ', b.lastname) AS paymentby,
    CONCAT(c.firstname, ' ', c.lastname) AS paymentto,
    a.amount,
    a.paidon,
    d.name AS paymentmode,
    f.status AS paymentstatus,
    a.description,
    a.banktransactionid,
    e.name AS paymentfor,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.entityid,
    a.officeid,
    a.tds,
    a.professiontax,
    a.month,
    a.deduction 
FROM 
    ref_contractual_payments a, 
    usertable b, 
    usertable c, 
    mode_of_payment d, 
    payment_for e,
    paymentrequeststatus f
WHERE 
    a.paymentto = b.id 
    AND a.paymentby = c.id 
    AND a.paymentmode = d.id 
    AND a.paymentfor = e.id
    AND a.paymentstatus = f.id;



CREATE OR REPLACE FUNCTION delete_from_get_payments_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM ref_contractual_payments WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_payments_view
INSTEAD OF DELETE ON get_payments_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_payments_view();


CREATE VIEW get_employee_view AS
SELECT DISTINCT
    a.id,
    a.employeename,
    a.employeeid,
    a.userid,
    b.name AS role,
    a.dateofjoining,
    a.dob,
    a.panno,
    a.status,
    a.phoneno,
    a.email,
    a.addressline1,
    a.addressline2,
    a.suburb,
    c.city,
    a.state,
    d.name as country,
    a.createdby,
    a.isdeleted,
    e.name as entity,
    f.name as lob,
    a.lastdateofworking,
    a.designation
FROM
    employee a,
    role b,
    cities c,
    country d,
    entity e,
    lob f
WHERE
    (a.roleid = b.id) AND
    a.city = c.id AND
    a.country = d.id AND
    (a.entityid = e.id) AND
    (a.lobid = f.id);




CREATE OR REPLACE FUNCTION delete_from_get_employee_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM employee WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_employee_view
INSTEAD OF DELETE ON get_employee_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_employee_view();


CREATE VIEW get_locality_view AS
SELECT DISTINCT
    a.id,
    a.locality,
    b.city as city,
    b.state as state,
    c.name as country,
    c.id as countryid
FROM 
    locality a,
    cities b,
    country c
WHERE
    a.cityid = b.id AND
    b.countryid = c.id;




CREATE OR REPLACE FUNCTION delete_from_get_locality_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM locality WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_locality_view
INSTEAD OF DELETE ON get_locality_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_locality_view();


CREATE VIEW get_research_prospect_view AS
SELECT DISTINCT
    a.id,
    a.personname,
    a.suburb,
    a.city,
    a.state,
    c.name,
    a.country,
    a.propertylocation,
    a.possibleservices,
    a.dated,
    a.createdby,
    a.isdeleted
FROM 
    research_prospect a,
    cities b,
    country c
WHERE
    a.country = c.id;


CREATE OR REPLACE FUNCTION delete_from_get_research_prospect_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM research_prospect WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_research_prospect_view
INSTEAD OF DELETE ON get_research_prospect_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_research_prospect_view();
