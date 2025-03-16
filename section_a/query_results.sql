
=== Waiting for MySQL to be ready ===


=== Query Results ===

-- 1. Write a query to display the name (first_name and last_name) and department ID of all employees in departments 30 or 100 in ascending order.
SELECT CONCAT(first_name, ' ', last_name) as full_name, department_id 
     FROM employees 
     WHERE department_id IN (30, 100)
     ORDER BY first_name, last_name;;

full_name	department_id
Alexander Khoo	30
Daniel Faviet	100
Den Raphaely	30
Guy Himuro	30
Ismael Sciarra	100
John Chen	100
Jose Manuel Urman	100
Karen Colmenares	30
Luis Popp	100
Nancy Greenberg	100
Shelli Baida	30
Sigal Tobias	30

----------------------------------------

-- 2. Write a query to find the manager ID and the salary of the lowest-paid employee for that manager.
SELECT 
        manager_id,
        MIN(salary) as lowest_salary
     FROM employees
     WHERE manager_id IS NOT NULL
     GROUP BY manager_id
     ORDER BY manager_id;;

manager_id	lowest_salary
0	24000.00
100	5800.00
101	4400.00
102	9000.00
103	4200.00
108	6900.00
114	2500.00
120	2200.00
121	2100.00
122	2200.00
123	2500.00
124	2500.00
145	7000.00
146	7000.00
147	6200.00
148	6100.00
149	6200.00
201	6000.00
205	8300.00

----------------------------------------

-- 3. Write a query to find the name (first_name and last_name) and the salary of the employees who earn more than the employee whose last name is Bell.
WITH bell_salary AS (
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
     ORDER BY salary DESC;;

first_name	last_name	salary
Steven	King	24000.00
Neena	Kochhar	17000.00
Lex	De Haan	17000.00
John	Russell	14000.00
Karen	Partners	13500.00
Michael	Hartstein	13000.00
Alberto	Errazuriz	12000.00
Nancy	Greenberg	12000.00
Shelley	Higgins	12000.00
Lisa	Ozer	11500.00
Ellen	Abel	11000.00
Den	Raphaely	11000.00
Gerald	Cambrault	11000.00
Clara	Vishney	10500.00
Eleni	Zlotkey	10500.00
Harrison	Bloom	10000.00
Janette	King	10000.00
Peter	Tucker	10000.00
Hermann	Baer	10000.00
Tayler	Fox	9600.00
Danielle	Greene	9500.00
David	Bernstein	9500.00
Patrick	Sully	9500.00
Alexander	Hunold	9000.00
Peter	Hall	9000.00
Daniel	Faviet	9000.00
Allan	McEwen	9000.00
Alyssa	Hutton	8800.00
Jonathon	Taylor	8600.00
Jack	Livingston	8400.00
William	Gietz	8300.00
John	Chen	8200.00
Adam	Fripp	8200.00
Matthew	Weiss	8000.00
Lindsey	Smith	8000.00
Christopher	Olsen	8000.00
Payam	Kaufling	7900.00
Jose Manuel	Urman	7800.00
Ismael	Sciarra	7700.00
Nanette	Cambrault	7500.00
Louise	Doran	7500.00
William	Smith	7400.00
Elizabeth	Bates	7300.00
Mattea	Marvins	7200.00
Oliver	Tuvault	7000.00
Kimberely	Grant	7000.00
Sarath	Sewall	7000.00
Luis	Popp	6900.00
David	Lee	6800.00
Susan	Mavris	6500.00
Shanta	Vollman	6500.00
Sundar	Ande	6400.00
Charles	Johnson	6200.00
Amit	Banda	6200.00
Sundita	Kumar	6100.00
Pat	Fay	6000.00
Bruce	Ernst	6000.00
Kevin	Mourgos	5800.00
Valli	Pataballa	4800.00
David	Austin	4800.00
Jennifer	Whalen	4400.00
Diana	Lorentz	4200.00
Nandita	Sarchand	4200.00
Alexis	Bull	4100.00

----------------------------------------

-- 4. Write a query to find the name (first_name and last_name), job, department ID and name of all employees that work in London.
SELECT 
        e.first_name,
        e.last_name,
        e.job_id,
        e.department_id,
        d.department_name
     FROM employees e
     JOIN departments d ON e.department_id = d.department_id
     JOIN locations l ON d.location_id = l.location_id
     WHERE l.city = 'London'
     ORDER BY e.first_name, e.last_name;;

first_name	last_name	job_id	department_id	department_name
Susan	Mavris	HR_REP	40	Human Resources

----------------------------------------

-- 5. Write a query to get the department name and number of employees in the department.
SELECT 
        d.department_name,
        COUNT(e.employee_id) as employee_count
     FROM departments d
     LEFT JOIN employees e ON d.department_id = e.department_id
     GROUP BY d.department_name
     ORDER BY employee_count DESC;;

department_name	employee_count
Shipping	45
Sales	34
Purchasing	6
Finance	6
IT	5
Executive	3
Marketing	2
Accounting	2
Public Relations	1
Human Resources	1
Administration	1
Payroll	0
Recruiting	0
Retail Sales	0
Government Sales	0
IT Helpdesk	0
NOC	0
IT Support	0
Operations	0
Contracting	0
Construction	0
Manufacturing	0
Benefits	0
Shareholder Services	0
Control And Credit	0
Corporate Tax	0
Treasury	0

----------------------------------------

