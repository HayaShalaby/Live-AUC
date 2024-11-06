create schema liveatauc;

use liveatauc;

create table users(
email varchar(50) not null primary key, 
userName varchar(50) not null, 
Fname varchar(50),
Lname varchar(50), 
major varchar(15) not null,
friends int, 
pfp varchar(100), 
userPassword varchar(100), 
phone int, 
points int
);

create table Interest(
userEmail varchar(50) not null,
interest varchar(50) not null, 
foreign key (userEmail) references users(email),
primary key (userEmail, interest) 
);

create table appEvents(
event_id int not null primary key, 
eventName varchar(50), 
Audience varchar(15), 
Price decimal(5, 2), 
eventDesc varchar(500), 
Organizer_email varchar(50), 
eventStatus varchar(15),
DatenTime datetime
);

create table Event_categories(
event_id int not null, 
tag varchar(50) not null, 
foreign key (event_id) references appEvents(event_id),
primary key (event_id, tag) 
);

create table Event_images(
event_id int not null, 
image varchar(500) not null, 
foreign key (event_id) references appEvents(event_id),
primary key (event_id, image) 
);

create table Event_attendees(
event_id int not null, 
userEmail varchar(50) not null, 
foreign key (event_id) references appEvents(event_id),
foreign key (userEmail) references users(email),
primary key (event_id, userEmail) 
);