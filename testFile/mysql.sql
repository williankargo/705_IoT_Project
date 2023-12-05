CREATE TABLE emp(empid INTEGER NOT NULL PRIMARY KEY, empname TEXT NOT NULL, email NOT NULL);

INSERT INTO emp(empid, empname, email) VALUES (2, "TOM", "test2@test.com");

INSERT INTO emp(empid, empname, email) VALUES (3, "PETER", "test3@test.com");

SELECT * FROM emp;