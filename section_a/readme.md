# MySQL Docker Setup

This project sets up a MySQL database using Docker, initialized with a predefined schema and data.

## Prerequisites

- Docker
- Docker Compose

## Configuration

The database is configured with the following credentials:

- Database name: `sql_test`
- Root password: `rootpassword`
- User: `user`
- Password: `userpassword`
- Port: `3306`

## Getting Started

1. Make sure Docker is running on your system
2. Open a terminal in this directory
3. Run the following command to start the database:
   ```bash
   docker-compose up -d
   ```

The database will be initialized with the schema and data from `sql_db.sql`.

Inside this folder run oddsscanner_test_health.sh script to execute the queries that the test requires. After executing queris this script will print the results to the console and generate a file called query_results.sql with the results.


```bash
./oddsscanner_test_health.sh
```

## Connecting to the Database

You can connect to the database using any MySQL client with these credentials:

- Host: `localhost`
- Port: `3306`
- Database: `sql_test`
- Username: `user`
- Password: `userpassword`

## Stopping the Database

To stop the database, run:
```bash
docker-compose down
```

## Data Persistence

The database data is persisted in the `./mysql-data` directory. This ensures your data remains intact even after stopping and restarting the container.

Section A - MySQL
1. Write a query to display the name (first_name and last_name) and department ID of all employees in departments 30 or 100 in ascending order.
2. Write a query to find the manager ID and the salary of the lowest-paid employee for that manager.
3. Write a query to find the name (first_name and last_name) and the salary of the employees who earn more than the employee whose last name is Bell.
4. Write a query to find the name (first_name and last_name), job, department ID and name of all employees that work in London.
5. Write a query to get the department name and number of employees in the department. Link to database:
https://drive.google.com/file/d/11s8I2Yyw3qz0BjuT6_wayHHM_uesuEqI/view?usp=sharing