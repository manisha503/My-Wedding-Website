#!/bin/bash
sqlite3 ../../WeddingWebsite.db <<!
.headers on
select * from users;
!
