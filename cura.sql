
CREATE INDEX ON usertable(id);
CREATE INDEX ON mode_of_payment(id);
CREATE INDEX ON payment_for(id);
CREATE INDEX ON z_paymentrequeststatus(id);
--CREATE INDEX ON paymentrequeststatus(id);
CREATE INDEX ON entity(id);
CREATE VIEW get_payments_view AS
SELECT
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
    g.name as entity,
    a.officeid,
    a.tds,
    a.professiontax,
    a.month,
    a.deduction

FROM ref_contractual_payments a
inner JOIN usertable b ON a.paymentto = b.id
inner JOIN usertable c ON a.paymentby = c.id
inner JOIN mode_of_payment d ON a.paymentmode = d.id
inner JOIN payment_for e ON a.paymentfor = e.id
inner JOIN z_paymentrequeststatus f ON a.paymentstatus = f.id
inner JOIN entity g ON a.entityid = g.id;

--FROM ref_contractual_payments a,
--    usertable b,
--    usertable c,
--    mode_of_payment d,
--    payment_for e,
--    paymentrequeststatus f,
--    entity g
--WHERE
--    a.paymentto = b.id
--    AND a.paymentby = c.id
--    AND a.paymentmode = d.id
--    AND a.paymentfor = e.id
--    AND a.paymentstatus = f.id
--    AND a.entityid = g.id;



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
SELECT
    a.id,
    a.employeename,
    a.employeeid,
    a.userid,
    b.name AS role,
    a.roleid,
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
SELECT
    a.id,
    a.locality,
    a.cityid,
    b.city as city,
    b.state as state,
    c.name as name,
    c.name as country
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
SELECT
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


CREATE VIEW get_builder_view AS
SELECT
    a.id,
    a.buildername,
    a.phone1,
    a.phone2,
    a.email1,
    a.email2,
    a.addressline1,
    a.addressline2,
    a.suburb,
    b.city,
    a.state,
    c.name as country,
    a.zip,
    a.website,
    a.comments,
    a.dated,
    a.createdby,
    a.isdeleted
FROM 
    builder a,
    cities b,
    country c
WHERE 
    a.city = b.id AND
    a.country = c.id;

CREATE OR REPLACE FUNCTION delete_from_get_builder_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM builder WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_builder_view
INSTEAD OF DELETE ON get_builder_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_builder_view();

CREATE VIEW get_cities_view AS
SELECT
    a.id,
    a.city,
    a.state,
    a.countryid,
    b.name as country
FROM 
    cities a,
    country b
WHERE a.countryid = b.id;

CREATE OR REPLACE FUNCTION delete_from_get_cities_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM cities WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_cities_view
INSTEAD OF DELETE ON get_cities_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_cities_view();

CREATE VIEW get_projects_view AS
SELECT
    b.buildername,
    a.builderid,
    a.projectname,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city,
    a.state,
    a.country,
    a.zip,
    a.nearestlandmark,
    a.project_type,
    c.name as projecttypename, --project type
    a.mailgroup1,
    a.mailgroup2,
    a.website,
    a.project_legal_status,
    d.name as projectlegalstatusname, --project legal status
    a.rules,
    a.completionyear,
    a.jurisdiction,
    a.taluka,
    a.corporationward,
    a.policechowkey,
    a.policestation,
    a.maintenance_details,
    a.numberoffloors,
    a.numberofbuildings,
    a.approxtotalunits,
    a.tenantstudentsallowed,
    a.tenantworkingbachelorsallowed,
    a.tenantforeignersallowed,
    a.otherdetails,
    a.duespayablemonth,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.id
FROM
    project a,
    builder b,
    project_type c,
    project_legal_status d
WHERE
    a.builderid = b.id AND
    a.project_type = c.id AND
    a.project_legal_status = d.id;

CREATE OR REPLACE FUNCTION delete_from_get_projects_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM projects WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_projects_view
INSTEAD OF DELETE ON get_projects_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_projects_view();

CREATE VIEW get_builder_contact_view AS
SELECT
    a.id,
    b.buildername,
    a.builderid,
    a.contactname,
    a.email1,
    a.jobtitle,
    a.businessphone,
    a.homephone,
    a.mobilephone,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city,
    a.state,
    a.country,
    a.zip,
    a.notes,
    a.dated,
    a.createdby,
    a.isdeleted
FROM
    builder_contacts a,
    builder b
WHERE 
    a.builderid = b.id;

CREATE OR REPLACE FUNCTION delete_from_get_builder_contacts_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM builder_contacts WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_builder_contacts_view
INSTEAD OF DELETE ON get_builder_contact_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_builder_contacts_view();


