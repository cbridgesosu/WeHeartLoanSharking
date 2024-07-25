/*
This file is based on the example provided in CS340 at Oregon State University.
Access URL: https://canvas.oregonstate.edu/courses/1967354/assignments/9690212
Access Date: 2024-07-25
*/

--These are some Database Manipulation queries for a partially implemented Project Website 
-- using the bsg database.
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.

/*
-- get all Planet IDs and Names to populate the Homeworld dropdown
SELECT planet_id, name FROM bsg_planets
*/

-- Retrieve all Client information to populate Add Client, Update Client or Delete Client pages
SELECT * FROM Clients;

-- Retrieve all Enforcer information to show on Add New Enforcer page
SELECT * FROM Enforcers;

-- Retrieve all assignments between Enforcers and Clients on Assigned Clients page
SELECT * FROM EnforcersHasClients;

-- Retrieve all Business (Location) information to display on Add Location page
SELECT * FROM BusinessLocations;

-- Retrieve all Loan information to display on Add Loan page
SELECT * FROM Loans;

-- Retrieve all Collection information to display on Add Collection page
SELECT * FROM Collections;

-- add a new client
INSERT INTO Clients (firstName, lastName, inGoodStanding) VALUES (:fnameInput, :lnameInput, 0);

-- add a new Enforcer 
INSERT INTO Enforcers (firstName, lastName, startDate) VALUES (:fnameInput, :lnameInput, :dateInput);





-- get all characters and their homeworld name for the List People page
SELECT bsg_people.character_id, fname, lname, bsg_planets.name AS homeworld, age FROM bsg_people INNER JOIN bsg_planets ON homeworld = bsg_planets.planet_id

-- get a single character's data for the Update People form
SELECT character_id, fname, lname, homeworld, age FROM bsg_people WHERE character_id = :character_ID_selected_from_browse_character_page

-- get all character's data to populate a dropdown for associating with a certificate  
SELECT character_id AS pid, fname, lname FROm bsg_people 
-- get all certificates to populate a dropdown for associating with people
SELECT certification_id AS cid, title FROM bsg_cert

-- get all peoople with their current associated certificates to list
SELECT pid, cid, CONCAT(fname,' ',lname) AS name, title AS certificate 
FROM bsg_people 
INNER JOIN bsg_cert_people ON bsg_people.character_id = bsg_cert_people.pid 
INNER JOIN bsg_cert on bsg_cert.certification_id = bsg_cert_people.cid 
ORDER BY name, certificate

-- add a new character
INSERT INTO bsg_people (fname, lname, homeworld, age) VALUES (:fnameInput, :lnameInput, :homeworld_id_from_dropdown_Input, :ageInput)

-- associate a character with a certificate (M-to-M relationship addition)
INSERT INTO bsg_cert_people (pid, cid) VALUES (:character_id_from_dropdown_Input, :certification_id_from_dropdown_Input)

-- update a character's data based on submission of the Update Character form 
UPDATE bsg_people SET fname = :fnameInput, lname= :lnameInput, homeworld = :homeworld_id_from_dropdown_Input, age= :ageInput WHERE id= :character_ID_from_the_update_form

-- delete a character
DELETE FROM bsg_people WHERE id = :character_ID_selected_from_browse_character_page

-- dis-associate a certificate from a person (M-to-M relationship deletion)
DELETE FROM bsg_cert_people WHERE pid = :character_ID_selected_from_certificate_and_character_list AND cid = :certification_ID_selected_from-certificate_and_character_list
