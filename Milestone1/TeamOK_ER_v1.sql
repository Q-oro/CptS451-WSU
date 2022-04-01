-------------------------------TEAM OK------------------------------

CREATE TABLE Business(
    businessID CHAR(22) PRIMARY KEY,
    name VARCHAR NOT NULL,
    review_count INTEGER, 
    stars INTEGER,
    is_open INTEGER,
);

CREATE TABLE Address(
    businessID CHAR(22),
    state VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    postal_code VARCHAR NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY (businessID),
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

CREATE TABLE Attributes(
    attributeName VARCHAR,
    attributeValue VARCHAR,
    businessID VARCHAR(22),
    PRIMARY KEY(attributeName, businessID)
    FOREIGN KEY(businessID) REFERENCES Business(businessID)
);

CREATE TABLE Hours(
    day_of_week INTEGER,
    openTime TIME,
    closeTime TIME,
    businessID VARCHAR(22),
    PRIMARY KEY (day_of_week, businessID),
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

CREATE TABLE Categories(
    categoryName VARCHAR,
    businessID VARCHAR(22),
    PRIMARY KEY (categoryName, businessID),
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

--------------------------------------------------------------------

CREATE TABLE User(
    userID VARCHAR(22),
    average_stars FLOAT,
    cool INTEGER,
    fans INTEGER,
    funny INTEGER,
    name VARCHAR,
    tipcount INTEGER,
    useful INTEGER,
    yelping_since VARCHAR NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE Friend(
    userID VARCHAR(22),
    friendID1 VARCHAR(22),
    friendID2 VARCHAR(22),
    PRIMARY KEY (userID,friendID1,friendID2) 
    FOREIGN KEY (userID) REFERENCES User(userID)
    FOREIGN KEY (friendID1) REFERENCES Friend(friendID1)
    FOREIGN KEY (friendID2) REFERENCES Friend(friendID2)
);

--------------------------------------------------------------------

CREATE TABLE Tip(
    businessID CHAR(22),
    userID VARCHAR(22),
    likes INTEGER,
    text VARCHAR NOT NULL,
    date DATE,
    PRIMARY KEY (businessID, userID, date)
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
    FOREIGN KEY (userID) REFERENCES User(userID)
);

--------------------------------------------------------------------

CREATE TABLE Check_in(
    day VARCHAR,
    time VARCHAR,
    year VARCHAR,
    month VARCHAR,
    businessID VARCHAR(22),
    PRIMARY KEY (day, time, year, month, businessID)
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

--------------------------------------------------------------------