CREATE VIEW get_client_info_view AS
SELECT 
    a.id,
    a.firstname,
    a.middlename,
    a.lastname,
    concat_ws(' ',a.firstname,a.middlename,a.lastname) as clientname,
    a.salutation,
    a.clienttype,
    b.name as clienttypename,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city,
    a.state,
    c.name as country,
    a.zip,
    a.homephone,
    a.workphone,
    a.mobilephone,
    a.email1,
    a.email2,
    a.employername,
    a.comments,
    a.photo,
    a.onlineaccreated,
    a.localcontact1name,
    a.localcontact1address,
    a.localcontact1details,
    a.localcontact2name,
    a.localcontact2address,
    a.localcontact2details,
    a.includeinmailinglist,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.entityid,
    a.tenantof,
    concat_ws(' ',d.firstname,d.middlename,d.lastname) as tenantofname,
    a.tenantofproperty,
    concat_ws('-',e.propertydescription,e.suburb) as tenantofpropertyname
FROM
    client a,
    client_type b,
    country c,
    client d,
    client_property e
WHERE
    a.clienttype = b.id and a.country = c.id
    and a.tenantof = d.id and a.tenantofproperty = e.id;


CREATE OR REPLACE FUNCTION delete_from_get_client_info_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM client WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_client_info_view
INSTEAD OF DELETE ON get_client_info_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_client_info_view();

CREATE VIEW get_client_property_view AS
SELECT DISTINCT
    a.id,
    CONCAT(b.firstname,' ',b.middlename,' ',b.lastname) as client,
    a.clientid,
    c.projectname as project,
    a.projectid,
    a.propertytype as propertytypeid,
    d.name as propertytype,
    a.suburb,
    a.city as cityid,
    a.city,
    a.state,
    a.country as countryid,
    f.name as country,
    a.layoutdetails,
    a.numberofparkings,
    a.internalfurnitureandfittings,
    a.leveloffurnishing,
    a.status as propertystatus,
    g.name as status,
    a.initialpossessiondate,
    a.poagiven,
    a.poaid,
    a.electricityconsumernumber,
    a.electricitybillingunit,
    a.otherelectricitydetails,
    a.gasconnectiondetails,
    a.propertytaxnumber,
    CONCAT(h.firstname,' ',h.lastname) as clientservicemanager,
    CONCAT(i.firstname,' ',i.lastname) as propertymanager,
    a.comments,
    a.propertyownedbyclientonly,
    a.textforposting,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.electricitybillingduedate
FROM
    client_property a
LEFT JOIN
    client b ON a.clientid = b.id
LEFT JOIN
    project c ON a.projectid = c.id
LEFT JOIN
    property_type d ON a.propertytype = d.id
LEFT JOIN
    country f ON a.country = f.id
LEFT JOIN
    property_status g ON a.status = g.id
LEFT JOIN
    usertable h ON a.clientservicemanager = h.id
LEFT JOIN
    usertable i ON a.propertymanager = i.id;


CREATE OR REPLACE FUNCTION delete_from_get_client_property_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM client WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_client_property_view
INSTEAD OF DELETE ON get_client_property_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_client_property_view();

CREATE VIEW get_orders_view AS
SELECT
    a.id,
    a.clientid,
    CONCAT(g.firstname,' ',g.lastname) as client_name,
    a.orderdate,
    a.earlieststartdate,
    a.expectedcompletiondate,
    a.actualcompletiondate,
    a.owner,
    CONCAT(b.firstname,' ',b.lastname) as owner_name,
    a.comments,
    a.status,
    a.description,
    a.service,
    a.clientpropertyid,
    a.vendorid,
    c.vendorname,
    a.assignedtooffice,
    d.name as officename,
    a.billable,
    a.statusupdatedtimestamp,
    CONCAT(e.firstname,' ',e.lastname) as defaulttaskowner,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.glcode,
    a.entityid,
    f.name as entity,
    a.tallyledgerid
FROM
    orders a,
    usertable b,
    vendor c,
    office d,
    usertable e,
    entity f,
    client g
WHERE
    a.owner = b.id AND
    a.vendorid = c.id AND
    a.assignedtooffice = d.id AND
    a.default_task_owner = e.id AND
    a.entityid = f.id AND
    a.clientid = g.id;

-- Create a new sequence if it doesn't exist starting from the maximum value of column id + 1
CREATE SEQUENCE IF NOT EXISTS builder_id_seq OWNED BY builder.id;

-- Set the initial value of the sequence based on the maximum value of column id in the builder table
SELECT setval('builder_id_seq', COALESCE(max(id), 0) + 1, false) FROM builder;

-- Alter the table to set the default value of column id to use the sequence
ALTER TABLE builder ALTER COLUMN id SET DEFAULT nextval('builder_id_seq');

