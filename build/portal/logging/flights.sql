CREATE TABLE adsb_flights( 
  id INT(11) AUTO_INCREMENT PRIMARY KEY, 
  flight VARCHAR(100) NOT NULL, 
  lastSeen VARCHAR(100) NULL);
