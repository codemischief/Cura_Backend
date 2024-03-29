
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
    payment_for e 
WHERE 
    a.paymentto = b.id 
    AND a.paymentby = c.id 
    AND a.paymentmode = d.id 
    AND a.paymentfor = e.id;



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