-- Charles Holz
-- Christopher Bridges
-- CS340 - Group 41
-- We ❤️ Loan Sharking

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

-- SELECT Rank Names to dynamically populate dropdown when adding an Enforcer
SELECT rankName FROM Ranks;

-- add a new client
INSERT INTO Clients (firstName, lastName, inGoodStanding) VALUES (:fnameInput, :lnameInput, 0);

-- add a new Enforcer 
INSERT INTO Enforcers (firstName, lastName, startDate) VALUES (:fnameInput, :lnameInput, :dateInput);

-- Query to populate the display table
SELECT enforcerHasClientID, Enforcers.firstName, Enforcers.lastName, Clients.firstName, Clients.lastName FROM EnforcersHasClients INNER JOIN Enforcers ON EnforcersHasClients.enforcerID=Enforcers.enforcerID INNER JOIN Clients ON EnforcersHasClients.clientID=Clients.clientID ORDER BY enforcerHasClientID;

-- Query to polulate the select client dropdown  
SELECT clientID, firstName, lastName FROM Clients;

-- Query to polulate the select enforcer dropdown 
SELECT enforcerID, firstName, lastName FROM Enforcers;

-- Insert query for add new enforcers_has_client 
INSERT INTO EnforcersHasClients (enforcerID, clientID) VALUES (%s, %s);
    
-- Perform the update in the database with the values supplied by the user if the request is a POST
UPDATE EnforcersHasClients SET EnforcersHasClients.clientID = {clientID}, EnforcersHasClients.enforcerID = {enforcerID} WHERE EnforcersHasClients.enforcerHasClientID = {id};

-- Query to populate the display table on the enforcers page, including Enforcers without ranks
SELECT enforcerID, firstName, lastName, startDate, rankName FROM Enforcers LEFT JOIN Ranks ON Enforcers.rankID=Ranks.rankID ORDER BY enforcerID;

-- Query to polulate the select ranks dropdown  
SELECT rankID, rankName FROM Ranks;

-- Insert query for add new enforcer
INSERT INTO Enforcers (firstName, lastName, startDate, rankID) VALUES (firstName, lastName, startDate, rankID); 

-- Query to delete enforcer entry with selected ID
DELETE FROM Enforcers WHERE enforcerID = enforcerID; 

--Query to populate form with current enforcer attributes, in the update page
SELECT enforcerID, firstName, lastName, startDate, Ranks.rankID, rankName FROM Enforcers LEFT JOIN Ranks ON Ranks.rankID=Enforcers.rankID WHERE enforcerID = (enforcerID);

-- Query to populate ranks select dropdown on enforcers update page
SELECT * FROM Ranks;

-- Query to update eforcer attributes
UPDATE Enforcers SET Enforcers.firstName = firstName, Enforcers.lastName = lastName, Enforcers.startDate = startDate, Enforcers.rankID = rankID WHERE Enforcers.enforcerID = enforcerID;

-- Query to insert a record into the Clients table
INSERT INTO Clients (firstName, lastName, inGoodStanding) VALUES (firstName, lastName, inGoodStanding);

-- Query to populate the update Client page with the currently selected Client attributes
SELECT * FROM Clients WHERE clientID = (clientID);

-- Query to update the Client record
UPDATE Clients SET Clients.firstName = firstName, Clients.lastName = lastName, Clients.inGoodStanding =inGoodStanding WHERE Clients.clientID = clientID;

-- Query to delete Client with the selected ID
DELETE FROM Clients WHERE clientID = clientID;

-- Queries to populate the Enforcers Has Clients select table
SELECT enforcerHasClientID, Enforcers.firstName, Enforcers.lastName, Clients.firstName, Clients.lastName FROM EnforcersHasClients INNER JOIN Enforcers ON EnforcersHasClients.enforcerID=Enforcers.enforcerID INNER JOIN Clients ON EnforcersHasClients.clientID=Clients.clientID ORDER BY enforcerHasClientID;
SELECT clientID, firstName, lastName FROM Clients;
SELECT enforcerID, firstName, lastName FROM Enforcers;

