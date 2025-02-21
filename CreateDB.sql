CREATE TABLE Auth
(
  id       INT  NOT NULL UNIQUE,
  FOREIGN KEY (email) REFERENCES User (email),
  password TEXT NOT NULL,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE Products
(
  id          INT  NOT NULL UNIQUE,
  supplier_id INT  NOT NULL,
  name        TEXT NULL    ,
  description TEXT NULL    ,
  price       INT  NULL    ,
  moq         INT  NULL    ,
  PRIMARY KEY (id AUTOINCREMENT),
  FOREIGN KEY (supplier_id) REFERENCES Supplier (id)
);

CREATE TABLE Review
(
  id          INT      NOT NULL UNIQUE,
  writer_id   INT      NOT NULL,
  product_id  INT      NOT NULL,
  supplier_id INT      NOT NULL,
  rating      INT      NULL    ,
  label       TEXT     NULL    ,
  content     TEXT     NULL    ,
  date        DATETIME NULL    ,
  PRIMARY KEY (id AUTOINCREMENT),
  FOREIGN KEY (writer_id) REFERENCES User (id),
  FOREIGN KEY (product_id) REFERENCES Products (id),
  FOREIGN KEY (supplier_id) REFERENCES Supplier (id)
);

CREATE TABLE Supplier
(
  id              INT      NOT NULL UNIQUE,
  name            TEXT     NOT NULL UNIQUE,
  address         TEXT     NOT NULL,
  email           TEXT     NOT NULL UNIQUE,
  phone           TEXT     NULL    ,
  date_registered DATETIME NULL    ,
  description     TEXT     NULL    ,
  PRIMARY KEY (id AUTOINCREMENT)
);

CREATE TABLE User
(
  id              INT      NOT NULL UNIQUE,
  name            TEXT     NOT NULL UNIQUE,
  address         TEXT     NOT NULL,
  email           TEXT     NOT NULL UNIQUE,
  phone           TEXT     NULL    ,
  date_registered DATETIME NOT NULL,
  industry        TEXT     NOT NULL,
  is_staff        BOOLEAN  NOT NULL,
  description     TEXT     NULL    ,
  PRIMARY KEY (id AUTOINCREMENT)
);