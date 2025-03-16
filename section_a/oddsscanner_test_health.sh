#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

# Output file
OUTPUT_FILE="query_results.sql"

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
    echo -e "\n=== $1 ===\n" >> $OUTPUT_FILE
}

# Function to execute MySQL query and check result
execute_query() {
    local query="$1"
    local description="$2"
    
    echo -e "${YELLOW}${description}${NC}"
    echo -e "-- ${description}\n${query};\n" >> $OUTPUT_FILE
    result=$(docker exec -i mysql_db mysql -uuser -puserpassword sql_test -e "$query" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Query executed successfully${NC}"
        echo "$result"
        echo "$result" >> $OUTPUT_FILE
    else
        echo -e "${RED}Query failed${NC}"
        echo "-- Query failed" >> $OUTPUT_FILE
    fi
    echo -e "----------------------------------------"
    echo -e "\n----------------------------------------\n" >> $OUTPUT_FILE
}

# Wait for MySQL to be ready
print_header "Waiting for MySQL to be ready"
for i in {1..30}; do
    if docker exec mysql_db mysqladmin -uuser -puserpassword ping &>/dev/null; then
        echo -e "${GREEN}MySQL is ready!${NC}"
        break
    fi
    echo -n "."
    sleep 1
    if [ $i -eq 30 ]; then
        echo -e "\n${RED}Timeout waiting for MySQL to start${NC}"
        exit 1
    fi
done

# Execute the specific queries
print_header "Query Results"

# 1. Write a query to display the name (first_name and last_name) and department ID of all employees in departments 30 or 100 in ascending order.
execute_query \
    "SELECT CONCAT(first_name, ' ', last_name) as full_name, department_id 
     FROM employees 
     WHERE department_id IN (30, 100)
     ORDER BY first_name, last_name;" \
    "1. Write a query to display the name (first_name and last_name) and department ID of all employees in departments 30 or 100 in ascending order."

# 2. Write a query to find the manager ID and the salary of the lowest-paid employee for that manager.
execute_query \
    "SELECT 
        manager_id,
        MIN(salary) as lowest_salary
     FROM employees
     WHERE manager_id IS NOT NULL
     GROUP BY manager_id
     ORDER BY manager_id;" \
    "2. Write a query to find the manager ID and the salary of the lowest-paid employee for that manager."

# 3. Write a query to find the name (first_name and last_name) and the salary of the employees who earn more than the employee whose last name is Bell.
execute_query \
    "WITH bell_salary AS (
        SELECT salary 
        FROM employees 
        WHERE last_name = 'Bell'
        LIMIT 1
     )
     SELECT 
        first_name,
        last_name,
        salary
     FROM employees
     WHERE salary > (SELECT salary FROM bell_salary)
     ORDER BY salary DESC;" \
    "3. Write a query to find the name (first_name and last_name) and the salary of the employees who earn more than the employee whose last name is Bell."

# 4. Write a query to find the name (first_name and last_name), job, department ID and name of all employees that work in London.
execute_query \
    "SELECT 
        e.first_name,
        e.last_name,
        e.job_id,
        e.department_id,
        d.department_name
     FROM employees e
     JOIN departments d ON e.department_id = d.department_id
     JOIN locations l ON d.location_id = l.location_id
     WHERE l.city = 'London'
     ORDER BY e.first_name, e.last_name;" \
    "4. Write a query to find the name (first_name and last_name), job, department ID and name of all employees that work in London."

# 5. Write a query to get the department name and number of employees in the department.
execute_query \
    "SELECT 
        d.department_name,
        COUNT(e.employee_id) as employee_count
     FROM departments d
     LEFT JOIN employees e ON d.department_id = e.department_id
     GROUP BY d.department_name
     ORDER BY employee_count DESC;" \
    "5. Write a query to get the department name and number of employees in the department."

# Final message
echo -e "\n${GREEN}All queries executed. Results saved to ${OUTPUT_FILE}.${NC}" 