
CREATE INDEX ON usertable(id);
CREATE INDEX ON mode_of_payment(id);
CREATE INDEX ON payment_for(id);
CREATE INDEX ON z_paymentrequeststatus(id);
--CREATE INDEX ON paymentrequeststatus(id);
CREATE INDEX ON entity(id);

-- Create the table
CREATE TABLE z_paymentrequeststatus (
    id INT,
    status TEXT
);

-- Create the table
CREATE TABLE order_status (
    id INT,
    name TEXT
);

-- Insert data into the table
INSERT INTO order_status (id, name) VALUES
(1, 'On hold'),
(2, 'Estimate Given'),
(4, 'Cancelled'),
(6, 'Billed'),
(9, 'In progress'),
(5, 'Closed (Work Done & Collection Completed)'),
(8, 'Work Done - Pending Collection');


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
    g.name as entity,
    a.officeid,
    a.tds,
    a.professiontax,
    a.month,
    a.deduction

FROM ref_contractual_payments a
LEFT JOIN usertable b ON a.paymentto = b.id
LEFT JOIN usertable c ON a.paymentby = c.id
LEFT JOIN mode_of_payment d ON a.paymentmode = d.id
LEFT JOIN payment_for e ON a.paymentfor = e.id
LEFT JOIN z_paymentrequeststatus f ON a.paymentstatus = f.id
LEFT JOIN entity g ON a.entityid = g.id;

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
SELECT DISTINCT
    a.id,
    a.employeename,
    a.employeeid,
    a.userid,
    b.role_name AS role,
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
    employee a
LEFT JOIN 
    roles b ON a.roleid = b.id
LEFT JOIN
    cities c ON a.city = c.id
LEFT JOIN
    country d ON a.country = d.id
LEFT JOIN
    entity e ON a.entityid = e.id
LEFT JOIN
    lob f ON a.lobid = f.id;




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

CREATE VIEW get_lob_view AS
 SELECT DISTINCT a.id,
    a.name,
    concat_ws(' '::text, b.firstname, b.lastname) AS lob_head,
    a.company,
    c.name AS entity
   FROM lob a
     LEFT JOIN usertable_old b ON a.lob_head = b.id
     LEFT JOIN entity_old c ON a.entityid = c.id;



CREATE VIEW get_locality_view AS
SELECT
    a.id,
    a.locality,
    a.cityid,
    b.city as city,
    b.state as state,
    c.name as name,
    c.name as country,
    c.id as countryid
FROM 
    locality a
LEFT JOIN
    cities b ON a.cityid = b.id
LEFT JOIN
    country c ON b.countryid = c.id;
    




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
    research_prospect a
LEFT JOIN
    country c ON a.country = c.id;


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
SELECT DISTINCT
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
    builder a
LEFT JOIN
    cities b ON a.city = b.id
LEFT JOIN
    country c ON a.country = c.id;

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
SELECT DISTINCT
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
    project a
LEFT JOIN
    builder b ON a.builderid = b.id
LEFT JOIN
    project_type c ON a.project_type = c.id
LEFT JOIN
    project_legal_status d ON a.project_legal_status = d.id;

CREATE OR REPLACE FUNCTION delete_from_get_projects_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM projects WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple
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
    builder_contacts a
LEFT JOIN
    builder b ON a.builderid = b.id;

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
    concat_ws(' ',a.firstname,NULLIF(a.middlename,''),a.lastname) as clientname,
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
    client a
LEFT JOIN 
    client_type b ON a.clienttype = b.id
LEFT JOIN 
    country c ON a.country = c.id
LEFT JOIN 
    client d ON a.tenantof = d.id
