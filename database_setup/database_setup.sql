--- Scripts to set up database modeling

-- state dimension table (d_state)
insert into d_state (state_code, state_name)
values
	('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
	('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
;


-- unit dimension table d_unit
create table d_unit (
    unit_id bigint primary key not null auto_increment, 
    unit_desc varchar(50) 
);

insert into d_unit (unit_desc)
values ('million_kilowatthours');


-- sector dimension table d_sector
create table d_sector (
    sector_id bigint primary key not null auto_increment,
    sector_code varchar(3) not null,
    sector_desc varchar(50) not null
);

insert into d_sector (sector_code, sector_desc)
values ('COM', 'Commercial'), ('IND', 'Industrial'), ('RES', 'Residential'), ('TRA', 'Transportation'),
       ('OTH', 'Other');


-- fact table f_elec_sales
create table f_elec_sales (
    entry_id bigint primary key not null auto_increment,
    state_id bigint,
    sector_id bigint,
    unit_id bigint,
    date date,
    sales decimal(25,5),
    last_updated datetime,
    foreign key (state_id) references d_state (state_id) on delete no action,
    foreign key (sector_id) references d_sector (sector_id) on delete no action,
    foreign key (unit_id) references d_unit (unit_id) on delete no action
);

alter table f_elec_sales
add constraint duplicate_control unique(state_id, sector_id, unit_id, date)
;