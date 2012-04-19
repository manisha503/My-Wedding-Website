#!/bin/bash

sh dump.sh > users.txt
mail -s "User Data" manisha.parekh@gmail.com < users.txt
