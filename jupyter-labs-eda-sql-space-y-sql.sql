-- Display the names of the unique launch sites in the space mission
select distinct Launch_Site from spaceY;

-- Display 5 records where launch sites begin with the string 'CCA'
select * from spaceY where Launch_Site like 'CCA%' limit 5;

-- Display the total payload mass carried by boosters launched by NASA (CRS)
select sum(payload_mass__kg_) from spaceY where customer = 'NASA (CRS)';

-- Display average payload mass carried by booster version F9 v1.1
select avg(payload_mass__kg_) from spaceY where booster_version like 'F9 v1.1%';
 
-- List the date when the first successful landing outcome in ground pad was acheived.
-- * Hint:Use min function*
select min(Date) from spaceY where landing__outcome = 'Success (ground pad)';

-- List the names of the boosters which have success in drone ship and
-- have payload mass greater than 4000 but less than 6000
select booster_version, payload_mass__kg_, landing__outcome from spaceY where 
landing__outcome = 'Success (drone ship)'
and 
(payload_mass__kg_ between 4000 and 6000) ;

-- List the total number of successful and failure mission outcomes
select count(*) from spaceY where mission_outcome like 'Success%';
select count(*) from spaceY where mission_outcome like 'Failure%';
 
-- List the names of the booster_versions which have carried the maximum payload mass. 
-- Use a subquery
select booster_version, payload_mass__kg_ from spaceY where 
payload_mass__kg_ =
(select max(payload_mass__kg_) from spaceY);


-- List the records which will display the month names, failure landing_outcomes in drone ship,
-- booster versions, launch_site for the months in year 2015.
-- ** Note: SQLLite does not support monthnames. So you need to use substr(Date, 4, 2) 
--          as month to get the months and substr(Date,7,4)='2015' for year.**
select month(Date) as month, landing__outcome, booster_version, launch_site
from spaceY
where year(Date) = '2015'
and
landing__outcome = 'Failure (drone ship)';


-- Rank the count of successful landing_outcomes between
-- the date 04-06-2010 and 20-03-2017 in descending order.
select Date, landing__outcome from
(select * from spaceY where landing__outcome like 'Success%'
and (Date between '2010-04-06' and '2017-03-20'))
order by date desc;