-- Query to add a new relationship in the intersection table.
INSERT INTO EnforcersHasClients (enforcerID, clientID) VALUES (enforcerID, clientID);

-- Query to delete enforcer_has_client entry with selected ID
DELETE FROM EnforcersHasClients WHERE enforcerHasClientID = enforcerHasClientID;

-- Setup queries for Clients, Enforcers and the Selected relationship to edit.
SELECT clientID, firstName, lastName FROM Clients;
SELECT enforcerID, firstName, lastName FROM Enforcers;
SELECT * FROM EnforcersHasClients WHERE enforcerHasClientID = id;

-- Query to update the relationship in the intersection table with user supplied values
UPDATE EnforcersHasClients SET EnforcersHasClients.clientID = clientID, EnforcersHasClients.enforcerID = enforcerID WHERE EnforcersHasClients.enforcerHasClientID = id;

-- Query to populate the clients select dropdown
SELECT clientID, firstName, lastName FROM Clients;

-- Query to populate the locations display table
SELECT businessID, streetAddress, cityName, stateName, zipCode, Clients.firstName, Clients.lastName FROM BusinessLocations JOIN Clients ON BusinessLocations.ownerID = Clients.clientID;

-- Query to insert a new Business Location
INSERT INTO BusinessLocations (ownerID, streetAddress, cityName, stateName, zipCode) VALUES (clientID, streetAddress, stateName, cityName, zipCode);

-- Query to delete location entry with selected ID
DELETE FROM BusinessLocations WHERE businessID = businessID;

-- Queries to populate loan display table
(SELECT loanID, firstName, lastName, originationAmount, originationDate, interestRate, paymentDue FROM Loans INNER JOIN Clients ON Loans.clientID=Clients.clientID ORDER BY loanID) AS Loans
(SELECT loanID, SUM(amountCollected) AS amountPaid FROM Collections GROUP BY loanID) AS collectionSum
(SELECT Loans.loanID, Loans.originationAmount - collectionSum.amountPaid AS principalRemaining FROM {query_amountCollected} INNER JOIN Loans ON Loans.loanID=collectionSum.loanID) AS amountPaid
SELECT Loans.loanID, interestRate, originationAmount, originationDate, firstName, lastName, paymentDue, principalRemaining FROM {query_Loans} LEFT JOIN {query_amountPaid} ON Loans.loanID=amountPaid.loanID;
-- Query to populate client select dropdown
SELECT clientID, firstName, lastName FROM Clients;

-- Insert query to add a new loan
INSERT INTO Loans (clientID, originationAmount, principalRemaining, originationDate, interestRate, paymentDue) VALUES (clientID, originationAmount, originationAmount, NOW(), interestRate, dueDate);

-- Query to delete the selected loan
DELETE FROM Loans WHERE loanID = loanID;

-- Query to populate locations select dropdown
SELECT * FROM BusinessLocations;

-- Query to populate enforcers select dropdown
SELECT * FROM Enforcers;

-- Query to populate loans select dropdown
SELECT * FROM Loans INNER JOIN Clients ON Clients.clientID=Loans.clientID;

-- Query to populate collections display table
SELECT * FROM Collections INNER JOIN BusinessLocations ON Collections.businessID=BusinessLocations.businessID INNER JOIN Enforcers ON Enforcers.enforcerID=Collections.enforcerID;

-- Insert query for add new collection
INSERT INTO Collections (enforcerID, loanID, businessID, amountCollected, dateOfCollection) VALUES (enforcerID, loanID, businessID, amountCollected, NOW());

-- Query to delete collection entry with selected ID
DELETE FROM Collections WHERE collectionID = collectionID;

-- Query to populate ranks display table
SELECT * FROM Ranks ORDER BY rankID;

-- Insert query to add new rank
INSERT INTO Ranks (rankName) VALUES (rankName);

-- Query to delete rank entry with selected ID
DELETE FROM Ranks WHERE rankID = rankID;