<p align="center">An AirBnB clone.</p>

---

## Description

This project is called "AirBnB clone". It is a complete web application in progress, which will ultimately integrate database storage, 
a back-end API, and front-end interfacing.

Currently, the project only implements the back-end console.

## Classes:

AirBnB clone contains the following classes:

|     | BaseModel | FileStorage                         | User | State | City | Amenity | Place | Review |
| --- | --------- |-------------------------------------| -----| ----- | -----| ------- | ----- | ------ |
| **PUBLIC INSTANCE ATTRIBUTES** | `id`<br>`created_at`<br>`updated_at` |                                     | Inherits from `BaseModel` | Inherits from `BaseModel` | Inherits from `BaseModel` | Inherits from `BaseModel` | Inherits from `BaseModel` | Inherits from `BaseModel` |
| **PUBLIC INSTANCE METHODS** | `save`<br>`to_dict` | `all`<br>`new`<br>`save`<br>`reload` | "" | "" | "" | "" | "" | "" |
| **PUBLIC CLASS ATTRIBUTES** | |                                     | `email`<br>`password`<br>`first_name`<br>`last_name`| `name` | `state_id`<br>`name` | `name` | `city_id`<br>`user_id`<br>`name`<br>`description`<br>`number_rooms`<br>`number_bathrooms`<br>`max_guest`<br>`price_by_night`<br>`latitude`<br>`longitude`<br>`amenity_ids` | `place_id`<br>`user_id`<br>`text` | 
| **PRIVATE CLASS ATTRIBUTES** | | `file_path`<br>`objects`            | | | | | | |

## Storage:

The classes above are managed by a storage system abstracted within the `FileStorage` class.

Upon initialization of the backend, the AirBnB clone creates a `FileStorage` instance named `storage`.
This `storage` instance retrieves its data from class instances preserved in the `file.json` JSON file.
Any creation, modification, or deletion of class instances is tracked and reflected in the `file.json`
by the `storage` instance.

## Console:

The console serves as a command line interpreter that simplifies
the handling of the AirBnB clone's backend operations.
It's designed to oversee all the classes that the application employs.

### Using the Console

The console for the AirBnB clone operates in two modes: interactive and non-interactive.
For non-interactive mode, direct any command(s) through a pipeline to run the `console.py` 
file from the command line.

```
$ echo "help" | ./console.py
(hbnb) 
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb) 
$
```

To use the AirBnB clone console in interactive mode, run the 
file `console.py` by itself:

```
$ ./console.py
```

The console displays a prompt for input when running in interactive mode:

``` 
$ ./console.py
(hbnb) 
```

Enter the command `quit` to quit the console or enter the EOF signal 
(`ctrl-D`).

```
$ ./console.py
(hbnb) quit
$
```

```
$ ./console.py
(hbnb) EOF
$
```

### Console Commands

The AirBnB clone console supports the following commands:

* **create**
  * Usage: `create <class>`

Creates a new instance of a given class. The class' ID is printed and 
the instance is saved to the file `file.json`.

```
$ ./console.py
(hbnb) create BaseModel
ff1c276d-8448-4037-bef7-4c5b59d80829
(hbnb) quit
$ cat file.json ; echo ""
{"BaseModel.ff1c276d-8448-4037-bef7-4c5b59d80829": {"updated_at": "2024-05-20T20:30:00.000000", "created_at": 
"2024-05-20T20:30:00.000000", "__class__": "BaseModel", "id": 
"ff1c276d-8448-4037-bef7-4c5b59d80829"}}
```

* **show**
  * Usage: `show <class> <id>` or `<class>.show(<id>)`

Prints the string representation of a class instance based on a given id.

