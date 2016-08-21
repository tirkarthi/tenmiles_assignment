# tenmiles_assignment
A timesheet management application

# GET /api/clients/

Get details of the client

```
{
    "id": 9,
    "user" : 9
    "name": "q",
    "company_info" : "qq"
    "email" : "q@q.com"
}
```

# POST /api/projects/

Create a new project

* client - Client ID
* start_date - Start date of the project
* cost_per_hour - Cost per hour for the project

Format : Example : http POST :9000/api/projects/ start_date=<start_date> client=<client_id> cost_per_hour=<cost_per_hour>
Example : http POST :9000/api/projects/ start_date=2015-01-01 client=3 cost_per_hour=12
Output :

```
{
    "id": 9,
    "client": 3,
    "start_date": "2015-01-01"
    "cost_per_hour": "12"
}
```

# GET /api/projects/

Get a list of all projects for the client

```
[{
    "id": 9,
    "client": 3,
    "start_date": "2015-01-01"
    "cost_per_hour": "12"
},
{
    "id": 10,
    "client": 3,
    "start_date": "2016-01-01"
    "cost_per_hour": "17"
}]
```

# GET /api/project/{id}

Get details of a project

* id - Project ID
* client - Client ID
* cost_per_hour - Cost per hour in hours
* start_date - Start date of the project

Example : http :9000/api/projects/4

Output :

```
{
    "id": 4,
    "client": 3,
    "start_date": "2016-01-01"
    "cost_per_hour": "17"
}
```

# POST /api/timesheets/

Create a new timesheet entry

* project - Project ID
* time_spent - Time spent in hours
* date - Date of the timesheet entry

Format : http POST <host>/api/timesheets/ date=<date> project=<project_id> time_spent=<time>
Example : http POST :9000/api/timesheets/ date=2016-01-01 project=3 time_spent=12
Output :

```
{
    "id": 9,
    "project_id": 3,
    "date": "2016-01-01"
    "time_spent": "12"
}
```

# GET /api/timesheets/

Get a list of timesheets for all projects

```
[{
    "date" : "2016-01-01"
    "time_spent" : 2
    "project" : 3
}
{
    "date" : "2016-01-01"
    "time_spent" : 2
    "project" : 4
}]
```

# GET /api/timesheets/{id}

Get details of a timesheet

* project - Project ID
* time_spent - Time spent in hours
* date - Date of the timesheet entry

Example : http :9000/api/timesheets/4

Output :

```
{
    "date" : "2016-01-01"
    "time_spent" : 2
    "project" : 3
} 
```
