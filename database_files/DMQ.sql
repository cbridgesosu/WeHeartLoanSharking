/*
This file is based on the example provided in CS340 at Oregon State University.
Access URL: https://canvas.oregonstate.edu/courses/1967354/assignments/9690212
Access Date: 2024-07-25
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

-- Retrieve all Rank information to display on Add Rank page
SELECT * FROM Ranks;

-- add a new client
INSERT INTO Clients (firstName, lastName, inGoodStanding) VALUES (:fnameInput, :lnameInput, 0);

-- add a new Enforcer 
INSERT INTO Enforcers (firstName, lastName, startDate) VALUES (:fnameInput, :lnameInput, :dateInput);

-- add a new Location
INSERT INTO BusinessLocations (ownerID, streetAddress, cityName, stateName, zipCode)
VALUES (:ownerID, :streetAddress, :cityName, :stateName, :zipCode);

-- add a new Loan
INSERT INTO Loans (clientID, originationAmount, principalRemaining, originationDate, interestRate, paymentDue)
VALUES (:clientID, :originationAmount, :originationAmount, :originationDate, :interestRate, :dayOfMonthDue);

-- add a new Collection
INSERT INTO Collections (enforcerID, loanID, businessID, amountCollected, dateOfCollection)
VALUES (:enforcerID, :loanID, :businessID, :amountCollected, :dateOfCollection);

-- add a new Rank
INSERT INTO Ranks (rankName)
VALUES (:rankName);

-- Assign client to enforcer (add a new client / enforcer relationship)
INSERT INTO EnforcersHasClients (enforcerID, clientID)
VALUES (:enforcerID, :clientID);

-- delete a client
DELETE FROM Clients WHERE clientID = :clientID_selected_from_delete_client_page;

-- update a client
UPDATE Clients SET firstName = :fnameInput, lastName= :lnameInput, inGoodStanding = :inGoodStanding_Input WHERE id= :clientID_selected_from_the_update_form;