LEFT JOIN
    client_property e ON a.tenantofproperty = e.id;



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
    CONCAT(b.firstname,' ',NULLIF(b.middlename,''),' ',b.lastname) as client,
    a.clientid,
    c.projectname as project,
    a.projectid,
    a.propertydescription as description,
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
    concat_ws(' ',c.projectname,a.propertydescription) as property,
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
SELECT DISTINCT
    a.id,
    a.clientid,
    CONCAT(g.firstname,' ',NULLIF(g.middlename,''),' ',g.lastname) as clientname,
    a.orderdate,
    a.earlieststartdate,
    a.expectedcompletiondate,
    a.actualcompletiondate,
    a.owner,
    CONCAT(b.firstname,' ',b.lastname) as ownername,
     a.id,concat_ws('-',concat_ws(' ',b.firstname,b.lastname),briefdescription
    a.comments,
    a.status,
    h.name as orderstatus,
    a.briefdescription,
    a.additionalcomments,
    a.service,
    e.service as servicename,
    a.clientpropertyid,
    concat_ws('-',i.suburb,i.propertydescription) as clientproperty,
    a.vendorid,
    c.vendorname,
    a.assignedtooffice,
    d.name as officename,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.entityid,
    f.name as entity,
    a.tallyledgerid
FROM
    orders a
LEFT JOIN
    usertable b ON a.owner = b.id
LEFT JOIN
    vendor c ON a.vendorid = c.id
LEFT JOIN
    office d ON a.assignedtooffice = d.id
LEFT JOIN
    services e ON a.service = e.id
LEFT JOIN
    entity f ON a.entityid = f.id
LEFT JOIN
    client g ON a.clientid = g.id
LEFT JOIN
    order_status h ON a.status = h.id
LEFT JOIN
    client_property i ON a.clientpropertyid = i.id;

CREATE SEQUENCE IF NOT EXISTS payments_id_seq OWNED BY ref_contractual_payments.id;
SELECT setval('payments_id_seq', COALESCE(max(id), 0) + 1, false) FROM ref_contractual_payments;
ALTER TABLE ref_contractual_payments ALTER COLUMN id SET DEFAULT nextval('payments_id_seq');

CREATE SEQUENCE IF NOT EXISTS orders_id_seq OWNED BY orders.id;
SELECT setval('orders_id_seq', COALESCE(max(id), 0) + 1, false) FROM orders;
ALTER TABLE orders ALTER COLUMN id SET DEFAULT nextval('orders_id_seq');


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

CREATE SEQUENCE IF NOT EXISTS country_id_seq OWNED BY country.id;
SELECT setval('country_id_seq', COALESCE(max(id), 0) + 1, false) FROM country;
ALTER TABLE country ALTER COLUMN id SET DEFAULT nextval('country_id_seq');

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


alter table client_property alter column initialpossessiondate date;

alter table client_property add column website text;
alter table client_property add column email text;

SELECT setval('client_property_id_seq', (SELECT MAX(id) FROM client_property));

ALTER TABLE client_property_caretaking_agreement RENAME COLUMN pmaholder TO poaholder;

CREATE VIEW get_client_receipt_view AS
SELECT DISTINCT
    a.id,
    a.receivedby,
    concat_ws(' ',f.firstname,f.lastname) as receivedbyname,
    a.amount,
    a.tds,
    a.recddate,
    a.paymentmode,
    g.name as paymentmodename,
    a.clientid,
    concat_ws(' ',e.firstname,NULLIF(e.middlename,''),e.lastname) as clientname,
    a.receiptdesc,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.serviceamount,
    a.reimbursementamount,
    a.entityid,
    b.name as entity,
    c.name as howreceived,
    a.howreceivedid,
    d.name as office,
    a.officeid
FROM
    client_receipt a
LEFT JOIN 
    entity b ON a.entityid = b.id
LEFT JOIN 
    howreceived c ON a.howreceivedid = c.id
LEFT JOIN 
    office d ON a.officeid = d.id
LEFT JOIN
    client e ON a.clientid = e.id
LEFT JOIN
    usertable f ON a.receivedby = f.id
LEFT JOIN
    mode_of_payment g ON a.paymentmode = g.id;

CREATE OR REPLACE FUNCTION delete_from_get_client_receipt_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM client_receipt WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_trigger_for_get_client_receipt_view
INSTEAD OF DELETE ON get_client_receipt_view
FOR EACH ROW
EXECUTE FUNCTION delete_from_get_client_receipt_view();

CREATE SEQUENCE IF NOT EXISTS client_receipt_id_seq OWNED BY client_receipt.id;
SELECT setval('client_receipt_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_receipt;
ALTER TABLE client_receipt ALTER COLUMN id SET DEFAULT nextval('client_receipt_id_seq');

ALTER TABLE client_receipt ALTER COLUMN recddate set type date;

CREATE SEQUENCE IF NOT EXISTS client_property_caretaking_agreement_id_seq OWNED BY client_property_caretaking_agreement.id;
SELECT setval('client_property_caretaking_agreement_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_caretaking_agreement;
ALTER TABLE client_property_caretaking_agreement ALTER COLUMN id SET DEFAULT nextval('client_property_caretaking_agreement_id_seq');



CREATE VIEW get_client_property_pma_view AS
SELECT DISTINCT
    a.id,
    a.clientpropertyid,
    concat_ws('-',d.project,d.suburb) as propertydescription,
    d.propertystatus,
    d.status as propertystatusname,
    d.client as clientname,
    d.clientid,
    d.status,
    a.startdate,
    a.enddate,
    a.actualenddate,
    a.active,
    a.scancopy,
    a.reasonforearlyterminationifapplicable,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.description,
    a.rented,
    a.fixed,
    a.rentedtax,
    a.fixedtax,
    a.orderid,
    b.briefdescription as orderdescription,
    a.poastartdate,
    a.poaenddate,
    a.poaholder
FROM
    client_property_caretaking_agreement a
LEFT JOIN
    orders b ON a.orderid = b.id
LEFT JOIN
    get_client_property_view d ON a.clientpropertyid = d.id;


CREATE OR REPLACE FUNCTION get_client_property_pma_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM client_property_caretaking_agreement WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER get_client_property_pma_view
INSTEAD OF DELETE ON get_client_property_pma_view
FOR EACH ROW
EXECUTE FUNCTION get_client_property_pma_view();

CREATE VIEW get_client_property_lla_view AS
SELECT DISTINCT
    a.id,
    a.clientpropertyid,
    d.client as clientname,
    d.clientid,
    concat_ws('-',d.project,d.suburb) as propertydescription,
    d.propertystatus,
    d.status as propertystatusname,
    a.orderid,
    b.briefdescription as orderdescription,
    a.startdate,
    a.actualenddate,
    a.durationinmonth,
    a.depositamount,
    a.rentamount,
    a.registrationtype,
    a.rentpaymentdate,
    a.noticeperiodindays,
    a.active,
    a.llscancopy,
    a.dated,
    a.createdby,
    a.isdeleted
FROM 
    client_property_leave_license_details a
LEFT JOIN
    orders b ON a.orderid = b.id
LEFT JOIN
    get_client_property_view d ON a.clientpropertyid = d.id;

CREATE SEQUENCE IF NOT EXISTS client_property_leave_license_details_id_seq OWNED BY client_property_leave_license_details.id;
SELECT setval('client_property_leave_license_details_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_leave_license_details;
ALTER TABLE client_property_leave_license_details ALTER COLUMN id SET DEFAULT nextval('client_property_leave_license_details_id_seq');

CREATE OR REPLACE FUNCTION get_client_property_lla_view() RETURNS TRIGGER AS $$
BEGIN
    -- Perform delete operation on the underlying table(s)
    DELETE FROM client_property_leave_license_details WHERE id = OLD.id;
    -- You might need additional delete operations if data is spread across multiple tables
    -- If so, add DELETE statements for those tables here.
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER get_client_property_lla_view
INSTEAD OF DELETE ON get_client_property_lla_view
FOR EACH ROW
EXECUTE FUNCTION get_client_property_lla_view();

CREATE SEQUENCE IF NOT EXISTS order_status_change_id_seq OWNED BY order_status_change.id;
SELECT setval('order_status_change_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_status_change;
ALTER TABLE order_status_change ALTER COLUMN id SET DEFAULT nextval('order_status_change_id_seq');

CREATE TABLE order_photos (
    id int,
    orderid int,
    photolink text,
    description text,
    phototakenwhen timestamp,
    dated timestamp,
    createdby int,
    isdeleted boolean
);

CREATE SEQUENCE IF NOT EXISTS order_photos_id_seq OWNED BY order_photos.id;
SELECT setval('order_photos_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_photos;
ALTER TABLE order_photos ALTER COLUMN id SET DEFAULT nextval('order_photos_id_seq');

ALTER TABLE order_invoice ALTER COLUMN invoicedate type date;

CREATE VIEW get_orders_invoice_view AS
SELECT DISTINCT
    a.id,
    a.clientid,
    concat_ws(' ',b.firstname,NULLIF(b.middlename,''),b.lastname) as clientname,
    a.orderid,
    d.briefdescription as ordername,
    a.estimatedate,
    a.estimateamount,
    a.invoicedate,
    a.invoiceamount,
    a.quotedescription,
    a.createdon,
    a.baseamount,
    a.tax,
    a.entityid,
    c.name as entityname,
    a.dated,
    a.createdby,
    concat_ws(' ',e.firstname,e.lastname) as createdbyname
FROM
    order_invoice a
LEFT JOIN
    client b ON a.clientid = b.id
LEFT JOIN
    entity c ON a.entityid = c.id
LEFT JOIN
    orders d ON a.orderid = d.id
LEFT JOIN
    usertable e ON a.createdby = e.id;

 alter table order_receipt alter column recddate type date;

 CREATE VIEW get_orders_receipt_view AS
 SELECT DISTINCT
    a.id,
    a.receivedby,
    concat_ws(' ',b.firstname,b.lastname) as receivedbyname,
    a.amount,
    a.tds,
    a.recddate,
    a.paymentmode,
    c.name as paymentmodename,
    a.orderid,
    i.clientid,
    concat_ws(' ',j.firstname,NULLIF(j.middlename,''),j.lastname) as clientname,
    i.clientpropertyid,
    concat_ws(' ',k.suburb,k.propertydescription) as clientproperty,
    d.briefdescription,
    a.receiptdesc,
    a.dated,
    a.createdby,
    concat_ws(' ',h.firstname,h.lastname) as createdbyname,
    a.isdeleted,
    a.createdon,
    a.entityid,
    f.name as entity,
    a.officeid,
    g.name as office
FROM
    order_receipt a
LEFT JOIN
    usertable b ON a.receivedby = b.id
LEFT JOIN
    mode_of_payment c ON a.paymentmode = c.id
LEFT JOIN
    orders d ON a.orderid = d.id
LEFT JOIN
    entity f ON a.entityid = f.id
LEFT JOIN
    office g ON a.officeid = g.id
LEFT JOIN
    usertable h ON a.createdby = h.id
LEFT JOIN
    orders i ON a.orderid = i.id
LEFT JOIN
    client j ON i.clientid = j.id
LEFT JOIN
    client_property k ON i.clientpropertyid = k.id;

CREATE SEQUENCE IF NOT EXISTS order_receipt_id_seq OWNED BY order_receipt.id;
SELECT setval('order_receipt_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_receipt;
ALTER TABLE order_receipt ALTER COLUMN id SET DEFAULT nextval('order_receipt_id_seq');

CREATE VIEW get_vendor_view AS
SELECT DISTINCT
    a.id,
    a.vendorname,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city as cityid,
    b.city AS city,
    a.state,
    a.country as countryid,
    c.name AS country,
    a.type,
    a.details,
    a.category AS categoryid,
    e.name AS category, -- Using table e for vendor_Category
    a.phone1,
    a.email,
    a.ownerinfo,
    a.panno,
    a.tanno,
    a.vattinno,
    a.gstservicetaxno,
    a.lbtno,
    a.tdssection,
    a.bankname,
    a.bankbranch,
    a.bankcity,
    a.bankacctholdername,
    a.bankacctno,
    a.bankifsccode,
    a.bankaccttype,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.companydeductee,
    a.tallyledgerid,
    d.tallyledger
FROM vendor a
LEFT JOIN cities b ON a.city = b.id
LEFT JOIN country c ON a.country = c.id
LEFT JOIN tallyledger d ON a.tallyledgerid = d.id
LEFT JOIN vendor_category e ON a.category = e.id; -- Joining with vendor_Category table using alias e

CREATE SEQUENCE IF NOT EXISTS vendor_id_seq OWNED BY vendor.id;
SELECT setval('vendor_id_seq', COALESCE(max(id), 0) + 1, false) FROM vendor;
ALTER TABLE vendor ALTER COLUMN id SET DEFAULT nextval('vendor_id_seq');

CREATE SEQUENCE IF NOT EXISTS order_vendorestimate_id_seq OWNED BY order_vendorestimate.id;
SELECT setval('order_vendorestimate_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_vendorestimate;
ALTER TABLE order_vendorestimate ALTER COLUMN id SET DEFAULT nextval('order_vendorestimate_id_seq');

alter table order_vendorestimate alter column invoicedate type date;
alter table order_vendorestimate alter column estimatedate type date;

CREATE VIEW get_vendor_invoice_view AS
SELECT DISTINCT
    a.id,
    a.estimatedate,
    a.amount,
    a.estimatedesc,
    a.orderid,
    b.briefdescription,
    b.clientid,
    concat_ws(' ',f.firstname,NULLIF(f.middlename,''),f.lastname) as clientname,
    a.vendorid,
    c.vendorname,
    a.invoicedate,
    a.invoiceamount,
    a.dated,
    a.createdby,
    concat_ws(' ',g.firstname,g.lastname) as createdbyname,
    a.isdeleted,
    a.createdon,
    a.notes,
    a.vat1,
    a.vat2,
    a.servicetax,
    a.invoicenumber,
    a.entityid,
    d.name as entity,
    a.officeid,
    e.name as office
FROM
    order_vendorestimate a
LEFT JOIN
    orders b ON a.orderid = b.id
LEFT JOIN
    vendor c ON a.vendorid = c.id
LEFT JOIN
    entity d ON a.entityid = d.id
LEFT JOIN
    office e ON a.officeid = e.id
LEFT JOIN
    client f ON b.clientid = f.id
LEFT JOIN
    usertable g ON a.createdby = g.id;

alter table project_amenities add column "4BHK" bool;
alter table project_amenities add column other bool;
alter table project_amenities add column "RK" bool;
alter table project_amenities add column other bool;
alter table project_amenities add column duplex bool;

alter table order_payment alter column paymentdate type date;

CREATE VIEW get_vendor_payment_view AS
SELECT DISTINCT
    a.id,
    a.paymentby,
    concat_ws(' ',b.firstname,b.lastname) as paymentbyname,
    a.amount,
    a.paymentdate,
    a.orderid,
    c.clientid,
    concat_ws(' ',i.firstname,NULLIF(i.middlename,''),i.lastname) as clientname,
    c.briefdescription,
    c.clientpropertyid,
    j.propertydescription,
    a.vendorid,
    d.vendorname,
    a.mode,
    e.name as modeofpayment,
    a.description,
    a.tds,
    a.servicetaxamount,
    a.dated,
    a.createdby,
    concat_ws(' ',f.firstname,f.lastname) as createdbyname,
    a.isdeleted,
    a.createdon,
    a.entityid,
    g.name as entity,
    a.officeid,
    h.name as office
FROM
    order_payment a
LEFT JOIN
    usertable b ON a.paymentby = b.id
LEFT JOIN
    orders c ON a.orderid = c.id
LEFT JOIN
    vendor d ON a.vendorid = d.id
LEFT JOIN
    mode_of_payment e ON a.mode = e.id
LEFT JOIN
    usertable f ON a.createdby = f.id
LEFT JOIN
    entity g ON a.entityid = g.id
LEFT JOIN
    office h ON a.officeid = h.id
LEFT JOIN
    client i ON c.clientid = i.id
LEFT JOIN
    client_property j ON c.clientpropertyid = j.id;

CREATE SEQUENCE IF NOT EXISTS order_payment_id_seq OWNED BY order_payment.id;
SELECT setval('order_payment_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_payment;
ALTER TABLE order_payment ALTER COLUMN id SET DEFAULT nextval('order_payment_id_seq');

delete from order_status where id=7;
update order_status set name='Closed (Work Done & Collection Completed)' where id=5;
update order_status set name='Work Done - Pending Collection' where id=8;

CREATE SEQUENCE IF NOT EXISTS clientleavelicensetenant_id_seq OWNED BY clientleavelicensetenant.id;
SELECT setval('clientleavelicensetenant_id_seq', COALESCE(max(id), 0) + 1, false) FROM clientleavelicensetenant;
ALTER TABLE clientleavelicensetenant ALTER COLUMN id SET DEFAULT nextval('clientleavelicensetenant_id_seq');

-- order payment list view

CREATE or REPLACE VIEW userview AS
SELECT
    u.ID AS UserId,
    u.UserName,
    u.RoleId,
    u.Password,
    u.OfficeId,
    u.LOBId,
    u.UserCode,
    u.FirstName,
    u.LastName,
    u.Status,
    CASE
        WHEN u.Status = 'true' THEN 'Active'
        ELSE 'Inactive'
    END AS UserStatus,
    u.FirstName || ' ' || u.LastName AS FullName,
    u.EMail2,
    u.EMail1,
    u.AddressLine1,
    u.AddressLine2,
    u.Suburb,
    u.State,
    u.Zip,
    u.Dated,
    u.CreatedBy AS CreatedById,
    u.IsDeleted,
    created_user.FirstName || ' ' || created_user.LastName AS CreatedBy,
    u.EffectiveDate,
    u.Homephone,
    u.Workphone,
    u.City,
    u.Country,
    r.role_name AS RoleName,
    u.EntityId
FROM
    usertable u
    INNER JOIN usertable created_user ON u.CreatedBy = created_user.ID
    LEFT JOIN Roles r ON u.RoleId = r.ID
WHERE
    u.IsDeleted = 'false' or u.isdeleted=null;






CREATE or replace VIEW clientview AS
SELECT
    Client.ID,
    Client.FirstName,
    Client.MiddleName,
    Client.LastName,
    Client.FirstName || ' ' || Client.LastName AS FullName,
    Client.Salutation,
    Client.ClientType,
    Client.AddressLine1,
    Client.AddressLine2,
    Client.Suburb,
    Client.City,
    Client.State,
    Client.Country,
    Client.Zip,
    Client.HomePhone,
    Client.WorkPhone,
    Client.MobilePhone,
    Client.EMail1,
    Client.EMail2,
    Client.EmployerName,
    Client.Comments,
    Client.Photo,
    Client.OnlineACCreated,
    Client.LocalContact1Name,
    Client.LocalContact1Address,
    Client.LocalContact1Details,
    Client.LocalContact2Name,
    Client.LocalContact2Address,
    Client.LocalContact2Details,
    Client.Dated,
    Client.CreatedBy AS CreatedById,
    Client.IsDeleted,
    usertable.UserName,
    usertable.FirstName || ' ' || usertable.LastName AS CreatedBy,
    Client_Type.Name AS ClientTypeName,
    Country.Name AS CountryName,
    Client.IncludeInMailingList,
    Client.EntityId,
    Tenant.FirstName || ' ' || Tenant.LastName AS Tenantof,
    Client.Tenantof AS TenantofId
FROM
    Client
    INNER JOIN usertable ON Client.CreatedBy = usertable.ID
    INNER JOIN Client_Type ON Client.ClientType = Client_Type.ID
    INNER JOIN Country ON Client.Country = Country.ID
    LEFT OUTER JOIN Client AS Tenant ON Client.Tenantof = Tenant.ID
WHERE
    Client.IsDeleted = 'false'  or client.isdeleted=null;




CREATE or replace VIEW propertiesview AS
SELECT
    Client_Property.ClientID,
    Client_Property.ProjectID,
    Client_Property.PropertyDescription,
    Client_Property.PropertyType,
    Client_Property.LayoutDetails,
    Client_Property.NumberOfParkings,
    Client_Property.InternalFurnitureAndFittings,
    Client_Property.LevelOfFurnishing,
    Client_Property.Status,
    Client_Property.InitialPossessionDate,
    Client_Property.POAGiven,
    Client_Property.POAID,
    Client_Property.ElectricityConsumerNumber,
    Client_Property.ElectricityBillingUnit,
    Client_Property.OtherElectricityDetails,
    Client_Property.GasConnectionDetails,
    Client_Property.PropertyTaxNumber,
    Client_Property.ClientServiceManager,
    Client_Property.PropertyManager,
    Client_Property.Comments,
    Client_Property.PropertyOwnedByClientOnly,
    Client_Property.TextForPosting,
    Client_Property.Dated,
    Client_Property.CreatedBy AS CreatedById,
    Property_Status.Name AS Property_Status,
    Property_Type.Name AS Property_Type,
    usertable.FirstName || ' ' || usertable.LastName AS CreatedBy,
    Level_Of_furnishing.Name AS Level_Of_furnishing,
    Client.FirstName || ' ' || Client.LastName AS ClientName,
    Client_Property.ID,
    Client_Property.Suburb,
    Client_Property.City,
    Client_Property.State,
    Client_Property.Country AS CountryId,
    Country.Name AS Country,
    Client_Property.ID AS PropertyID,
    Project.ProjectName,
    Client_Property.ElectricityBillingDueDate
FROM
    Client_Property
    INNER JOIN Property_Type ON Client_Property.PropertyType = Property_Type.ID
    INNER JOIN Property_Status ON Client_Property.Status = Property_Status.ID
    INNER JOIN usertable ON Client_Property.CreatedBy = usertable.ID
    INNER JOIN Level_Of_furnishing ON Client_Property.LevelOfFurnishing = Level_Of_furnishing.ID
    INNER JOIN Client ON Client_Property.ClientID = Client.ID
    INNER JOIN Project ON Client_Property.ProjectID = Project.ID
    LEFT OUTER JOIN Country ON Client_Property.Country = Country.ID
WHERE
    Client_Property.IsDeleted = 'false' or client_property.isdeleted=null
ORDER BY
    Client.FirstName || ' ' || Client.LastName;




CREATE or replace VIEW ordersview AS
SELECT
    orders.BriefDescription,
    orders.EarliestStartDate,
    orders.ExpectedCompletionDate,
    orders.ActualCompletionDate AS ActualCompletionDate,
    orders.Owner,
    orders.Comments,
    orders.Status,
    orders.additionalcomments,
    orders.Service AS ServiceId,
    orders.ClientPropertyID,
    orders.VendorID,
    orders.AssignedToOffice AS AssignedToOfficeId,
    orders.Billable,
    orders.Dated,
    orders.CreatedBy AS CreatedById,
    orders.IsDeleted,
    Order_Status.Name AS OrderStatus,
    Services.Service,
    Office.Name AS AssignedToOffice,
    Vendor.VendorName,
    usertable.FirstName || ' ' || usertable.LastName AS CreatedBy,
    orders.ID,
    CASE
        WHEN EXTRACT(DAY FROM AGE(Orders.StatusUpdatedTimeStamp, CURRENT_DATE)) > 999 THEN -1
        ELSE EXTRACT(DAY FROM AGE(Orders.StatusUpdatedTimeStamp, CURRENT_DATE))
    END AS Ageing,
    userview.FullName AS OwnerName,
    orders.OrderDate,
    propertiesview.PropertyDescription,
    propertiesview.PropertyType AS PropertyTypeId,
    propertiesview.Status AS PropertyStatusId,
    propertiesview.Property_Status,
    propertiesview.Property_Type,
    propertiesview.Suburb,
    clientview.FullName AS ClientName,
    clientview.ClientTypeName,
    orders.ClientID,
    propertiesview.PropertyManager,
    propertiesview.ClientServiceManager,
    orders.Default_Task_Owner,
    LOB.Name AS LOBName,
    Services.ServiceType,
    orders.GLCode,
    orders.EntityId,
    Entity.Name AS EntityName,
    TallyLedger.TallyLedger,
    orders.TallyLedgerId,
    orders.StatusUpdatedTimeStamp,
    clientview.HomePhone,
    clientview.WorkPhone,
    clientview.MobilePhone,
    clientview.EMail1,
    clientview.EMail2
FROM
    usertable
    INNER JOIN orders ON usertable.ID = orders.CreatedBy
    INNER JOIN Order_Status ON Order_Status.ID = orders.Status
    INNER JOIN Services ON orders.Service = Services.ID
    INNER JOIN Office ON orders.AssignedToOffice = Office.ID
    LEFT OUTER JOIN Vendor ON orders.VendorID = Vendor.ID
    INNER JOIN userview ON orders.Owner = userview.UserId
    INNER JOIN clientview ON orders.ClientID = clientview.ID
    INNER JOIN LOB ON Services.LOB = LOB.ID
    LEFT OUTER JOIN TallyLedger ON orders.TallyLedgerId = TallyLedger.ID
    LEFT OUTER JOIN Entity ON orders.EntityId = Entity.ID
    LEFT OUTER JOIN propertiesview ON orders.ClientPropertyID = propertiesview.ID
WHERE
    Orders.IsDeleted = 'false' or orders.isdeleted = null;





CREATE OR REPLACE FUNCTION getFinancialYear(date_input TIMESTAMP)
RETURNS VARCHAR(7) AS $$
DECLARE
    ret_val VARCHAR(7);
    month_val INTEGER;
    year_val INTEGER;
BEGIN
    month_val := EXTRACT(MONTH FROM date_input);
    year_val := EXTRACT(YEAR FROM date_input);

    -- Assuming that the financial year starts from April
    IF month_val > 3 THEN
        ret_val := year_val || '-' || LPAD((year_val + 1)::TEXT, 2, '0');
    ELSE
        ret_val := (year_val - 1) || '-' || LPAD(year_val::TEXT, 2, '0');
    END IF;

    RETURN ret_val;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION getMonthYear(date_input TIMESTAMP)
RETURNS VARCHAR(8) AS $$
DECLARE
    ret_val VARCHAR(8);
BEGIN
    ret_val := TO_CHAR(date_input, 'Mon-YYYY');
    RETURN ret_val;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE VIEW orderpaymentview AS
SELECT
  Order_Payment.ID,
  Order_Payment.PaymentBy AS PaymentById,
  Order_Payment.Amount,
  Order_Payment.PaymentDate,
  Order_Payment.OrderID,
  Order_Payment.VendorID,
  Order_Payment.Mode,
  Order_Payment.Description,
  Order_Payment.ServiceTaxAmount,
  Order_Payment.Dated,
  Order_Payment.CreatedBy AS CreatedById,
  Order_Payment.IsDeleted,
  Mode_Of_payment.Name AS Mode_Of_payment,
  User_1.FirstName || ' ' || User_1.LastName AS CreatedBy,
  usertable.FirstName || ' ' || usertable.LastName AS PaymentBy,
  ordersview.ClientName,
  ordersview.BriefDescription AS OrderDescription,
  Order_Payment.TDS,
  propertiesview.PropertyDescription,
  Vendor.VendorName,
  ordersview.LOBName,
  ordersview.ServiceType,
  ordersview.ServiceId,
  getMonthYear(Order_Payment.PaymentDate) AS MonthYear,
  getFinancialYear(Order_Payment.PaymentDate) AS FY,
  Order_Payment.EntityId,
  Entity.Name AS EntityName,
  Order_Payment.OfficeId,
  Office.Name AS OfficeName,
  ordersview.ClientID,
  ordersview.Service,
  ordersview.TallyLedger
FROM
  Order_Payment
  LEFT OUTER JOIN usertable ON Order_Payment.PaymentBy = usertable.ID
  LEFT OUTER JOIN Office ON Office.ID = Order_Payment.OfficeId
  LEFT OUTER JOIN Mode_Of_payment ON Order_Payment.Mode = Mode_Of_payment.ID
  INNER JOIN usertable AS User_1 ON Order_Payment.CreatedBy = User_1.ID
  INNER JOIN ordersview ON Order_Payment.OrderID = ordersview.ID
  LEFT OUTER JOIN propertiesview ON ordersview.ClientPropertyID = propertiesview.PropertyID
    AND ordersview.ClientID = propertiesview.ClientID
  INNER JOIN Vendor ON Order_Payment.VendorID = Vendor.ID
  LEFT OUTER JOIN Entity ON Order_Payment.EntityId = Entity.ID;

-- order payment list view


-- order receipt view


CREATE SEQUENCE payment_source_id_seq;

CREATE TABLE payment_source (
    id bigint NOT NULL DEFAULT nextval('payment_source_id_seq'::regclass),
    name text NOT NULL,
    CONSTRAINT idx_93250_pk_payment_source PRIMARY KEY (id)
);

ALTER SEQUENCE payment_source_id_seq OWNED BY payment_source.id;

INSERT INTO payment_source (id, name) VALUES
(1, 'Client'),
(2, 'Builder'),
(3, 'Society'),
(4, 'Tenant'),
(5, 'Broker'),
(6, 'Internal cash transfer'),
(7, 'Director'),
(8, 'Buyer');

CREATE VIEW orderreceiptview AS
SELECT
  Mode_Of_payment.Name AS "PaymentMode",
  usertable.FirstName || ' ' || usertable.LastName AS "ReceivedBy",
  User_1.FirstName || ' ' || User_1.LastName AS "Createdby",
  OrdersView.ClientName,
  OrdersView.BriefDescription AS "OrderDescription",
  Order_Receipt.ID,
  Order_Receipt.ReceivedBy AS "ReceivedById",
  Order_Receipt.Amount,
  Order_Receipt.RecdDate,
  Order_Receipt.PaymentMode AS "PaymentModeId",
  Order_Receipt.OrderID,
  Order_Receipt.ReceiptDesc,
  Order_Receipt.OfficeId,
  Office.Name AS "OfficeName",
  Order_Receipt.PaymentSource AS "PaymentSourceId",
  Order_Receipt.Dated,
  Order_Receipt.Createdby AS "CreatedbyId",
  Order_Receipt.IsDeleted,
  Payment_Source.Name AS "PaymentSource",
  Order_Receipt.TDS,
  PropertiesView.PropertyDescription,
  getMonthYear(Order_Receipt.RecdDate) AS "MonthYear",
  getFinancialYear(Order_Receipt.RecdDate) AS "FY",
  OrdersView.Service,
  OrdersView.LOBName,
  OrdersView.ServiceType,
  OrdersView.TallyLedger,
  OrdersView.TallyLedgerId,
  OrdersView.ServiceId,
  Order_Receipt.EntityId,
  Entity.Name AS "EntityName",
  OrdersView.ClientTypeName,
  OrdersView.ClientID
FROM
  Order_Receipt
  LEFT JOIN usertable ON Order_Receipt.ReceivedBy = usertable.ID
  LEFT JOIN Mode_Of_payment ON Order_Receipt.PaymentMode = Mode_Of_payment.ID
  INNER JOIN usertable AS User_1 ON Order_Receipt.Createdby = User_1.ID
  INNER JOIN OrdersView ON Order_Receipt.OrderID = OrdersView.ID
  LEFT JOIN Entity ON Order_Receipt.EntityId = Entity.ID
  LEFT JOIN PropertiesView ON OrdersView.ClientPropertyID = PropertiesView.ID
  LEFT JOIN Payment_Source ON Order_Receipt.PaymentSource = Payment_Source.ID
  LEFT JOIN Office ON Order_Receipt.OfficeId = Office.ID
WHERE
  Order_Receipt.IsDeleted = false;

-- order receipt view