```
$ ./console.py
(hbnb) create User
e4f5b6c7-d8e9-0fab-cdef-123456abcdef
(hbnb)
(hbnb) show User e4f5b6c7-d8e9-0fab-cdef-123456abcdef
[User] (e4f5b6c7-d8e9-0fab-cdef-123456abcdef) {'id': 'e4f5b6c7-d8e9-0fab-cdef-123456abcdef', 
'created_at': datetime.datetime(2024, 5, 20, 20, 45, 30, 123456), 
'updated_at': datetime.datetime(2024, 5, 20, 20, 45, 30, 123456)}
(hbnb) 
(hbnb) User.show(e4f5b6c7-d8e9-0fab-cdef-123456abcdef)
[User] (e4f5b6c7-d8e9-0fab-cdef-123456abcdef) {'id': 'e4f5b6c7-d8e9-0fab-cdef-123456abcdef', 
'created_at': datetime.datetime(2024, 5, 20, 20, 45, 30, 123456), 
'updated_at': datetime.datetime(2024, 5, 20, 20, 45, 30, 123456)}
(hbnb) 
```
* **destroy**
  * Usage: `destroy <class> <id>` or `<class>.destroy(<id>)`

Deletes a class instance based on a given id. The storage file `file.json` 
is updated accordingly.

```
$ ./console.py
(hbnb) create State
abc12345-6789-def0-1234-56789abcdef0
(hbnb) create Place
fedcba98-7654-3210-fedc-ba9876543210
(hbnb)
(hbnb) destroy State abc12345-6789-def0-1234-56789abcdef0
(hbnb) Place.destroy(fedcba98-7654-3210-fedc-ba9876543210)
(hbnb) quit
$ cat file.json ; echo ""
{}
```

* **all**
  * Usage: `all` or `all <class>` or `<class>.all()`

Prints the string representations of all instances of a given class. If no 
class name is provided, the command prints all instances of every class.

```
$ ./console.py
(hbnb) create BaseModel
12345678-abcd-efab-cdef-abcdef123456
(hbnb) create BaseModel
87654321-dcba-feba-fedc-ba9876543210
(hbnb) create User
abcdef12-3456-7890-abcd-ef1234567890
(hbnb) create User
fedcba98-7654-3210-fedc-ba9876543210
(hbnb)
(hbnb) all BaseModel
["[BaseModel] (87654321-dcba-feba-fedc-ba9876543210) {'updated_at': datetime.datetime(2024, 5, 20, 20, 50, 30, 123456), 
'created_at': datetime.datetime(2024, 5, 20, 20, 50, 30, 123456), 'id': '87654321-dcba-feba-fedc-ba9876543210'}", 
"[BaseModel] (12345678-abcd-efab-cdef-abcdef123456) {'updated_at': datetime.datetime(2024, 5, 20, 20, 48, 25, 654321), 
'created_at': datetime.datetime(2024, 5, 20, 20, 48, 25, 654321), 'id': '12345678-abcd-efab-cdef-abcdef123456'}"]
(hbnb)
(hbnb) User.all()
["[User] (fedcba98-7654-3210-fedc-ba9876543210) {'updated_at': datetime.datetime(2024, 5, 20, 20, 52, 15, 987654), 
'created_at': datetime.datetime(2024, 5, 20, 20, 52, 15, 987654), 'id': 'fedcba98-7654-3210-fedc-ba9876543210'}", 
"[User] (abcdef12-3456-7890-abcd-ef1234567890) {'updated_at': datetime.datetime(2024, 5, 20, 20, 51, 45, 210987), 
'created_at': datetime.datetime(2024, 5, 20, 20, 51, 45, 210987), 'id': 'abcdef12-3456-7890-abcd-ef1234567890'}"]
(hbnb) 
(hbnb) all
["[User] (fedcba98-7654-3210-fedc-ba9876543210) {'updated_at': datetime.datetime(2024, 5, 20, 20, 52, 15, 987654), 
'created_at': datetime.datetime(2024, 5, 20, 20, 52, 15, 987654), 'id': 'fedcba98-7654-3210-fedc-ba9876543210'}", 
"[BaseModel] (87654321-dcba-feba-fedc-ba9876543210) {'updated_at': datetime.datetime(2024, 5, 20, 20, 50, 30, 123456), 
'created_at': datetime.datetime(2024, 5, 20, 20, 50, 30, 123456), 'id': '87654321-dcba-feba-fedc-ba9876543210'}", 
"[User] (abcdef12-3456-7890-abcd-ef1234567890) {'updated_at': datetime.datetime(2024, 5, 20, 20, 51, 45, 210987), 
'created_at': datetime.datetime(2024, 5, 20, 20, 51, 45, 210987), 'id': 'abcdef12-3456-7890-abcd-ef1234567890'}", 
"[BaseModel] (12345678-abcd-efab-cdef-abcdef123456) {'updated_at': datetime.datetime(2024, 5, 20, 20, 48, 25, 654321), 
'created_at': datetime.datetime(2024, 5, 20, 20, 48, 25, 654321), 'id': '12345678-abcd-efab-cdef-abcdef123456'}"]
(hbnb)
```

