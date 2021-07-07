CREATE DATABASE IF NOT EXISTS issee_you;

CREATE TABLE iss_data ( 
    time TIME default NULL,
    latitude VARCHAR(255) default NULL,
    longitude VARCHAR(255) default NULL,
    distance float default NULL,
    PRIMARY KEY (time)
);

INSERT INTO iss_data (time, latitude, longitude, distance)
VALUES ('00:00:00', "27.9242", "50.2854", DEFAULT);