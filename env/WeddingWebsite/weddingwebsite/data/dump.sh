#!/bin/bash
sqlite3 ../../WeddingWebsite.db <<!
.headers on
select count(*) as num_families_accepted from (select * from users where accepted=1 group by family_id);
select count(*) as num_families_declined from (select * from users where declined=1 group by family_id);
select sum(num_rsvp_garba) as num_people_garba from (select num_rsvp_garba from users where accepted=1 group by family_id);
select sum(num_rsvp_wedding) as num_people_wedding from (select num_rsvp_wedding from users where accepted=1 group by family_id);
select sum(num_rsvp_reception) as num_people_reception from (select num_rsvp_reception from users where accepted=1 group by family_id);
select * from users;
!
