# Client-Server
Basic Client-Server model using python, that takes commands and will proceed to process and modify a .csv file.

This project is based off a school assigment, where it is acting as a DBMS with a multi-client's connecting to one server on the localhost, and allowing the server to handle all of the requests.

This project requires:
* pandas
* csv
* random
* socket
* threading

Client | Server
------ | ------
Insert | _string_ {insert, FirstName, LastName, DoB}
Find | _int_ {find, MemberID}
Update | _string_ {update, MemberID, newFirstName, newLastName, newDoB}
Delete | _int_ {delete, MemberID}
PrintAll | _returns_ {All data in the csv}
Print | _int n_ : _int m_ {returns n -> m of the csv}


## ToDo List:
- [ ] add random name generator, based on the names.txt
- [ ] fix insert
- [ ] add update, and delete options
- [ ] Create a CLI 'GUI'
- [ ] fix closing
- [ ] add server shutdown command to the Client.py
- [ ] add regex for inputs
- [ ] add a print_all inputs
- [ ] add a print_range
