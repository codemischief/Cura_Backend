SET SEARCH_PATH = dbo;
CREATE EXTENSION tablefunc;

alter table "user" rename to usertable;
alter table "order" rename to orders;
alter table cocbusinessgroup rename to cocbusinessgrouptype;
alter table collegeoustypes rename to collegetypes;

alter table client_property drop CONSTRAINT fk_client_property_ref_user2;
alter table client_property drop CONSTRAINT fk_client_property_ref_user1;
alter table agencytype rename to departmenttype;
alter table professionals add column professionalid text;
alter table project_photos rename column phototakenwhen to date_taken;
alter table project_photos alter column date_taken type date;
alter table client_receipt rename column "Visible to client" to visibletoclient;
alter table collegetypes rename column collegeousid to id;
alter table research_employer add column notes text;
alter table research_prospect add column email1 text;
alter table research_prospect add column phoneno text;
alter table client_property_leave_license_details alter column startdate type date;
alter table client_property_leave_license_details alter column actualenddate type date;
alter table ref_contractual_payments alter column paidon type date;
alter table client_property_poa alter column poaeffectivedate type date;
alter table client_property_poa alter column poaenddate type date;
ALTER TABLE orders ALTER COLUMN orderdate TYPE date;
ALTER TABLE orders ALTER COLUMN earlieststartdate TYPE date;
ALTER TABLE orders ALTER COLUMN expectedcompletiondate TYPE date;
ALTER TABLE orders ALTER COLUMN actualcompletiondate TYPE date;
alter table project_contacts alter column effectivedate type date;
alter table project_contacts alter column tenureenddate type date;



ALTER TABLE client_property_owner DROP COLUMN owner1addressline1;
ALTER TABLE client_property_owner DROP COLUMN owner1addressline2;
ALTER TABLE client_property_owner DROP COLUMN owner1suburb;
ALTER TABLE client_property_owner DROP COLUMN owner1city;
ALTER TABLE client_property_owner DROP COLUMN owner1state;
ALTER TABLE client_property_owner DROP COLUMN owner1country;
ALTER TABLE client_property_owner DROP COLUMN owner1zip;
ALTER TABLE client_property_owner DROP COLUMN owner1occupation;
ALTER TABLE client_property_owner DROP COLUMN owner1employername;
ALTER TABLE client_property_owner DROP COLUMN owner1birthyear;
ALTER TABLE client_property_owner DROP COLUMN owner1relation;
ALTER TABLE client_property_owner DROP COLUMN owner1relationwith;
ALTER TABLE client_property_owner DROP COLUMN owner2addressline1;
ALTER TABLE client_property_owner DROP COLUMN owner2addressline2;
ALTER TABLE client_property_owner DROP COLUMN owner2suburb;
ALTER TABLE client_property_owner DROP COLUMN owner2city;
ALTER TABLE client_property_owner DROP COLUMN owner2state;
ALTER TABLE client_property_owner DROP COLUMN owner2country;
ALTER TABLE client_property_owner DROP COLUMN owner2zip;
ALTER TABLE client_property_owner DROP COLUMN owner2birthyr;
ALTER TABLE client_property_owner DROP COLUMN owner2occupation;
ALTER TABLE client_property_owner DROP COLUMN owner2employer;
ALTER TABLE client_property_owner DROP COLUMN owner2relation;
ALTER TABLE client_property_owner DROP COLUMN owner2relationwith;
ALTER TABLE client_property_owner DROP COLUMN otherownerdetails;

ALTER TABLE bankst ADD CONSTRAINT amount CHECK (amount >= 0);
ALTER TABLE client_property ADD CONSTRAINT numberofparkings CHECK (numberofparkings >= 0);
ALTER TABLE project ADD CONSTRAINT numberoffloors CHECK (numberoffloors >= 0);
ALTER TABLE project ADD CONSTRAINT numberofbuildings CHECK (numberofbuildings >= 0);
ALTER TABLE project ADD CONSTRAINT approxtotalunits CHECK (approxtotalunits >= 0);
ALTER TABLE order_invoice ADD CONSTRAINT invoiceamount CHECK (invoiceamount >= 0);
ALTER TABLE order_invoice ADD CONSTRAINT estimateamount CHECK (estimateamount >= 0);
ALTER TABLE order_invoice ADD CONSTRAINT baseamount CHECK (baseamount >= 0);
ALTER TABLE order_invoice ADD CONSTRAINT tax CHECK (tax >= 0);
ALTER TABLE client_receipt ADD CONSTRAINT serviceamount CHECK (serviceamount >= 0);
ALTER TABLE client_receipt ADD CONSTRAINT reimbursementamount CHECK (reimbursementamount >= 0);
ALTER TABLE client_receipt ADD CONSTRAINT tds CHECK (tds >= 0);
ALTER TABLE client_receipt ADD CONSTRAINT amount CHECK (amount >= 0);
ALTER TABLE order_receipt ADD CONSTRAINT amount CHECK (amount >= 0);
ALTER TABLE order_receipt ADD CONSTRAINT tds CHECK (tds >= 0);
ALTER TABLE order_vendorestimate ADD CONSTRAINT amount CHECK (amount >= 0);
ALTER TABLE order_vendorestimate ADD CONSTRAINT invoiceamount CHECK (invoiceamount >= 0);
ALTER TABLE order_vendorestimate ADD CONSTRAINT servicetax CHECK (servicetax >= 0);
ALTER TABLE order_vendorestimate ADD CONSTRAINT vat1 CHECK (vat1 >= 0);
ALTER TABLE order_payment ADD CONSTRAINT amount CHECK (amount >= 0);
ALTER TABLE order_payment ADD CONSTRAINT servicetaxamount CHECK (servicetaxamount >= 0);
ALTER TABLE order_payment ADD CONSTRAINT tds CHECK (tds >= 0);
ALTER TABLE client_property_caretaking_agreement ADD CONSTRAINT rented CHECK (rented >= 0);
ALTER TABLE client_property_caretaking_agreement ADD CONSTRAINT fixed CHECK (fixed >= 0);
ALTER TABLE client_property_leave_license_details ADD CONSTRAINT rentamount CHECK (rentamount >= 0);
ALTER TABLE client_property_leave_license_details ADD CONSTRAINT durationinmonth CHECK (durationinmonth >= 0);
ALTER TABLE client_property_leave_license_details ADD CONSTRAINT noticeperiodindays CHECK (noticeperiodindays >= 0);
ALTER TABLE client_property_leave_license_details ADD CONSTRAINT depositamount CHECK (depositamount >= 0);
ALTER TABLE ref_contractual_payments ADD CONSTRAINT amount CHECK (amount >= 0);


ALTER TABLE client_property_owner
ADD COLUMN owner1aadhaarno text;

ALTER TABLE client_property_owner
ADD COLUMN owner1pancollected boolean;

ALTER TABLE client_property_owner
ADD COLUMN owner1aadhaarcollected boolean;

ALTER TABLE client_property_owner
ADD COLUMN owner2aadhaarno text;

ALTER TABLE client_property_owner
ADD COLUMN owner2pancollected boolean;

ALTER TABLE client_property_owner
ADD COLUMN owner2aadhaarcollected boolean;

ALTER TABLE client_property_owner
ADD COLUMN owner3aadhaarno text;

ALTER TABLE client_property_owner
ADD COLUMN owner3pancollected boolean;

ALTER TABLE client_property_owner
ADD COLUMN owner3aadhaarcollected boolean;

ALTER TABLE client_property_owner
ADD COLUMN comments text;


CREATE SEQUENCE IF NOT EXISTS cities_id_seq OWNED BY cities.id;
SELECT setval('cities_id_seq', COALESCE(max(id), 0) + 1, false) FROM cities;
ALTER TABLE cities ALTER COLUMN id SET DEFAULT nextval('cities_id_seq');

CREATE SEQUENCE IF NOT EXISTS orders_id_seq OWNED BY orders.id;
SELECT setval('orders_id_seq', COALESCE(max(id), 0) + 1, false) FROM orders;
ALTER TABLE orders ALTER COLUMN id SET DEFAULT nextval('orders_id_seq');

CREATE SEQUENCE IF NOT EXISTS locality_id_seq OWNED BY locality.id;
SELECT setval('locality_id_seq', COALESCE(max(id), 0) + 1, false) FROM locality;
ALTER TABLE locality ALTER COLUMN id SET DEFAULT nextval('locality_id_seq');
-- alter table "user" rename to usertable;
-- alter table "order" rename to orders;
-- alter table cocbusinessgroup rename to cocbusinessgrouptype;
-- alter table collegeoustypes rename to collegetypes;
alter table collegeous rename to colleges;
alter table client add column tenantofproperty int;
alter table orders rename column description to additionalcomments;
CREATE TABLE roles_to_rules_map (
    id SERIAL NOT NULL,
    rule_id integer,
    role_id integer,
    PRIMARY KEY (id)
);
--Commands to restore table roles
-- CREATE TABLE roles_to_rules_map (
--     id INTEGER,
--     rule_id INTEGER,
--     role_id INTEGER
-- );

CREATE TABLE token_access_config (
    timedata INTEGER,
    type VARCHAR(20)
);



CREATE TABLE rules (
    id SERIAL NOT NULL,
    module character varying(255) NOT NULL,
    method character varying(255) NOT NULL,
    status boolean NOT NULL,
    PRIMARY KEY (id)
);


INSERT INTO collegetypes (name) VALUES ('College');
INSERT INTO collegetypes (name) VALUES ('Pre-Primary School');
INSERT INTO collegetypes (name) VALUES ('Day Care');
INSERT INTO collegetypes (name) VALUES ('High School');
INSERT INTO collegetypes (name) VALUES ('Primary School');