-- For client table
CREATE SEQUENCE IF NOT EXISTS client_id_seq OWNED BY client.id;
SELECT setval('client_id_seq', COALESCE(max(id), 0) + 1, false) FROM client;
ALTER TABLE client ALTER COLUMN id SET DEFAULT nextval('client_id_seq');

-- For client_access table
CREATE SEQUENCE IF NOT EXISTS client_access_id_seq OWNED BY client_access.id;
SELECT setval('client_access_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_access;
ALTER TABLE client_access ALTER COLUMN id SET DEFAULT nextval('client_access_id_seq');

-- For client_legal_info table
CREATE SEQUENCE IF NOT EXISTS client_legal_info_id_seq OWNED BY client_legal_info.id;
SELECT setval('client_legal_info_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_legal_info;
ALTER TABLE client_legal_info ALTER COLUMN id SET DEFAULT nextval('client_legal_info_id_seq');

-- For client_bank_info table
CREATE SEQUENCE IF NOT EXISTS client_bank_info_id_seq OWNED BY client_bank_info.id;
SELECT setval('client_bank_info_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_bank_info;
ALTER TABLE client_bank_info ALTER COLUMN id SET DEFAULT nextval('client_bank_info_id_seq');

-- For client_poa table
CREATE SEQUENCE IF NOT EXISTS client_poa_id_seq OWNED BY client_poa.id;
SELECT setval('client_poa_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_poa;
ALTER TABLE client_poa ALTER COLUMN id SET DEFAULT nextval('client_poa_id_seq');

CREATE SEQUENCE IF NOT EXISTS project_id_seq OWNED BY project.id;
SELECT setval('project_id_seq', COALESCE(max(id), 0) + 1, false) FROM project;
ALTER TABLE project ALTER COLUMN id SET DEFAULT nextval('project_id_seq');

CREATE SEQUENCE IF NOT EXISTS project_amenities_id_seq OWNED BY project_amenities.id;
SELECT setval('project_amenities_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_amenities;
ALTER TABLE project_amenities ALTER COLUMN id SET DEFAULT nextval('project_amenities_id_seq');

CREATE SEQUENCE IF NOT EXISTS project_bank_details_id_seq OWNED BY project_bank_details.id;
SELECT setval('project_bank_details_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_bank_details;
ALTER TABLE project_bank_details ALTER COLUMN id SET DEFAULT nextval('project_bank_details_id_seq');

CREATE SEQUENCE IF NOT EXISTS project_contacts_id_seq OWNED BY project_contacts.id;
SELECT setval('project_contacts_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_contacts;
ALTER TABLE project_contacts ALTER COLUMN id SET DEFAULT nextval('project_contacts_id_seq');

CREATE SEQUENCE IF NOT EXISTS project_photos_id_seq OWNED BY project_photos.id;
SELECT setval('project_photos_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_photos;
ALTER TABLE project_photos ALTER COLUMN id SET DEFAULT nextval('project_photos_id_seq');

CREATE TABLE project_photos(
    id int,
    projectid int,
    photo_link text,
    description text,
    date_taken date,
    dated timestamp(3),
    createdby int,
    isdeleted boolean
);

CREATE SEQUENCE IF NOT EXISTS client_property_id_seq OWNED BY client_property.id;
SELECT setval('client_property_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property;
ALTER TABLE client_property ALTER COLUMN id SET DEFAULT nextval('client_property_id_seq');

CREATE SEQUENCE IF NOT EXISTS client_property_photos_id_seq OWNED BY client_property_photos.id;
SELECT setval('client_property_photos_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_photos;
ALTER TABLE client_property_photos ALTER COLUMN id SET DEFAULT nextval('client_property_photos_id_seq');

CREATE SEQUENCE IF NOT EXISTS client_property_poa_id_seq OWNED BY client_property_poa.id;
SELECT setval('client_property_poa_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_poa;
ALTER TABLE client_property_poa ALTER COLUMN id SET DEFAULT nextval('client_property_poa_id_seq');


CREATE SEQUENCE IF NOT EXISTS client_property_owner_id_seq OWNED BY client_property_owner.id;
SELECT setval('client_property_owner_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_owner;
ALTER TABLE client_property_owner ALTER COLUMN id SET DEFAULT nextval('client_property_owner_id_seq');

SELECT * FROM client_property WHERE id=18194;
SELECT * FROM client_property_photos WHERE clientpropertyid=18194;
SELECT * FROM client_property_poa WHERE clientpropertyid=18194;
SELECT * FROM client_property_owner WHERE propertyid=18194;

INSERT INTO your_table (column1, column2, ...)
VALUES (value1, value2, ...)
RETURNING *;

alter table client_property alter column initialpossessiondate date;

alter table client_property add column website text;
alter table client_property add column email text;

SELECT setval('client_property_id_seq', (SELECT MAX(id) FROM client_property));
