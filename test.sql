CREATE TABLE test(
	id int(10) auto_increment not null,
	name varchar(20),
	lastname varchar(40),
	sex varchar(20),
	age int(3),
	asignature varchar(40),
	email varchar(30),
	password varchar(20),
	birthdate date(),
	primary key(id)
)ENGINE = INNODB;