INSERT INTO rules (id, module, method, status) VALUES (25, 'BuilderInfo', 'addBuilderInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (26, 'BuilderInfo', 'getBuilderInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (27, 'BuilderInfo', 'editBuilder', true);
INSERT INTO rules (id, module, method, status) VALUES (28, 'BuilderInfo', 'deleteBuilder', true);
INSERT INTO rules (id, module, method, status) VALUES (29, 'Country', 'getCountries', true);
INSERT INTO rules (id, module, method, status) VALUES (30, 'Country', 'addCountry', true);
INSERT INTO rules (id, module, method, status) VALUES (31, 'Country', 'editCountry', true);
INSERT INTO rules (id, module, method, status) VALUES (32, 'Country', 'deleteCountry', true);
INSERT INTO rules (id, module, method, status) VALUES (33, 'ProjectInfo', 'getProjects', true);
INSERT INTO rules (id, module, method, status) VALUES (34, 'ProjectInfo', 'deleteProject', true);
INSERT INTO rules (id, module, method, status) VALUES (35, 'ProjectInfo', 'addProject', true);
INSERT INTO rules (id, module, method, status) VALUES (36, 'ProjectInfo', 'editProject', true);
INSERT INTO rules (id, module, method, status) VALUES (37, 'Locality', 'getLocality', true);
INSERT INTO rules (id, module, method, status) VALUES (38, 'Locality', 'addLocality', true);
INSERT INTO rules (id, module, method, status) VALUES (39, 'Locality', 'editLocality', true);
INSERT INTO rules (id, module, method, status) VALUES (40, 'Locality', 'deleteLocality', true);
INSERT INTO rules (id, module, method, status) VALUES (41, 'LOB', 'getLob', true);
INSERT INTO rules (id, module, method, status) VALUES (42, 'LOB', 'addLob', true);
INSERT INTO rules (id, module, method, status) VALUES (43, 'LOB', 'editLob', true);
INSERT INTO rules (id, module, method, status) VALUES (44, 'LOB', 'deleteLob', true);
INSERT INTO rules (id, module, method, status) VALUES (45, 'Service', 'getServices', true);
INSERT INTO rules (id, module, method, status) VALUES (46, 'Service', 'addService', true);
INSERT INTO rules (id, module, method, status) VALUES (47, 'Service', 'editService', true);
INSERT INTO rules (id, module, method, status) VALUES (48, 'Service', 'deleteService', true);
INSERT INTO rules (id, module, method, status) VALUES (49, 'User', 'getUserInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (50, 'User', 'addUser', true);
INSERT INTO rules (id, module, method, status) VALUES (51, 'User', 'editUser', true);
INSERT INTO rules (id, module, method, status) VALUES (52, 'User', 'deleteUser', true);
INSERT INTO rules (id, module, method, status) VALUES (53, 'Employee', 'getEmployee', true);
INSERT INTO rules (id, module, method, status) VALUES (54, 'Employee', 'addEmployee', true);
INSERT INTO rules (id, module, method, status) VALUES (55, 'Employee', 'editEmployee', true);
INSERT INTO rules (id, module, method, status) VALUES (56, 'Employee', 'deleteEmployee', true);
INSERT INTO rules (id, module, method, status) VALUES (57, 'ClientInfo', 'getClientInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (58, 'ClientInfo', 'addClientInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (59, 'ClientInfo', 'editClientInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (60, 'ClientInfo', 'deleteClientInfo', true);
INSERT INTO rules (id, module, method, status) VALUES (61, 'ClientProperty', 'getClientProperty', true);
INSERT INTO rules (id, module, method, status) VALUES (62, 'ClientProperty', 'addClientProperty', true);
INSERT INTO rules (id, module, method, status) VALUES (63, 'ClientProperty', 'editClientProperty', true);
INSERT INTO rules (id, module, method, status) VALUES (64, 'ClientProperty', 'deleteClientProperty', true);
INSERT INTO rules (id, module, method, status) VALUES (65, 'Vendor', 'getVendors', true);
INSERT INTO rules (id, module, method, status) VALUES (66, 'Vendor', 'addVendors', true);
INSERT INTO rules (id, module, method, status) VALUES (67, 'Vendor', 'editVendors', true);
INSERT INTO rules (id, module, method, status) VALUES (68, 'Vendor', 'deleteVendors', true);
INSERT INTO rules (id, module, method, status) VALUES (69, 'Order', 'getOrders', true);
INSERT INTO rules (id, module, method, status) VALUES (70, 'Order', 'addOrders', true);
INSERT INTO rules (id, module, method, status) VALUES (71, 'Order', 'editOrders', true);
INSERT INTO rules (id, module, method, status) VALUES (72, 'Order', 'deleteOrders', true);
INSERT INTO rules (id, module, method, status) VALUES (73, 'BankStatement', 'getbankst', true);
INSERT INTO rules (id, module, method, status) VALUES (74, 'BankStatement', 'addbankst', true);
INSERT INTO rules (id, module, method, status) VALUES (75, 'BankStatement', 'editbankst', true);
INSERT INTO rules (id, module, method, status) VALUES (76, 'BankStatement', 'deletebankst', true);
INSERT INTO rules (id, module, method, status) VALUES (82, 'ClientInvoice', 'getOrdersInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (83, 'ClientInvoice', 'addOrdersInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (84, 'ClientInvoice', 'editOrdersInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (85, 'ClientInvoice', 'deleteOrdersInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (86, 'VendorInvoice', 'getVendorInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (87, 'VendorInvoice', 'addVendorInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (88, 'VendorInvoice', 'editVendorInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (89, 'VendorInvoice', 'deleteVendorInvoice', true);
INSERT INTO rules (id, module, method, status) VALUES (90, 'ClientReceipt', 'getClientReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (91, 'ClientReceipt', 'editClientReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (92, 'ClientReceipt', 'deleteClientReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (93, 'ClientReceipt', 'addClientReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (94, 'OrderReceipt', 'getOrderReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (95, 'OrderReceipt', 'addOrderReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (96, 'OrderReceipt', 'editOrdersReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (97, 'OrderReceipt', 'deleteOrdersReceipt', true);
INSERT INTO rules (id, module, method, status) VALUES (98, 'VendorPayment', 'getVendorPayment', true);
INSERT INTO rules (id, module, method, status) VALUES (99, 'VendorPayment', 'addVendorPayment', true);
INSERT INTO rules (id, module, method, status) VALUES (100, 'VendorPayment', 'editVendorPayment', true);
INSERT INTO rules (id, module, method, status) VALUES (101, 'VendorPayment', 'deleteVendorPayment', true);
INSERT INTO rules (id, module, method, status) VALUES (102, 'PMAAgreement', 'getClientPMAAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (103, 'PMAAgreement', 'addClientPMAAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (104, 'PMAAgreement', 'editClientPMAAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (105, 'PMAAgreement', 'deleteClientPMAAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (106, 'LLAgreement', 'getClientLLAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (107, 'LLAgreement', 'addClientLLAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (108, 'LLAgreement', 'editClientLLAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (109, 'LLAgreement', 'deleteClientLLAgreement', true);
INSERT INTO rules (id, module, method, status) VALUES (110, 'PMABilling', 'getPMABilling', true);
INSERT INTO rules (id, module, method, status) VALUES (111, 'PMABilling', 'addPMABilling', true);
INSERT INTO rules (id, module, method, status) VALUES (112, 'City', 'getCities', true);
INSERT INTO rules (id, module, method, status) VALUES (113, 'City', 'addCities', true);
INSERT INTO rules (id, module, method, status) VALUES (114, 'City', 'editCities', true);
INSERT INTO rules (id, module, method, status) VALUES (115, 'City', 'deleteCities', true);
INSERT INTO rules (id, module, method, status) VALUES (116, 'ResearchProspect', 'getResearchProspect', true);
INSERT INTO rules (id, module, method, status) VALUES (117, 'ResearchProspect', 'addResearchProspect', true);
INSERT INTO rules (id, module, method, status) VALUES (118, 'ResearchProspect', 'editResearchProspect', true);
INSERT INTO rules (id, module, method, status) VALUES (119, 'ResearchProspect', 'deleteResearchProspect', true);
INSERT INTO rules (id, module, method, status) VALUES (120, 'ResearchEmployer', 'getResearchEmployer', true);
INSERT INTO rules (id, module, method, status) VALUES (121, 'ResearchEmployer', 'addResearchEmployer', true);
INSERT INTO rules (id, module, method, status) VALUES (122, 'ResearchEmployer', 'editResearchEmployer', true);
INSERT INTO rules (id, module, method, status) VALUES (123, 'ResearchEmployer', 'deleteResearchEmployer', true);
INSERT INTO rules (id, module, method, status) VALUES (124, 'ResearchGovtAgencies', 'getResearchGovtAgencies', true);
INSERT INTO rules (id, module, method, status) VALUES (125, 'ResearchGovtAgencies', 'addResearchGovtAgencies', true);
INSERT INTO rules (id, module, method, status) VALUES (126, 'ResearchGovtAgencies', 'editResearchGovtAgencies', true);
INSERT INTO rules (id, module, method, status) VALUES (127, 'ResearchGovtAgencies', 'deleteResearchGovtAgencies', true);
INSERT INTO rules (id, module, method, status) VALUES (128, 'ResearchRealEstateAgents', 'getResearchAgents', true);
INSERT INTO rules (id, module, method, status) VALUES (129, 'ResearchRealEstateAgents', 'addResearchAgents', true);
INSERT INTO rules (id, module, method, status) VALUES (130, 'ResearchRealEstateAgents', 'editResearchAgents', true);
INSERT INTO rules (id, module, method, status) VALUES (131, 'ResearchRealEstateAgents', 'deleteResearchAgents', true);
INSERT INTO rules (id, module, method, status) VALUES (132, 'ResearchOwners', 'getResearchOwners', true);
INSERT INTO rules (id, module, method, status) VALUES (133, 'ResearchOwners', 'addResearchOwners', true);
INSERT INTO rules (id, module, method, status) VALUES (134, 'ResearchOwners', 'editResearchOwners', true);
INSERT INTO rules (id, module, method, status) VALUES (135, 'ResearchOwners', 'deleteResearchOwners', true);
INSERT INTO rules (id, module, method, status) VALUES (136, 'ResearchApartments', 'getResearchApartments', true);
INSERT INTO rules (id, module, method, status) VALUES (137, 'ResearchApartments', 'addResearchApartments', true);
INSERT INTO rules (id, module, method, status) VALUES (138, 'ResearchApartments', 'editResearchApartments', true);
INSERT INTO rules (id, module, method, status) VALUES (139, 'ResearchApartments', 'deleteResearchApartments', true);
INSERT INTO rules (id, module, method, status) VALUES (140, 'ResearchFriends', 'getResearchFriends', true);
INSERT INTO rules (id, module, method, status) VALUES (141, 'ResearchFriends', 'addResearchFriends', true);
INSERT INTO rules (id, module, method, status) VALUES (142, 'ResearchFriends', 'editResearchFriends', true);
INSERT INTO rules (id, module, method, status) VALUES (143, 'ResearchFriends', 'deleteResearchFriends', true);
INSERT INTO rules (id, module, method, status) VALUES (144, 'ResearchBanksAndBranches', 'getResearchBanksAndBranches', true);
INSERT INTO rules (id, module, method, status) VALUES (145, 'ResearchBanksAndBranches', 'addResearchBanksAndBranches', true);
INSERT INTO rules (id, module, method, status) VALUES (146, 'ResearchBanksAndBranches', 'editResearchBanksAndBranches', true);
INSERT INTO rules (id, module, method, status) VALUES (147, 'ResearchBanksAndBranches', 'deleteResearchBanksAndBranches', true);
INSERT INTO rules (id, module, method, status) VALUES (148, 'ResearchCOCAndBusinessGroup', 'getResearchCOCAndBusinessGroup', true);
INSERT INTO rules (id, module, method, status) VALUES (79, 'Payment', 'addPayment', true);
INSERT INTO rules (id, module, method, status) VALUES (80, 'Payment', 'editPayment', true);
INSERT INTO rules (id, module, method, status) VALUES (81, 'Payment', 'deletePayment', true);
INSERT INTO rules (id, module, method, status) VALUES (149, 'ResearchCOCAndBusinessGroup', 'addResearchCOCAndBusinessGroup', true);
INSERT INTO rules (id, module, method, status) VALUES (150, 'ResearchCOCAndBusinessGroup', 'editResearchCOCAndBusinessGroup', true);
INSERT INTO rules (id, module, method, status) VALUES (151, 'ResearchCOCAndBusinessGroup', 'deleteResearchCOCAndBusinessGroup', true);
INSERT INTO rules (id, module, method, status) VALUES (152, 'ResearchProfessional', 'getResearchProfessional', true);
INSERT INTO rules (id, module, method, status) VALUES (153, 'ResearchProfessional', 'addResearchProfessional', true);
INSERT INTO rules (id, module, method, status) VALUES (154, 'ResearchProfessional', 'editResearchProfessional', true);
INSERT INTO rules (id, module, method, status) VALUES (155, 'ResearchProfessional', 'deleteResearchProfessional', true);
INSERT INTO rules (id, module, method, status) VALUES (156, 'ResearchMandals', 'getResearchMandals', true);
INSERT INTO rules (id, module, method, status) VALUES (157, 'ResearchMandals', 'addResearchMandals', true);
INSERT INTO rules (id, module, method, status) VALUES (158, 'ResearchMandals', 'editResearchMandals', true);
INSERT INTO rules (id, module, method, status) VALUES (159, 'ResearchMandals', 'deleteResearchMandals', true);
INSERT INTO rules (id, module, method, status) VALUES (160, 'ResearchArchitect', 'getResearchArchitect', true);
INSERT INTO rules (id, module, method, status) VALUES (161, 'ResearchArchitect', 'addResearchArchitect', true);
INSERT INTO rules (id, module, method, status) VALUES (162, 'ResearchArchitect', 'editResearchArchitect', true);
INSERT INTO rules (id, module, method, status) VALUES (163, 'ResearchArchitect', 'deleteResearchArchitect', true);
INSERT INTO rules (id, module, method, status) VALUES (164, 'ResearchColleges', 'getResearchColleges', true);
INSERT INTO rules (id, module, method, status) VALUES (165, 'ResearchColleges', 'addResearchColleges', true);
INSERT INTO rules (id, module, method, status) VALUES (166, 'ResearchColleges', 'editResearchColleges', true);
INSERT INTO rules (id, module, method, status) VALUES (167, 'ResearchColleges', 'deleteResearchColleges', true);
INSERT INTO rules (id, module, method, status) VALUES (171, 'getLobEntityPayments', 'getLobEntityPayments', true);
INSERT INTO rules (id, module, method, status) VALUES (170, 'LOBReceiptPayments', 'getLobServicePayments', true);
INSERT INTO rules (id, module, method, status) VALUES (168, 'EntityReceiptPayments', 'getLobServicePaymentsConsolidated', true);
INSERT INTO rules (id, module, method, status) VALUES (173, 'deletebyid', 'delete', true);
INSERT INTO rules (id, module, method, status) VALUES (172, 'deletebyid', 'get', true);
INSERT INTO rules (id, module, method, status) VALUES (174, 'ClientStatement', 'getClientStatement', true);
INSERT INTO rules (id, module, method, status) VALUES (175, 'ClientStatement', 'addClientStatement', true);
INSERT INTO rules (id, module, method, status) VALUES (78, 'Payment', 'getPayments', true);
INSERT INTO rules (id, module, method, status) VALUES (179, 'editCompanyKey', 'editBuilderContact', true);
INSERT INTO rules (id, module, method, status) VALUES (178, 'BuilderContact', 'deleteBuilderContact', true);
INSERT INTO rules (id, module, method, status) VALUES (177, 'BuilderContact', 'getBuilderContactsById', true);
INSERT INTO rules (id, module, method, status) VALUES (176, 'BuilderContact', 'addNewBuilderContact', true);
INSERT INTO rules (id, module, method, status) VALUES (180, 'companykey', 'editCompanyKey', true);
INSERT INTO rules (id, module, method, status) VALUES (181, 'companykey', 'getCompanyKey', true);
INSERT INTO rules (id, module, method, status) VALUES (182, 'BuilderContact', 'getBuilderContact', true);
INSERT INTO rules (id, module, method, status) VALUES (183, 'BuilderContact', 'addBuilderContact', true);
INSERT INTO rules (id, module, method, status) VALUES (184, 'BuilderContact', 'editBuilderContact', true);
INSERT INTO rules (id, module, method, status) VALUES (185, 'BuilderContact', 'deleteBuilderContact', true);




INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (1, 25, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (2, 26, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (3, 27, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (4, 28, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (5, 25, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (6, 26, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (7, 27, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (8, 25, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (9, 26, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (10, 27, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (11, 25, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (12, 26, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (13, 27, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (14, 26, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (15, 29, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (16, 30, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (17, 31, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (18, 32, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (19, 33, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (20, 34, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (21, 35, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (22, 36, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (24, 35, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (25, 36, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (26, 33, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (27, 35, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (28, 36, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (23, 33, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (29, 33, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (30, 35, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (31, 36, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (32, 33, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (33, 37, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (34, 38, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (35, 39, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (36, 40, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (37, 41, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (38, 42, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (39, 43, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (40, 44, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (41, 45, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (42, 46, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (43, 47, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (44, 48, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (45, 49, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (46, 50, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (47, 51, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (48, 52, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (49, 53, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (50, 54, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (52, 56, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (51, 55, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (53, 57, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (54, 58, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (55, 59, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (56, 60, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (57, 57, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (58, 58, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (59, 59, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (60, 57, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (61, 58, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (62, 59, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (63, 57, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (64, 58, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (65, 59, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (66, 57, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (67, 61, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (68, 62, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (69, 63, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (70, 64, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (71, 61, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (72, 62, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (73, 63, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (74, 61, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (75, 62, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (76, 63, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (78, 61, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (79, 62, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (80, 64, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (81, 61, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (82, 65, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (83, 66, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (84, 67, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (85, 68, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (86, 65, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (87, 66, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (88, 67, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (89, 65, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (90, 66, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (91, 67, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (93, 65, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (94, 69, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (95, 70, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (96, 71, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (97, 72, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (98, 69, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (99, 70, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (100, 71, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (101, 69, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (102, 70, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (103, 71, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (104, 69, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (105, 70, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (106, 71, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (107, 69, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (108, 73, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (109, 74, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (110, 75, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (111, 76, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (112, 73, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (113, 74, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (114, 75, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (115, 73, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (116, 74, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (117, 75, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (118, 73, 4);
-- INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (119, 74, 4);
-- INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (120, 75, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (121, 73, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (122, 78, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (123, 79, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (124, 80, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (125, 81, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (136, 82, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (137, 83, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (138, 84, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (139, 85, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (140, 82, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (141, 83, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (142, 84, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (143, 82, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (144, 83, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (145, 84, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (146, 82, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (147, 83, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (148, 84, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (149, 82, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (150, 86, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (151, 87, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (152, 88, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (153, 89, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (154, 86, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (155, 87, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (156, 88, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (157, 86, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (158, 87, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (159, 88, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (160, 86, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (161, 87, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (162, 88, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (163, 86, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (164, 90, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (165, 93, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (166, 91, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (167, 92, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (168, 90, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (169, 93, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (170, 91, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (171, 90, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (172, 93, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (173, 91, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (174, 90, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (175, 93, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (176, 91, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (177, 90, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (178, 94, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (179, 95, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (180, 96, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (181, 97, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (182, 94, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (183, 95, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (184, 96, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (185, 94, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (186, 95, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (187, 96, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (188, 94, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (189, 95, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (190, 96, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (191, 94, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (192, 98, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (193, 99, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (194, 100, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (195, 101, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (196, 98, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (197, 99, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (198, 100, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (199, 98, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (200, 99, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (201, 100, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (202, 98, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (203, 99, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (204, 100, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (205, 98, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (206, 102, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (207, 103, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (208, 104, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (209, 105, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (210, 102, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (211, 102, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (212, 103, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (213, 104, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (214, 102, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (215, 102, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (216, 106, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (217, 107, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (219, 109, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (220, 106, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (221, 107, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (218, 108, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (222, 108, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (223, 106, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (224, 107, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (225, 108, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (226, 106, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (227, 107, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (228, 108, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (229, 106, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (230, 110, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (231, 111, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (232, 110, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (233, 110, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (234, 110, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (235, 110, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (236, 111, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (237, 112, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (238, 113, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (239, 114, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (240, 115, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (241, 116, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (242, 117, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (243, 118, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (244, 119, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (245, 116, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (246, 117, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (247, 118, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (248, 119, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (249, 116, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (250, 117, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (251, 118, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (252, 116, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (253, 117, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (254, 118, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (255, 116, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (256, 120, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (257, 121, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (258, 122, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (259, 123, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (260, 120, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (261, 121, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (262, 122, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (263, 123, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (264, 120, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (265, 121, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (266, 122, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (267, 120, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (268, 121, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (269, 122, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (270, 120, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (271, 124, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (272, 125, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (273, 126, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (274, 127, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (275, 124, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (276, 125, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (277, 126, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (278, 127, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (279, 124, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (280, 125, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (281, 126, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (282, 124, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (283, 125, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (284, 126, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (285, 124, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (286, 128, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (287, 129, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (288, 130, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (289, 131, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (290, 128, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (291, 129, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (292, 130, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (293, 131, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (294, 128, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (295, 129, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (296, 130, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (297, 128, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (298, 129, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (299, 130, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (300, 128, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (301, 132, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (302, 133, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (303, 134, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (304, 135, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (305, 132, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (306, 133, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (307, 134, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (308, 135, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (309, 132, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (310, 133, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (311, 134, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (312, 132, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (313, 133, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (314, 134, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (315, 132, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (316, 136, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (317, 137, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (318, 138, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (319, 139, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (320, 136, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (321, 137, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (322, 138, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (323, 139, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (324, 136, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (325, 137, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (326, 138, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (327, 136, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (328, 137, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (329, 138, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (330, 136, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (331, 140, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (332, 141, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (333, 142, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (334, 143, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (335, 140, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (336, 141, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (337, 142, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (338, 143, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (339, 140, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (340, 141, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (341, 142, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (342, 140, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (343, 141, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (344, 142, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (345, 140, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (346, 144, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (347, 145, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (348, 146, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (349, 147, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (350, 144, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (351, 145, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (352, 146, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (353, 147, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (354, 144, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (355, 145, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (356, 146, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (357, 144, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (358, 145, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (359, 146, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (360, 144, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (361, 148, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (362, 149, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (363, 150, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (364, 151, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (365, 148, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (366, 149, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (367, 150, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (368, 151, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (369, 148, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (370, 149, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (371, 150, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (372, 148, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (373, 149, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (374, 150, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (375, 148, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (376, 152, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (377, 153, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (378, 154, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (379, 155, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (380, 152, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (381, 153, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (382, 154, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (383, 155, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (384, 152, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (385, 153, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (386, 154, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (387, 152, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (388, 153, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (389, 154, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (390, 152, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (391, 156, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (392, 157, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (393, 158, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (394, 159, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (395, 156, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (396, 157, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (397, 158, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (398, 159, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (399, 156, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (400, 157, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (401, 158, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (402, 156, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (403, 157, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (404, 158, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (405, 156, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (406, 160, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (407, 161, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (408, 162, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (409, 163, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (410, 160, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (411, 161, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (412, 162, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (413, 163, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (414, 160, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (415, 161, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (416, 162, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (417, 160, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (418, 161, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (419, 162, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (420, 160, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (421, 164, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (422, 165, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (423, 166, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (424, 167, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (425, 164, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (426, 165, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (427, 166, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (428, 167, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (429, 164, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (430, 165, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (431, 166, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (432, 164, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (433, 165, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (434, 166, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (435, 164, 5);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (436, 168, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (437, 170, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (438, 171, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (439, 172, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (440, 173, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (441, 174, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (442, 175, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (443, 65, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (444, 66, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (445, 67, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (446, 179, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (447, 180, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (448, 181, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (449, 182, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (450, 183, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (451, 184, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (452, 185, 1);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (453, 182, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (454, 183, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (455, 184, 2);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (456, 182, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (457, 183, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (458, 184, 3);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (459, 182, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (460, 183, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (461, 184, 4);
INSERT INTO roles_to_rules_map (id, rule_id, role_id) VALUES (462, 182, 5);

INSERT INTO token_access_config (timedata, type) VALUES
(900, 'Login'),
(900, 'IdleTimeOut');
-- (180, 'Refresh')

CREATE TABLE tokens (
    id SERIAL,
    token text,-- Create the roles table
    key text,
    refresh_token text,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,--timestamp of when token was made
    active bool,
    userid int
);

CREATE TABLE refresh_tokens (
    id SERIAL,
    refresh_token text,
    key text,
    userid int
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name TEXT NOT NULL,
    status BOOLEAN NOT NULL
);

-- Insert data into the roles table
INSERT INTO roles (id, role_name, status) VALUES
(1, 'Admin', TRUE),
(2, 'Accounts', TRUE),
(4, 'Analyst', TRUE),
(5, 'Guest', TRUE),
(3, 'Property_Manager', TRUE);


-- Create the table
-- CREATE TABLE order_status (
--     id INT,
--     name TEXT
-- );

-- -- Insert data into the table
-- INSERT INTO order_status (id, name) VALUES
-- (1, 'On hold'),
-- (2, 'Estimate Given'),
-- (4, 'Cancelled'),
-- (6, 'Billed'),
-- (9, 'In progress'),
-- (5, 'Closed (Work Done & Collection Completed)'),
-- (8, 'Work Done - Pending Collection');


ALTER TABLE client_property_caretaking_agreement
ALTER COLUMN startdate TYPE date;

ALTER TABLE client_property_caretaking_agreement
ALTER COLUMN poastartdate TYPE date;

ALTER TABLE client_property_caretaking_agreement
ALTER COLUMN actualenddate TYPE date;

ALTER TABLE client_property_caretaking_agreement
ALTER COLUMN enddate TYPE date;

ALTER TABLE client_property_caretaking_agreement
ALTER COLUMN poaenddate TYPE date;

ALTER TABLE client_property_caretaking_agreement
ALTER COLUMN societyduespaidtilldate TYPE date;

ALTER TABLE client_poa
ALTER COLUMN poaeffectivedate TYPE date;

ALTER TABLE client_poa
ALTER COLUMN poaenddate TYPE date;

ALTER TABLE client_property_photos
ALTER COLUMN phototakenwhen TYPE date;



alter table client_property alter column clientservicemanager type text;
alter table client_property alter column propertymanager type text;

alter table client_property add column indexiicollected boolean;


alter table client_property alter column initialpossessiondate type date;

alter table client_property add column website text;
alter table client_property add column email text;
ALTER TABLE client_property_caretaking_agreement RENAME COLUMN pmaholder TO poaholder;
ALTER TABLE client_receipt ALTER COLUMN recddate type date;

alter table order_photos rename COLUMN "desc" to description;
alter table order_receipt alter column recddate type date;

ALTER TABLE order_invoice ALTER COLUMN invoicedate type date;
 alter table vendor rename column servicetaxno to gstservicetaxno;

alter table order_vendorestimate alter column invoicedate type date;
alter table order_vendorestimate alter column estimatedate type date;


alter table order_vendorestimate alter column invoicedate type date;
alter table order_vendorestimate alter column estimatedate type date;


alter table order_vendorestimate alter column invoicedate type date;
alter table order_vendorestimate alter column estimatedate type date;

alter table project_amenities add column "4BHK" bool;
alter table project_amenities add column other bool;
alter table project_amenities add column "RK" bool;
alter table project_amenities add column other bool;
alter table project_amenities add column duplex bool;
alter table project_amenities add column penthouse bool;

alter table order_payment alter column paymentdate type date;

update order_status set name='Closed (Work Done & Collection Completed)' where id=5;
update order_status set name='Work Done - Pending Collection' where id=8;

alter table realestateagents rename column registered to rera_registration_number;

ALTER TABLE realestateagents ADD COLUMN registered bool;


alter table employee alter column dateofjoining type date;
alter table employee alter column lastdateofworking type date;
alter table employee alter column dob type date;
alter table research_government_agencies rename column agencytype to departmenttype;
alter table bankst add column isdeleted bool;
update bankst set isdeleted=false;
alter table client_property alter column propertymanager type text;
alter table bankst alter column date type date;
alter table bankst rename column "Cr/Dr" to crdr;
alter table banksandbranches add column branchaddress text;
alter table banksandbranches rename column contact to contactperson;
alter table banksandbranches add column notes text;
alter table bankst rename column "AvailableBalance(INR)" to availablebalance;

alter table bankst rename column receivedby to receivedhow;
alter table professionals rename column phoneno to professionid;

alter table professionals rename column phoneno1 to phonenumber;




CREATE VIEW get_research_mandalas_view AS
 SELECT DISTINCT a.id,
    a.name,
    a.typeid,
    b.name AS typename,
    a.emailid,
    a.phoneno,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.suburb,
    a.city AS cityid,
    c.city,
    a.state,
    a.country AS countryid,
    d.name AS country,
    a.website,
    a.email1,
    a.email2,
    a.contactname1,
    a.contactname2,
    a.phoneno1,
    a.phoneno2,
    a.excludefrommailinglist
   FROM mandalas a
     LEFT JOIN mandaltypes b ON a.typeid = b.mandalid
     LEFT JOIN cities c ON a.city = c.id
     LEFT JOIN country d ON a.country = d.id;

CREATE VIEW get_payments_view AS
SELECT DISTINCT
    a.id,
    CONCAT(b.firstname, ' ', b.lastname) AS paymentby,
    CONCAT(c.firstname, ' ', c.lastname) AS paymentto,
    a.amount,
    a.paidon,
    d.name AS paymentmode,
    a.paymentstatus,
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
LEFT JOIN usertable b ON a.paymentby = b.id
LEFT JOIN usertable c ON a.paymentto = c.id
LEFT JOIN mode_of_payment d ON a.paymentmode = d.id
LEFT JOIN payment_for e ON a.paymentfor = e.id
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



-- CREATE OR REPLACE FUNCTION delete_from_get_payments_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM ref_contractual_payments WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_payments_view
-- INSTEAD OF DELETE ON get_payments_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_payments_view();

--tobedone
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
    CASE a.status WHEN true THEN 'Active' ELSE 'Inactive' END AS statusmap,
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



-- CREATE OR REPLACE FUNCTION delete_from_get_employee_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM employee WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_employee_view
-- INSTEAD OF DELETE ON get_employee_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_employee_view();

--tobedone

CREATE VIEW get_lob_view AS
 SELECT DISTINCT a.id,
    a.name,
    concat_ws(' '::text, b.firstname, b.lastname) AS lob_head,
    a.company,
    c.name AS entity
   FROM lob a
     LEFT JOIN usertable b ON a.lob_head = b.id
     LEFT JOIN entity c ON a.entityid = c.id;



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
    




-- CREATE OR REPLACE FUNCTION delete_from_get_locality_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM locality WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_locality_view
-- INSTEAD OF DELETE ON get_locality_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_locality_view();


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
    a.email1,
    a.phoneno,
    a.dated,
    a.createdby,
    a.isdeleted
FROM 
    research_prospect a
LEFT JOIN
    country c ON a.country = c.id;


-- CREATE OR REPLACE FUNCTION delete_from_get_research_prospect_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM research_prospect WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_research_prospect_view
-- INSTEAD OF DELETE ON get_research_prospect_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_research_prospect_view();


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

-- CREATE OR REPLACE FUNCTION delete_from_get_builder_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM builder WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_builder_view
-- INSTEAD OF DELETE ON get_builder_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_builder_view();

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

-- CREATE OR REPLACE FUNCTION delete_from_get_cities_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM cities WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_cities_view
-- INSTEAD OF DELETE ON get_cities_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_cities_view();

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
    a.id,
    TRIM(TRAILING ', ' FROM CONCAT(
        CASE WHEN a.tenantworkingbachelorsallowed THEN 'Tenant Working Bachelors Allowed, ' ELSE '' END,
        CASE WHEN a.tenantforeignersallowed THEN 'Tenant Foreigners Allowed, ' ELSE '' END,
        CASE WHEN a.tenantstudentsallowed THEN 'Tenant Students Allowed, ' ELSE '' END
    )) AS tenant
FROM
    project a
LEFT JOIN
    builder b ON a.builderid = b.id
LEFT JOIN
    project_type c ON a.project_type = c.id
LEFT JOIN
    project_legal_status d ON a.project_legal_status = d.id;


-- CREATE OR REPLACE FUNCTION delete_from_get_projects_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM projects WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_projects_view
-- INSTEAD OF DELETE ON get_projects_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_projects_view();

CREATE OR REPLACE VIEW get_builder_contact_view AS
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
    a.city as cityid,
    c.city,
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
    builder b ON a.builderid = b.id
LEFT JOIN
    cities c ON a.city = c.id;

-- CREATE OR REPLACE FUNCTION delete_from_get_builder_contacts_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM builder_contacts WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_builder_contacts_view
-- INSTEAD OF DELETE ON get_builder_contact_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_builder_contacts_view();


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



-- CREATE OR REPLACE FUNCTION delete_from_get_client_info_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM client WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_client_info_view
-- INSTEAD OF DELETE ON get_client_info_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_client_info_view();

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
    a.clientservicemanager,
    a.propertymanager,
    concat_ws(' ',c.projectname,a.propertydescription) as property,
    a.comments,
    a.propertyownedbyclientonly,
    a.textforposting,
    a.dated,
    a.createdby,
    a.isdeleted,
    a.electricitybillingduedate,
    h.buildername
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
    builder h ON a.projectid = h.id;


-- CREATE OR REPLACE FUNCTION delete_from_get_client_property_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM client WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_client_property_view
-- INSTEAD OF DELETE ON get_client_property_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_client_property_view();


CREATE VIEW get_orders_view AS
 SELECT DISTINCT a.id,
    a.clientid,
    concat(g.firstname, ' ', NULLIF(g.middlename, ''::text), ' ', g.lastname) AS clientname,
    a.orderdate,
    a.earlieststartdate,
    a.expectedcompletiondate,
    a.actualcompletiondate,
    a.owner,
    concat(b.firstname, ' ', b.lastname) AS ownername,
    concat_ws('-'::text, concat_ws(' '::text, b.firstname, b.lastname), a.briefdescription) AS ordername,
    a.comments,
    a.status,
    h.name AS orderstatus,
    a.briefdescription,
    a.additionalcomments,
    a.service,
    e.service AS servicename,
    a.clientpropertyid,
    concat_ws('-'::text, i.suburb, i.propertydescription) AS clientproperty,
    a.vendorid,
    c.vendorname,
    a.assignedtooffice,
    d.name AS officename,
    a.dated,
    a.createdby,
    concat_ws(' '::text, j.firstname, j.lastname) AS createdbyname,
    a.isdeleted,
    a.entityid,
    f.name AS entity,
    a.tallyledgerid,
    (EXTRACT(epoch FROM age(CURRENT_DATE::timestamp with time zone, COALESCE(a.earlieststartdate, a.orderdate)::timestamp with time zone)) / 86400::numeric)::integer AS ageing
   FROM orders a
     LEFT JOIN usertable b ON a.owner = b.id
     LEFT JOIN vendor c ON a.vendorid = c.id
     LEFT JOIN office d ON a.assignedtooffice = d.id
     LEFT JOIN services e ON a.service = e.id
     LEFT JOIN entity f ON a.entityid = f.id
     LEFT JOIN client g ON a.clientid = g.id
     LEFT JOIN order_status h ON a.status = h.id
     LEFT JOIN client_property i ON a.clientpropertyid = i.id
     LEFT JOIN usertable j ON a.createdby = j.id;


-- CREATE SEQUENCE IF NOT EXISTS payments_id_seq OWNED BY ref_contractual_payments.id;
-- SELECT setval('payments_id_seq', COALESCE(max(id), 0) + 1, false) FROM ref_contractual_payments;
-- ALTER TABLE ref_contractual_payments ALTER COLUMN id SET DEFAULT nextval('payments_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS orders_id_seq OWNED BY orders.id;
-- SELECT setval('orders_id_seq', COALESCE(max(id), 0) + 1, false) FROM orders;
-- ALTER TABLE orders ALTER COLUMN id SET DEFAULT nextval('orders_id_seq');


-- -- Create a new sequence if it doesn't exist starting from the maximum value of column id + 1
-- CREATE SEQUENCE IF NOT EXISTS builder_id_seq OWNED BY builder.id;

-- -- Set the initial value of the sequence based on the maximum value of column id in the builder table
-- SELECT setval('builder_id_seq', COALESCE(max(id), 0) + 1, false) FROM builder;

-- -- Alter the table to set the default value of column id to use the sequence
-- ALTER TABLE builder ALTER COLUMN id SET DEFAULT nextval('builder_id_seq');

-- -- For client table
-- CREATE SEQUENCE IF NOT EXISTS client_id_seq OWNED BY client.id;
-- SELECT setval('client_id_seq', COALESCE(max(id), 0) + 1, false) FROM client;
-- ALTER TABLE client ALTER COLUMN id SET DEFAULT nextval('client_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS country_id_seq OWNED BY country.id;
-- SELECT setval('country_id_seq', COALESCE(max(id), 0) + 1, false) FROM country;
-- ALTER TABLE country ALTER COLUMN id SET DEFAULT nextval('country_id_seq');

-- -- For client_access table
-- CREATE SEQUENCE IF NOT EXISTS client_access_id_seq OWNED BY client_access.id;
-- SELECT setval('client_access_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_access;
-- ALTER TABLE client_access ALTER COLUMN id SET DEFAULT nextval('client_access_id_seq');

-- -- For client_legal_info table
-- CREATE SEQUENCE IF NOT EXISTS client_legal_info_id_seq OWNED BY client_legal_info.id;
-- SELECT setval('client_legal_info_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_legal_info;
-- ALTER TABLE client_legal_info ALTER COLUMN id SET DEFAULT nextval('client_legal_info_id_seq');

-- -- For client_bank_info table
-- CREATE SEQUENCE IF NOT EXISTS client_bank_info_id_seq OWNED BY client_bank_info.id;
-- SELECT setval('client_bank_info_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_bank_info;
-- ALTER TABLE client_bank_info ALTER COLUMN id SET DEFAULT nextval('client_bank_info_id_seq');

-- -- For client_poa table
-- CREATE SEQUENCE IF NOT EXISTS client_poa_id_seq OWNED BY client_poa.id;
-- SELECT setval('client_poa_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_poa;
-- ALTER TABLE client_poa ALTER COLUMN id SET DEFAULT nextval('client_poa_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS project_id_seq OWNED BY project.id;
-- SELECT setval('project_id_seq', COALESCE(max(id), 0) + 1, false) FROM project;
-- ALTER TABLE project ALTER COLUMN id SET DEFAULT nextval('project_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS project_amenities_id_seq OWNED BY project_amenities.id;
-- SELECT setval('project_amenities_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_amenities;
-- ALTER TABLE project_amenities ALTER COLUMN id SET DEFAULT nextval('project_amenities_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS project_bank_details_id_seq OWNED BY project_bank_details.id;
-- SELECT setval('project_bank_details_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_bank_details;
-- ALTER TABLE project_bank_details ALTER COLUMN id SET DEFAULT nextval('project_bank_details_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS project_contacts_id_seq OWNED BY project_contacts.id;
-- SELECT setval('project_contacts_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_contacts;
-- ALTER TABLE project_contacts ALTER COLUMN id SET DEFAULT nextval('project_contacts_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS project_photos_id_seq OWNED BY project_photos.id;
-- SELECT setval('project_photos_id_seq', COALESCE(max(id), 0) + 1, false) FROM project_photos;
-- ALTER TABLE project_photos ALTER COLUMN id SET DEFAULT nextval('project_photos_id_seq');

-- CREATE TABLE project_photos(
--     id int,
--     projectid int,
--     photo_link text,
--     description text,
--     date_taken date,
--     dated timestamp(3),
--     createdby int,
--     isdeleted boolean
-- );

-- CREATE SEQUENCE IF NOT EXISTS client_property_id_seq OWNED BY client_property.id;
-- SELECT setval('client_property_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property;
-- ALTER TABLE client_property ALTER COLUMN id SET DEFAULT nextval('client_property_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS client_property_photos_id_seq OWNED BY client_property_photos.id;
-- SELECT setval('client_property_photos_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_photos;
-- ALTER TABLE client_property_photos ALTER COLUMN id SET DEFAULT nextval('client_property_photos_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS client_property_poa_id_seq OWNED BY client_property_poa.id;
-- SELECT setval('client_property_poa_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_poa;
-- ALTER TABLE client_property_poa ALTER COLUMN id SET DEFAULT nextval('client_property_poa_id_seq');


-- CREATE SEQUENCE IF NOT EXISTS client_property_owner_id_seq OWNED BY client_property_owner.id;
-- SELECT setval('client_property_owner_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_owner;
-- ALTER TABLE client_property_owner ALTER COLUMN id SET DEFAULT nextval('client_property_owner_id_seq');



-- SELECT setval('client_property_id_seq', (SELECT MAX(id) FROM client_property));


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

-- CREATE OR REPLACE FUNCTION delete_from_get_client_receipt_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM client_receipt WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER delete_trigger_for_get_client_receipt_view
-- INSTEAD OF DELETE ON get_client_receipt_view
-- FOR EACH ROW
-- EXECUTE FUNCTION delete_from_get_client_receipt_view();

-- CREATE SEQUENCE IF NOT EXISTS client_receipt_id_seq OWNED BY client_receipt.id;
-- SELECT setval('client_receipt_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_receipt;
-- ALTER TABLE client_receipt ALTER COLUMN id SET DEFAULT nextval('client_receipt_id_seq');



-- CREATE SEQUENCE IF NOT EXISTS client_property_caretaking_agreement_id_seq OWNED BY client_property_caretaking_agreement.id;
-- SELECT setval('client_property_caretaking_agreement_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_caretaking_agreement;
-- ALTER TABLE client_property_caretaking_agreement ALTER COLUMN id SET DEFAULT nextval('client_property_caretaking_agreement_id_seq');



CREATE VIEW get_client_property_pma_view AS
SELECT DISTINCT
    a.id,
    a.clientpropertyid,
    concat_ws('-',d.project,d.suburb) as propertydescription,
    d.propertystatus,
    d.status as propertystatusname,
    d.client as clientname,
    d.clientid,
    CASE a.active WHEN true THEN 'Active' ELSE 'Inactive' END AS activemap,
    a.startdate,
    a.enddate,
    a.actualenddate,
    d.status,
    a.scancopy,
    a.active,
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


-- CREATE OR REPLACE FUNCTION get_client_property_pma_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM client_property_caretaking_agreement WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER get_client_property_pma_view
-- INSTEAD OF DELETE ON get_client_property_pma_view
-- FOR EACH ROW
-- EXECUTE FUNCTION get_client_property_pma_view();

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
    CASE a.active WHEN true THEN 'Active' ELSE 'Inactive' END AS activemap,    
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

-- CREATE SEQUENCE IF NOT EXISTS client_property_leave_license_details_id_seq OWNED BY client_property_leave_license_details.id;
-- SELECT setval('client_property_leave_license_details_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_property_leave_license_details;
-- ALTER TABLE client_property_leave_license_details ALTER COLUMN id SET DEFAULT nextval('client_property_leave_license_details_id_seq');

-- CREATE OR REPLACE FUNCTION get_client_property_lla_view() RETURNS TRIGGER AS $$
-- BEGIN
--     -- Perform delete operation on the underlying table(s)
--     DELETE FROM client_property_leave_license_details WHERE id = OLD.id;
--     -- You might need additional delete operations if data is spread across multiple tables
--     -- If so, add DELETE statements for those tables here.
--     RETURN OLD;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER get_client_property_lla_view
-- INSTEAD OF DELETE ON get_client_property_lla_view
-- FOR EACH ROW
-- EXECUTE FUNCTION get_client_property_lla_view();

-- CREATE SEQUENCE IF NOT EXISTS order_status_change_id_seq OWNED BY order_status_change.id;
-- SELECT setval('order_status_change_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_status_change;
-- ALTER TABLE order_status_change ALTER COLUMN id SET DEFAULT nextval('order_status_change_id_seq');



-- CREATE SEQUENCE IF NOT EXISTS order_photos_id_seq OWNED BY order_photos.id;
-- SELECT setval('order_photos_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_photos;
-- ALTER TABLE order_photos ALTER COLUMN id SET DEFAULT nextval('order_photos_id_seq');



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
    a.isdeleted,
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

-- CREATE SEQUENCE IF NOT EXISTS order_receipt_id_seq OWNED BY order_receipt.id;
-- SELECT setval('order_receipt_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_receipt;
-- ALTER TABLE order_receipt ALTER COLUMN id SET DEFAULT nextval('order_receipt_id_seq');


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

-- CREATE SEQUENCE IF NOT EXISTS vendor_id_seq OWNED BY vendor.id;
-- SELECT setval('vendor_id_seq', COALESCE(max(id), 0) + 1, false) FROM vendor;
-- ALTER TABLE vendor ALTER COLUMN id SET DEFAULT nextval('vendor_id_seq');



-- CREATE SEQUENCE IF NOT EXISTS order_vendorestimate_id_seq OWNED BY order_vendorestimate.id;
-- SELECT setval('order_vendorestimate_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_vendorestimate;
-- ALTER TABLE order_vendorestimate ALTER COLUMN id SET DEFAULT nextval('order_vendorestimate_id_seq');


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

-- CREATE SEQUENCE IF NOT EXISTS order_payment_id_seq OWNED BY order_payment.id;
-- SELECT setval('order_payment_id_seq', COALESCE(max(id), 0) + 1, false) FROM order_payment;
-- ALTER TABLE order_payment ALTER COLUMN id SET DEFAULT nextval('order_payment_id_seq');

delete from order_status where id=7;


-- CREATE SEQUENCE IF NOT EXISTS clientleavelicensetenant_id_seq OWNED BY clientleavelicensetenant.id;
-- SELECT setval('clientleavelicensetenant_id_seq', COALESCE(max(id), 0) + 1, false) FROM clientleavelicensetenant;
-- ALTER TABLE clientleavelicensetenant ALTER COLUMN id SET DEFAULT nextval('clientleavelicensetenant_id_seq');


--tobedone
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




-- CREATE or replace VIEW propertiesview AS
-- SELECT
--     Client_Property.ClientID,
--     Client_Property.ProjectID,
--     Client_Property.PropertyDescription,
--     Client_Property.PropertyType,
--     Client_Property.LayoutDetails,
--     Client_Property.NumberOfParkings,
--     Client_Property.InternalFurnitureAndFittings,
--     Client_Property.LevelOfFurnishing,
--     Client_Property.Status,
--     Client_Property.InitialPossessionDate,
--     Client_Property.POAGiven,
--     Client_Property.POAID,
--     Client_Property.ElectricityConsumerNumber,
--     Client_Property.ElectricityBillingUnit,
--     Client_Property.OtherElectricityDetails,
--     Client_Property.GasConnectionDetails,
--     Client_Property.PropertyTaxNumber,
--     Client_Property.ClientServiceManager,
--     Client_Property.PropertyManager,
--     Client_Property.Comments,
--     Client_Property.PropertyOwnedByClientOnly,
--     Client_Property.TextForPosting,
--     Client_Property.Dated,
--     Client_Property.CreatedBy AS CreatedById,
--     Property_Status.Name AS Property_Status,
--     Property_Type.Name AS Property_Type,
--     usertable.FirstName || ' ' || usertable.LastName AS CreatedBy,
--     Level_Of_furnishing.Name AS Level_Of_furnishing,
--     Client.FirstName || ' ' || Client.LastName AS ClientName,
--     Client_Property.ID,
--     Client_Property.Suburb,
--     Client_Property.City,
--     Client_Property.State,
--     Client_Property.Country AS CountryId,
--     Country.Name AS Country,
--     Client_Property.ID AS PropertyID,
--     Project.ProjectName,
--     Client_Property.ElectricityBillingDueDate
-- FROM
--     Client_Property
--     INNER JOIN Property_Type ON Client_Property.PropertyType = Property_Type.ID
--     INNER JOIN Property_Status ON Client_Property.Status = Property_Status.ID
--     INNER JOIN usertable ON Client_Property.CreatedBy = usertable.ID
--     INNER JOIN Level_Of_furnishing ON Client_Property.LevelOfFurnishing = Level_Of_furnishing.ID
--     INNER JOIN Client ON Client_Property.ClientID = Client.ID
--     INNER JOIN Project ON Client_Property.ProjectID = Project.ID
--     LEFT OUTER JOIN Country ON Client_Property.Country = Country.ID
-- WHERE
--     Client_Property.IsDeleted = 'false' or client_property.isdeleted=null
-- ORDER BY
--     Client.FirstName || ' ' || Client.LastName;

CREATE VIEW PropertiesView AS
SELECT DISTINCT ON (cp.id) cp.clientid, 
                    cp.projectid, 
                    cp.propertydescription, 
                    cp.propertytype,
                    cp.layoutdetails, 
                    cp.numberofparkings, 
                    cp.internalfurnitureandfittings, 
                    cp.leveloffurnishing,
                    cp.status, 
                    cp.initialpossessiondate, 
                    cp.poagiven, 
                    cp.poaid,
                    cp.electricityconsumernumber, 
                    cp.electricitybillingunit, 
                    cp.otherelectricitydetails,
                    cp.gasconnectiondetails, 
                    cp.propertytaxnumber, 
                    cp.clientservicemanager, 
                    cp.propertymanager,
                    cp.comments, 
                    cp.propertyownedbyclientonly, 
                    cp.textforposting, 
                    cp.dated,
                    cp.createdby AS createdbyid, 
                    ps.name AS property_status, 
                    pt.name AS property_type,
                    usr.firstname || ' ' || usr.lastname AS createdby, 
                    lof.name AS level_of_furnishing,
                    c.firstname || ' ' || c.lastname AS clientname, 
                    cp.id, 
                    cp.suburb, 
                    cp.city, 
                    cp.state,
                    co.name AS country, 
                    cp.id AS propertyid, 
                    pr.projectname,
                    cp.electricitybillingduedate
FROM client_property cp
INNER JOIN property_type pt ON cp.propertytype = pt.id
INNER JOIN property_status ps ON cp.status = ps.id
INNER JOIN usertable usr ON cp.createdby = usr.id
INNER JOIN level_of_furnishing lof ON cp.leveloffurnishing = lof.id
INNER JOIN client c ON cp.clientid = c.id
INNER JOIN project pr ON cp.projectid = pr.id
LEFT OUTER JOIN country co ON cp.country = co.id
WHERE cp.isdeleted = FALSE
ORDER BY cp.id, clientname;




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
RETURNS text AS $$
DECLARE
    ret_val text;
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
RETURNS text AS $$
DECLARE
    ret_val text;
BEGIN
    ret_val := TO_CHAR(date_input, 'Mon-YYYY');
    RETURN ret_val;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getMonthYear(date_input TIMESTAMP WITHOUT TIME ZONE)
RETURNS text AS $$
DECLARE
    ret_val text;
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
  ordersview.TallyLedger,
 'OP' as type
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


-- CREATE SEQUENCE payment_source_id_seq;

-- CREATE TABLE payment_source (
--     id bigint NOT NULL DEFAULT nextval('payment_source_id_seq'::regclass),
--     name text NOT NULL,
--     CONSTRAINT idx_93250_pk_payment_source PRIMARY KEY (id)
-- );

-- ALTER SEQUENCE payment_source_id_seq OWNED BY payment_source.id;

-- INSERT INTO payment_source (id, name) VALUES
-- (1, 'Client'),
-- (2, 'Builder'),
-- (3, 'Society'),
-- (4, 'Tenant'),
-- (5, 'Broker'),
-- (6, 'Internal cash transfer'),
-- (7, 'Director'),
-- (8, 'Buyer');



CREATE OR REPLACE VIEW orderreceiptview AS
SELECT
  Mode_Of_payment.Name AS PaymentMode,
  usertable.FirstName || ' ' || usertable.LastName AS ReceivedBy,
  User_1.FirstName || ' ' || User_1.LastName AS Createdby,
  OrdersView.ClientName,
  OrdersView.BriefDescription AS OrderDescription,
  Order_Receipt.ID,
  Order_Receipt.ReceivedBy AS ReceivedById,
  Order_Receipt.Amount,
  Order_Receipt.RecdDate,
  Order_Receipt.PaymentMode AS PaymentModeId,
  Order_Receipt.OrderID,
  Order_Receipt.ReceiptDesc,
  Order_Receipt.OfficeId,
  Office.Name AS OfficeName,
  Order_Receipt.PaymentSource AS PaymentSourceId,
  Order_Receipt.Dated,
  Order_Receipt.Createdby AS CreatedbyId,
  Order_Receipt.IsDeleted,
  Payment_Source.Name AS PaymentSource,
  Order_Receipt.TDS,
  PropertiesView.PropertyDescription,
  getMonthYear(Order_Receipt.RecdDate) AS MonthYear,
  getFinancialYear(Order_Receipt.RecdDate) AS FY,
  OrdersView.Service,
  OrdersView.LOBName,
  OrdersView.ServiceType,
  OrdersView.TallyLedger,
  OrdersView.TallyLedgerId,
  OrdersView.ServiceId,
  Order_Receipt.EntityId,
  Entity.Name AS EntityName,
  OrdersView.ClientTypeName,
  OrdersView.ClientID,
  'OR' as type
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

-- CREATE VIEW ordersview AS
-- SELECT DISTINCT
--     orders.briefdescription, 
--     earlieststartdate, 
--     orders.expectedcompletiondate, 
--     orders.actualcompletiondate, 
--     orders.owner, 
--     orders.comments, 
--     orders.status, 
--     orders.additionalcomments, 
--     orders.service AS serviceid, 
--     orders.clientpropertyid, 
--     orders.vendorid, 
--     orders.assignedtooffice AS assignedtoofficeid, 
--     orders.billable, 
--     orders.dated, 
--     orders.createdby AS createdbyid, 
--     orders.isdeleted, 
--     order_status.name AS orderstatus, 
--     services.service, 
--     office.name AS assignedtooffice, 
--     vendor.vendorname, 
--     ut1.firstname || ' ' || ut1.lastname AS createdby, 
--     orders.id, 
--     CASE 
--         WHEN DATE_PART('day', CURRENT_DATE - orders.statusupdatedtimestamp) >  999 THEN - 1 
--         ELSE DATE_PART('day', CURRENT_DATE - orders.statusupdatedtimestamp)
--     END AS ageing, 
--     ut2.firstname || ' ' || ut2.lastname AS ownername, 
--     orders.orderdate, 
--     get_client_property_view.description AS propertydescription, 
--     get_client_property_view.propertytype AS propertytypeid, 
--     get_client_property_view.status AS propertystatusid, 
--     get_client_property_view.propertystatus, 
--     get_client_property_view.propertytype, 
--     get_client_property_view.suburb, 
--     get_client_info_view.clientname, 
--     get_client_info_view.clienttypename, 
--     orders.clientid, 
--     get_client_property_view.propertymanager, 
--     get_client_property_view.clientservicemanager, 
--     orders.default_task_owner, 
--     lob.name AS lobname, 
--     services.servicetype, 
--     orders.glcode, 
--     orders.entityid, 
--     entity.name AS entityname, 
--     tallyledger.tallyledger, 
--     orders.tallyledgerid, 
--     orders.statusupdatedtimestamp, 
--     get_client_info_view.homephone, 
--     get_client_info_view.workphone, 
--     get_client_info_view.mobilephone, 
--     get_client_info_view.email1, 
--     get_client_info_view.email2
-- FROM
--     orders 
-- INNER JOIN
--     order_status ON orders.status = order_status.id
-- INNER JOIN
--     services ON orders.service = services.id
-- LEFT OUTER JOIN
--     vendor ON orders.vendorid = vendor.id
-- INNER JOIN
--     office ON orders.assignedtooffice = office.id
-- INNER JOIN
--     usertable ut1 ON orders.createdby = ut1.id
-- INNER JOIN
--     usertable ut2 ON orders.owner = ut2.id
-- INNER JOIN
--     get_client_property_view ON orders.clientpropertyid = get_client_property_view.id
-- INNER JOIN
--     get_client_info_view ON orders.clientid = get_client_info_view.id
-- INNER JOIN
--     lob ON services.lob = lob.id
-- LEFT OUTER JOIN
--     tallyledger ON orders.tallyledgerid = tallyledger.id
-- LEFT OUTER JOIN
--     entity ON orders.entityid = entity.id
-- WHERE
--     orders.isdeleted = FALSE;


-- CREATE VIEW orderpaymentview AS
-- SELECT DISTINCT
--        op.id,
--        op.paymentby AS paymentbyid,
--        op.amount,
--        op.paymentdate,
--        op.orderid,
--        op.vendorid,
--        op.mode,
--        op.description,
--        op.servicetaxamount,
--        op.dated,
--        op.createdby AS createdbyid,
--        op.isdeleted,
--        mop.name AS mode_of_payment,
--        u1.firstname || ' ' || u1.lastname AS createdby,
--        ut.firstname || ' ' || ut.lastname AS paymentby,
--        ov.clientname,
--        ov.briefdescription AS orderdescription,
--        op.tds,
--        pv.propertydescription,
--        v.vendorname,
--        ov.lobname,
--        ov.servicetype,
--        ov.serviceid,
--        EXTRACT(MONTH FROM op.paymentdate) AS monthyear,
--        EXTRACT(MONTH FROM op.paymentdate) AS fy,
--        op.entityid,
--        e.name AS entityname,
--        op.officeid,
--        o.name AS officename,
--        ov.clientid,
--        ov.service,
--        ov.tallyledger
-- FROM order_payment op
-- LEFT OUTER JOIN usertable u ON op.paymentby = u.id
-- LEFT OUTER JOIN office o ON o.id = op.officeid
-- LEFT OUTER JOIN mode_of_payment mop ON op.mode = mop.id
-- INNER JOIN usertable AS u1 ON op.createdby = u1.id
-- INNER JOIN usertable AS ut ON op.paymentby = ut.id
-- INNER JOIN ordersview ov ON op.orderid = ov.id
-- LEFT OUTER JOIN propertiesview pv ON ov.clientpropertyid = pv.propertyid AND ov.clientid = pv.clientid
-- INNER JOIN vendor v ON op.vendorid = v.id
-- LEFT OUTER JOIN entity e ON op.entityid = e.id;

CREATE OR REPLACE FUNCTION getfinancialyear(_date DATE)
RETURNS TEXT AS 
$$
DECLARE
    input_year INT;
    start_year TEXT;
BEGIN
    input_year := EXTRACT(YEAR FROM _date);

    -- Determine the start year of the financial year based on the month of the input date
    IF EXTRACT(MONTH FROM _date) > 3 THEN
        start_year := input_year::TEXT;
    ELSE
        start_year := (input_year::INT - 1)::TEXT;
    END IF;

    RETURN start_year || '-' || RIGHT((start_year::INT + 1)::TEXT, 2);
END;
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION getMonthYear(_Date DATE) 
RETURNS TEXT AS 
$$
DECLARE
    _RetVal TEXT;
BEGIN
    _RetVal := TO_CHAR(_Date, 'Mon') || '-' || TO_CHAR(_Date, 'YYYY');
    RETURN _RetVal;
END;
$$
LANGUAGE PLPGSQL;

-- CREATE SEQUENCE IF NOT EXISTS usertable_id_seq OWNED BY usertable.id;
-- SELECT setval('usertable_id_seq', COALESCE(max(id), 0) + 1, false) FROM usertable;
-- ALTER TABLE usertable ALTER COLUMN id SET DEFAULT nextval('usertable_id_seq');

CREATE VIEW get_users_view AS
SELECT DISTINCT
    a.id,
    a.username,
    a.roleid,
    b.role_name,
    a.password,
    a.officeid,
    c.name AS office,
    a.lobid,
    d.name AS lob,
    a.usercode,
    a.firstname,
    a.lastname,
    concat_ws(' ',a.firstname,a.lastname) as fullname,
    CASE a.status WHEN true THEN 'Active' ELSE 'Inactive' END AS statusmap,
    a.status,
    a.effectivedate,
    a.homephone,
    a.workphone,
    a.email1,
    a.email2,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city AS cityid,
    e.city,
    a.state,
    a.country as countryid,
    f.name as country,
    a.zip,
    a.dated,
    a.createdby,
    concat_ws(' ',g.firstname,g.lastname) AS createdbyname,
    a.isdeleted,
    a.entityid,
    h.name AS entity
FROM
    usertable a
LEFT JOIN
    roles b ON a.roleid = b.id
LEFT JOIN
    office c ON a.officeid = c.id
LEFT JOIN
    lob d ON a.lobid = d.id
LEFT JOIN
    cities e ON a.city = e.id
LEFT JOIN
    country f ON a.country = f.id
LEFT JOIN
    usertable g ON a.createdby = g.id
LEFT JOIN
    entity h ON a.entityid = h.id;


CREATE VIEW get_services_view AS
SELECT DISTINCT
    a.id,
    a.lob as lobid,
    b.name as lob,
    a.service,
    a.active,
    a.dated,
    a.createdby as createdbyid,
    concat_ws(' ',c.firstname,c.lastname) as createdby,
    a.isdeleted,
    a.servicetype,
    a.category2,
    a.tallyledgerid,
    d.tallyledger
FROM
    services a
LEFT JOIN
    lob b ON a.lob = b.id
LEFT JOIN
    usertable c ON a.createdby = c.id
LEFT JOIN
    tallyledger d ON a.tallyledgerid = d.id;
 

CREATE VIEW get_research_employer_view AS
SELECT DISTINCT
    a.id,
    a.employername,
    a.industry,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city,
    a.state,
    a.country as countryid,
    b.name as countryname,
    a.zip,
    a.hc,
    a.notes,
    a.website,
    CASE a.onsiteopportunity WHEN true THEN 'Yes' ELSE 'No' END AS onsiteopportunitytext,
    a.onsiteopportunity,
    a.contactname1,
    a.contactname2,
    a.contactphone1,
    a.contactphone2,
    a.contactmail1,
    a.contactmail2,
    a.hrcontactname,
    a.hrcontactmail,
    a.hrcontactphone,
    a.admincontactname,
    a.admincontactmail,
    a.admincontactphone,
    a.dated,
    a.createdby,
    a.isdeleted
FROM
    research_employer a
LEFT JOIN
    country b ON a.country = b.id;

-- CREATE SEQUENCE IF NOT EXISTS research_employer_id_seq OWNED BY research_employer.id;
-- SELECT setval('research_employer_id_seq', COALESCE(max(id), 0) + 1, false) FROM research_employer;
-- ALTER TABLE research_employer ALTER COLUMN id SET DEFAULT nextval('research_employer_id_seq');


CREATE view contractualpaymentsview AS
 SELECT ref_contractual_payments.id,
    ref_contractual_payments.paymentto AS paymenttoid,
    ref_contractual_payments.paidon,
    ref_contractual_payments.paymentmode AS paymentmodeid,
    ref_contractual_payments.description,
    ref_contractual_payments.banktransactionid,
    ref_contractual_payments.paymentfor AS paymentforid,
    ref_contractual_payments.dated,
    ref_contractual_payments.createdby,
    ref_contractual_payments.isdeleted,
    payment_for.name AS paymentfor,
    userview.fullname AS paymentto,
    mode_of_payment.name AS paymentmode,
    ref_contractual_payments.amount,
    ref_contractual_payments.paymentby AS paymentbyid,
    userview_1.fullname AS paymentby,
    getmonthyear(ref_contractual_payments.paidon::timestamp without time zone) AS monthyear,
    getfinancialyear(ref_contractual_payments.paidon::date) AS fy,
    ref_contractual_payments.entityid,
    entity.name AS entityname,
    ref_contractual_payments.officeid,
    office.name AS officename,
    ref_contractual_payments.tds,
    ref_contractual_payments.professiontax,
    ref_contractual_payments.month,
    ref_contractual_payments.deduction
   FROM ref_contractual_payments
     JOIN office ON office.id = ref_contractual_payments.officeid
     JOIN mode_of_payment ON ref_contractual_payments.paymentmode = mode_of_payment.id
     JOIN payment_for ON ref_contractual_payments.paymentfor = payment_for.id
     JOIN userview ON ref_contractual_payments.paymentto = userview.userid
     LEFT JOIN entity ON mode_of_payment.entityid = entity.id AND ref_contractual_payments.entityid = entity.id
     LEFT JOIN userview userview_1 ON ref_contractual_payments.paymentby = userview_1.userid;




CREATE OR REPLACE VIEW get_research_realestate_agents_view AS
SELECT DISTINCT
    a.id,
    a.nameofagent,
    a.agencyname,
    a.emailid,
    a.phoneno,
    a.phoneno2,
    a.address,
    a.localitiesdealing,
    a.nameofpartners,
    CASE a.registered WHEN true THEN 'Yes' ELSE 'No' END as registered,
    a.isdeleted,
    a.dated,
    a.createdby,
    a.rera_registration_number
FROM
    realestateagents a;

-- CREATE SEQUENCE IF NOT EXISTS realestateagents_id_seq OWNED BY realestateagents.id;
-- SELECT setval('realestateagents_id_seq', COALESCE(max(id), 0) + 1, false) FROM realestateagents;
-- ALTER TABLE realestateagents ALTER COLUMN id SET DEFAULT nextval('realestateagents_id_seq');

CREATE OR REPLACE VIEW get_bankst_view AS
SELECT
    a.id,
    a.modeofpayment,
    f.name AS mode,
    a.date,
    a.amount,
    a.particulars,
    a.crdr,
    CASE LOWER(a.crdr)
        WHEN 'cr' THEN 'Credit'
        WHEN 'dr' THEN 'Debit'
        ELSE NULL
    END AS creditdebit,
    a.chequeno,
    a.availablebalance,
    a.dateadded,
    a.clientid,
    a.orderid,
    a.receivedhow,
    a.details,
    a.vendorid,
    a.createdby,
    a.isdeleted,
    CONCAT_WS(' ', b.firstname, b.middlename, b.lastname) AS clientname,
    c.briefdescription AS orderdescription,
    d.vendorname,
    CONCAT_WS(' ', e.firstname, e.lastname) AS createdbyname
FROM
    bankst a
LEFT JOIN
    client b ON a.clientid = b.id
LEFT JOIN
    orders c ON a.orderid = c.id
LEFT JOIN
    vendor d ON a.vendorid = d.id
LEFT JOIN
    usertable e ON a.createdby = e.id
LEFT JOIN
    mode_of_payment f ON a.modeofpayment = f.id;


CREATE VIEW get_cocandbusinessgroup_view AS
SELECT DISTINCT
    a.id,
    a.name,
    a.suburb,
    a.phoneno,
    a.contactperson1,
    a.emailid,
    a.contactperson2,
    a.email1,
    a.email2,
    a.contactname1,
    a.contactname2,
    a.createdby,
    concat_ws(' ',b.firstname,b.lastname) AS createdbyname,
    a.dated,
    a.isdeleted,
    a.city as cityid,
    c.city,
    a.state,
    d.name as countryname,
    a.country,
    a.groupid,
    e.name as groupname,
    a.address,
    a.excludefrommailinglist
FROM
    cocandbusinessgroup a
LEFT JOIN
    usertable b ON a.createdby = b.id
LEFT JOIN
    cities c ON a.city = c.id
LEFT JOIN
    country d ON a.country = d.id
LEFT JOIN
    cocbusinessgrouptype e ON a.groupid = e.id;

-- CREATE SEQUENCE IF NOT EXISTS cocandbusinessgroup_id_seq OWNED BY cocandbusinessgroup.id;
-- SELECT setval('cocandbusinessgroup_id_seq', COALESCE(max(id), 0) + 1, false) FROM cocandbusinessgroup;
-- ALTER TABLE cocandbusinessgroup ALTER COLUMN id SET DEFAULT nextval('cocandbusinessgroup_id_seq');

-- CREATE TABLE college (
--     id BIGINT,
--     name TEXT,
--     typeid INTEGER,
--     emailid TEXT,
--     phoneno TEXT,
--     dated TIMESTAMP,
--     createdby INTEGER NOT NULL,
--     isdeleted BOOLEAN,
--     suburb TEXT,
--     city INTEGER,
--     state TEXT,
--     country INTEGER,
--     website TEXT,
--     email1 TEXT,
--     email2 TEXT,
--     contactname1 TEXT,
--     contactname2 TEXT,
--     phoneno1 TEXT,
--     phoneno2 TEXT,
--     excludefrommailinglist BOOLEAN
-- );

-- CREATE TABLE collegetypes (
--     id bigint,
--     name text
-- );

-- CREATE TABLE serviceapartmentsandguesthouses (
--     id BIGINT PRIMARY KEY,
--     name TEXT,
--     emailid TEXT,
--     phoneno TEXT,
--     website TEXT,
--     contactperson1 TEXT,
--     contactperson2 TEXT,
--     email1 TEXT,
--     email2 TEXT,
--     contactname1 TEXT,
--     contactname2 TEXT,
--     createdby INTEGER,
--     dated TIMESTAMP WITH TIME ZONE,
--     isdeleted BOOLEAN,
--     suburb TEXT,
--     city INTEGER,
--     state TEXT,
--     country INTEGER,
--     apartments_guesthouse TEXT
-- );

-- CREATE TABLE banksandbranches (
--     id BIGINT,
--     name TEXT,
--     emailid TEXT,
--     phoneno TEXT,
--     website TEXT,
--     contact TEXT,
--     dated TIMESTAMP WITH TIME ZONE,
--     createdby INTEGER NOT NULL,
--     isdeleted BOOLEAN,
--     excludefrommailinglist BOOLEAN
-- );

-- CREATE TABLE mandalas (
--     id BIGINT PRIMARY KEY,
--     name TEXT,
--     typeid INTEGER,
--     emailid TEXT,
--     phoneno TEXT,
--     dated TIMESTAMP WITH TIME ZONE,
--     createdby INTEGER NOT NULL,
--     isdeleted BOOLEAN,
--     suburb TEXT,
--     city INTEGER,
--     state TEXT,
--     country INTEGER,
--     website TEXT,
--     email1 TEXT,
--     email2 TEXT,
--     contactname1 TEXT,
--     contactname2 TEXT,
--     phoneno1 TEXT,
--     phoneno2 TEXT,
--     excludefrommailinglist BOOLEAN
-- );

-- CREATE TABLE friends (
--     id BIGINT PRIMARY KEY,
--     name TEXT,
--     emailid TEXT,
--     phoneno TEXT,
--     contactname TEXT,
--     societyname TEXT,
--     employer TEXT,
--     dated TIMESTAMP WITH TIME ZONE,
--     createdby INTEGER NOT NULL,
--     isdeleted BOOLEAN,
--     suburb TEXT,
--     city INTEGER,
--     state TEXT,
--     country INTEGER,
--     notes TEXT,
--     excludefrommailinglist BOOLEAN
-- );

-- CREATE TABLE research_government_agencies (
--     id BIGINT,
--     agencyname TEXT,
--     addressline1 TEXT,
--     addressline2 TEXT,
--     suburb TEXT,
--     city TEXT,
--     state TEXT,
--     country INTEGER,
--     zip TEXT,
--     agencytype INTEGER,
--     details TEXT,
--     contactname TEXT,
--     contactmail TEXT,
--     contactphone TEXT,
--     dated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
--     createdby INTEGER NOT NULL,
--     isdeleted BOOLEAN NOT NULL,
--     maplink TEXT
-- );

CREATE VIEW get_professionals_view AS
SELECT DISTINCT
    a.id,
    a.name,
    a.typeid,
    b.name as type,
    a.emailid,
    a.professionalid,
    a.dated,
    a.createdby,
    concat_ws(' ',c.firstname,c.lastname) as createdbyname,
    a.isdeleted,
    a.suburb,
    a.city as cityid,
    d.city,
    a.state,
    a.country as countryid,
    e.name as country,
    a.website,
    a.excludefrommailinglist,
    a.phonenumber
FROM
    professionals a
LEFT JOIN
    professionaltypes b ON a.typeid = b.professionalid
LEFT JOIN
    usertable c ON a.createdby = c.id
LEFT JOIN
    cities d ON a.city = d.id
LEFT JOIN
    country e ON a.country = e.id;

-- CREATE SEQUENCE IF NOT EXISTS professionals_id_seq OWNED BY professionals.id;
-- SELECT setval('professionals_id_seq', COALESCE(max(id), 0) + 1, false) FROM professionals;
-- ALTER TABLE professionals ALTER COLUMN id SET DEFAULT nextval('professionals_id_seq');

CREATE OR REPLACE VIEW orderreceiptview AS
SELECT
  Mode_Of_payment.Name AS PaymentMode,
  usertable.FirstName || ' ' || usertable.LastName AS ReceivedBy,
  User_1.FirstName || ' ' || User_1.LastName AS Createdby,
  OrdersView.ClientName,
  OrdersView.BriefDescription AS OrderDescription,
  Order_Receipt.ID,
  Order_Receipt.ReceivedBy AS ReceivedById,
  Order_Receipt.Amount,
  Order_Receipt.RecdDate,
  Order_Receipt.PaymentMode AS PaymentModeId,
  Order_Receipt.OrderID,
  Order_Receipt.ReceiptDesc,
  Order_Receipt.OfficeId,
  Office.Name AS OfficeName,
  Order_Receipt.PaymentSource AS PaymentSourceId,
  Order_Receipt.Dated,
  Order_Receipt.Createdby AS CreatedbyId,
  Order_Receipt.IsDeleted,
  Payment_Source.Name AS PaymentSource,
  Order_Receipt.TDS,
  PropertiesView.PropertyDescription,
  getMonthYear(Order_Receipt.RecdDate) AS MonthYear,
  getFinancialYear(Order_Receipt.RecdDate) AS FY,
  OrdersView.Service,
  OrdersView.LOBName,
  OrdersView.ServiceType,
  OrdersView.TallyLedger,
  OrdersView.TallyLedgerId,
  OrdersView.ServiceId,
  Order_Receipt.EntityId,
  Entity.Name AS EntityName,
  OrdersView.ClientTypeName,
  OrdersView.ClientID,
  'OR' AS type,
  '' AS vendorname
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


CREATE VIEW get_research_govt_agencies_view AS
SELECT
    a.id,
    a.agencyname,
    a.addressline1,
    a.addressline2,
    a.suburb,
    a.city,
    a.state,
    a.country as countryid,
    b.name as country,
    a.zip,
    a.departmenttype as departmenttypeid,
    c.name as departmenttype,
    a.details,
    a.contactname,
    a.contactmail,
    a.contactphone,
    a.dated,
    a.createdby as createdbyid,
    concat_ws(' ',d.firstname,d.lastname) as createdby,
    a.isdeleted,
    a.maplink
FROM
    research_government_agencies a
LEFT JOIN
    country b ON a.country = b.id
LEFT JOIN
    departmenttype c ON a.departmenttype = c.id
LEFT JOIN
    usertable d ON a.createdby = d.id;


-- CREATE SEQUENCE IF NOT EXISTS research_government_agencies_id_seq OWNED BY research_government_agencies.id;
-- SELECT setval('research_government_agencies_id_seq', COALESCE(max(id), 0) + 1, false) FROM research_government_agencies;
-- ALTER TABLE research_government_agencies ALTER COLUMN id SET DEFAULT nextval('research_government_agencies_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS friends_id_seq OWNED BY friends.id;
-- SELECT setval('friends_id_seq', COALESCE(max(id), 0) + 1, false) FROM friends;
-- ALTER TABLE friends ALTER COLUMN id SET DEFAULT nextval('friends_id_seq');

CREATE VIEW get_research_friends_view AS
SELECT
    a.id,
    a.name,
    a.emailid,
    a.phoneno,
    a.contactname as friendof,
    a.societyname,
    a.employer,
    a.dated,
    a.isdeleted,
    a.createdby,
    a.suburb,
    a.city as cityid,
    b.city,
    a.state,
    a.country as countryid,
    c.name as country,
    a.notes,
    a.excludefrommailinglist
FROM
    friends a
LEFT JOIN
    cities b ON a.city = b.id
LEFT JOIN
    country c ON a.country = c.id;

-- CREATE TABLE mandaltypes(
--     mandalid int,
--     name text
-- );

CREATE VIEW lltenant_view AS
SELECT DISTINCT
    a.id,
    a.leavelicenseid,
    a.tenantid,
    concat_ws(' ',b.firstname,b.middlename,b.lastname) as tenantname,
    a.dated,
    a.createdby,
    a.isdeleted
FROM
    clientleavelicensetenant a
LEFT JOIN
    client b ON a.tenantid = b.id;

-- CREATE SEQUENCE IF NOT EXISTS banksandbranches_id_seq OWNED BY banksandbranches.id;
-- SELECT setval('banksandbranches_id_seq', COALESCE(max(id), 0) + 1, false) FROM banksandbranches;
-- ALTER TABLE banksandbranches ALTER COLUMN id SET DEFAULT nextval('banksandbranches_id_seq');




CREATE OR REPLACE VIEW orderinvoicelistview AS
SELECT order_invoice.id,
    order_invoice.orderid,
    order_invoice.invoicedate,
    order_invoice.invoiceamount,
    order_invoice.createdby AS createdbyid,
    order_invoice.isdeleted,
    (usertable.firstname || ' '::text) || usertable.lastname AS createdby,
    getmonthyear(order_invoice.invoicedate::timestamp without time zone) AS monthyear,
    getfinancialyear(order_invoice.invoicedate) AS fy,
    order_invoice.entityid,
    entity.name AS entityname,
    order_invoice.dated,
    orders.briefdescription AS orderdescription,
    (client.firstname || ' '::text) || client.lastname AS clientname,
    lob.name AS lobname,
    services.id AS serviceid,
    services.service,
    orders.clientid,
    'OI'::text AS type,
    ''::text AS vendorname,
    ''::text AS mode
FROM lob
     RIGHT JOIN services ON lob.id = services.lob
     RIGHT JOIN orders ON services.id = orders.service
     JOIN order_invoice ON orders.id = order_invoice.orderid
     JOIN client ON orders.clientid = client.id
     LEFT JOIN usertable ON order_invoice.createdby = usertable.id
     LEFT JOIN entity ON order_invoice.entityid = entity.id;

create or replace view ordervendorestimatelistview as
 SELECT order_vendorestimate.id,
    order_vendorestimate.vendorid,
    vendor.vendorname,
    orders.service AS serviceid,
    order_vendorestimate.orderid,
    orders.briefdescription,
    (client.firstname || ' '::text) || client.lastname AS clientname,
    entity.name AS entityname,
    services.service,
    services.lob AS lobid,
    getmonthyear(order_vendorestimate.estimatedate::timestamp without time zone) AS monthyear,
    getfinancialyear(order_vendorestimate.estimatedate) AS fy,
    lob.name AS lobname,
    orders.clientid,
    order_vendorestimate.invoicedate,
    order_vendorestimate.invoiceamount,
    orders.isdeleted,
    'VI' as type,
    '' as mode
   FROM vendor
     RIGHT JOIN order_vendorestimate ON vendor.id = order_vendorestimate.vendorid
     LEFT JOIN entity ON order_vendorestimate.entityid = entity.id
     LEFT JOIN orders ON order_vendorestimate.orderid = orders.id
     LEFT JOIN client ON orders.clientid = client.id
     JOIN services ON orders.service = services.id
     JOIN lob ON services.lob = lob.id
    WHERE order_vendorestimate.isdeleted = false;

CREATE OR REPLACE VIEW clientreceiptlistview AS 
 SELECT mode_of_payment.name AS paymentmode,
    (client.firstname || ' '::text) || client.lastname AS clientname,
    client_receipt.id,
    client_receipt.amount,
    client_receipt.recddate,
    client_receipt.paymentmode AS paymentmodeid,
    client_receipt.clientid,
    client_receipt.createdby AS createdbyid,
    client_receipt.isdeleted,
    client_receipt.entityid,
    entity.name AS entityname,
    getmonthyear(client_receipt.recddate::timestamp without time zone) AS monthyear,
    getfinancialyear(client_receipt.recddate) AS fy,
    'CR' as type,
    '' as vendorname,
    '' as orderid,
    '' as orderdescription,
    '' as service,
    '' as serviceid,
    '' as lobname
    
   FROM client_receipt
     LEFT JOIN usertable ON usertable.id = client_receipt.receivedby
     LEFT JOIN mode_of_payment ON client_receipt.paymentmode = mode_of_payment.id
     LEFT JOIN client ON client_receipt.clientid = client.id
     LEFT JOIN entity ON client_receipt.entityid = entity.id;


CREATE OR REPLACE VIEW orderreceiptlobview AS
SELECT 
    RecdDate AS date,
    MonthYear,
    SUM(Amount) AS orderreceiptamount,
    LOBName,
    Service,
    ServiceId
FROM 
    orderreceiptview
GROUP BY 
    LOBName,
    RecdDate,
    Service,
    ServiceId,
    MonthYear;
    
    
CREATE OR REPLACE VIEW orderpaymentlobview AS
SELECT
    OrderPaymentView.PaymentDate AS date,
    OrderPaymentView.MonthYear,
    SUM(OrderPaymentView.Amount) AS paymentamount,
    OrderPaymentView.LOBName,
    OrderPaymentView.Service,
    OrderPaymentView.ServiceId
FROM
    orderpaymentview
GROUP BY
    OrderPaymentView.LOBName,
    OrderPaymentView.PaymentDate,
    OrderPaymentView.Service,
    OrderPaymentView.ServiceId,
    OrderPaymentView.MonthYear;

CREATE OR REPLACE VIEW datewiselobserviceview AS
SELECT
    lobname,
    service,
    date,
    SUM(COALESCE(orderreceiptamount, 0)) AS orderreceiptamount,
    SUM(COALESCE(paymentamount, 0)) AS paymentamount,
    SUM(COALESCE(orderreceiptamount, 0)) - SUM(COALESCE(paymentamount, 0)) AS diff
FROM (
    SELECT
        lobname,
        service,
        orderreceiptamount,
        0 AS paymentamount,
        serviceid,
        date
    FROM
        orderreceiptlobview

    UNION ALL

    SELECT
        lobname,
        service,
        0 AS orderreceiptamount,
        paymentamount,
        serviceid,
        date
    FROM
        orderpaymentlobview
) AS tempdata
GROUP BY
    lobname,
    service,
    date;

CREATE OR REPLACE VIEW orderinvoiceview AS
 SELECT oi.id,
    oi.clientid,
    oi.orderid,
    oi.estimatedate,
    oi.estimateamount,
    oi.invoicedate,
    oi.invoiceamount,
    oi.quotedescription,
    oi.visibletoclient AS visibletoclientbit,
    oi.paymentsourceid,
    oi.dated,
    oi.createdby AS createdbyid,
    oi.isdeleted,
    (ut.firstname || ' '::text) || ut.lastname AS createdby,
    ov.clientname,
    ov.briefdescription AS orderdescription,
    ov.propertydescription,
    oi.baseamount,
    oi.tax,
        CASE
            WHEN oi.visibletoclient = true THEN 'Yes'::text
            ELSE 'No'::text
        END AS visibletoclient,
    ov.owner,
    oi.entityid,
    e.name AS entityname
   FROM order_invoice oi
     JOIN usertable ut ON oi.createdby = ut.id
     JOIN ordersview ov ON oi.orderid = ov.id
     LEFT JOIN entity e ON oi.entityid = e.id;

CREATE OR REPLACE VIEW PMABillingTrendView AS
 SELECT ct.clientname,
    ct.gy AS fy,
    COALESCE(ct.jan, 0::numeric) AS jan,
    COALESCE(ct.feb, 0::numeric) AS feb,
    COALESCE(ct.mar, 0::numeric) AS mar,
    COALESCE(ct.apr, 0::numeric) AS apr,
    COALESCE(ct.may, 0::numeric) AS may,
    COALESCE(ct.jun, 0::numeric) AS jun,
    COALESCE(ct.jul, 0::numeric) AS jul,
    COALESCE(ct.aug, 0::numeric) AS aug,
    COALESCE(ct.sep, 0::numeric) AS sep,
    COALESCE(ct.oct, 0::numeric) AS oct,
    COALESCE(ct.nov, 0::numeric) AS nov,
    COALESCE(ct."dec", 0::numeric) AS "dec"
   FROM crosstab('SELECT ClientName, EXTRACT(YEAR FROM InvoiceDate), EXTRACT(MONTH FROM InvoiceDate) AS MONTH, SUM(InvoiceAmount)
          FROM PMABillingListView
          GROUP BY ClientName, EXTRACT(YEAR FROM InvoiceDate), EXTRACT(MONTH FROM InvoiceDate)
          ORDER BY ClientName, EXTRACT(YEAR FROM InvoiceDate), EXTRACT(MONTH FROM InvoiceDate)'::text,
           'VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12)'::text) 
           ct(clientname text, gy text, jan numeric, feb numeric, mar numeric, apr numeric, may numeric, jun numeric, jul numeric, aug numeric, sep numeric, oct numeric, nov numeric, dec numeric);

CREATE VIEW RptBankstAmount AS

SELECT
    COALESCE(SUM(CASE WHEN BankSt.crdr = 'DR' THEN BankSt.Amount ELSE 0 END), 0) AS BankStAMount,
    BankSt.Date,
    BankSt.ModeofPayment,
    Mode_Of_payment.Name
FROM
    BankSt
INNER JOIN
    Mode_Of_payment ON BankSt.ModeofPayment = Mode_Of_payment.ID
GROUP BY
    BankSt.Date,
    BankSt.ModeofPayment,
    Mode_Of_payment.Name;

CREATE VIEW RptOrderAmount AS

SELECT
    COALESCE(SUM(Order_Receipt.Amount), 0) AS ORAmount,
    Order_Receipt.RecdDate AS Date,
    Mode_Of_payment.Name,
    Order_Receipt.PaymentMode
FROM
    Order_Receipt
INNER JOIN
    Mode_Of_payment ON Order_Receipt.PaymentMode = Mode_Of_payment.ID
WHERE
    Order_Receipt.IsDeleted = false
GROUP BY
    Order_Receipt.RecdDate,
    Mode_Of_payment.Name,
    Order_Receipt.PaymentMode;

CREATE VIEW RptClientAmount AS

SELECT
    COALESCE(SUM(Client_Receipt.Amount), 0) AS CRAMount,
    Client_Receipt.RecdDate AS Date,
    Mode_Of_payment.Name,
    Client_Receipt.PaymentMode
FROM
    Client_Receipt
INNER JOIN
    Mode_Of_payment ON Client_Receipt.PaymentMode = Mode_Of_payment.ID
WHERE
    Client_Receipt.IsDeleted = false
GROUP BY
    Client_Receipt.RecdDate,
    Mode_Of_payment.Name,
    Client_Receipt.PaymentMode;


CREATE VIEW BankReconcillationview AS

SELECT
    p.Date,
    p.PaymentMode,
    COALESCE(p.Bankst, 0) AS BankStAMount,
    COALESCE(p.ORAmount, 0) AS ORAmount,
    COALESCE(p.CRAMount, 0) AS CRAMount
FROM
    (
        SELECT
            COALESCE(BankSt.Date, ORAmount.Date, CRAMount.Date) AS Date,
            COALESCE(BankSt.Name, ORAmount.Name, CRAMount.Name) AS PaymentMode,
            COALESCE(BankSt.BankStAMount, 0) AS Bankst,
            COALESCE(ORAmount.ORAmount, 0) AS ORAmount,
            COALESCE(CRAMount.CRAMount, 0) AS CRAMount
        FROM
            RptBankstAmount AS BankSt
        FULL OUTER JOIN RptOrderAmount AS ORAmount ON BankSt.Date = ORAmount.Date AND BankSt.Name = ORAmount.Name
        FULL OUTER JOIN RptClientAmount AS CRAMount ON BankSt.Date = CRAMount.Date AND BankSt.Name = CRAMount.Name
    ) AS p;



CREATE VIEW rpt_daily_bank_receipts_reco AS
 SELECT bankreconcillationview.date,
    sum(bankreconcillationview.bankstamount) AS bankst_cr,
    sum(bankreconcillationview.cramount) AS client_receipt,
    sum(bankreconcillationview.oramount) AS order_receipt
   FROM bankreconcillationview
  WHERE bankreconcillationview.paymentmode = 'DAP-ICICI-42'::text AND bankreconcillationview.date >= '2022-01-01'::date AND bankreconcillationview.date <= '2022-10-01'::date
  GROUP BY bankreconcillationview.date
  ORDER BY bankreconcillationview.date DESC;

CREATE VIEW RptContractualPaymentAmount1 AS
 SELECT COALESCE(sum(ref_contractual_payments.amount), 0::numeric) AS cpamount,
    ref_contractual_payments.paidon AS date,
    mode_of_payment.name,
    ref_contractual_payments.paymentmode
   FROM ref_contractual_payments
     JOIN mode_of_payment ON ref_contractual_payments.paymentmode = mode_of_payment.id
  WHERE ref_contractual_payments.isdeleted = false
  GROUP BY ref_contractual_payments.paidon, mode_of_payment.name, ref_contractual_payments.paymentmode;

CREATE VIEW rpt_bank_transfer_reco AS
 SELECT 'OrderReceipt'::text AS type,
    orderreceiptview.orderdescription,
    orderreceiptview.recddate AS date,
    orderreceiptview.paymentmode AS mode,
    orderreceiptview.amount
   FROM orderreceiptview
  WHERE orderreceiptview.orderid = 429163 AND orderreceiptview.recddate > '2016-03-31'::date AND orderreceiptview.isdeleted = false
UNION ALL
 SELECT 'OrderPayment'::text AS type,
    orderpaymentview.orderdescription,
    orderpaymentview.paymentdate AS date,
    orderpaymentview.mode_of_payment AS mode,
    orderpaymentview.amount * '-1'::integer::numeric AS amount
   FROM orderpaymentview
  WHERE orderpaymentview.orderid = 429163 AND orderpaymentview.paymentdate > '2016-03-31'::date AND orderpaymentview.isdeleted = false;

CREATE VIEW vendor_invoice AS
 SELECT order_invoice.id,
    order_invoice.invoicedate,
    order_invoice.invoiceamount,
    order_invoice.quotedescription,
    client.firstname,
    client.lastname,
    vendor.vendorname,
    orders.briefdescription
   FROM vendor
     JOIN orders ON vendor.id = orders.vendorid
     JOIN order_invoice ON orders.id = order_invoice.orderid
     JOIN client ON order_invoice.clientid = client.id;

CREATE VIEW PMABillingListView AS
 SELECT oiv.clientname,
    oiv.orderdescription,
    oiv.baseamount,
    oiv.propertydescription,
    oiv.tax,
    oiv.entityname,
    oiv.entityid,
    oiv.owner,
    oiv.createdby,
    oiv.isdeleted,
    oiv.createdbyid,
    oiv.dated,
    oiv.paymentsourceid,
    oiv.quotedescription,
    oiv.invoiceamount,
    oiv.invoicedate,
    oiv.estimateamount,
    oiv.estimatedate,
    ov.service,
    ov.serviceid,
    EXTRACT(MONTH FROM oiv.invoicedate) AS invoicemonth,
    EXTRACT(year FROM oiv.invoicedate) AS invoiceyear
   FROM orderinvoiceview oiv
     JOIN ordersview ov ON oiv.orderid = ov.id AND ov.serviceid = 62;

CREATE OR REPLACE VIEW clientreceiptview AS
SELECT
    mode_of_payment.name AS paymentmode,
    u1.firstname || ' ' || u1.lastname AS receivedby,
    u2.firstname || ' ' || u2.lastname AS createdby,
    c.firstname || ' ' || c.lastname AS clientname,
    client_receipt.id,
    client_receipt.receivedby AS receivedbyid,
    client_receipt.amount,
    client_receipt.recddate,
    client_receipt.paymentmode AS paymentmodeid,
    client_receipt.clientid,
    client_receipt.paymentstatus,
    client_receipt.receiptdesc,
    client_receipt.banktransactionid,
    client_receipt.paymentsource AS paymentsourceid,
    client_receipt.dated,
    client_receipt.createdby AS createdbyid,
    client_receipt.isdeleted,
    payment_source.name AS paymentsource,
    client_receipt.tds,
    CASE WHEN client_receipt.syncronized = 'true' THEN 'Syncronized' ELSE 'Asyncronized' END AS syncronized,
    client_receipt.visibletoclient,
    client_receipt.serviceamount,
    client_receipt.reimbursementamount,
    CASE WHEN client_receipt.visibletoclient = 'true' THEN 'Yes' ELSE 'No' END AS visible_to_client,
    client_receipt.entityid,
    entity.name AS entityname,
    howreceived.name,
    client_receipt.howreceivedid,
    client_receipt.officeid,
    office.name AS officename
FROM
    client_receipt
INNER JOIN usertable u1 ON u1.id = client_receipt.receivedby
INNER JOIN office ON office.id = client_receipt.officeid
INNER JOIN mode_of_payment ON client_receipt.paymentmode = mode_of_payment.id
INNER JOIN usertable u2 ON u2.id = client_receipt.createdby
INNER JOIN client c ON client_receipt.clientid = c.id
LEFT OUTER JOIN howreceived ON client_receipt.howreceivedid = howreceived.id
LEFT OUTER JOIN entity ON client_receipt.entityid = entity.id
LEFT OUTER JOIN payment_source ON client_receipt.paymentsource = payment_source.id;


create or replace view rpt_pmaclient as 

 SELECT 'Invoice'::text AS type,
    ordersview.clientname,
    order_invoice.id,
    order_invoice.invoicedate AS date,
    order_invoice.invoiceamount AS amount,
    NULL::numeric AS tds,
    replace(replace(ordersview.briefdescription, chr(10), ''::text), chr(13), ''::text) AS orderdetails,
    entity.name AS entity,
    services.service,
    replace(replace(order_invoice.quotedescription, chr(10), ''::text), chr(13), ''::text) AS details,
    ''::text AS mode,
    ordersview.clienttypename AS clienttype,
    ordersview.id AS orderid,
    ordersview.clientid,
    getmonthyear(order_invoice.invoicedate::timestamp without time zone) AS monthyear,
    getfinancialyear(order_invoice.invoicedate) AS fy,
    ordersview.lobname
   FROM order_invoice
     LEFT JOIN ordersview ON ordersview.id = order_invoice.orderid
     LEFT JOIN entity ON entity.id = order_invoice.entityid
     LEFT JOIN services ON services.id = ordersview.serviceid
  WHERE ordersview.clienttypename ilike '%PMA%'::text
UNION ALL
 SELECT 'Payment'::text AS type,
    clientview.fullname AS clientname,
    clientreceiptview.id,
    clientreceiptview.recddate AS date,
    '-1'::integer::numeric * clientreceiptview.amount AS amount,
    clientreceiptview.tds,
    NULL::text AS orderdetails,
    entity.name AS entity,
    NULL::text AS service,
    howreceived.name AS details,
    clientreceiptview.paymentmode AS mode,
    clientview.clienttypename AS clienttype,
    NULL::bigint AS orderid,
    clientview.id AS clientid,
    getmonthyear(clientreceiptview.recddate::timestamp without time zone) AS monthyear,
    getfinancialyear(clientreceiptview.recddate) AS fy,
    NULL::text AS lobname
   FROM clientview
     JOIN clientreceiptview ON clientview.id = clientreceiptview.clientid
     LEFT JOIN entity ON clientreceiptview.entityid = entity.id
     LEFT JOIN howreceived ON clientreceiptview.howreceivedid = howreceived.id
  WHERE clientview.clienttypename ilike '%PMA%'::text;

CREATE VIEW rpt_pmaclient_receivables AS
SELECT 
    clientname AS clientname,
    SUM(amount) AS amount
FROM rpt_pmaclient
WHERE entity LIKE '%CURA%' AND 
      type NOT LIKE '%OrderRec%'
GROUP BY clientname;

-- CREATE SEQUENCE IF NOT EXISTS architech_id_seq OWNED BY architech.id;
-- SELECT setval('architech_id_seq', COALESCE(max(id), 0) + 1, false) FROM architech;
-- ALTER TABLE architech ALTER COLUMN id SET DEFAULT nextval('architech_id_seq');

-- CREATE SEQUENCE IF NOT EXISTS colleges_id_seq OWNED BY colleges.id;
-- SELECT setval('colleges_id_seq', COALESCE(max(id), 0) + 1, false) FROM colleges;
-- ALTER TABLE colleges ALTER COLUMN id SET DEFAULT nextval('colleges_id_seq');

CREATE VIEW get_research_architect_view AS
SELECT
    a.id,
    a.name,
    a.emailid,
    a.phoneno,
    a.project,
    a.societyname,
    a.dated,
    a.createdby,
    concat_ws(' ',b.firstname,b.lastname) as createdbyname,
    a.isdeleted,
    a.suburb,
    a.city as cityid,
    c.city,
    a.state,
    a.country as countryid,
    d.name as country,
    a.excludefrommailinglist
FROM
    architech a
LEFT JOIN
    usertable b ON a.createdby=b.id
LEFT JOIN
    cities c ON a.city = c.id
LEFT JOIN
    country d ON a.country = d.id;

CREATE VIEW get_research_colleges_view AS
SELECT DISTINCT
    a.id,
    a.name,
    a.typeid,
    e.name as type,
    a.emailid,
    a.phoneno,
    a.dated,
    a.createdby,
    concat_ws(' ',b.firstname,b.lastname) as createdbyname,
    a.isdeleted,
    a.suburb,
    a.city as cityid,
    c.city,
    a.state,
    a.country as countryid,
    d.name as country,
    a.website,
    a.email1,
    a.email2,
    a.contactname1,
    a.contactname2,
    a.phoneno1,
    a.phoneno2,
    a.excludefrommailinglist
FROM
    colleges a
LEFT JOIN
    usertable b ON a.createdby = b.id
LEFT JOIN
    cities c ON a.city = c.id
LEFT JOIN
    country d ON a.country = d.id
LEFT JOIN
    collegetypes e ON a.typeid = e.id;



-- CREATE SEQUENCE IF NOT EXISTS owners_id_seq OWNED BY owners.id;
-- SELECT setval('owners_id_seq', COALESCE(max(id), 0) + 1, false) FROM owners;
-- ALTER TABLE owners ALTER COLUMN id SET DEFAULT nextval('owners_id_seq');

CREATE VIEW clientstatementview AS
SELECT
    'Invoice' AS type,
    ov.clientname,
    oi.id,
    oi.invoicedate AS date,
    oi.invoiceamount AS amount,
    NULL AS tds,
    ov.briefdescription AS orderdetails,
    e.name AS entity,
    s.service,
    oi.quotedescription AS details,
    oi.visibletoclient,
    ov.clientid,
    '' AS mode,
    ov.lobname AS lob_name
FROM
    order_invoice oi
LEFT JOIN
    ordersview ov ON ov.id = oi.orderid
LEFT JOIN
    entity e ON e.id = oi.entityid
LEFT JOIN
    services s ON s.id = ov.serviceid

UNION

SELECT
    'C Receipt' AS type,
    cv.fullname,
    crv.id,
    crv.recddate AS date,
    crv.amount AS amount,
    crv.tds,
    NULL AS orderdetails,
    e.name AS entity,
    NULL AS service,
    crv.receiptdesc AS details,
    crv.visibletoclient,
    cv.id,
    crv.paymentmode AS mode,
    '' AS lob_name
FROM
    clientview cv
INNER JOIN
    clientreceiptview crv ON cv.id = crv.clientid
LEFT JOIN
    entity e ON crv.entityid = e.id

UNION

SELECT
    'Payment' AS type,
    cv.fullname,
    opv.id,
    opv.paymentdate AS date,
    opv.amount AS amount,
    opv.tds,
    opv.orderdescription AS orderdetails,
    e.name AS entity,
    opv.service AS service,
    opv.description AS details,
    FALSE AS visible_to_client,
    cv.id,
    opv.mode_of_payment AS mode,
    opv.lobname AS lob_name
FROM
    clientview cv
INNER JOIN
    orderpaymentview opv ON cv.id = opv.clientid
LEFT JOIN
    entity e ON opv.entityid = e.id

UNION

SELECT
    'Order Receipt' AS type,
    cv.fullname,
    orv.id,
    orv.recddate AS date,
    orv.amount AS amount,
    orv.tds,
    orv.orderdescription AS orderdetails,
    e.name AS entity,
    orv.service AS service,
    orv.receiptdesc AS details,
    FALSE AS visible_to_client,
    cv.id AS clientid,
    orv.paymentmode AS mode,
    orv.lobname AS lob_name
FROM
    clientview cv
INNER JOIN
    orderreceiptview orv ON cv.id = orv.clientid
LEFT JOIN
    entity e ON orv.entityid = e.id;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW duplicateclients AS
SELECT
    c.firstname,
    c.lastname,
    COUNT(c.email1) AS count,
    c.clienttype,
    ct.name AS clienttypename,
    c.firstname || ' ' || c.lastname AS clientname
FROM
    client c
INNER JOIN
    client_type ct ON c.clienttype = ct.id
GROUP BY
    c.email1,
    c.firstname,
    c.lastname,
    c.clienttype,
    ct.name,
    c.isdeleted
HAVING
    COUNT(c.email1) > 1
    AND c.isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW clientbankdetails AS
SELECT
    c.firstname,
    c.lastname,
    ca.onlinemailid,
    cbi.bankname,
    cbi.bankbranch,
    cbi.bankaccountno,
    cbi.bankaccountholdername,
    cbi.bankcity,
    cbi.bankifsccode,
    cbi.bankaccounttype,
    c.firstname || ' ' || c.lastname AS clientname
FROM
    client_access ca
INNER JOIN
    client c ON ca.clientid = c.id
INNER JOIN
    client_bank_info cbi ON c.id = cbi.clientid;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW rpt_nonpmaclient
AS
SELECT 'Invoice'::text AS type,
    ov.clientname,
    oi.id,
    oi.invoicedate AS date,
    oi.invoiceamount AS amount,
    NULL::numeric AS tds,
    replace(replace(ov.briefdescription, chr(10), ''::text), chr(13), ''::text) AS orderdetails,
    e.name AS entity,
    s.service,
    replace(replace(oi.quotedescription, chr(10), ''::text), chr(13), ''::text) AS details,
    ''::text AS mode,
    ov.clienttypename AS client_type,
    ov.id AS order_id,
    ov.clientid,
    getmonthyear(oi.invoicedate::timestamp without time zone) AS monthyear,
    getfinancialyear(oi.invoicedate) AS fy,
    ov.lobname
   FROM order_invoice oi
     LEFT JOIN ordersview ov ON ov.id = oi.orderid
     LEFT JOIN entity e ON e.id = oi.entityid
     LEFT JOIN services s ON s.id = ov.serviceid
WHERE ov.clienttypename NOT LIKE '%PMA%' AND ov.clientname NOT LIKE '%1-%'

UNION ALL
 SELECT 'Payment'::text AS type,
    cv.fullname AS clientname,
    crv.id,
    crv.recddate AS date,
    '-1'::integer::numeric * crv.amount AS amount,
    crv.tds,
    NULL::text AS orderdetails,
    e.name AS entity,
    NULL::text AS service,
    hr.name AS details,
    crv.paymentmode AS mode,
    cv.clienttypename AS client_type,
    NULL::bigint AS order_id,
    cv.id AS clientid,
    getmonthyear(crv.recddate::timestamp without time zone) AS monthyear,
    getfinancialyear(crv.recddate) AS fy,
    NULL::text AS lobname
   FROM clientview cv
     JOIN clientreceiptview crv ON cv.id = crv.clientid
     LEFT JOIN entity e ON crv.entityid = e.id
     LEFT JOIN howreceived hr ON crv.howreceivedid = hr.id
WHERE cv.clienttypename NOT LIKE '%PMA%' AND cv.firstname NOT LIKE '%1-%'
UNION ALL
 SELECT 'OrderRec'::text AS type,
    cv.fullname AS clientname,
    orv.id,
    orv.recddate AS date,
    '-1'::integer::numeric * orv.amount AS amount,
    orv.tds,
    orv.orderdescription AS orderdetails,
    e.name AS entity,
    orv.service,
    orv.receiptdesc AS details,
    orv.paymentmode AS mode,
    cv.clienttypename AS client_type,
    orv.orderid AS order_id,
    cv.id AS clientid,
    getmonthyear(orv.recddate::timestamp without time zone) AS monthyear,
    getfinancialyear(orv.recddate) AS fy,
    orv.lobname
   FROM clientview cv
     JOIN orderreceiptview orv ON cv.id = orv.clientid
     LEFT JOIN entity e ON orv.entityid = e.id
WHERE cv.clienttypename NOT LIKE '%PMA%' AND cv.firstname NOT LIKE '%1-%';



-- CREATE VIEW rpt_nonpmaclient AS
-- SELECT
--     'Invoice' AS type,
--     ov.clientname,
--     oi.id,
--     oi.invoicedate AS date,
--     oi.invoiceamount AS amount,
--     NULL AS tds,
--     REPLACE(REPLACE(ov.briefdescription, CHR(10), ''), CHR(13), '') AS orderdetails,
--     e.name AS entity,
--     s.service,
--     REPLACE(REPLACE(oi.quotedescription, CHR(10), ''), CHR(13), '') AS details,
--     '' AS mode,
--     ov.clienttypename AS client_type,
--     ov.id AS order_id,
--     ov.clientid AS clientid,
--     getmonthyear(oi.invoicedate) AS monthyear,
--     getfinancialyear(oi.invoicedate) AS fy,
--     ov.lobname AS lobname
-- FROM
--     order_invoice oi
-- LEFT JOIN
--     ordersview ov ON ov.id = oi.orderid
-- LEFT JOIN
--     entity e ON e.id = oi.entityid
-- LEFT JOIN
--     services s ON s.id = ov.serviceid
-- WHERE
--     ov.clienttypename NOT LIKE 'pma - owner' AND
--     ov.clientname NOT LIKE '%1-%'

-- UNION ALL

-- SELECT
--     'Payment' AS type,
--     cv.fullname,
--     crv.id,
--     crv.recddate AS date,
--     -1 * crv.amount AS amount,
--     crv.tds,
--     NULL AS orderdetails,
--     e.name AS entity,
--     NULL AS service,
--     hr.name AS details,
--     crv.paymentmode AS mode,
--     cv.clienttypename AS client_type,
--     NULL AS order_id,
--     cv.id AS clientid,
--     getmonthyear(crv.recddate) AS monthyear,
--     getfinancialyear(crv.recddate) AS fy,
--     NULL AS lobname
-- FROM
--     clientview cv
-- INNER JOIN
--     clientreceiptview crv ON cv.id = crv.clientid
-- LEFT JOIN
--     entity e ON crv.entityid = e.id
-- LEFT JOIN
--     howreceived hr ON crv.howreceivedid = hr.id
-- WHERE
--     cv.clienttypename NOT LIKE 'pma - owner' AND
--     cv.firstname NOT LIKE '%1-%'

-- UNION ALL

-- SELECT
--     'OrderRec' AS type,
--     cv.fullname,
--     orv.id,
--     orv.recddate AS date,
--     -1 * orv.amount AS amount,
--     orv.tds,
--     orv.orderdescription AS orderdetails,
--     e.name AS entity,
--     orv.service AS service,
--     orv.receiptdesc AS details,
--     orv.paymentmode AS mode,
--     cv.clienttypename AS client_type,
--     orv.orderid AS order_id,
--     cv.id AS clientid,
--     getmonthyear(orv.recddate) AS monthyear,
--     getfinancialyear(orv.recddate) AS fy,
--     orv.lobname AS lobname
-- FROM
--     clientview cv
-- INNER JOIN
--     orderreceiptview orv ON cv.id = orv.clientid
-- LEFT JOIN
--     entity e ON orv.entityid = e.id
-- WHERE
--     cv.clienttypename NOT LIKE 'pma - owner' AND
--     cv.firstname NOT LIKE '%1-%';


-- CREATE VIEW client_property_leave_license_detailsview AS
-- SELECT 
--     CASE 
--         WHEN cplld.active = 'true' THEN 'Active' 
--         ELSE 'Inactive' 
--     END AS status,
--     cplld.clientpropertyid,
--     cplld.orderid,
--     cplld.startdate,
--     cplld.vacatingdate,
--     cplld.durationinmonth,
--     cplld.actualenddate,
--     cplld.depositamount,
--     cplld.rentamount,
--     cplld.registrationtype,
--     cplld.rentpaymentdate,
--     cplld.paymentcycle,
--     cplld.reasonforclosure,
--     cplld.noticeperiodindays,
--     cplld.modeofrentpaymentid,
--     cplld.clientpropertyorderid,
--     cplld.signedby,
--     cplld.active,
--     cplld.tenantsearchmode AS tenantsearchmodeid,
--     cplld.llscancopy,
--     cplld.pvscancopy,
--     cplld.dated,
--     cplld.createdby AS expr2,
--     cplld.isdeleted,
--     tsm.name AS tenantsearchmode,
--     cplld.id,
--     cplld.comments,
--     pv.clientname,
--     pv.propertydescription,
--     ov.propertydescription AS expr1,
--     getmonthyear(cplld.startdate) AS startdatemonthyear,
--     getmonthyear(cplld.actualenddate) AS enddatemonthyear,
--     ov.orderstatus,
--     ov.status AS orderstatusid,
--     pv.clientid,
--     pv.propertytaxnumber,
--     pv.property_status,
--     pv.electricitybillingunit,
--     pv.electricityconsumernumber
-- FROM 
--     client_property_leave_license_details cplld
-- INNER JOIN
--     propertiesview pv ON cplld.clientpropertyid = pv.id
-- LEFT OUTER JOIN
--     tenant_search_mode tsm ON cplld.tenantsearchmode = tsm.id
-- LEFT OUTER JOIN
--     ordersview ov ON cplld.orderid = ov.id
-- WHERE 
--     cplld.isdeleted = false;

CREATE OR REPLACE VIEW client_property_leave_license_detailsview AS
SELECT
        CASE
            WHEN cplld.active = true THEN 'Active'::text
            ELSE 'Inactive'::text
        END AS status,
    cplld.clientpropertyid,
    cplld.orderid,
    cplld.startdate,
    cplld.vacatingdate,
    cplld.durationinmonth,
    cplld.actualenddate,
    cplld.depositamount,
    cplld.rentamount,
    cplld.registrationtype,
    cplld.rentpaymentdate,
    cplld.paymentcycle,
    cplld.reasonforclosure,
    cplld.noticeperiodindays,
    cplld.modeofrentpaymentid,
    cplld.clientpropertyorderid,
    cplld.signedby,
    cplld.active,
    cplld.tenantsearchmode AS tenantsearchmodeid,
    cplld.llscancopy,
    cplld.pvscancopy,
    cplld.dated,
    cplld.createdby AS expr2,
    cplld.isdeleted,
    cplld.id,
    cplld.comments,
    pv.clientname,
    pv.propertydescription,
    ov.propertydescription AS expr1,
    ( SELECT getmonthyear(cplld.startdate::timestamp without time zone) AS getmonthyear) AS startdatemonthyear,
    ( SELECT getmonthyear(cplld.actualenddate::timestamp without time zone) AS getmonthyear) AS enddatemonthyear,
    ov.orderstatus,
    ov.status AS orderstatusid,
    pv.clientid,
    pv.propertytaxnumber,
    pv.property_status,
    pv.electricitybillingunit,
    pv.electricityconsumernumber,
    ov.service,
    ov.lobname,
    ov.entityname,
    cv.clienttype,
    cv.clienttypename
   FROM client_property_leave_license_details cplld
     JOIN propertiesview pv ON cplld.clientpropertyid = pv.id
     JOIN clientview cv ON pv.clientid = cv.id
     LEFT JOIN ordersview ov ON cplld.orderid = ov.id;



CREATE VIEW rpt_client_property_caretaking_agreementview AS
SELECT
    cpca.id,
    cpca.clientpropertyid,
    cpca.startdate,
    cpca.enddate,
    cpca.actualenddate,
    cpca.monthlymaintenancedate,
    cpca.monthlymaintenanceamount,
    cpca.active,
    cpca.scancopy,
    cpca.reasonforearlyterminationifapplicable,
    cpca.dated,
    cpca.createdby AS createdbyid,
    cpca.isdeleted,
    ut.firstname || ' ' || ut.lastname AS createdby,
    CASE
        WHEN cpca.active = TRUE THEN 'Active'
        ELSE 'Inactive'
    END AS status,
    pv.clientname,
    pv.propertydescription,
    pv.property_status AS propertystatus,
    pv.electricitybillingduedate,
    pv.electricitybillingunit,
    pv.electricityconsumernumber,
    pv.propertytaxnumber,
    cpca.description,
    lnl.startdate AS lnlstartdate,
    lnl.actualenddate AS lnlenddate,
    lnl.rentamount,
    cpca.vacant,
    cpca.rented,
    cpca.fixed,
    cpca.vacanttax,
    cpca.rentedtax,
    cpca.fixedtax,
    cpca.electricitybillcreated,
    cpca.propertytaxbillcreated,
    cpca.pipedgasbillcreated,
    cpca.societyduesbillcreated,
    cpca.advanceforreimbursementcreated,
    cpca.createclientportalaccount,
    cpca.orderid,
    o.briefdescription AS orderdescription,
    pv.clientid,
    cli.fulllegalname,
    cv.clienttypename,
    cpca.poastartdate,
    cpca.poaenddate,
    cpca.ptaxpaidtilldate,
    cpca.societyduespaidtilldate,
    cpca.poaholder
FROM
    client_property_caretaking_agreement cpca
INNER JOIN
    usertable ut ON cpca.createdby = ut.id
INNER JOIN
    propertiesview pv ON cpca.clientpropertyid = pv.id
LEFT OUTER JOIN
    clientview cv ON pv.clientid = cv.id
LEFT OUTER JOIN
    client_legal_info cli ON pv.clientid = cli.clientid
LEFT OUTER JOIN
    orders o ON cpca.orderid = o.id
LEFT OUTER JOIN
    client_property_leave_license_detailsview lnl ON lnl.clientpropertyid = cpca.clientpropertyid AND lnl.active = TRUE;



-- CREATE VIEW client_property_leave_license_detailsview AS
-- SELECT 
--     CASE 
--         WHEN cplld.active = 'true' THEN 'Active' 
--         ELSE 'Inactive' 
--     END AS status,
--     cplld.clientpropertyid,
--     cplld.orderid,
--     cplld.startdate,
--     cplld.vacatingdate,
--     cplld.durationinmonth,
--     cplld.actualenddate,
--     cplld.depositamount,
--     cplld.rentamount,
--     cplld.registrationtype,
--     cplld.rentpaymentdate,
--     cplld.paymentcycle,
--     cplld.reasonforclosure,
--     cplld.noticeperiodindays,
--     cplld.modeofrentpaymentid,
--     cplld.clientpropertyorderid,
--     cplld.signedby,
--     cplld.active,
--     cplld.llscancopy,
--     cplld.pvscancopy,
--     cplld.dated,
--     cplld.createdby AS expr2,
--     cplld.isdeleted,
--     cplld.id,
--     cplld.comments,
--     pv.clientname,
--     pv.propertydescription,
--     ov.propertydescription AS expr1,
--     getmonthyear(cplld.startdate) AS startdatemonthyear,
--     getmonthyear(cplld.actualenddate) AS enddatemonthyear,
--     ov.orderstatus,
--     ov.status AS orderstatusid,
--     pv.clientid,
--     pv.propertytaxnumber,
--     pv.property_status,
--     pv.electricitybillingunit,
--     pv.electricityconsumernumber
-- FROM 
--     client_property_leave_license_details cplld
-- INNER JOIN
--     propertiesview pv ON cplld.clientpropertyid = pv.id
-- LEFT OUTER JOIN
--     ordersview ov ON cplld.orderid = ov.id
-- WHERE 
--     cplld.isdeleted = false;



-----------------------------------------------------------------------------------------------------------------------------------------




CREATE VIEW projectsview AS
SELECT 
    project.id,
    project.builderid,
    project.addressline1,
    project.addressline2,
    project.suburb,
    project.city AS cityid,
    project.state,
    project.country,
    project.zip,
    project.project_type,
    project.mailgroup1,
    project.mailgroup2,
    project.website,
    project.project_legal_status,
    project.rules,
    project.completionyear,
    project.jurisdiction,
    project.taluka,
    project.corporationward,
    project.policechowkey,
    project.policestation,
    project.maintenance_details,
    project.numberoffloors,
    project.numberofbuildings,
    project.approxtotalunits,
    project.tenantstudentsallowed,
    project.tenantworkingbachelorsallowed,
    project.tenantforeignersallowed,
    project.otherdetails,
    project.duespayablemonth,
    project.dated,
    project.createdby AS createdbyid,
    project.isdeleted,
    cities.city,
    country.name AS countryname,
    usertable.firstname || ' ' || usertable.lastname AS createdby,
    project.projectname,
    project.nearestlandmark,
    builder.buildername,
    project_type.name AS projecttype,
    CASE 
        WHEN project.tenantstudentsallowed = '1' THEN 'Tenant Students Allowed,'
        ELSE '' 
    END 
    || CASE 
        WHEN project.tenantworkingbachelorsallowed = '1' THEN ' Tenant Working Bachelors Allowed,'
        ELSE '' 
    END 
    || CASE 
        WHEN project.tenantforeignersallowed = '1' THEN ' Tenant Foreigners Allowed' 
        ELSE '' 
    END AS tenantallowed
FROM     
    project
INNER JOIN
    cities ON project.city = cities.id
INNER JOIN
    country ON project.country = country.id
INNER JOIN
    usertable ON project.createdby = usertable.id
INNER JOIN
    builder ON project.builderid = builder.id
INNER JOIN
    project_type ON project.project_type = project_type.id;

CREATE VIEW projectcontactsview AS
SELECT
    pv.buildername,
    pv.projectname,
    pv.city,
    pv.suburb,
    pc.contactname,
    pc.phone,
    pc.email,
    pc.effectivedate,
    pc.role,
    pc.tenureenddate,
    pc.details
FROM
    project_contacts pc
INNER JOIN
    projectsview pv ON pc.projectid = pv.id;
------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW ClientSummaryView AS
SELECT
    OrdersView.ID AS OrderId,
    COALESCE(OrdersView.ClientName, '') as ClientName,
    COALESCE(OrdersView.PropertyDescription, '') as PropertyDescription,
    COALESCE(OrdersView.BriefDescription, '') as BriefDescription,
    COALESCE(OrdersView.Service, '') as Service,
    COALESCE(SumVendorEstimate.EstimateAmount, 0) AS VendorEstimate,
    COALESCE(SumVendorEstimate.InvoiceAmount, 0) AS VendorInvoiceAmount,
    COALESCE(SumPayment.paymentamount, 0) AS SumPayment,
    COALESCE(SumInvoice.EstimateAmount, 0) as EstimateAmount,
    CASE
        WHEN OrdersView.OrderStatus = 'Cancelled' THEN 0
        ELSE
            CASE
                WHEN COALESCE(SumInvoice.invoiceamount, 0) = 0 THEN SumInvoice.EstimateAmount
                ELSE SumInvoice.invoiceamount
            END
    END - COALESCE(SumReceipt.receiptamount, 0) AS ComputedPending,
    COALESCE(SumReceipt.receiptamount, 0) AS SumReceipt,
    OrdersView.OrderDate,
    COALESCE(OrdersView.OrderStatus, '') as OrderStatus,
    COALESCE(SumInvoice.invoiceamount, 0) as invoiceamount,
    COALESCE(SumReceipt.receiptamount - SumPayment.paymentamount - SumInvoice.TaxAmount, 0) AS Profit,
    COALESCE(OrdersView.Owner, 0) as Owner,
    COALESCE(OrdersView.Status, 0) AS OrderStatusId,
    COALESCE(OrdersView.LOBName, '') as LOBName,
    COALESCE(OrdersView.OwnerName, '') as OwnerName,
    COALESCE(OrdersView.ServiceType, '') as ServiceType,
    OrdersView.ClientID,
    COALESCE(OrdersView.ServiceId, 0) as ServiceId,
    COALESCE(OrdersView.Ageing, 0) as Ageing,
    COALESCE(OrdersView.EntityName, '') as EntityName
FROM
    OrdersView
LEFT OUTER JOIN (
    SELECT
        OrderID,
        SUM(InvoiceAmount) AS invoiceamount,
        SUM(EstimateAmount) AS EstimateAmount,
        SUM(COALESCE(Tax, 0)) AS TaxAmount
    FROM
        Order_Invoice
    GROUP BY
        OrderID
) AS SumInvoice ON OrdersView.ID = SumInvoice.OrderID
LEFT OUTER JOIN (
    SELECT
        OrderID,
        SUM(Amount + COALESCE(TDS, 0)) AS receiptamount
    FROM
        Order_Receipt
    GROUP BY
        OrderID
) AS SumReceipt ON OrdersView.ID = SumReceipt.OrderID
LEFT OUTER JOIN (
    SELECT
        OrderID,
        SUM(Amount) AS paymentamount
    FROM
        Order_Payment
    GROUP BY
        OrderID
) AS SumPayment ON OrdersView.ID = SumPayment.OrderID
LEFT OUTER JOIN (
    SELECT
        OrderID,
        SUM(InvoiceAmount) AS InvoiceAmount,
        SUM(Amount) AS EstimateAmount
    FROM
        Order_VendorEstimate
    GROUP BY
        OrderID
) AS SumVendorEstimate ON OrdersView.ID = SumVendorEstimate.OrderID;


    CREATE OR REPLACE VIEW rpt_clientswithadvanceholdingamounts AS
    SELECT clientsummaryview.clientname,
        COALESCE(sum(clientsummaryview.sumpayment), 0::numeric) AS payments,
        COALESCE(sum(clientsummaryview.sumreceipt), 0::numeric) AS receipts,
        row_number() OVER (ORDER BY clientsummaryview.clientname) AS rn
    FROM clientsummaryview
    WHERE clientsummaryview.service ~~* '%Advance hold%'::text
    GROUP BY clientsummaryview.clientname
    HAVING COALESCE(sum(clientsummaryview.sumpayment), 0::numeric) < COALESCE(sum(clientsummaryview.sumreceipt), 0::numeric);



------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE VIEW rpt_clients_transactions AS
SELECT
    'Invoice' AS type,
    ov.clientname,
    oi.id,
    oi.invoicedate AS date,
    oi.invoiceamount AS amount,
    NULL AS tds,
    REPLACE(REPLACE(ov.briefdescription, CHR(10), ''), CHR(13), '') AS orderdetails,
    e.name AS entity,
    s.service,
    REPLACE(REPLACE(oi.quotedescription, CHR(10), ''), CHR(13), '') AS details,
    '' AS mode,
    ov.clienttypename AS client_type,
    ov.id AS order_id,
    ov.clientid AS clientid,
    getmonthyear(oi.invoicedate) AS monthyear,
    getfinancialyear(oi.invoicedate) AS fy,
    ov.lobname
FROM
    order_invoice oi
LEFT JOIN
    ordersview ov ON ov.id = oi.orderid
LEFT JOIN
    entity e ON e.id = oi.entityid
LEFT JOIN
    services s ON s.id = ov.serviceid
WHERE
    LOWER(ov.clienttypename) = '%pma%'

UNION ALL

SELECT
    'Payment' AS type,
    cv.fullname,
    crv.id,
    crv.recddate AS date,
    -1 * crv.amount AS amount,
    crv.tds,
    NULL AS orderdetails,
    e.name AS entity,
    NULL AS service,
    hr.name AS details,
    crv.paymentmode AS mode,
    cv.clienttypename,
    NULL AS order_id,
    cv.id AS clientid,
    getmonthyear(crv.recddate) AS monthyear,
    getfinancialyear(crv.recddate) AS fy,
    NULL AS lobname
FROM
    clientview cv
INNER JOIN
    clientreceiptview crv ON cv.id = crv.clientid
LEFT JOIN
    entity e ON crv.entityid = e.id
LEFT JOIN
    howreceived hr ON crv.howreceivedid = hr.id
WHERE
    LOWER(cv.clienttypename) = '%pma%'

UNION ALL

SELECT
    'OrderRec' AS type,
    cv.fullname,
    orv.id,
    orv.recddate AS date,
    -1 * orv.amount AS amount,
    orv.tds,
    orv.orderdescription AS orderdetails,
    e.name AS entity,
    orv.service,
    orv.receiptdesc AS details,
    orv.paymentmode AS mode,
    cv.clienttypename,
    NULL AS order_id,
    cv.id AS clientid,
    getmonthyear(orv.recddate) AS monthyear,
    getfinancialyear(orv.recddate) AS fy,
    orv.lobname
FROM
    clientview cv
INNER JOIN
    orderreceiptview orv ON cv.id = orv.clientid
LEFT JOIN
    entity e ON orv.entityid = e.id
WHERE
    LOWER(cv.clienttypename) = '%pma%';

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW get_owners_view AS
    SELECT DISTINCT
        a.id,
        a.societyname,
        a.name,
        a.propertytaxno,
        a.address,
        a.phoneno,
        a.emailid,
        a.corporation,
        a.dated,
        a.createdby,
        concat_ws(' ',d.firstname,d.lastname) as createdbyname,
        a.isdeleted,
        a.suburb,
        a.city as cityid,
        b.city,
        a.state,
        a.country as countryid,
        c.name as country,
        a.isexcludedmailinglist,
        a.propertydetails,
        a.propertyfor,
        a.phoneno1,
        a.phoneno2,
        a.source
    FROM
        owners a
    LEFT JOIN
        cities b ON a.city = b.id
    LEFT JOIN
        country c ON a.country = c.id
    LEFT JOIN
        usertable d ON a.createdby = d.id;

-------------------------------------------------------------------------------------------------------------

--  CREATE SEQUENCE IF NOT EXISTS client_receipt_id_seq OWNED BY client_receipt.id;
-- SELECT setval('client_receipt_id_seq', COALESCE(max(id), 0) + 1, false) FROM client_receipt;
-- ALTER TABLE client_receipt ALTER COLUMN id SET DEFAULT nextval('client_receipt_id_seq');

--  CREATE SEQUENCE IF NOT EXISTS builder_contacts_id_seq OWNED BY builder_contacts.id;
-- SELECT setval('builder_contacts_id_seq', COALESCE(max(id), 0) + 1, false) FROM builder_contacts;
-- ALTER TABLE builder_contacts ALTER COLUMN id SET DEFAULT nextval('builder_contacts_id_seq');


--10.04


CREATE VIEW tally_orderpayment_bank2bank AS
SELECT
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
CASE 
    WHEN mode = 5 THEN 'DAP-ICICI-65'
    WHEN mode = 17 THEN 'DAP-ICICI-42'
    ELSE 'SENDINGMODE'
END AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 'Intra Bank transfer' AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid
FROM orderpaymentview
WHERE serviceid = 76
  AND isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.03

CREATE VIEW tally_orderpayments_bank2cash AS
SELECT
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
 CASE 
    WHEN mode = 3 THEN 'DAP-ICICI-42'
    WHEN mode <> 3 THEN 'Cash'
 END AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 'Bank-Cash Withdraw/Deposit Contra' AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid
FROM orderpaymentview
WHERE serviceid = 75
  AND isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.02

CREATE OR REPLACE VIEW tally_orderpayments_taxes AS
SELECT 
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
 orderdescription AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 clientname || '- ' || orderdescription || '- ' || description AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid,
 'Payment' AS type
FROM orderpaymentview
WHERE clientid = 15284
  AND isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.06

CREATE VIEW Tally_OrderPayments_Vendors AS
SELECT 

    ''::text AS uniqueid,
    orderpaymentview.paymentdate AS date,
    'Payment'::text AS voucher,
    'Payment'::text AS vouchertype,
    ''::text AS vouchernumber,
    orderpaymentview.vendorname AS drledger,
    orderpaymentview.mode_of_payment AS crledger,
    orderpaymentview.amount AS ledgeramount,
    (orderpaymentview.clientname || '- ' || 
     orderpaymentview.orderdescription || '- ' || 
     orderpaymentview.description || 
     CASE 
         WHEN orderpaymentview.tds > 0.01
         THEN '- TDS-' || orderpaymentview.tds
         ELSE ''
     END) AS narration,
    ''::text AS instrumentno,
    ''::text AS instrumentdate,
    orderpaymentview.mode,
    orderpaymentview.entityid,
    orderpaymentview.tds,
    orderpaymentview.serviceid,
    orderpaymentview.clientid
FROM orderpaymentview
WHERE 
    orderpaymentview.clientid <> ALL (ARRAY[15284, 15285]) 
    AND orderpaymentview.isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.07

CREATE VIEW tally_orderpayments_with_tds AS
SELECT 
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
 vendorname AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 clientname || '- ' || orderdescription || '- ' || description AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid
FROM orderpaymentview
WHERE clientid NOT IN (15284, 15285)
  AND isdeleted = false
  AND tds > 0.00;

------------------------------------------------------------------------------------------------------------------------------------------

--10.01

CREATE VIEW tally_clientreceipt AS
SELECT
 ' ' AS uniqueid,
 CAST(recddate AS DATE) AS date,
 'Receipt' AS type,
 'Receipt' AS vouchertype,    
 ' ' AS vouchernumber,
 paymentmode AS drledger,
 clientname AS crledger,
 amount AS ledgeramount,
 'Received in ICICI Bank' AS narration,
 ' ' AS instrumentno,
 ' ' AS instrumentdate,
 paymentmodeid,
 entityid
FROM clientreceiptlistview
WHERE isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.05

CREATE OR REPLACE VIEW tally_cr_to_salesinvoice AS
 SELECT ' '::text AS uniqueid,
    'Sales'::text AS base_vch_type,
    'GST Invoice'::text AS vch_type,
    ' '::text AS vch_no,
    client_receipt.recddate AS vch_date,
    ' '::text AS ref_no,
    ' '::text AS ref_date,
    (client.firstname || ' '::text) || client.lastname AS party,
    ' '::text AS gstin,
    'Maharashtra'::text AS state,
    'Property Services'::text AS item_name,
    ' '::text AS item_hsn_code,
    ' '::text AS item_units,
    ' '::text AS item_qty,
    ' '::text AS item_rate,
    ' '::text AS item_discountpercentage,
    round(client_receipt.amount / 1.18, 2) AS item_amount,
    ' '::text AS igst_percentage,
    ' '::text AS igst_amount,
    '9'::text AS cgst_percentage,
    round(client_receipt.amount * 0.076271, 2) AS cgst_amount,
    '9'::text AS sgst_percentage,
    round(client_receipt.amount * 0.076271, 2) AS sgst_amount,
    'GST Sale B2C'::text AS sales_purchase_ledger,
    ' '::text AS igst_ledger,
    'Output CGST'::text AS cgst_ledger,
    'Output SGST'::text AS sgst_ledger,
    'Real estate service fees (HSN 9972)'::text AS narration,
    'Yes'::text AS auto_round_off_yes_no,
    client_receipt.tds,
    client_receipt.serviceamount,
    client_receipt.reimbursementamount,
    client_receipt.entityid,
    client_receipt.paymentmode AS paymentmodeid
   FROM client_receipt
     JOIN client ON client_receipt.clientid = client.id
     JOIN entity ON client_receipt.entityid = entity.id
  WHERE entity.name ~~* '%CURA%'::text AND client_receipt.isdeleted = false AND client_receipt.recddate > '2023-12-31'::date
 LIMIT 100;
------------------------------------------------------------------------------------------------------------------------------------------

-- SELECT 
--     SUM(receipts) - SUM(payments) AS diff
-- FROM 
--     bankstbalanceview
-- WHERE 
--     name LIKE '%DAP-ICICI-42%' 
--     AND date <= '2024-03-31';

create view bank_pmt_rcpts as SELECT
'Payment' as Type,
- 1 * Order_Payment.amount AS AMOUNT, PaymentDate::date AS DATE, Mode_Of_payment.Name AS BankName
FROM            Order_Payment, Mode_Of_payment
WHERE        order_payment.Mode = mode_of_payment.ID AND (mode_of_payment.name NOT IN ('Cash'))
AND order_payment.IsDeleted <> true
UNION ALL

SELECT
'Receipt' as Type,
order_receipt.amount AS AMOUNT, order_receipt.RecdDate::date AS DATE, Mode_Of_payment.Name AS BankName
FROM            Order_Receipt, Mode_Of_payment
WHERE        Order_Receipt.PaymentMode = mode_of_payment.ID AND (mode_of_payment.name NOT IN ('Cash'))
AND Order_Receipt.IsDeleted <> true
UNION ALL

SELECT
'Payment' as Type,
- 1 * REF_Contractual_Payments.amount AS AMOUNT, PaidOn::date AS DATE, Mode_Of_payment.Name AS BankName
FROM            REF_Contractual_Payments, Mode_Of_payment
WHERE        REF_Contractual_Payments.PaymentMode = mode_of_payment.ID AND (mode_of_payment.name NOT IN ('Cash'))
AND REF_Contractual_Payments.IsDeleted <> true;

-- SELECT
--     SUM(amount)
-- FROM
--     bank_pmt_rcpts
-- WHERE
--     bankname LIKE '%DAP-ICICI-42%'
--     AND date <= '2024-03-31';


-- alter table client_property alter column propertyemanager type text;


-- CREATE SEQUENCE IF NOT EXISTS serviceapartmentsandguesthouses_id_seq OWNED BY serviceapartmentsandguesthouses.id;
-- SELECT setval('serviceapartmentsandguesthouses_id_seq', COALESCE(max(id), 0) + 1, false) FROM serviceapartmentsandguesthouses;
-- ALTER TABLE serviceapartmentsandguesthouses ALTER COLUMN id SET DEFAULT nextval('serviceapartmentsandguesthouses_id_seq');

CREATE VIEW get_apartment_view AS
SELECT
    a.id,
    a.name,
    a.emailid,
    a.phoneno,
    a.website,
    a.contactperson1,
    a.contactperson2,
    a.email1,
    a.email2,
    a.contactname1,
    a.contactname2,
    a.createdby,
    CONCAT(u.firstname, ' ', u.lastname) AS createdbyname,
    a.dated,
    a.isdeleted,
    a.suburb,
    b.city AS city,
    a.state,
    a.country AS countryid,
    c.name AS country,
    a.apartments_guesthouse
FROM
    serviceapartmentsandguesthouses AS a
LEFT JOIN
    cities AS b ON a.city = b.id
LEFT JOIN
    country AS c ON a.country = c.id
LEFT JOIN
    usertable AS u ON a.createdby = u.id;

--11.1

CREATE VIEW TotalClientIDsView AS
SELECT 'Property ID' AS Type, Client.ID AS ClientID, Client_Property.ID AS RelatedID
FROM Client
INNER JOIN Client_Property ON Client.ID = Client_Property.ClientID

UNION

SELECT 'ClientReceipt ID' AS Type, Client.ID AS ClientID, Client_Receipt.ID AS RelatedID
FROM Client
INNER JOIN Client_Receipt ON Client.ID = Client_Receipt.ClientID

UNION

SELECT 'Order ID' AS Type, Client.ID AS ClientID, Orders.ID AS RelatedID
FROM Client
INNER JOIN Orders ON Client.ID = Orders.ClientID

UNION

SELECT 'ClientPOA ID' AS Type, Client.ID AS ClientID, Client_POA.ID AS RelatedID
FROM Client
INNER JOIN Client_POA ON Client.ID = Client_POA.ClientID

UNION

SELECT 'BankSt ID' AS Type, Client.ID AS ClientID, BankSt.ID AS RelatedID
FROM Client
INNER JOIN BankSt ON Client.ID = BankSt.ClientID;

------------------------------------------------------------------------------------------------------------------------------------------

--11.2

CREATE VIEW TotalOrderIDsView AS
SELECT 'Order Receipt ID' AS Type, Orders.ID, Order_Receipt.ID AS OrderID
FROM Orders
INNER JOIN Order_Receipt ON Orders.ID = Order_Receipt.OrderID

UNION 

SELECT 'Order Payment ID' AS Type, Orders.ID, Order_Payment.ID AS OrderID
FROM Orders
INNER JOIN Order_Payment ON Orders.ID = Order_Payment.OrderID

UNION

SELECT 'Order Invoice ID' AS Type, Orders.ID, Order_Invoice.ID AS OrderID
FROM Orders
INNER JOIN Order_Invoice ON Orders.ID = Order_Invoice.OrderID

UNION

SELECT 'Vendor Invoice ID' AS Type, Orders.ID, Order_VendorEstimate.ID AS OrderID
FROM Orders
INNER JOIN Order_VendorEstimate ON Orders.ID = Order_VendorEstimate.OrderID

UNION

SELECT 'Order Task ID' AS Type, Orders.ID, Order_Task.ID AS OrderID
FROM Orders
INNER JOIN Order_Task ON Orders.ID = Order_Task.OrderID

UNION

SELECT 'Order Status Change ID' AS Type, Orders.ID, Order_Status_Change.ID AS OrderID
FROM Orders
INNER JOIN Order_Status_Change ON Orders.ID = Order_Status_Change.OrderID;

------------------------------------------------------------------------------------------------------------------------------------------

--11.3

CREATE VIEW TotalVendorIDsView AS
SELECT 'Order Payment ID' AS Type, Vendor.ID, Order_Payment.ID AS VendorID
FROM Vendor
INNER JOIN Order_Payment ON Vendor.ID = Order_Payment.VendorID

UNION

SELECT 'Vendor Invoice ID' AS Type, Vendor.ID, Order_VendorEstimate.ID AS VendorID
FROM Vendor
INNER JOIN Order_VendorEstimate ON Vendor.ID = Order_VendorEstimate.VendorID

UNION

SELECT 'BankSt ID' AS Type, Vendor.ID, BankSt.ID AS VendorID
FROM Vendor
INNER JOIN BankSt ON Vendor.ID = BankSt.VendorID;

-----------------------------------------------------------------------------------------------------------------------------------------

--13.1

-- CREATE VIEW VendorSummaryForFinancialYearView AS
-- SELECT
--     Vendor.VendorName,
--     Vendor.AddressLine1,
--     Vendor.AddressLine2,
--     Vendor.Suburb,
--     Vendor.PANNo,
--     Vendor.TANNo,
--     Vendor.VATTinNo,
--     Vendor.GSTServiceTaxNo,  -- Changed column name
--     Vendor.LBTNo,
--     Vendor.TDSSection,
--     CASE WHEN Vendor.Registered = 'true' THEN 'Yes' ELSE 'No' END AS Registered,
--     Vendor.BankName,
--     Vendor.BankBranch,
--     Vendor.BankCity,
--     Vendor.BankAcctHolderName,
--     Vendor.BankAcctNo,
--     Vendor.BankIFSCCode,
--     Vendor.BankMICRCode,
--     Vendor.BankAcctType,
--     Vendor.VendorDealerStatus,
--     OrderPaymentView.ID,
--     OrderPaymentView.PaymentById,
--     OrderPaymentView.Amount,
--     OrderPaymentView.PaymentDate,
--     OrderPaymentView.OrderID,
--     OrderPaymentView.VendorID,
--     OrderPaymentView.Mode,
--     OrderPaymentView.Description,
--     OrderPaymentView.ServiceTaxAmount,
--     OrderPaymentView.Dated,
--     OrderPaymentView.CreatedById,
--     OrderPaymentView.IsDeleted,
--     OrderPaymentView.Mode_Of_payment,
--     OrderPaymentView.CreatedBy,
--     OrderPaymentView.PaymentBy,
--     OrderPaymentView.ClientName,
--     OrderPaymentView.OrderDescription,
--     OrderPaymentView.TDS,
--     OrderPaymentView.PropertyDescription,
--     OrderPaymentView.VendorName AS Expr1,
--     OrderPaymentView.LOBName,
--     OrderPaymentView.ServiceType,
--     OrderPaymentView.ServiceId,
--     OrderPaymentView.MonthYear,
--     OrderPaymentView.FY
-- FROM Vendor
-- INNER JOIN OrderPaymentView ON Vendor.ID = OrderPaymentView.VendorID;


------------------------------------------------------------------------------------------------------------------------------------------

--13.2

CREATE VIEW OrderVendorEstimateView AS
SELECT
    Order_VendorEstimate.EstimateDate,
    Order_VendorEstimate.Amount,
    Order_VendorEstimate.ID,
    Order_VendorEstimate.EstimateDesc,
    Order_VendorEstimate.OrderID,
    Order_VendorEstimate.VendorID,
    Order_VendorEstimate.InvoiceDate,
    Order_VendorEstimate.InvoiceAmount,
    OrdersView.BriefDescription,
    OrdersView.ClientName,
    Vendor.VendorName,
    Order_VendorEstimate.Notes,
    Order_VendorEstimate.InvoiceNumber,
    Order_VendorEstimate.Vat1,
    Order_VendorEstimate.Vat2,
    Order_VendorEstimate.ServiceTax,
    OrdersView.ClientID,
    Order_VendorEstimate.CreatedBy AS CreatedById,
    UserView.FullName AS CreatedBy,
    Order_VendorEstimate.EntityId,
    Entity.Name AS EntityName,
    Order_VendorEstimate.OfficeId,
    Office.Name AS OfficeName
FROM
    Order_VendorEstimate
INNER JOIN
    OrdersView ON Order_VendorEstimate.OrderID = OrdersView.ID
INNER JOIN
    Office ON Office.ID = Order_VendorEstimate.OfficeId
INNER JOIN
    UserView ON Order_VendorEstimate.CreatedBy = UserView.UserId
LEFT OUTER JOIN
    Entity ON Order_VendorEstimate.EntityId = Entity.ID
LEFT OUTER JOIN
    Vendor ON Vendor.ID = Order_VendorEstimate.VendorID;

CREATE VIEW vendorstatementview AS
SELECT
    'Invoice' AS type,
    ordervendorestimateview.invoicedate AS invoicedate_orderpaymentdate,
    ordervendorestimateview.invoiceamount AS invoiceamount_orderpaymentamount,
    ordervendorestimateview.briefdescription AS estimatedescription_orderdescription,
    ordervendorestimateview.clientname AS clientname_vendorname,
    NULL AS modeofpayment,
    ordersview.clientname,
    entity.name AS entityname,
    ordersview.clientid,
    ordervendorestimateview.vendorid,
    ordervendorestimateview.id,
    to_char(ordervendorestimateview.invoicedate, 'YYYY-MM') AS monthyear
FROM
    ordersview
INNER JOIN
    ordervendorestimateview ON ordersview.id = ordervendorestimateview.orderid
LEFT OUTER JOIN
    entity ON ordervendorestimateview.entityid = entity.id
UNION
SELECT
    'Payments' AS type,
    order_payment.paymentdate,
    order_payment.amount,
    ordersview.briefdescription AS orderdescription,
    vendor.vendorname,
    mode_of_payment.name AS modeofpayment,
    ordersview.clientname,
    entity.name,
    ordersview.id,
    vendor.id AS vendorid,
    order_payment.id,
    to_char(order_payment.paymentdate, 'YYYY-MM') AS monthyear
FROM
    mode_of_payment
INNER JOIN
    order_payment ON mode_of_payment.id = order_payment.mode
INNER JOIN
    vendor ON order_payment.vendorid = vendor.id
INNER JOIN
    ordersview ON order_payment.orderid = ordersview.id
INNER JOIN
    client ON ordersview.clientid = client.id
LEFT OUTER JOIN
    entity ON order_payment.entityid = entity.id;


------------------------------------------------------------------------------------------------------------------------------------------

--17.1

 CREATE VIEW FIN_TDS_Paid_By_Vendor AS
SELECT
    Vendor.VendorName,
    CASE WHEN Vendor.companydeductee != false THEN 'YES' ELSE 'NO' END AS companydeductee,
    Vendor_Category.Name AS VendorCategory,
    CASE WHEN Vendor.Registered != false THEN 'Yes' ELSE 'No' END AS Registered,
    Order_Payment.PaymentDate,
    Order_Payment.Amount,
    getMonthYear(Order_Payment.PaymentDate) AS MonthYear,
    getFinancialYear(Order_Payment.PaymentDate) AS FY,
    Mode_Of_payment.Name AS PaymentMode,
    Order_Payment.TDS,
    Vendor.PANNo,
    Vendor.TDSSection,
    Order_Payment.ID
FROM
    Order_Payment
INNER JOIN Vendor ON Order_Payment.VendorID = Vendor.ID
INNER JOIN Vendor_Category ON Vendor.Category = Vendor_Category.ID
INNER JOIN Mode_Of_payment ON Order_Payment.Mode = Mode_Of_payment.ID
WHERE
    Order_Payment.TDS > 0;

------------------------------------------------------------------------------------------------------------------------------------------

--17.2

CREATE VIEW VendorSummaryForFinancialYearView AS
SELECT
    Vendor.VendorName,
    Vendor.AddressLine1,
    Vendor.AddressLine2,
    Vendor.Suburb,
    Vendor.PANNo,
    Vendor.TANNo,
    Vendor.VATTinNo,
    Vendor.LBTNo,
    Vendor.TDSSection,
    Vendor.gstservicetaxno,
    CASE WHEN Vendor.Registered = 'true' THEN 'Yes' ELSE 'No' END AS Registered,
    Vendor.BankName,
    Vendor.BankBranch,
    Vendor.BankCity,
    Vendor.BankAcctHolderName,
    Vendor.BankAcctNo,
    Vendor.BankIFSCCode,
    Vendor.BankMICRCode,
    Vendor.BankAcctType,
    Vendor.VendorDealerStatus,
    OrderPaymentView.ID,
    OrderPaymentView.PaymentById,
    OrderPaymentView.Amount,
    OrderPaymentView.PaymentDate,
    OrderPaymentView.OrderID,
    OrderPaymentView.VendorID,
    OrderPaymentView.Mode,
    OrderPaymentView.Description,
    OrderPaymentView.ServiceTaxAmount,
    OrderPaymentView.Dated,
    OrderPaymentView.CreatedById,
    OrderPaymentView.IsDeleted,
    OrderPaymentView.Mode_Of_payment,
    OrderPaymentView.CreatedBy,
    OrderPaymentView.PaymentBy,
    OrderPaymentView.ClientName,
    OrderPaymentView.OrderDescription,
    OrderPaymentView.TDS,
    OrderPaymentView.PropertyDescription,
    OrderPaymentView.VendorName AS Expr1,
    OrderPaymentView.LOBName,
    OrderPaymentView.ServiceType,
    OrderPaymentView.ServiceId,
    OrderPaymentView.MonthYear,
    OrderPaymentView.FY
FROM
    Vendor
INNER JOIN
    OrderPaymentView ON Vendor.ID = OrderPaymentView.VendorID;

------------------------------------------------------------------------------------------------------------------------------------------


------------------------------------------------------------------------------------------------------------------------------------------

--17.3

create view tdspaidtogovernment as
SELECT 
    replace(replace(orders.briefdescription, ''::text, ''::text),
    ''::text, ''::text) AS order_description,
    order_payment.amount,
    order_payment.paymentdate as date,
    replace(replace(order_payment.description, ''::text, ''::text),
    ''::text, ''::text) AS payment_description,
    vendor.vendorname,
    orders.id AS orderid
   FROM order_payment
     JOIN orders ON order_payment.orderid = orders.id
     JOIN vendor ON order_payment.vendorid = vendor.id
  WHERE orders.id = ANY (ARRAY[31648::bigint, 10770::bigint, 31649::bigint, 353444::bigint, 122525::bigint]);




CREATE VIEW agedorders AS
SELECT 
  lobname,
  orderstatus,
  service,
  clientname,
  briefdescription,
  propertydescription,
  COALESCE(DATE_PART('day', NOW() - orderdate), 9999) AS agingdays
FROM ordersview
WHERE isdeleted = false;

create view vendorsummary as
 SELECT ordersview.clientname,
    ordersview.briefdescription,
    vendor.vendorname,
    COALESCE(tempdatatable.estimateamount, 0::numeric) AS estimateamount,
    COALESCE(tempdatatable.invoiceamount, 0::numeric) AS invoiceamount,
    tempdatatable.orderid,
    COALESCE(tempdatatable.paymentamount, 0::numeric) AS paymentamount,
    tempdatatable.vendorid,
    tempdatatable.computedpending,
    ordersview.service,
    ordersview.ownername
   FROM ordersview
     LEFT JOIN ( SELECT sum(amount.estimateamount) AS estimateamount,
            sum(amount.invoiceamount) AS invoiceamount,
            sum(amount.paymentamount) AS paymentamount,
            amount.vendorid,
            ordersview_1.id AS orderid,
                CASE
                    WHEN COALESCE(sum(amount.invoiceamount), 0::numeric) = 0::numeric THEN COALESCE(sum(amount.estimateamount), 0::numeric)
                    ELSE COALESCE(sum(amount.invoiceamount), 0::numeric)
                END - COALESCE(sum(amount.paymentamount), 0::numeric) AS computedpending
           FROM ordersview ordersview_1
             LEFT JOIN ( SELECT orderpaymentview.vendorid,
                    COALESCE(orderpaymentview.tds, 0::numeric) + orderpaymentview.amount AS paymentamount,
                    0 AS estimateamount,
                    0 AS invoiceamount,
                    orderpaymentview.orderid
                   FROM orderpaymentview
                UNION ALL
                 SELECT ordervendorestimateview.vendorid,
                    0 AS paymentamount,
                    ordervendorestimateview.amount AS estimateamount,
                    ordervendorestimateview.invoiceamount,
                    ordervendorestimateview.orderid
                   FROM ordervendorestimateview) amount ON amount.orderid = ordersview_1.id
          GROUP BY ordersview_1.id, amount.vendorid) tempdatatable ON tempdatatable.orderid = ordersview.id
     LEFT JOIN vendor ON vendor.id = tempdatatable.vendorid
  WHERE tempdatatable.vendorid IS NOT NULL AND (ordersview.orderstatus <> ALL (ARRAY['Inquiry'::text, 'Cancelled'::text, 'Estimate Given'::text]));


--    create view monthlybalanceview as  SELECT sum(COALESCE(fin_bank_transactions_daily_summary.payments, 0::numeric)) AS payments,
--     fin_bank_transactions_daily_summary.name,
--     fin_bank_transactions_daily_summary.monthyear,
--     sum(COALESCE(fin_bank_transactions_daily_summary.receipts, 0::numeric)) AS receipts,
--     sum(COALESCE(fin_bank_transactions_daily_summary.receipts, 0::numeric)) - sum(COALESCE(fin_bank_transactions_daily_summary.payments, 0::numeric)) AS total,
--     sum(COALESCE(fin_bank_transactions_daily_summary.bankreceipts, 0::numeric)) AS bankreceipts,
--     sum(COALESCE(fin_bank_transactions_daily_summary.bankpayments, 0::numeric)) AS bankpayments,
--     sum(COALESCE(fin_bank_transactions_daily_summary.bankreceipts, 0::numeric)) - sum(COALESCE(fin_bank_transactions_daily_summary.bankpayments, 0::numeric)) AS banktotal
--    FROM fin_bank_transactions_daily_summary
--   GROUP BY fin_bank_transactions_daily_summary.name, fin_bank_transactions_daily_summary.monthyear
--   ORDER BY fin_bank_transactions_daily_summary.monthyear DESC;

CREATE VIEW pmaclientportalreport AS
   SELECT DISTINCT c.id AS clientid,
    (c.firstname || ' '::text) || c.lastname AS fullname,
    c.email1,
    c.email2,
    COALESCE(emails.email, ''::text) AS email
   FROM client c
     LEFT JOIN LATERAL ( SELECT string_agg(b.onlinemailid, ', '::text) AS email
           FROM client_access b
          WHERE b.clientid = c.id) emails ON true
  WHERE c.clienttype = 7;

CREATE VIEW orderreceiptlobentityview AS
 SELECT orderreceiptview.recddate AS date,
    orderreceiptview.monthyear,
    sum(orderreceiptview.amount) AS orderreceiptamount,
    orderreceiptview.lobname,
    orderreceiptview.entityid,
    orderreceiptview.entityname
   FROM orderreceiptview
  GROUP BY orderreceiptview.lobname, orderreceiptview.recddate, orderreceiptview.monthyear, orderreceiptview.entityid, orderreceiptview.entityname;
CREATE VIEW orderpaymentlobentityview AS
 SELECT orderpaymentview.paymentdate AS date,
    orderpaymentview.monthyear,
    sum(orderpaymentview.amount) AS paymentamount,
    orderpaymentview.lobname,
    orderpaymentview.entityid,
    orderpaymentview.entityname
   FROM orderpaymentview
  GROUP BY orderpaymentview.lobname, orderpaymentview.paymentdate, orderpaymentview.monthyear, orderpaymentview.entityid, orderpaymentview.entityname;

CREATE VIEW datewiselobentityview AS
 SELECT tempdata.lobname,
    tempdata.date,
    tempdata.monthyear,
    tempdata.entityid,
    tempdata.entityname,
    sum(COALESCE(tempdata.orderreceiptamount, 0::numeric)) AS orderreceiptamount,
    sum(COALESCE(tempdata.paymentamount, 0::numeric)) AS paymentamount,
    sum(COALESCE(tempdata.orderreceiptamount, 0::numeric)) - sum(COALESCE(tempdata.paymentamount, 0::numeric)) AS diff
   FROM ( SELECT orderreceiptlobentityview.lobname,
            orderreceiptlobentityview.date,
            orderreceiptlobentityview.monthyear,
            orderreceiptlobentityview.orderreceiptamount,
            0 AS paymentamount,
            orderreceiptlobentityview.entityid,
            orderreceiptlobentityview.entityname
           FROM orderreceiptlobentityview
        UNION ALL
         SELECT orderpaymentlobentityview.lobname,
            orderpaymentlobentityview.date,
            orderpaymentlobentityview.monthyear,
            0 AS orderreceiptamount,
            orderpaymentlobentityview.paymentamount,
            orderpaymentlobentityview.entityid,
            orderpaymentlobentityview.entityname
           FROM orderpaymentlobentityview) tempdata
  GROUP BY tempdata.lobname, tempdata.date, tempdata.monthyear, tempdata.entityid, tempdata.entityname;

--duplication x6

-- CREATE VIEW rpt_client_property_caretaking_agreementview AS
-- SELECT
--     cpca.id,
--     cpca.clientpropertyid,
--     cpca.startdate,
--     cpca.enddate,
--     cpca.actualenddate,
--     cpca.monthlymaintenancedate,
--     cpca.monthlymaintenanceamount,
--     cpca.active,
--     cpca.scancopy,
--     cpca.reasonforearlyterminationifapplicable,
--     cpca.dated,
--     cpca.createdby AS createdbyid,
--     cpca.isdeleted,
--     ut.firstname || ' ' || ut.lastname AS createdby,
--     CASE
--         WHEN cpca.active = TRUE THEN 'Active'
--         ELSE 'Inactive'
--     END AS status,
--     pv.clientname,
--     pv.propertydescription,
--     pv.property_status AS propertystatus,
--     pv.electricitybillingduedate,
--     pv.electricitybillingunit,
--     pv.electricityconsumernumber,
--     pv.propertytaxnumber,
--     cpca.description,
--     lnl.startdate AS lnlstartdate,
--     lnl.actualenddate AS lnlenddate,
--     lnl.rentamount,
--     cpca.vacant,
--     cpca.rented,
--     cpca.fixed,
--     cpca.vacanttax,
--     cpca.rentedtax,
--     cpca.fixedtax,
--     cpca.electricitybillcreated,
--     cpca.propertytaxbillcreated,
--     cpca.pipedgasbillcreated,
--     cpca.societyduesbillcreated,
--     cpca.advanceforreimbursementcreated,
--     cpca.createclientportalaccount,
--     cpca.orderid,
--     o.briefdescription AS orderdescription,
--     pv.clientid,
--     cli.fulllegalname,
--     cv.clienttypename,
--     cpca.poastartdate,
--     cpca.poaenddate,
--     cpca.ptaxpaidtilldate,
--     cpca.societyduespaidtilldate,
--     cpca.poaholder
-- FROM
--     client_property_caretaking_agreement cpca
-- INNER JOIN
--     usertable ut ON cpca.createdby = ut.id
-- INNER JOIN
--     propertiesview pv ON cpca.clientpropertyid = pv.id
-- LEFT OUTER JOIN
--     clientview cv ON pv.clientid = cv.id
-- LEFT OUTER JOIN
--     client_legal_info cli ON pv.clientid = cli.clientid
-- LEFT OUTER JOIN
--     orders o ON cpca.orderid = o.id
-- LEFT OUTER JOIN
--     client_property_leave_license_detailsview lnl ON lnl.clientpropertyid = cpca.clientpropertyid AND lnl.active = TRUE;



-----------------------------------------------------------------------------------------------------------------------------------------


-- CREATE VIEW projectcontactsview AS
-- SELECT
--     pv.buildername,
--     pv.projectname,
--     pv.city,
--     pv.suburb,
--     pc.contactname,
--     pc.phone,
--     pc.email,
--     pc.effectivedate,
--     pc.role,
--     pc.tenureenddate,
--     pc.details
-- FROM
--     project_contacts pc
-- INNER JOIN
--     projectsview pv ON pc.projectid = pv.id;

-- CREATE VIEW projectsview AS
-- SELECT 
--     project.id,
--     project.builderid,
--     project.addressline1,
--     project.addressline2,
--     project.suburb,
--     project.city AS cityid,
--     project.state,
--     project.country,
--     project.zip,
--     project.project_type,
--     project.mailgroup1,
--     project.mailgroup2,
--     project.website,
--     project.project_legal_status,
--     project.rules,
--     project.completionyear,
--     project.jurisdiction,
--     project.taluka,
--     project.corporationward,
--     project.policechowkey,
--     project.policestation,
--     project.maintenance_details,
--     project.numberoffloors,
--     project.numberofbuildings,
--     project.approxtotalunits,
--     project.tenantstudentsallowed,
--     project.tenantworkingbachelorsallowed,
--     project.tenantforeignersallowed,
--     project.otherdetails,
--     project.duespayablemonth,
--     project.dated,
--     project.createdby AS createdbyid,
--     project.isdeleted,
--     cities.city,
--     country.name AS countryname,
--     usertable.firstname || ' ' || usertable.lastname AS createdby,
--     project.projectname,
--     project.nearestlandmark,
--     builder.buildername,
--     project_type.name AS projecttype,
--     CASE 
--         WHEN project.tenantstudentsallowed = '1' THEN 'Tenant Students Allowed,'
--         ELSE '' 
--     END 
--     || CASE 
--         WHEN project.tenantworkingbachelorsallowed = '1' THEN ' Tenant Working Bachelors Allowed,'
--         ELSE '' 
--     END 
--     || CASE 
--         WHEN project.tenantforeignersallowed = '1' THEN ' Tenant Foreigners Allowed' 
--         ELSE '' 
--     END AS tenantallowed
-- FROM     
--     project
-- INNER JOIN
--     cities ON project.city = cities.id
-- INNER JOIN
--     country ON project.country = country.id
-- INNER JOIN
--     usertable ON project.createdby = usertable.id
-- INNER JOIN
--     builder ON project.builderid = builder.id
-- INNER JOIN
--     project_type ON project.project_type = project_type.id;

------------------------------------------------------------------------------------------------------------------------------------------
-- CREATE VIEW ClientSummaryView AS
-- SELECT
--     OrdersView.ID AS OrderId,
--     COALESCE(OrdersView.ClientName, '') as ClientName,
--     COALESCE(OrdersView.PropertyDescription, '') as PropertyDescription,
--     COALESCE(OrdersView.BriefDescription, '') as BriefDescription,
--     COALESCE(OrdersView.Service, '') as Service,
--     COALESCE(SumVendorEstimate.EstimateAmount, 0) AS VendorEstimate,
--     COALESCE(SumVendorEstimate.InvoiceAmount, 0) AS VendorInvoiceAmount,
--     COALESCE(SumPayment.paymentamount, 0) AS SumPayment,
--     COALESCE(SumInvoice.EstimateAmount, 0) as EstimateAmount,
--     CASE
--         WHEN OrdersView.OrderStatus = 'Cancelled' THEN 0
--         ELSE
--             CASE
--                 WHEN COALESCE(SumInvoice.invoiceamount, 0) = 0 THEN SumInvoice.EstimateAmount
--                 ELSE SumInvoice.invoiceamount
--             END
--     END - COALESCE(SumReceipt.receiptamount, 0) AS ComputedPending,
--     COALESCE(SumReceipt.receiptamount, 0) AS SumReceipt,
--     OrdersView.OrderDate,
--     COALESCE(OrdersView.OrderStatus, '') as OrderStatus,
--     COALESCE(SumInvoice.invoiceamount, 0) as invoiceamount,
--     COALESCE(SumReceipt.receiptamount - SumPayment.paymentamount - SumInvoice.TaxAmount, 0) AS Profit,
--     COALESCE(OrdersView.Owner, 0) as Owner,
--     COALESCE(OrdersView.Status, 0) AS OrderStatusId,
--     COALESCE(OrdersView.LOBName, '') as LOBName,
--     COALESCE(OrdersView.OwnerName, '') as OwnerName,
--     COALESCE(OrdersView.ServiceType, '') as ServiceType,
--     OrdersView.ClientID,
--     COALESCE(OrdersView.ServiceId, 0) as ServiceId,
--     COALESCE(OrdersView.Ageing, 0) as Ageing,
--     COALESCE(OrdersView.EntityName, '') as EntityName
-- FROM
--     OrdersView
-- LEFT OUTER JOIN (
--     SELECT
--         OrderID,
--         SUM(InvoiceAmount) AS invoiceamount,
--         SUM(EstimateAmount) AS EstimateAmount,
--         SUM(COALESCE(Tax, 0)) AS TaxAmount
--     FROM
--         Order_Invoice
--     GROUP BY
--         OrderID
-- ) AS SumInvoice ON OrdersView.ID = SumInvoice.OrderID
-- LEFT OUTER JOIN (
--     SELECT
--         OrderID,
--         SUM(Amount + COALESCE(TDS, 0)) AS receiptamount
--     FROM
--         Order_Receipt
--     GROUP BY
--         OrderID
-- ) AS SumReceipt ON OrdersView.ID = SumReceipt.OrderID
-- LEFT OUTER JOIN (
--     SELECT
--         OrderID,
--         SUM(Amount) AS paymentamount
--     FROM
--         Order_Payment
--     GROUP BY
--         OrderID
-- ) AS SumPayment ON OrdersView.ID = SumPayment.OrderID
-- LEFT OUTER JOIN (
--     SELECT
--         OrderID,
--         SUM(InvoiceAmount) AS InvoiceAmount,
--         SUM(Amount) AS EstimateAmount
--     FROM
--         Order_VendorEstimate
--     GROUP BY
--         OrderID
-- ) AS SumVendorEstimate ON OrdersView.ID = SumVendorEstimate.OrderID;


-- CREATE VIEW rpt_clientswithadvanceholdingamounts AS
-- SELECT
--     clientname,
--     COALESCE(SUM(sumpayment), 0) AS payments,
--     COALESCE(SUM(sumreceipt), 0) AS receipts,
--     row_number() OVER (ORDER BY clientname) AS rn
-- FROM
--     clientsummaryview
-- WHERE
--     service = 'H-Advance Paid'
-- GROUP BY
--     clientname
-- HAVING
--     COALESCE(SUM(sumpayment), 0) < COALESCE(SUM(sumreceipt), 0);


------------------------------------------------------------------------------------------------------------------------------------------


-- CREATE VIEW rpt_clients_transactions AS
-- SELECT
--     'Invoice' AS type,
--     ov.clientname,
--     oi.id,
--     oi.invoicedate AS date,
--     oi.invoiceamount AS amount,
--     NULL AS tds,
--     REPLACE(REPLACE(ov.briefdescription, CHR(10), ''), CHR(13), '') AS orderdetails,
--     e.name AS entity,
--     s.service,
--     REPLACE(REPLACE(oi.quotedescription, CHR(10), ''), CHR(13), '') AS details,
--     '' AS mode,
--     ov.clienttypename AS client_type,
--     ov.id AS order_id,
--     ov.clientid AS clientid,
--     getmonthyear(oi.invoicedate) AS monthyear,
--     getfinancialyear(oi.invoicedate) AS fy,
--     ov.lobname
-- FROM
--     order_invoice oi
-- LEFT JOIN
--     ordersview ov ON ov.id = oi.orderid
-- LEFT JOIN
--     entity e ON e.id = oi.entityid
-- LEFT JOIN
--     services s ON s.id = ov.serviceid
-- WHERE
--     LOWER(ov.clienttypename) = 'pma-owner'

-- UNION ALL

-- SELECT
--     'Payment' AS type,
--     cv.fullname,
--     crv.id,
--     crv.recddate AS date,
--     -1 * crv.amount AS amount,
--     crv.tds,
--     NULL AS orderdetails,
--     e.name AS entity,
--     NULL AS service,
--     hr.name AS details,
--     crv.paymentmode AS mode,
--     cv.clienttypename,
--     NULL AS order_id,
--     cv.id AS clientid,
--     getmonthyear(crv.recddate) AS monthyear,
--     getfinancialyear(crv.recddate) AS fy,
--     NULL AS lobname
-- FROM
--     clientview cv
-- INNER JOIN
--     clientreceiptview crv ON cv.id = crv.clientid
-- LEFT JOIN
--     entity e ON crv.entityid = e.id
-- LEFT JOIN
--     howreceived hr ON crv.howreceivedid = hr.id
-- WHERE
--     LOWER(cv.clienttypename) = 'pma-owner'

-- UNION ALL

-- SELECT
--     'OrderRec' AS type,
--     cv.fullname,
--     orv.id,
--     orv.recddate AS date,
--     -1 * orv.amount AS amount,
--     orv.tds,
--     orv.orderdescription AS orderdetails,
--     e.name AS entity,
--     orv.service,
--     orv.receiptdesc AS details,
--     orv.paymentmode AS mode,
--     cv.clienttypename,
--     NULL AS order_id,
--     cv.id AS clientid,
--     getmonthyear(orv.recddate) AS monthyear,
--     getfinancialyear(orv.recddate) AS fy,
--     orv.lobname
-- FROM
--     clientview cv
-- INNER JOIN
--     orderreceiptview orv ON cv.id = orv.clientid
-- LEFT JOIN
--     entity e ON orv.entityid = e.id
-- WHERE
--     LOWER(cv.clienttypename) = 'pma-owner';

------------------------------------------------------------------------------------------------------------------------------------------

-- CREATE VIEW clientstatementview AS
-- SELECT
--     'Invoice' AS type,
--     ov.clientname,
--     oi.id,
--     oi.invoicedate AS date,
--     oi.invoiceamount AS amount,
--     NULL AS tds,
--     ov.briefdescription AS orderdetails,
--     e.name,
--     s.service,
--     oi.quotedescription AS details,
--     oi.visibletoclient,
--     ov.clientid,
--     '' AS mode,
--     ov.lobname AS lob_name
-- FROM
--     order_invoice oi
-- LEFT JOIN
--     ordersview ov ON ov.id = oi.orderid
-- LEFT JOIN
--     entity e ON e.id = oi.entityid
-- LEFT JOIN
--     services s ON s.id = ov.serviceid

-- UNION

-- SELECT
--     'C Receipt' AS type,
--     cv.fullname,
--     crv.id,
--     crv.recddate AS date,
--     crv.amount AS amount,
--     crv.tds,
--     NULL AS orderdetails,
--     e.name AS entity,
--     NULL AS service,
--     crv.receiptdesc AS details,
--     crv.visibletoclient,
--     cv.id,
--     crv.paymentmode AS mode,
--     '' AS lob_name
-- FROM
--     clientview cv
-- INNER JOIN
--     clientreceiptview crv ON cv.id = crv.clientid
-- LEFT JOIN
--     entity e ON crv.entityid = e.id

-- UNION

-- SELECT
--     'Payment' AS type,
--     cv.fullname,
--     opv.id,
--     opv.paymentdate AS date,
--     opv.amount AS amount,
--     opv.tds,
--     opv.orderdescription AS orderdetails,
--     e.name AS entity,
--     opv.service AS service,
--     opv.description AS details,
--     FALSE AS visible_to_client,
--     cv.id,
--     opv.mode_of_payment AS mode,
--     opv.lobname AS lob_name
-- FROM
--     clientview cv
-- INNER JOIN
--     orderpaymentview opv ON cv.id = opv.clientid
-- LEFT JOIN
--     entity e ON opv.entityid = e.id

-- UNION

-- SELECT
--     'Order Receipt' AS type,
--     cv.fullname,
--     orv.id,
--     orv.recddate AS date,
--     orv.amount AS amount,
--     orv.tds,
--     orv.orderdescription AS orderdetails,
--     e.name AS entity,
--     orv.service AS service,
--     orv.receiptdesc AS details,
--     FALSE AS visible_to_client,
--     cv.id AS clientid,
--     orv.paymentmode AS mode,
--     orv.lobname AS lob_name
-- FROM
--     clientview cv
-- INNER JOIN
--     orderreceiptview orv ON cv.id = orv.clientid
-- LEFT JOIN
--     entity e ON orv.entityid = e.id;

------------------------------------------------------------------------------------------------------------------------------------------

-- CREATE VIEW duplicateclients AS
-- SELECT
--     c.firstname,
--     c.lastname,
--     COUNT(c.email1) AS count,
--     c.clienttype,
--     ct.name
-- FROM
--     client c
-- INNER JOIN
--     client_type ct ON c.clienttype = ct.id
-- GROUP BY
--     c.email1,
--     c.firstname,
--     c.lastname,
--     c.clienttype,
--     ct.name,
--     c.isdeleted
-- HAVING
--     COUNT(c.email1) > 1
--     AND c.isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

-- CREATE VIEW clientbankdetails AS
-- SELECT
--     c.firstname,
--     c.lastname,
--     ca.onlinemailid,
--     cbi.bankname,
--     cbi.bankbranch,
--     cbi.bankaccountno,
--     cbi.bankaccountholdername,
--     cbi.bankcity,
--     cbi.bankifsccode,
--     cbi.bankaccounttype
-- FROM
--     client_access ca
-- INNER JOIN
--     client c ON ca.clientid = c.id
-- INNER JOIN
--     client_bank_info cbi ON c.id = cbi.clientid;

------------------------------------------------------------------------------------------------------------------------------------------


-- CREATE VIEW rpt_nonpmaclient AS
-- SELECT
--     'Invoice' AS type,
--     ov.clientname,
--     oi.id,
--     oi.invoicedate AS date,
--     oi.invoiceamount AS amount,
--     NULL AS tds,
--     REPLACE(REPLACE(ov.briefdescription, CHR(10), ''), CHR(13), '') AS orderdetails,
--     e.name AS entity,
--     s.service,
--     REPLACE(REPLACE(oi.quotedescription, CHR(10), ''), CHR(13), '') AS details,
--     '' AS mode,
--     ov.clienttypename AS client_type,
--     ov.id AS order_id,
--     ov.clientid AS clientid,
--     getmonthyear(oi.invoicedate) AS monthyear,
--     getfinancialyear(oi.invoicedate) AS fy,
--     ov.lobname AS lobname
-- FROM
--     order_invoice oi
-- LEFT JOIN
--     ordersview ov ON ov.id = oi.orderid
-- LEFT JOIN
--     entity e ON e.id = oi.entityid
-- LEFT JOIN
--     services s ON s.id = ov.serviceid
-- WHERE
--     ov.clienttypename NOT LIKE 'pma - owner' AND
--     ov.clientname NOT LIKE '%1-%'

-- UNION ALL

-- SELECT
--     'Payment' AS type,
--     cv.fullname,
--     crv.id,
--     crv.recddate AS date,
--     -1 * crv.amount AS amount,
--     crv.tds,
--     NULL AS orderdetails,
--     e.name AS entity,
--     NULL AS service,
--     hr.name AS details,
--     crv.paymentmode AS mode,
--     cv.clienttypename AS client_type,
--     NULL AS order_id,
--     cv.id AS clientid,
--     getmonthyear(crv.recddate) AS monthyear,
--     getfinancialyear(crv.recddate) AS fy,
--     NULL AS lobname
-- FROM
--     clientview cv
-- INNER JOIN
--     clientreceiptview crv ON cv.id = crv.clientid
-- LEFT JOIN
--     entity e ON crv.entityid = e.id
-- LEFT JOIN
--     howreceived hr ON crv.howreceivedid = hr.id
-- WHERE
--     cv.clienttypename NOT LIKE 'pma - owner' AND
--     cv.firstname NOT LIKE '%1-%'

-- UNION ALL

-- SELECT
--     'OrderRec' AS type,
--     cv.fullname,
--     orv.id,
--     orv.recddate AS date,
--     -1 * orv.amount AS amount,
--     orv.tds,
--     orv.orderdescription AS orderdetails,
--     e.name AS entity,
--     orv.service AS service,
--     orv.receiptdesc AS details,
--     orv.paymentmode AS mode,
--     cv.clienttypename AS client_type,
--     orv.orderid AS order_id,
--     cv.id AS clientid,
--     getmonthyear(orv.recddate) AS monthyear,
--     getfinancialyear(orv.recddate) AS fy,
--     orv.lobname AS lobname
-- FROM
--     clientview cv
-- INNER JOIN
--     orderreceiptview orv ON cv.id = orv.clientid
-- LEFT JOIN
--     entity e ON orv.entityid = e.id
-- WHERE
--     cv.clienttypename NOT LIKE 'pma - owner' AND
--     cv.firstname NOT LIKE '%1-%';

-- 1. Bank Record - Client Order Receipt Mismatch Details

CREATE VIEW rptinternal_sumclientreceiptsview AS
SELECT
    clientview.fullname, 
    SUM(client_receipt.amount) AS receiptamount, 
    CAST(client_receipt.recddate AS DATE) AS date, 
    mode_of_payment.name AS paymentmode, 
    mode_of_payment.id AS paymentmodeid, 
    clientview.id AS clientid
FROM client_receipt 
INNER JOIN mode_of_payment 
    ON client_receipt.paymentmode = mode_of_payment.id 
INNER JOIN clientview 
    ON client_receipt.clientid = clientview.id
WHERE client_receipt.isdeleted = FALSE 
    AND client_receipt.recddate >= '2016-04-01' 
    AND mode_of_payment.id <> 3
GROUP BY client_receipt.recddate, mode_of_payment.name, clientview.fullname, mode_of_payment.id, clientview.id;

CREATE VIEW rptinternal_sumorderreceiptsview AS
SELECT
    clientview.fullname, 
    CAST(order_receipt.recddate AS DATE) AS date, 
    mode_of_payment.name AS paymentmode, 
    SUM(order_receipt.amount) AS receiptamount, 
    clientview.id AS clientid, 
    mode_of_payment.id AS paymentmodeid
FROM orders 
INNER JOIN order_receipt 
    ON order_receipt.orderid = orders.id 
INNER JOIN mode_of_payment 
    ON order_receipt.paymentmode = mode_of_payment.id 
INNER JOIN clientview 
    ON orders.clientid = clientview.id
WHERE order_receipt.isdeleted = FALSE 
    AND order_receipt.recddate >= '2016-04-01' 
    AND mode_of_payment.id <> 3
GROUP BY order_receipt.recddate, mode_of_payment.name, clientview.fullname, clientview.id, mode_of_payment.id;

CREATE VIEW rpt_clientandorderreceiptmismatchdetails AS
SELECT 
    'clientreceipt' AS type, 
    COALESCE(rptinternal_sumclientreceiptsview.receiptamount, 0) - COALESCE(rptinternal_sumorderreceiptsview.receiptamount, 0) AS diff, 
    rptinternal_sumclientreceiptsview.date, 
    rptinternal_sumclientreceiptsview.paymentmode, 
    rptinternal_sumclientreceiptsview.fullname, 
    ROW_NUMBER() OVER (ORDER BY rptinternal_sumclientreceiptsview.fullname) AS rn
FROM rptinternal_sumclientreceiptsview 
LEFT OUTER JOIN rptinternal_sumorderreceiptsview 
    ON rptinternal_sumclientreceiptsview.date = rptinternal_sumorderreceiptsview.date 
    AND rptinternal_sumclientreceiptsview.paymentmodeid = rptinternal_sumorderreceiptsview.paymentmodeid 
    AND rptinternal_sumclientreceiptsview.clientid = rptinternal_sumorderreceiptsview.clientid
WHERE COALESCE(rptinternal_sumclientreceiptsview.receiptamount, 0) - COALESCE(rptinternal_sumorderreceiptsview.receiptamount, 0) <> 0 
    AND rptinternal_sumclientreceiptsview.fullname NOT LIKE '1%'
UNION ALL
SELECT 
    'orderreceipt' AS type, 
    COALESCE(rptinternal_sumorderreceiptsview.receiptamount, 0) - COALESCE(rptinternal_sumclientreceiptsview.receiptamount, 0) AS diff, 
    rptinternal_sumorderreceiptsview.date, 
    rptinternal_sumorderreceiptsview.paymentmode, 
    rptinternal_sumorderreceiptsview.fullname, 
    ROW_NUMBER() OVER (ORDER BY rptinternal_sumorderreceiptsview.fullname) AS rn
FROM rptinternal_sumorderreceiptsview 
LEFT OUTER JOIN rptinternal_sumclientreceiptsview 
    ON rptinternal_sumorderreceiptsview.date = rptinternal_sumclientreceiptsview.date 
    AND rptinternal_sumorderreceiptsview.paymentmodeid = rptinternal_sumclientreceiptsview.paymentmodeid 
    AND rptinternal_sumorderreceiptsview.clientid = rptinternal_sumclientreceiptsview.clientid
WHERE COALESCE(rptinternal_sumorderreceiptsview.receiptamount, 0) - COALESCE(rptinternal_sumclientreceiptsview.receiptamount, 0) <> 0 
    AND rptinternal_sumorderreceiptsview.fullname NOT LIKE '1%';
------------------------------------------------------------------------------------------------------------------------------------------

--2. Bank Record - Bank Balance Reconciliation

CREATE OR REPLACE VIEW BankSTBalanceView AS
SELECT
    ID,
    date,
    Name,
    SUM(COALESCE(Payments, 0)) AS Payments,
    SUM(COALESCE(Receipts, 0)) AS Receipts,
    ModeofPayment,
    MonthYear
FROM (
    SELECT
        BankSt.ID,
        BankSt.ModeofPayment,
        getMonthYear(BankSt.date) AS MonthYear,
        BankSt.date,
        Mode_Of_payment.Name,
        SUM(CASE WHEN BankSt.crdr = 'DR' THEN BankSt.Amount ELSE 0 END) AS Payments,
        0 AS Receipts
    FROM
        BankSt
        INNER JOIN Mode_Of_payment ON BankSt.ModeofPayment = Mode_Of_payment.ID
    GROUP BY
        BankSt.ModeofPayment,
        BankSt.date,
        Mode_Of_payment.Name,
        BankSt.ID,
        getMonthYear(BankSt.date)
    
    UNION ALL
    
    SELECT
        BankSt.ID,
        BankSt.ModeofPayment,
        getMonthYear(BankSt.date) AS MonthYear,
        BankSt.date,
        Mode_Of_payment.Name,
        0 AS Payments,
        SUM(CASE WHEN BankSt.crdr = 'CR' THEN BankSt.Amount ELSE 0 END) AS Receipts
    FROM
        BankSt
        INNER JOIN Mode_Of_payment ON BankSt.ModeofPayment = Mode_Of_payment.ID
    GROUP BY
        BankSt.ModeofPayment,
        BankSt.date,
        Mode_Of_payment.Name,
        BankSt.ID,
        getMonthYear(BankSt.date)
) AS TempData
GROUP BY
    ModeofPayment,
    date,
    Name,
    ID,
    MonthYear
LIMIT 100;


------------------------------------------------------------------------------------------------------------------------------------------

--3. Bank Record - Monthly Bank Summary


CREATE VIEW fin_bank_transactions_daily_pmts_summary AS
SELECT
    mode_of_payment.name,
    orderpaymentview.monthyear,
    orderpaymentview.paymentdate AS date,
    SUM(orderpaymentview.amount) AS payments,
    mode_of_payment.id AS modeid
FROM
    orderpaymentview
    INNER JOIN mode_of_payment ON orderpaymentview.mode_of_payment = mode_of_payment.name
WHERE
    orderpaymentview.isdeleted = false
GROUP BY
    mode_of_payment.name,
    orderpaymentview.monthyear,
    orderpaymentview.paymentdate,
    mode_of_payment.id;

CREATE VIEW fin_bank_transactions_daily_rcpts_summary AS
SELECT
    mode_of_payment.name,
    orderreceiptview.monthyear,
    orderreceiptview.recddate AS date,
    SUM(orderreceiptview.amount) AS payments,
    mode_of_payment.id AS modeid
FROM
    orderreceiptview
    INNER JOIN mode_of_payment ON orderreceiptview.paymentmode = mode_of_payment.name
WHERE
    orderreceiptview.isdeleted = false
GROUP BY
    mode_of_payment.name,
    orderreceiptview.monthyear,
    orderreceiptview.recddate,
    mode_of_payment.id;

CREATE VIEW fin_bank_transactions_daily_contractual_pmts_summary AS
SELECT
    paymentmode,
    monthyear,
    paidon AS date,
    SUM(amount) AS payments,
    paymentmodeid AS modeid
FROM
    contractualpaymentsview
WHERE
    paymentmode NOT IN ('Cash', 'Stores')
    AND isdeleted = false
GROUP BY
    paymentmode,
    monthyear,
    paidon,
    paymentmodeid;

CREATE VIEW fin_bank_transactions_daily_bankrcpts_summary AS
SELECT
    mode_of_payment.name,
    to_char(bankst.date, 'YYYY-MM') AS monthyear,
    bankst.date AS date,
    SUM(CASE WHEN bankst.crdr = 'CR' THEN bankst.amount ELSE 0 END) AS receipts,
    SUM(CASE WHEN bankst.crdr = 'DR' THEN bankst.amount ELSE 0 END) AS payments,
    mode_of_payment.id AS modeid
FROM
    bankst
    INNER JOIN mode_of_payment ON bankst.modeofpayment = mode_of_payment.id
GROUP BY
    mode_of_payment.name,
    to_char(bankst.date, 'YYYY-MM'),
    bankst.date,
    mode_of_payment.id;

CREATE VIEW fin_bank_transactions_daily_summary AS
SELECT
    name,
    monthyear,
    date,
    SUM(payments + COALESCE(cpayments, 0)) AS payments,
    SUM(COALESCE(reciepts, 0)) AS receipts,
    SUM(COALESCE(bankreciept, 0)) AS bankreceipts,
    SUM(COALESCE(bankpayments, 0)) AS bankpayments,
    modeid
FROM
    (
        SELECT
            name,
            monthyear,
            date,
            payments,
            0 AS reciepts,
            0 AS cpayments,
            0 AS bankreciept,
            0 AS bankpayments,
            modeid
        FROM
            fin_bank_transactions_daily_pmts_summary
        UNION
        SELECT
            name,
            monthyear,
            date,
            0 AS payments,
            payments AS reciepts,
            0 AS cpayments,
            0 AS bankreciept,
            0 AS bankpayments,
            modeid
        FROM
            fin_bank_transactions_daily_rcpts_summary
        UNION
        SELECT
            paymentmode,
            monthyear,
            date,
            0 AS payments,
            0 AS reciepts,
            payments AS cpayments,
            0 AS bankreciept,
            0 AS bankpayments,
            modeid
        FROM
            fin_bank_transactions_daily_contractual_pmts_summary
        UNION
        SELECT
            name,
            monthyear,
            date,
            0 AS payments,
            0 AS reciepts,
            0 AS cpayments,
            receipts AS bankreciept,
            payments AS bankpayments,
            modeid
        FROM
            fin_bank_transactions_daily_bankrcpts_summary
    ) AS tempdata
GROUP BY
    monthyear,
    date,
    name,
    modeid
ORDER BY
    date;


CREATE VIEW monthly_balance_view AS
SELECT DISTINCT ON (name, monthyear)
    SUM(COALESCE(payments, 0)) AS payments,
    name,
    monthyear,
    SUM(COALESCE(receipts, 0)) AS receipts,
    SUM(COALESCE(receipts, 0)) - SUM(COALESCE(payments, 0)) AS total,
    SUM(COALESCE(bankreceipts, 0)) AS bankreceipts,
    SUM(COALESCE(bankpayments, 0)) AS bankpayments,
    SUM(COALESCE(bankreceipts, 0)) - SUM(COALESCE(bankpayments, 0)) AS banktotal
FROM
    fin_bank_transactions_daily_summary
GROUP BY
    name,
    monthyear
ORDER BY
    monthyear DESC;

------------------------------------------------------------------------------------------------------------------------------------------

--4.


------------------------------------------------------------------------------------------------------------------------------------------

--5.

CREATE VIEW RptBankstAmount1 AS
SELECT
    COALESCE(SUM(CASE WHEN BankSt.crdr = 'DR' THEN BankSt.Amount ELSE 0 END), 0) AS BankStAMount,
    BankSt.Date,
    BankSt.ModeofPayment,
    Mode_Of_payment.Name
FROM
    BankSt
INNER JOIN
    Mode_Of_payment ON BankSt.ModeofPayment = Mode_Of_payment.ID
GROUP BY
    BankSt.Date,
    BankSt.ModeofPayment,
    Mode_Of_payment.Name;

CREATE VIEW rptorderpaymentamount1 As
 SELECT COALESCE(sum(order_payment.amount), 0::numeric) AS opamount,
    order_payment.paymentdate AS date,
    mode_of_payment.name,
    order_payment.mode
   FROM order_payment
     JOIN mode_of_payment ON order_payment.mode = mode_of_payment.id
  WHERE order_payment.isdeleted = false
  GROUP BY order_payment.paymentdate, mode_of_payment.name, order_payment.mode;

CREATE VIEW BankReconcillationviewPayment AS
 SELECT p.date,
    p.name AS paymentmode,
    COALESCE(sum(
        CASE
            WHEN p.type = 'Bankst'::text THEN p.amount
            ELSE 0::numeric
        END), 0::numeric) AS bankstamount,
    COALESCE(sum(
        CASE
            WHEN p.type = 'OPAMount'::text THEN p.amount
            ELSE 0::numeric
        END), 0::numeric) AS opamount,
    COALESCE(sum(
        CASE
            WHEN p.type = 'CPAMount'::text THEN p.amount
            ELSE 0::numeric
        END), 0::numeric) AS cpamount,
    COALESCE(sum(
        CASE
            WHEN p.type = 'CPAMount'::text THEN p.amount
            ELSE 0::numeric
        END), 0::numeric) + COALESCE(sum(
        CASE
            WHEN p.type = 'OPAMount'::text THEN p.amount
            ELSE 0::numeric
        END), 0::numeric) AS totalpayment
   FROM ( SELECT 'Bankst'::text AS type,
            rptbankstamount1.bankstamount AS amount,
            rptbankstamount1.date,
            rptbankstamount1.name
           FROM rptbankstamount1
        UNION ALL
         SELECT 'OPAMount'::text AS type,
            rptorderpaymentamount1.opamount AS amount,
            rptorderpaymentamount1.date,
            rptorderpaymentamount1.name
           FROM rptorderpaymentamount1
        UNION ALL
         SELECT 'CPAMount'::text AS type,
            rptcontractualpaymentamount1.cpamount AS amount,
            rptcontractualpaymentamount1.date,
            rptcontractualpaymentamount1.name
           FROM rptcontractualpaymentamount1) p
  GROUP BY p.date, p.name
  ORDER BY p.date DESC;




------------------------------------------------------------------------------------------------------------------------------------------

--6.
CREATE VIEW rpt_contractual_payment_amount1 AS
SELECT
    COALESCE(SUM(ref_contractual_payments.amount), 0) AS cpamount,
    ref_contractual_payments.paidon AS date,
    mode_of_payment.name,
    ref_contractual_payments.paymentmode
FROM
    ref_contractual_payments
INNER JOIN
    mode_of_payment ON ref_contractual_payments.paymentmode = mode_of_payment.id
WHERE
    ref_contractual_payments.isdeleted = false
GROUP BY
    ref_contractual_payments.paidon,
    mode_of_payment.name,
    ref_contractual_payments.paymentmode;

CREATE VIEW rpt_order_payment_amount1 AS
SELECT
    COALESCE(SUM(order_payment.amount), 0) AS opamount,
    order_payment.paymentdate AS date,
    mode_of_payment.name,
    order_payment.mode
FROM
    order_payment
INNER JOIN
    mode_of_payment ON order_payment.mode = mode_of_payment.id
WHERE
    order_payment.isdeleted = false
GROUP BY
    order_payment.paymentdate,
    mode_of_payment.name,
    order_payment.mode;
--10.04


-- CREATE VIEW tally_orderpayment_bank2bank AS
-- SELECT
--  '' AS uniqueid,
--  CAST(paymentdate AS DATE) AS date,
--  'Payment' AS voucher,
--  'Payment' AS vouchertype,
--  '' AS vouchernumber,
-- CASE 
--     WHEN mode = 5 THEN 'DAP-ICICI-65'
--     WHEN mode = 17 THEN 'DAP-ICICI-42'
--     ELSE 'SENDINGMODE'
-- END AS drledger,
--  mode_of_payment AS crledger,
--  amount AS ledgeramount,
--  clientname || '- ' || orderdescription || '- ' || description AS narration,
--  '' AS instrumentno,
--  '' AS instrumentdate,
--  mode,
--  entityid,
--  tds,
--  serviceid,
--  clientid
-- FROM orderpaymentview
-- WHERE serviceid = 76
--   AND isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.03

CREATE VIEW tally_orderpayments_bank2cash AS
SELECT
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
 CASE 
    WHEN mode = 3 THEN 'DAP-ICICI-42'
    WHEN mode <> 3 THEN 'Cash'
 END AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 clientname || '- ' || orderdescription || '- ' || description AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid
FROM orderpaymentview
WHERE serviceid = 75
  AND isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.02

-- CREATE VIEW tally_orderpayments_taxes AS
-- SELECT 
--  '' AS uniqueid,
--  CAST(paymentdate AS DATE) AS date,
--  'Payment' AS voucher,
--  'Payment' AS vouchertype,
--  '' AS vouchernumber,
--  orderdescription AS drledger,
--  mode_of_payment AS crledger,
--  amount AS ledgeramount,
--  clientname || '- ' || orderdescription || '- ' || description AS narration,
--  '' AS instrumentno,
--  '' AS instrumentdate,
--  mode,
--  entityid,
--  tds,
--  serviceid,
--  clientid
-- FROM orderpaymentview
-- WHERE clientid = 15284
--   AND isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.06

CREATE VIEW tally_orderpayments_no_tds AS
SELECT 
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
 vendorname AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 clientname || '- ' || orderdescription || '- ' || description AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid
FROM orderpaymentview
WHERE clientid NOT IN (15284, 15285)
  AND isdeleted = false
  AND (tds < 0.01 OR tds IS NULL);

------------------------------------------------------------------------------------------------------------------------------------------

--10.07

CREATE VIEW tally_orderpayments_with_tds AS
SELECT 
 '' AS uniqueid,
 CAST(paymentdate AS DATE) AS date,
 'Payment' AS voucher,
 'Payment' AS vouchertype,
 '' AS vouchernumber,
 vendorname AS drledger,
 mode_of_payment AS crledger,
 amount AS ledgeramount,
 clientname || '- ' || orderdescription || '- ' || description AS narration,
 '' AS instrumentno,
 '' AS instrumentdate,
 mode,
 entityid,
 tds,
 serviceid,
 clientid
FROM orderpaymentview
WHERE clientid NOT IN (15284, 15285)
  AND isdeleted = false
  AND tds > 0.00;

------------------------------------------------------------------------------------------------------------------------------------------

--10.01

-- CREATE VIEW tally_clientreceipt AS
-- SELECT
--  ' ' AS uniqueid,
--  CAST(recddate AS DATE) AS date,
--  'Receipt' AS type,
--  'Receipt' AS vouchertype,    
--  ' ' AS vouchernumber,
--  paymentmode AS drledger,
--  clientname AS crledger,
--  amount AS ledgeramount,
--  'Property management charges received' AS narration,
--  ' ' AS instrumentno,
--  ' ' AS instrumentdate,
--  paymentmodeid,
--  entityid
-- FROM clientreceiptlistview
-- WHERE isdeleted = false;

------------------------------------------------------------------------------------------------------------------------------------------

--10.05

-- CREATE OR REPLACE VIEW tally_cr_to_salesinvoice AS
-- SELECT
-- ' ' AS uniqueid,
-- 'Sales' AS base_vch_type,
-- 'GST Invoice' AS vch_type,
-- ' ' AS vch_no,
-- CAST(client_receipt.recddate AS DATE) AS vch_date,
-- ' ' AS ref_no,
-- ' ' AS ref_date,
-- client.firstname || ' ' || client.lastname AS party,
-- ' ' AS gstin,
-- 'Maharashtra' AS state,
-- 'Property Services' AS item_name,
-- ' ' AS item_hsn_code,
-- ' ' AS item_units,
-- ' ' AS item_qty,
-- ' ' AS item_rate,
-- ' ' AS item_discountpercentage,
-- ROUND(client_receipt.amount / 1.18, 2) AS item_amount,
-- ' ' AS igst_percentage,
-- ' ' AS igst_amount,
-- '9' AS cgst_percentage,
-- ROUND(client_receipt.amount * 0.076271, 2) AS cgst_amount,
-- '9' AS sgst_percentage,
-- ROUND(client_receipt.amount * 0.076271, 2) AS sgst_amount,
-- 'GST Sale B2C' AS sales_purchase_ledger,
-- ' ' AS igst_ledger,
-- 'Output CGST' AS cgst_ledger,
-- 'Output SGST' AS sgst_ledger,
-- 'Real estate service fees (HSN 9972)' AS narration,
-- 'Yes' AS auto_round_off_yes_no,
-- client_receipt.tds,
-- client_receipt.serviceamount,
-- client_receipt.reimbursementamount
-- FROM client_receipt
-- INNER JOIN client ON client_receipt.clientid = client.id
-- INNER JOIN entity ON client_receipt.entityid = entity.id
-- WHERE
-- entity.name ILIKE '%CURA%'
-- AND
-- client_receipt.isdeleted = false
-- AND
-- client_receipt.recddate > '2023-12-31'
-- LIMIT 100;

------------------------------------------------------------------------------------------------------------------------------------------

-- SELECT 
--     SUM(receipts) - SUM(payments) AS diff
-- FROM 
--     bankstbalanceview
-- WHERE 
--     name LIKE '%DAP-ICICI-42%' 
--     AND date <= '2024-03-31';


-- SELECT
--     SUM(amount)
-- FROM
--     bank_pmt_rcpts
-- WHERE
--     bankname LIKE '%DAP-ICICI-42%'
    -- AND date <= '2024-03-31';

--11.1

-- CREATE VIEW TotalClientIDsView AS
-- SELECT 'Property ID' AS Type, Client.ID AS ClientID, Client_Property.ID AS RelatedID
-- FROM Client
-- INNER JOIN Client_Property ON Client.ID = Client_Property.ClientID

-- UNION

-- SELECT 'ClientReceipt ID' AS Type, Client.ID AS ClientID, Client_Receipt.ID AS RelatedID
-- FROM Client
-- INNER JOIN Client_Receipt ON Client.ID = Client_Receipt.ClientID

-- UNION

-- SELECT 'Order ID' AS Type, Client.ID AS ClientID, Orders.ID AS RelatedID
-- FROM Client
-- INNER JOIN Orders ON Client.ID = Orders.ClientID

-- UNION

-- SELECT 'ClientPOA ID' AS Type, Client.ID AS ClientID, Client_POA.ID AS RelatedID
-- FROM Client
-- INNER JOIN Client_POA ON Client.ID = Client_POA.ClientID

-- UNION

-- SELECT 'BankSt ID' AS Type, Client.ID AS ClientID, BankSt.ID AS RelatedID
-- FROM Client
-- INNER JOIN BankSt ON Client.ID = BankSt.ClientID;

------------------------------------------------------------------------------------------------------------------------------------------

--11.2

-- CREATE VIEW TotalOrderIDsView AS
-- SELECT 'Order Receipt ID' AS Type, Orders.ID, Order_Receipt.ID AS OrderID
-- FROM Orders
-- INNER JOIN Order_Receipt ON Orders.ID = Order_Receipt.OrderID

-- UNION 

-- SELECT 'Order Payment ID' AS Type, Orders.ID, Order_Payment.ID AS OrderID
-- FROM Orders
-- INNER JOIN Order_Payment ON Orders.ID = Order_Payment.OrderID

-- UNION

-- SELECT 'Order Invoice ID' AS Type, Orders.ID, Order_Invoice.ID AS OrderID
-- FROM Orders
-- INNER JOIN Order_Invoice ON Orders.ID = Order_Invoice.OrderID

-- UNION

-- SELECT 'Vendor Invoice ID' AS Type, Orders.ID, Order_VendorEstimate.ID AS OrderID
-- FROM Orders
-- INNER JOIN Order_VendorEstimate ON Orders.ID = Order_VendorEstimate.OrderID

-- UNION

-- SELECT 'Order Task ID' AS Type, Orders.ID, Order_Task.ID AS OrderID
-- FROM Orders
-- INNER JOIN Order_Task ON Orders.ID = Order_Task.OrderID

-- UNION

-- SELECT 'Order Status Change ID' AS Type, Orders.ID, Order_Status_Change.ID AS OrderID
-- FROM Orders
-- INNER JOIN Order_Status_Change ON Orders.ID = Order_Status_Change.OrderID;

------------------------------------------------------------------------------------------------------------------------------------------

--11.3

-- CREATE VIEW TotalVendorIDsView AS
-- SELECT 'Order Payment ID' AS Type, Vendor.ID, Order_Payment.ID AS VendorID
-- FROM Vendor
-- INNER JOIN Order_Payment ON Vendor.ID = Order_Payment.VendorID

-- UNION

-- SELECT 'Vendor Invoice ID' AS Type, Vendor.ID, Order_VendorEstimate.ID AS VendorID
-- FROM Vendor
-- INNER JOIN Order_VendorEstimate ON Vendor.ID = Order_VendorEstimate.VendorID

-- UNION

-- SELECT 'BankSt ID' AS Type, Vendor.ID, BankSt.ID AS VendorID
-- FROM Vendor
-- INNER JOIN BankSt ON Vendor.ID = BankSt.VendorID;

--13.1

-- CREATE VIEW VendorSummaryForFinancialYearView AS
--  SELECT vendor.vendorname,
--     vendor.addressline1,
--     vendor.addressline2,
--     vendor.suburb,
--     vendor.panno,
--     vendor.tanno,
--     vendor.vattinno,
--     vendor.lbtno,
--     vendor.tdssection,
--     vendor.gstservicetaxno,
--         CASE
--             WHEN vendor.registered = true THEN 'Yes'::text
--             ELSE 'No'::text
--         END AS registered,
--     vendor.bankname,
--     vendor.bankbranch,
--     vendor.bankcity,
--     vendor.bankacctholdername,
--     vendor.bankacctno,
--     vendor.bankifsccode,
--     vendor.bankmicrcode,
--     vendor.bankaccttype,
--     vendor.vendordealerstatus,
--     orderpaymentview.id,
--     orderpaymentview.paymentbyid,
--     orderpaymentview.amount,
--     orderpaymentview.paymentdate,
--     orderpaymentview.orderid,
--     orderpaymentview.vendorid,
--     orderpaymentview.mode,
--     orderpaymentview.description,
--     orderpaymentview.servicetaxamount,
--     orderpaymentview.dated,
--     orderpaymentview.createdbyid,
--     orderpaymentview.isdeleted,
--     orderpaymentview.mode_of_payment,
--     orderpaymentview.createdby,
--     orderpaymentview.paymentby,
--     orderpaymentview.clientname,
--     orderpaymentview.orderdescription,
--     orderpaymentview.tds,
--     orderpaymentview.propertydescription,
--     orderpaymentview.vendorname AS expr1,
--     orderpaymentview.lobname,
--     orderpaymentview.servicetype,
--     orderpaymentview.serviceid,
--     orderpaymentview.monthyear,
--     orderpaymentview.fy
--    FROM vendor
--      JOIN orderpaymentview ON vendor.id = orderpaymentview.vendorid;

------------------------------------------------------------------------------------------------------------------------------------------

--11.2

CREATE VIEW OrderVendorEstimateView AS
SELECT
    Order_VendorEstimate.EstimateDate,
    Order_VendorEstimate.Amount,
    Order_VendorEstimate.ID,
    Order_VendorEstimate.EstimateDesc,
    Order_VendorEstimate.OrderID,
    Order_VendorEstimate.VendorID,
    Order_VendorEstimate.InvoiceDate,
    Order_VendorEstimate.InvoiceAmount,
    OrdersView.BriefDescription,
    OrdersView.ClientName,
    Vendor.VendorName,
    Order_VendorEstimate.Notes,
    Order_VendorEstimate.InvoiceNumber,
    Order_VendorEstimate.Vat1,
    Order_VendorEstimate.Vat2,
    Order_VendorEstimate.ServiceTax,
    OrdersView.ClientID,
    Order_VendorEstimate.CreatedBy AS CreatedById,
    UserView.FullName AS CreatedBy,
    Order_VendorEstimate.EntityId,
    Entity.Name AS EntityName,
    Order_VendorEstimate.OfficeId,
    Office.Name AS OfficeName
FROM
    Order_VendorEstimate
INNER JOIN
    OrdersView ON Order_VendorEstimate.OrderID = OrdersView.ID
INNER JOIN
    Office ON Office.ID = Order_VendorEstimate.OfficeId
INNER JOIN
    UserView ON Order_VendorEstimate.CreatedBy = UserView.UserId
LEFT OUTER JOIN
    Entity ON Order_VendorEstimate.EntityId = Entity.ID
LEFT OUTER JOIN
    Vendor ON Vendor.ID = Order_VendorEstimate.VendorID;

-- CREATE VIEW vendorstatementview AS
-- SELECT
--     'Invoice' AS type,
--     ordervendorestimateview.invoicedate AS invoicedate_orderpaymentdate,
--     ordervendorestimateview.invoiceamount AS invoiceamount_orderpaymentamount,
--     ordervendorestimateview.briefdescription AS estimatedescription_orderdescription,
--     ordervendorestimateview.clientname AS clientname_vendorname,
--     NULL AS modeofpayment,
--     ordersview.clientname,
--     entity.name AS entityname,
--     ordersview.clientid,
--     ordervendorestimateview.vendorid,
--     ordervendorestimateview.id,
--     to_char(ordervendorestimateview.invoicedate, 'YYYY-MM') AS monthyear
-- FROM
--     ordersview
-- INNER JOIN
--     ordervendorestimateview ON ordersview.id = ordervendorestimateview.orderid
-- LEFT OUTER JOIN
--     entity ON ordervendorestimateview.entityid = entity.id
-- UNION
-- SELECT
--     'Payments' AS type,
--     order_payment.paymentdate,
--     order_payment.amount,
--     ordersview.briefdescription AS orderdescription,
--     vendor.vendorname,
--     mode_of_payment.name AS modeofpayment,
--     ordersview.clientname,
--     entity.name,
--     ordersview.id,
--     vendor.id AS vendorid,
--     order_payment.id,
--     to_char(order_payment.paymentdate, 'YYYY-MM') AS monthyear
-- FROM
--     mode_of_payment
-- INNER JOIN
--     order_payment ON mode_of_payment.id = order_payment.mode
-- INNER JOIN
--     vendor ON order_payment.vendorid = vendor.id
-- INNER JOIN
--     ordersview ON order_payment.orderid = ordersview.id
-- INNER JOIN
--     client ON ordersview.clientid = client.id
-- LEFT OUTER JOIN
--     entity ON order_payment.entityid = entity.id;


------------------------------------------------------------------------------------------------------------------------------------------

--17.1

--  CREATE VIEW FIN_TDS_Paid_By_Vendor AS
-- SELECT
--     Vendor.VendorName,
--     CASE WHEN Vendor.companydeductee != false THEN 'YES' ELSE 'NO' END AS companydeductee,
--     Vendor_Category.Name AS VendorCategory,
--     CASE WHEN Vendor.Registered != false THEN 'Yes' ELSE 'No' END AS Registered,
--     Order_Payment.PaymentDate,
--     Order_Payment.Amount,
--     getMonthYear(Order_Payment.PaymentDate) AS MonthYear,
--     getFinancialYear(Order_Payment.PaymentDate) AS FY,
--     Mode_Of_payment.Name AS PaymentMode,
--     Order_Payment.TDS,
--     Vendor.PANNo,
--     Vendor.TDSSection,
--     Order_Payment.ID
-- FROM
--     Order_Payment
-- INNER JOIN Vendor ON Order_Payment.VendorID = Vendor.ID
-- INNER JOIN Vendor_Category ON Vendor.Category = Vendor_Category.ID
-- INNER JOIN Mode_Of_payment ON Order_Payment.Mode = Mode_Of_payment.ID
-- WHERE
--     Order_Payment.TDS > 0;

------------------------------------------------------------------------------------------------------------------------------------------

--17.2

-- CREATE VIEW VendorSummaryForFinancialYearView AS
-- SELECT
--     Vendor.VendorName,
--     Vendor.AddressLine1,
--     Vendor.AddressLine2,
--     Vendor.Suburb,
--     Vendor.PANNo,
--     Vendor.TANNo,
--     Vendor.VATTinNo,
--     Vendor.LBTNo,
--     Vendor.TDSSection,
--     Vendor.gstservicetaxno,
--     CASE WHEN Vendor.Registered = 'true' THEN 'Yes' ELSE 'No' END AS Registered,
--     Vendor.BankName,
--     Vendor.BankBranch,
--     Vendor.BankCity,
--     Vendor.BankAcctHolderName,
--     Vendor.BankAcctNo,
--     Vendor.BankIFSCCode,
--     Vendor.BankMICRCode,
--     Vendor.BankAcctType,
--     Vendor.VendorDealerStatus,
--     OrderPaymentView.ID,
--     OrderPaymentView.PaymentById,
--     OrderPaymentView.Amount,
--     OrderPaymentView.PaymentDate,
--     OrderPaymentView.OrderID,
--     OrderPaymentView.VendorID,
--     OrderPaymentView.Mode,
--     OrderPaymentView.Description,
--     OrderPaymentView.ServiceTaxAmount,
--     OrderPaymentView.Dated,
--     OrderPaymentView.CreatedById,
--     OrderPaymentView.IsDeleted,
--     OrderPaymentView.Mode_Of_payment,
--     OrderPaymentView.CreatedBy,
--     OrderPaymentView.PaymentBy,
--     OrderPaymentView.ClientName,
--     OrderPaymentView.OrderDescription,
--     OrderPaymentView.TDS,
--     OrderPaymentView.PropertyDescription,
--     OrderPaymentView.VendorName AS Expr1,
--     OrderPaymentView.LOBName,
--     OrderPaymentView.ServiceType,
--     OrderPaymentView.ServiceId,
--     OrderPaymentView.MonthYear,
--     OrderPaymentView.FY
-- FROM
--     Vendor
-- INNER JOIN
--     OrderPaymentView ON Vendor.ID = OrderPaymentView.VendorID;

------------------------------------------------------------------------------------------------------------------------------------------


--17.3




------------------------------------------------------------------------------------------------------------------------------------------

--17.3

-- CREATE VIEW TDSPaidtoGovernment AS
-- SELECT
--     REPLACE(REPLACE(orders.BriefDescription, E'\n', ''), E'\r', '') AS "Order Description",
--     Order_Payment.Amount,
--     TO_CHAR(Order_Payment.PaymentDate, 'DD-MM-YYYY') AS Date,
--     REPLACE(REPLACE(Order_Payment.Description, E'\n', ''), E'\r', '') AS "Payment Description",
--     Vendor.VendorName,
--     orders.ID AS OrderID
-- FROM
--     Order_Payment
-- INNER JOIN
--     orders ON Order_Payment.OrderID = orders.ID
-- INNER JOIN
--     Vendor ON Order_Payment.VendorID = Vendor.ID
-- WHERE
--     orders.ID IN (31648, 10770, 31649, 353444, 122525);

--16.1,5.1

CREATE VIEW orderstatisticsview AS
SELECT
    service,
    lobname,
    COUNT(CASE WHEN orderstatus = 'On Hold' THEN 1 END) AS on_hold,
    COUNT(CASE WHEN orderstatus = 'Estimate Given' THEN 1 END) AS estimate_given,
    COUNT(CASE WHEN orderstatus = 'Confirmed' THEN 1 END) AS confirmed,
    COUNT(CASE WHEN orderstatus = 'Cancelled' THEN 1 END) AS cancelled,
    COUNT(CASE WHEN orderstatus = 'Closed' THEN 1 END) AS closed,
    COUNT(CASE WHEN orderstatus = 'Billed' THEN 1 END) AS billed,
    COUNT(CASE WHEN orderstatus = 'Inquiry' THEN 1 END) AS inquiry,
    COUNT(CASE WHEN orderstatus = 'Completed' THEN 1 END) AS completed,
    COUNT(CASE WHEN orderstatus = 'In progress' THEN 1 END) AS in_progress
FROM ordersview
GROUP BY service, lobname;

------------------------------------------------------------------------------------------------------------------------------------------

--5.2

create view ordersummary as SELECT 
    clientsummaryview.clientname,
    clientsummaryview.propertydescription,
    clientsummaryview.briefdescription AS orderdescription,
    clientsummaryview.orderdate,
    clientsummaryview.orderstatus,
    clientsummaryview.entityname,
    clientsummaryview.service,
    clientsummaryview.lobname,
    clientsummaryview.sumpayment AS totalorderpayment,
    clientsummaryview.invoiceamount AS totalinvoiceamt,
    clientsummaryview.sumreceipt AS totalorderreceipt,
    clientsummaryview.computedpending,
    clientsummaryview.profit,
    clientsummaryview.orderid
   FROM clientsummaryview;

------------------------------------------------------------------------------------------------------------------------------------------

--6

-- CREATE OR REPLACE VIEW client_property_leave_license_detailsview AS
-- SELECT
--         CASE
--             WHEN cplld.active = true THEN 'Active'::text
--             ELSE 'Inactive'::text
--         END AS status,
--     cplld.clientpropertyid,
--     cplld.orderid,
--     cplld.startdate,
--     cplld.vacatingdate,
--     cplld.durationinmonth,
--     cplld.actualenddate,
--     cplld.depositamount,
--     cplld.rentamount,
--     cplld.registrationtype,
--     cplld.rentpaymentdate,
--     cplld.paymentcycle,
--     cplld.reasonforclosure,
--     cplld.noticeperiodindays,
--     cplld.modeofrentpaymentid,
--     cplld.clientpropertyorderid,
--     cplld.signedby,
--     cplld.active,
--     cplld.llscancopy,
--     cplld.pvscancopy,
--     cplld.dated,
--     cplld.createdby AS expr2,
--     cplld.isdeleted,
--     cplld.id,
--     cplld.comments,
--     pv.clientname,
--     pv.propertydescription,
--     ov.propertydescription AS expr1,
--     ( SELECT getmonthyear(cplld.startdate::timestamp without time zone) AS getmonthyear) AS startdatemonthyear,
--     ( SELECT getmonthyear(cplld.actualenddate::timestamp without time zone) AS getmonthyear) AS enddatemonthyear,
--     ov.orderstatus,
--     ov.status AS orderstatusid,
--     pv.clientid,
--     pv.propertytaxnumber,
--     pv.property_status,
--     pv.electricitybillingunit,
--     pv.electricityconsumernumber,
--     ov.service,
--     ov.lobname,
--     ov.entityname,
--     cv.clienttype,
--     cv.clienttypename
--    FROM client_property_leave_license_details cplld
--      JOIN propertiesview pv ON cplld.clientpropertyid = pv.id
--      JOIN clientview cv ON pv.clientid = cv.id
--  LEFT JOIN ordersview ov ON cplld.orderid = ov.id;
-- ------------------------------------------------------------------------------------------------------------------------------------------

--7.6

CREATE VIEW client_property_leave_license_detailslistview AS
SELECT
        CASE
            WHEN cplld.active = true THEN 'Active'::text
            ELSE 'Inactive'::text
        END AS status,
    cplld.clientpropertyid,
    cplld.orderid,
    cplld.startdate,
    cplld.vacatingdate,
    cplld.durationinmonth,
    cplld.actualenddate,
    cplld.depositamount,
    cplld.rentamount,
    cplld.registrationtype,
    cplld.rentpaymentdate,
    cplld.paymentcycle,
    cplld.reasonforclosure,
    cplld.noticeperiodindays,
    cplld.modeofrentpaymentid,
    cplld.clientpropertyorderid,
    cplld.signedby,
    cplld.active,
    cplld.tenantsearchmode AS tenantsearchmodeid,
    cplld.llscancopy,
    cplld.pvscancopy,
    cplld.dated,
    cplld.createdby AS expr2,
    cplld.isdeleted,
    cplld.id,
    cplld.comments,
    pv.clientname,
    pv.propertydescription,
    ov.propertydescription AS expr1,
    ( SELECT getmonthyear(cplld.startdate::timestamp without time zone) AS getmonthyear) AS startdatemonthyear,
    ( SELECT getmonthyear(cplld.actualenddate::timestamp without time zone) AS getmonthyear) AS enddatemonthyear,
    ov.orderstatus,
    ov.status AS orderstatusid,
    pv.clientid,
    pv.propertytaxnumber,
    pv.property_status,
    pv.electricitybillingunit,
    pv.electricityconsumernumber,
    ov.service,
    ov.lobname,
    ov.entityname,
    cv.clienttype,
    cv.clienttypename,
    'CR' AS type
   FROM client_property_leave_license_details cplld
     JOIN propertiesview pv ON cplld.clientpropertyid = pv.id
     JOIN clientview cv ON pv.clientid = cv.id
     LEFT JOIN ordersview ov ON cplld.orderid = ov.id;

    --16.3

CREATE VIEW clienttypecountview AS
SELECT
    COUNT(client.clienttype) AS total,
    client.clienttype,
    client_type.name
FROM
    client
INNER JOIN
    client_type ON client.clienttype = client_type.id
GROUP BY
    client.clienttype, client_type.name;

--------------------------------------------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW totalcountview AS
SELECT 
    'Client Receipt' AS type,
    COUNT(*) AS count,
    SUM(amount) AS amount
FROM 
    client_receipt
UNION
SELECT 
    'Order Receipt' AS type,
    COUNT(*) AS count,
    SUM(amount) AS amount
FROM 
    order_receipt
UNION
SELECT 
    'Cont Pay' AS type,
    COUNT(*) AS count,
    SUM(amount) AS amount
FROM 
    ref_contractual_payments
UNION
SELECT 
    'Order Payment' AS type,
    COUNT(*) AS count,
    SUM(amount) AS amount
FROM 
    order_payment
UNION
SELECT 
    'Client Invoice' AS type,
    COUNT(*) AS count,
    SUM(invoiceamount) AS amount
FROM 
    order_invoice
UNION
SELECT 
    'Vendor Invoice' AS type,
    COUNT(*) AS count,
    SUM(invoiceamount) AS amount
FROM 
    order_vendorestimate
UNION
SELECT 
    'Client' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    client
UNION
SELECT 
    'Order' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    orders
UNION
SELECT 
    'Task' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    order_task
UNION
SELECT 
    'Vendor' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    vendor
UNION
SELECT 
    'Builder' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    builder
UNION
SELECT 
    'Owners' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    owners
UNION
SELECT 
    'Client Properties' AS type,
    COUNT(*) AS count,
    SUM(0) AS amount
FROM 
    client_property
UNION
SELECT 
    'BankStatementRecords' AS Type, 
    COUNT(*) AS Count, 
    SUM(amount) AS Amount
FROM 
    BankSt
UNION
SELECT 
    'BuilderProjects' AS Type, 
    COUNT(*) AS Count, 
    SUM(0) AS Amount
FROM 
    Project
UNION
SELECT 
    'Users' AS Type, 
    COUNT(*) AS Count, 
    SUM(0) AS Amount
FROM 
    usertable
UNION
SELECT 
    'Employees' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM 
    Employee
UNION
SELECT
    'LOBs' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM LOB
UNION
SELECT 
    'Services' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM 
    Services
UNION
SELECT 
    'Cities' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM 
    Cities
UNION
SELECT 
    'Countries' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM 
    Country
UNION
SELECT 
    'PMA_Agreements' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM 
    Client_Property_Caretaking_Agreement
UNION
SELECT 
    'L_L_Agreements' AS Type,
    COUNT(*) AS Count,
    SUM(RentAmount) AS Amount
FROM 
    Client_Property_Leave_License_Details
UNION
SELECT 
    'Localities' AS Type,
    COUNT(*) AS Count,
    SUM(0) AS Amount
FROM Locality;
;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW ownersview AS
SELECT
    owners.name,
    owners.id,
    owners.emailid,
    owners.phoneno,
    owners.dated,
    owners.createdby,
    owners.suburb,
    cities.state,
    cities.city,
    cities.id AS cityid,
    cities.countryid,
    country.name AS countryname,
    owners.corporation,
    owners.propertytaxno,
    owners.societyname,
    owners.address,
    owners.isexcludedmailinglist,
    owners.phoneno1,
    owners.phoneno2,
    owners.propertyfor,
    owners.propertydetails,
    owners.source
FROM
    owners
LEFT OUTER JOIN
    cities ON owners.city = cities.id
LEFT OUTER JOIN
    country ON cities.countryid = country.id
WHERE
    owners.isdeleted = 'false';

CREATE VIEW ownersstatisticsview AS
SELECT
    COUNT(CASE WHEN source = 'Corporation' THEN 1 END) AS Corporation,
    COUNT(CASE WHEN source = 'RBS-Rentals' THEN 1 END) AS RBSRentals,
    COUNT(CASE WHEN source = 'RBS-Sales' THEN 1 END) AS RBSSales,
    COALESCE(SUM(CASE WHEN source = 'ID' THEN 1 END), -1) AS ID
FROM
    ownersview;

------------------------------------------------------------------------------------------------------------------------------------------

--14.2

CREATE VIEW fin_service_tax_paid_by_vendor AS
SELECT
    vendor.vendorname,
    vendor.gstservicetaxno,
    vendor_category.name AS vendorcategory,
    CASE WHEN vendor.registered THEN 'Yes' ELSE 'No' END AS registered,
    order_payment.paymentdate,
    order_payment.amount,
    order_payment.servicetaxamount,
    getmonthyear(order_payment.paymentdate) AS monthyear,
    getfinancialyear(order_payment.paymentdate) AS fy,
    mode_of_payment.name AS paymentmode,
    order_payment.id
FROM
    order_payment
INNER JOIN
    vendor ON order_payment.vendorid = vendor.id
INNER JOIN
    vendor_category ON vendor.category = vendor_category.id
INNER JOIN
    mode_of_payment ON order_payment.mode = mode_of_payment.id
WHERE
    order_payment.servicetaxamount > 0;

CREATE VIEW Rpt_SuspensePayments AS
SELECT
    ClientName,
    OrderDescription AS ORDERDESC,
    PaymentDate,
    Mode_Of_payment AS PAYMENTMODE,
    PaymentBy,
    Amount,
    Description AS PaymentDescription,
    VendorName,
    row_number() OVER (ORDER BY ClientName) AS RN
FROM
    OrderPaymentView
WHERE
    ClientName LIKE '%ZZZ%'
    AND Amount <> 0
ORDER BY
    PaymentDate DESC;

------------------------------------------------------------------------------------------------------------------------------------------


CREATE VIEW Rpt_SuspenseReceipts AS
SELECT
    ClientName,
    OrderDescription AS ORDERDESC,
    RecdDate,
    PaymentMode,
    ReceivedBy AS PAYMENTBY,
    Amount,
    ReceiptDesc AS ReceiptDescription,
    row_number() OVER (ORDER BY ClientName) AS RN
FROM
    OrderReceiptView
WHERE
    ClientName LIKE '%ZZZ%'
    AND Amount <> 0
ORDER BY
    RecdDate DESC;

------------------------------------------------------------------------------------------------------------------------------------------


CREATE VIEW Rpt_ClientsWithOrderButEmailMissing AS
SELECT
    FullName,
    ClientTypeName,
    CountryName,
    EMail1,
    EMail2
FROM
    ClientView
WHERE
    (EMail1 IS NULL AND (EMail2 = '' OR EMail2 LIKE 'tbd%') AND EXISTS
        (SELECT 1
         FROM Orders
         WHERE Orders.ClientID = ClientView.id))
    OR
    (EMail1 = '' AND (EMail2 = '' OR EMail2 LIKE 'tbd%') AND EXISTS
        (SELECT 1
         FROM Orders
         WHERE Orders.ClientID = ClientView.id))
    OR
    (EMail1 LIKE 'tbd%' AND (EMail2 = '' OR EMail2 LIKE 'tbd%') AND EXISTS
        (SELECT 1
         FROM Orders
         WHERE Orders.ClientID = ClientView.id));

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW VendorView AS
SELECT
    Vendor.ID,
    Vendor.VendorName,
    Vendor.CompanyDeductee,
    Vendor.AddressLine1,
    Vendor.AddressLine2,
    Vendor.Suburb,
    Vendor.State,
    Vendor.Zip,
    Vendor.Type,
    Vendor.ServiceType,
    Vendor.Details,
    Vendor.Category,
    Vendor.Phone1,
    Vendor.EMail,
    Vendor.OwnerInfo,
    Vendor.TANNo,
    Vendor.PANNo,
    Vendor.VATTinNo,
    Vendor.gstservicetaxno AS ServiceTaxNo,
    Vendor.LBTNo,
    Vendor.TDSSection,
    Vendor.Registered,
    Vendor.BankName,
    Vendor.BankBranch,
    Vendor.BankCity,
    Vendor.BankAcctHolderName,
    Vendor.BankAcctNo,
    Vendor.BankIFSCCode,
    Vendor.BankMICRCode,
    Vendor.BankAcctType,
    Vendor.VendorDealerStatus,
    Vendor.Dated,
    Vendor.CreatedBy AS CreatedById,
    Vendor.IsDeleted,
    UserTable.FirstName || ' ' || UserTable.LastName AS CreatedBy,
    Vendor_Category.Name AS CategoryName,
    Country.Name AS Country,
    Cities.City,
    Country.ID AS CountryId,
    Cities.ID AS CityId,
    TallyLedger.TallyLedger,
    Vendor.TallyLedgerId
FROM
    Vendor_Category
    INNER JOIN Vendor ON Vendor_Category.ID = Vendor.Category
    INNER JOIN UserTable ON Vendor.CreatedBy = UserTable.ID
    INNER JOIN Country ON Vendor.Country = Country.ID
    INNER JOIN Cities ON Vendor.City = Cities.ID
    LEFT OUTER JOIN TallyLedger ON Vendor.TallyLedgerId = TallyLedger.ID
WHERE
    Vendor.IsDeleted = FALSE;


CREATE VIEW Rpt_UserVendorMapping AS
SELECT
    UserView.UserId,
    UserView.UserName,
    UserView.UserStatus,
    VendorView.ID,
    VendorView.VendorName
FROM
    UserView
    LEFT OUTER JOIN Vendor_user_mapping ON UserView.UserId = Vendor_user_mapping.userid
    LEFT OUTER JOIN VendorView ON Vendor_user_mapping.vendorid = VendorView.ID;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW Rpt_BankTransactionsWithWrongNames AS
SELECT
    'Payment' AS type,
    ID,
    ClientName,
    OrderDescription,
    Mode_Of_payment,
    PaymentBy AS DoneBy,
    Amount
FROM
    OrderPaymentView
WHERE
    Mode_Of_payment NOT IN ('Cash', 'ZZZ-DO-NOT-USE')
    AND PaymentBy NOT LIKE '%anvay%'
UNION ALL
SELECT
    'Receipt' AS type,
    ID,
    ClientName,
    OrderDescription,
    paymentmode,
    ReceivedBy AS DoneBy,
    Amount
FROM
    OrderReceiptView
WHERE
    paymentmode NOT IN ('Cash', 'ZZZ-DO-NOT-USE')
    AND ReceivedBy NOT LIKE '%anvay%';

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW Rpt_EntityblankView AS
SELECT
    'OI' AS TYPE,
    OrdersView.ClientName,
    Order_Invoice.ID,
    Order_Invoice.InvoiceDate AS Date,
    Order_Invoice.InvoiceAmount AS Amount,
    NULL AS TDS,
    REPLACE(REPLACE(OrdersView.BriefDescription, CHR(10), ''), CHR(13), '') AS OrderDetails,
    Entity.Name AS Entity,
    Services.Service,
    OrdersView.LOBName,
    REPLACE(REPLACE(Order_Invoice.QuoteDescription, CHR(10), ''), CHR(13), '') AS Details,
    '' AS Mode,
    OrdersView.ClientTypeName AS "Client Type",
    OrdersView.ID AS "Order ID",
    OrdersView.ClientID AS ClientId,
    getMonthYear(Order_Invoice.InvoiceDate) AS MonthYear,
    getFinancialYear(Order_Invoice.InvoiceDate) AS FY
FROM
    Order_Invoice
    LEFT OUTER JOIN OrdersView ON OrdersView.ID = Order_Invoice.OrderID
    LEFT OUTER JOIN Entity ON Entity.ID = Order_Invoice.EntityId
    LEFT OUTER JOIN Services ON Services.ID = OrdersView.ServiceId
WHERE
    Entity.Name IS NULL
UNION ALL
SELECT
    'CR' AS TYPE,
    ClientView.FullName,
    ClientReceiptView.ID,
    ClientReceiptView.RecdDate AS Date,
    - (1 * ClientReceiptView.Amount),
    ClientReceiptView.TDS,
    NULL AS OrderDetails,
    Entity.Name AS Entity,
    NULL AS Service,
    NULL AS LOBName,
    HowReceived.Name AS Details,
    ClientReceiptView.PaymentMode AS Mode,
    ClientView.ClientTypeName,
    NULL AS "Order ID",
    ClientView.ID AS ClientId,
    getMonthYear(ClientReceiptView.RecdDate) AS MonthYear,
    getFinancialYear(ClientReceiptView.RecdDate) AS FY
FROM
    ClientView
    INNER JOIN ClientReceiptView ON ClientView.ID = ClientReceiptView.ClientID
    LEFT OUTER JOIN Entity ON ClientReceiptView.EntityId = Entity.ID
    LEFT OUTER JOIN HowReceived ON ClientReceiptView.HowReceivedId = HowReceived.ID
WHERE
    Entity.Name IS NULL
UNION ALL
SELECT
    'OR' AS TYPE,
    ClientView.FullName,
    OrderReceiptView.ID,
    OrderReceiptView.RecdDate AS Date,
    - (1 * OrderReceiptView.Amount) AS Expr1,
    OrderReceiptView.TDS,
    OrderReceiptView.OrderDescription AS OrderDetails,
    Entity.Name AS Entity,
    OrderReceiptView.Service,
    OrderReceiptView.LOBName,
    OrderReceiptView.ReceiptDesc AS Details,
    OrderReceiptView.PaymentMode AS Mode,
    ClientView.ClientTypeName,
    OrderReceiptView.OrderID AS "Order ID",
    ClientView.ID AS ClientId,
    getMonthYear(OrderReceiptView.RecdDate) AS MonthYear,
    getFinancialYear(OrderReceiptView.RecdDate) AS FY
FROM
    ClientView
    INNER JOIN OrderReceiptView ON ClientView.ID = OrderReceiptView.ClientID
    LEFT OUTER JOIN Entity ON OrderReceiptView.EntityId = Entity.ID
WHERE
    Entity.Name IS NULL
UNION ALL
SELECT
    'OP' AS TYPE,
    ClientView.FullName,
    OrderPaymentView.ID,
    OrderPaymentView.PaymentDate AS Date,
    - (1 * OrderPaymentView.Amount) AS Expr1,
    OrderPaymentView.TDS,
    OrderPaymentView.OrderDescription AS OrderDetails,
    Entity.Name AS Entity,
    OrderPaymentView.Service,
    OrderPaymentView.LOBName,
    OrderPaymentView.Description AS Details,
    OrderPaymentView.Mode_Of_payment AS Mode,
    ClientView.ClientTypeName,
    OrderPaymentView.OrderID AS "Order ID",
    ClientView.ID AS ClientId,
    getMonthYear(OrderPaymentView.PaymentDate) AS MonthYear,
    getFinancialYear(OrderPaymentView.PaymentDate) AS FY
FROM
    ClientView
    INNER JOIN OrderPaymentView ON ClientView.ID = OrderPaymentView.ClientID
    LEFT OUTER JOIN Entity ON OrderPaymentView.EntityId = Entity.ID
WHERE
    Entity.Name IS NULL
    AND OrderPaymentView.Mode_Of_payment NOT LIKE '%Stores%';

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW noPropertyOwnersView AS
SELECT
    Client.FirstName || ' ' || Client.LastName AS FullName,
    Client.ClientType,
    Client.ID,
    Client_Type.Name as clienttype_text
FROM
    Client
    INNER JOIN Client_Type ON Client.ClientType = Client_Type.ID
    LEFT OUTER JOIN Client_Property ON Client.ID = Client_Property.ClientID
WHERE
    Client_Property.ID IS NULL
    AND (Client.ClientType = 2 OR Client.ClientType = 7);

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW FIN_Agency_Services_Receipts_For_Taxes AS
SELECT
    Services.ServiceType,
    Services.Service,
    Client.FirstName,
    Client.LastName,
    orders.BriefDescription AS OrderDescription,
    Order_Receipt.Amount,
    Order_Receipt.PaymentMode,
    Order_Receipt.RecdDate,
    getMonthYear(Order_Receipt.RecdDate) AS MonthYear,
    getFinancialYear(Order_Receipt.RecdDate) AS FY,
    orders.ID,
    Order_Receipt.ID AS ReceiptId,
    Client.FirstName || ' ' || Client.LastName AS ClientName,
    Mode_Of_payment.Name AS PaymentModeName
FROM
    Client
    INNER JOIN orders ON Client.ID = orders.ClientID
    INNER JOIN Order_Receipt ON orders.ID = Order_Receipt.OrderID
    INNER JOIN Services ON orders.Service = Services.ID
    INNER JOIN Mode_Of_payment ON Order_Receipt.PaymentMode = Mode_Of_payment.ID
WHERE
    (Services.ServiceType = 'AgencyServices'
    OR Services.ServiceType = 'RepairServices'
    OR Services.ServiceType = 'Material')
    AND (Order_Receipt.PaymentMode IN (4, 5, 7, 8))
    AND Order_Receipt.EntityId = 1;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW Rpt_Client_And_Inquiry_MailIDs AS
SELECT
    tempdata.EMAIL,
    COALESCE(ROW_NUMBER() OVER (ORDER BY EMAIL), 0) AS RN
FROM
    (SELECT DISTINCT email1 AS EMAIL
     FROM client
     WHERE clienttype IN (SELECT id FROM client_type WHERE name = 'Owner - Individual') 
     AND (email1 IS NOT NULL AND email1 <> '' AND email1 <> 'tbd@tbd.com')
     UNION ALL
     SELECT DISTINCT email2 AS EMAIL
     FROM client
     WHERE clienttype IN (SELECT id FROM client_type WHERE name = 'Owner - Individual') 
     AND (email2 IS NOT NULL AND email2 <> '' AND email2 <> 'tbd@tbd.com')
     UNION ALL
     SELECT DISTINCT email AS EMAIL
     FROM research_inquiry
     WHERE ConvertedToClient = FALSE AND email <> '' AND email <> 'tbd@tbd.com') AS tempdata;

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW Rpt_AllTenantMailIds AS
SELECT
    FullName,
    FirstName,
    LastName,
    EMail1,
    EMail2,
    EmployerName
FROM
    ClientView
WHERE
    ClientTypeName = 'Tenant - Individual';

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW OwnersPhonenoView AS
WITH ue(id1) AS (
    SELECT MAX(ID) AS id1
    FROM Owners
    GROUP BY PhoneNo, PhoneNo1, PhoneNo2
)
SELECT ID, Name, PhoneNo, PhoneNo1, PhoneNo2 
FROM Owners t
INNER JOIN ue ON ue.id1 = t.id 
WHERE PhoneNo ~ '^[7-9]' OR PhoneNo != 'NA' OR PhoneNo != '';

------------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW ClientPhonenoView AS
 WITH ue(id1) AS (
         SELECT max(client.id) AS id1
           FROM client
          GROUP BY client.workphone, client.mobilephone, client.homephone
        )
 SELECT t.id,
    t.firstname,
    t.workphone,
    t.mobilephone,
    t.homephone,
    t.clienttype,
    t.lastname,
    (t.firstname || ' '::text) || t.lastname AS clientname,
    client_type.name AS clienttypename
   FROM client t
     JOIN ue ue_1 ON ue_1.id1 = t.id
     JOIN client_type ON t.clienttype = client_type.id
  WHERE t.mobilephone ~ '^[7-9]'::text OR t.mobilephone <> 'NA'::text OR t.mobilephone <> ''::text;