* **count**
  * Usage: `count <class>` or `<class>.count()`

Retrieves the number of instances of a given class.

```
$ ./console.py
(hbnb) create Place
98a7b6c5-d4e3-2f1a-g8h9-i0j1k2l3m4n5
(hbnb) create Place
o5p4n3m2-l1k0-j9h8-g1f2-e3d4-c5b6-a7a8
(hbnb) create City
z9y8-x7w6-v5u4-t3s2-r1q2-p0o9-n8m7
(hbnb) 
(hbnb) count Place
2
(hbnb) city.count()
1
(hbnb) 
```

* **update**
  * Usage: `update <class> <id> <attribute name> "<attribute value>"` or
`<class>.update(<id>, <attribute name>, <attribute value>)` or `<class>.update(
<id>, <attribute dictionary>)`.

Modifies an instance of a class using a specified ID along with a key/value pair 
or a set of attribute pairs within a dictionary. When invoking `update` 
with just one key/value pair, it's possible to alter only the "basic" attributes, 
excluding `id`, `created_at`, and `updated_at`. On the other hand, supplying a 
dictionary allows for the modification of any attribute.
```
$ ./console.py
(hbnb) create User
a1b2c3d4-e5f6-7890-abcd-ef1234567890
(hbnb)
(hbnb) update User a1b2c3d4-e5f6-7890-abcd-ef1234567890 first_name "Betty"
(hbnb) update User a1b2c3d4-e5f6-7890-abcd-ef1234567890 last_name "Bar"
(hbnb) update User a1b2c3d4-e5f6-7890-abcd-ef1234567890 email "aibnb@mail.com"
(hbnb) show User a1b2c3d4-e5f6-7890-abcd-ef1234567890
[User] (a1b2c3d4-e5f6-7890-abcd-ef1234567890) {'created_at': datetime.datetime(
2024, 5, 20, 20, 54, 39, 234382), 'email': 'airbnb@mail.com', 'first_name': 'Betty', 
'last_name': 'Bar', 'updated_at': datetime.datetime(2024, 5, 20, 20, 54, 39, 234382), 
'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'}
(hbnb)
(hbnb) User.update(a1b2c3d4-e5f6-7890-abcd-ef1234567890, address, "98 Mission St")
(hbnb) User.show(a1b2c3d4-e5f6-7890-abcd-ef1234567890)
[User] (a1b2c3d4-e5f6-7890-abcd-ef1234567890) {'created_at': datetime.datetime(
2024, 5, 20, 20, 54, 39, 234382), 'address': '98 Mission St', 'email': 'airbnb@mail.com', 
'first_name': 'Betty', 'last_name': 'Bar', 'updated_at': datetime.datetime(2024, 5, 20, 20, 54, 39, 234382), 
'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'}
(hbnb)
(hbnb) User.update(a1b2c3d4-e5f6-7890-abcd-ef1234567890, password, "root")
(hbnb) User.show(a1b2c3d4-e5f6-7890-abcd-ef1234567890)
[User] (a1b2c3d4-e5f6-7890-abcd-ef1234567890) {'created_at': datetime.datetime(
2024, 5, 20, 20, 54, 39, 234382), 'address': '98 Mission St', 'email': 'airbnb@mail.com', 
'first_name': 'Betty', 'last_name': 'Bar', 'password': 'root', 
'updated_at': datetime.datetime(2024, 5, 20, 20, 54, 39, 234382), 'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'}
(hbnb) 
```

## Testing:

The test cases for the AirBnB clone project are located in the tests directory. 
If you wish to execute all the tests at once, you can do so by running the command below:
```
$ python3 unittest -m discover tests
```

Or if you prefer, you can specify a single test file to run at a time:

```
$ python3 unittest -m tests/test_console.py
```

## Author:
* **Ikundwila Mwambona** <[ikumwana@gmail.com](ikumwana@gmail.com)>
