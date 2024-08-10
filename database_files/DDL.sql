-- Charles Holz
-- Christopher Bridges
-- CS340 - Group 41
-- We ❤️ Loan Sharking



-- Suggested edits from Step 2 draft page
-- URL: https://canvas.oregonstate.edu/courses/1967354/assignments/9690210?module_item_id=24460832
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;


--
-- Table structure for table `Clients`
--

CREATE OR REPLACE TABLE Clients (
  clientID int(11) NOT NULL AUTO_INCREMENT,
  firstName varchar(30) NOT NULL,
  lastName varchar(30),
  inGoodStanding BOOL DEFAULT 0 NOT NULL,
  CHECK (inGoodStanding >=0 AND inGoodStanding <= 1),
  PRIMARY KEY (clientID)
);

-- --------------------------------------------------------

--
-- Table structure for table `BusinessLocations`
--

CREATE OR REPLACE TABLE BusinessLocations (
  businessID int(11) NOT NULL AUTO_INCREMENT,
  ownerID int(11) NOT NULL,
  streetAddress varchar(100) NOT NULL,
  cityName varchar(40) NOT NULL,
  stateName varchar(20) DEFAULT NULL,
  zipCode char(5) DEFAULT NULL,
  PRIMARY KEY (businessID),
  FOREIGN KEY (ownerID) REFERENCES Clients(clientID) ON DELETE CASCADE
);

-- --------------------------------------------------------


--
-- Table structure for table `Enforcers`
--

CREATE OR REPLACE TABLE Enforcers (
  enforcerID int(11) NOT NULL UNIQUE AUTO_INCREMENT,
  firstName varchar(30) NOT NULL,
  lastName varchar(30),
  startDate date NOT NULL,
  rankID int(11) DEFAULT NULL,
  PRIMARY KEY (enforcerID),
  FOREIGN KEY (rankID) REFERENCES Ranks(rankID) ON DELETE NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `EnforcersHasClients`
--

CREATE OR REPLACE TABLE EnforcersHasClients (
  enforcerHasClientID int(11) NOT NULL AUTO_INCREMENT,
  enforcerID int(11) NOT NULL,
  clientID int(11) NOT NULL,
  PRIMARY KEY (enforcerHasClientID),
  FOREIGN KEY (clientID) REFERENCES Clients(clientID) ON DELETE CASCADE,
  FOREIGN KEY (enforcerID) REFERENCES Enforcers(enforcerID) ON DELETE CASCADE,
  CONSTRAINT unique_enforcer_clientID UNIQUE(enforcerID, clientID)
);

-- --------------------------------------------------------

--
-- Table structure for table `Loans`
--

CREATE OR REPLACE TABLE Loans (
  loanID int(11) NOT NULL AUTO_INCREMENT,
  clientID int(11) NOT NULL,
  originationAmount decimal(19,2) NOT NULL,
  principalRemaining decimal(19,2) NOT NULL,
  originationDate date NOT NULL,
  interestRate decimal(19,2) NOT NULL,
  paymentDue tinyint NOT NULL,
  PRIMARY KEY (loanID),
  FOREIGN KEY (clientID) REFERENCES Clients(clientID) ON DELETE CASCADE
);

-- --------------------------------------------------------

--
-- Table structure for table `Collections`
--

CREATE OR REPLACE TABLE `Collections` (
  collectionID int(11) NOT NULL UNIQUE AUTO_INCREMENT,
  enforcerID int(11) NOT NULL,
  loanID int(11) NOT NULL,
  businessID int(11) NOT NULL,
  amountCollected decimal(19,2) NOT NULL,
  dateOfCollection date NOT NULL,
  PRIMARY KEY (collectionID),
  FOREIGN KEY (enforcerID) REFERENCES Enforcers(enforcerID) ON DELETE CASCADE,
  FOREIGN KEY (loanID) REFERENCES Loans(loanID) ON DELETE CASCADE,
  FOREIGN KEY (businessID) REFERENCES BusinessLocations(businessID) ON DELETE CASCADE
);

-- --------------------------------------------------------

--
-- Table structure for table `Ranks`
--

CREATE OR REPLACE TABLE `Ranks` (
  rankID int(11) NOT NULL UNIQUE AUTO_INCREMENT,
  rankName varchar(40) UNIQUE NOT NULL,
  PRIMARY KEY (rankID)
);

-- --------------------------------------------------------

/*
   Insert data into table

   SELECT Clients.firstName, BusinessLocations.streetAddress, BusinessLocations.zipCode 
   FROM Clients 
   INNER JOIN BusinessLocations ON Clients.clientID = BusinessLocations.ownerID;
*/
INSERT INTO Clients (firstName, lastName, inGoodStanding)
VALUES ('Jon', 'Snow', 1),
('Cersei', 'Lannister', 0),
('Ned', 'Stark', 0);

INSERT INTO BusinessLocations (ownerID, streetAddress, cityName, stateName, zipCode)
VALUES (1, '1234 Main St', 'Chicago', 'Illinois', '60603'),
(1, '5678 Westeros Pl', 'Paris', 'Texas', '75462'),
(2, '23rd W. Broadway', 'New York', 'New York', '10016'),
(3, '327 Beagle St', 'San Diego', 'California', '92038');

/*
SELECT Clients.firstName, Loans.originationAmount 
   FROM Clients 
   INNER JOIN Loans ON Clients.clientID = Loans.clientID;
*/

INSERT INTO Loans (clientID, originationAmount, principalRemaining, originationDate, interestRate, paymentDue)
VALUES (1, 50000, 50000, '2024-07-04', 33, 15),
(1, 50000, 50000, '2024-07-05', 33, 15),
(2, 200000, 150000, '2022-01-01', 45, 1),
(3, 100000, 55000, '2023-12-25', 23, 10);

INSERT INTO Enforcers (firstName, lastName, startDate, rankID)
VALUES ('Sergei', NULL, '1990-01-01', 1),
('Elena', 'Stark', '2015-08-22', 2),
('Georg', 'Rulin', '2007-02-27', NULL);

INSERT INTO Collections (enforcerID, loanID, businessID, amountCollected, dateOfCollection)
VALUES (1, 1, 2, 1000, '2024-07-01'),
(2, 2, 1, 5000, '2024-07-10'),
(3, 3, 3, 1500, '2024-07-07');

INSERT INTO EnforcersHasClients (enforcerID, clientID)
VALUES (1, 3), (2, 1), (3, 3), (2, 3);

INSERT INTO Ranks (rankID, rankName)
VALUES (1, 'Underboss'), (2, 'Captain'), (3, 'Soldier');

-- Suggested edits from Step 2 draft page
-- URL: https://canvas.oregonstate.edu/courses/1967354/assignments/9690210?module_item_id=24460832
SET FOREIGN_KEY_CHECKS=1;
COMMIT;