# 📝 SQL

*   **CREATE : Crear elementos**

    ```sql
    CREATE DATABASE company;

    # Create an Index on a Table 

    CREATE INDEX idx_department ON employees (department);

    #CREATE: Create a New Table, Database or Index

    CREATE TABLE employees (
      employee_id INT PRIMARY KEY,
      first_name VARCHAR(50),
      last_name VARCHAR(50),
      department VARCHAR(50),
      salary DECIMAL(10, 2)
    );
    ```


*   **USE: usar actual**

    ```sql
    USE company;
    ```


*   **ALTER : modificar elementos**

    ```sql
    ALTER DATABASE database_name

    #ALTER TABLE: Modify An Existing Table's Structure

    ALTER TABLE employees
    ADD COLUMN new_column INT;
    ```


*   **INSERT INTO: añadir elementos**

    ```sql
    INSERT INTO employees (employee_id, first_name, last_name, department, salary)
    VALUES
      (1, 'John', 'Doe', 'HR', 50000.00),
      (2, 'Jane', 'Smith', 'IT', 60000.00),
      (3, 'Alice', 'Johnson', 'Finance', 55000.00),
      (4, 'Bob', 'Williams', 'IT', 62000.00),
      (5, 'Emily', 'Brown', 'HR', 48000.00);
    ```


*   **DROP DATABASE: Delete an Existing Database**

    ```sql
    DROP DATABASE company;

    #Remove an Index 

    DROP INDEX IF EXISTS idx_department;
    ```


*   **SELECT: obtener información**

    ```sql
    SELECT * FROM employees;
    ```


*   **DISTINCT: Seleccionar valores unicos de una columna**

    ```sql
    SELECT DISTINCT department FROM employees;
    ```


*   **WHERE: Filtra filas segun criterios**

    ```sql
    SELECT * FROM employees WHERE salary > 55000.00;
    ```


*   **LIMIT: Limita el numero de filas segun criterio**

    ```sql
    SELECT * FROM employees LIMIT 3;
    ```


*   **UPDATE: Modifica registros de una tabla**

    ```sql
    UPDATE employees
    SET salary = 55000.00
    WHERE employee_id = 1;
    ```


*   **DELETE: Elimina registros de una tabla**

    ```sql
    DELETE FROM employees
    WHERE employee_id = 5;
    ```


*   **WHERE: Filtra filas segun criterios**

    ```sql
    SELECT * FROM employees
    WHERE department = 'IT';
    ```


*   **LIKE: Busca coincidencias**

    ```sql
    SELECT * FROM employees
    WHERE first_name LIKE 'J%';
    ```


*   **IN: Cualquier coincidencia en la lista**

    ```sql
    SELECT * FROM employees
    WHERE department IN ('HR', 'Finance');
    ```


*   **IS NULL: Busca valores NULL**

    ```sql
    SELECT * FROM employees
    WHERE department IS NULL;
    ```


*   **ORDER BY: Ordena los resultados segun criterio**

    ```sql
    SELECT * FROM employees
    ORDER BY salary DESC;
    ```


*   **SUBQUERYS**

    ```sql
    # Single Row

    SELECT first_name, last_name
    FROM employees
    WHERE salary = (SELECT MAX(salary) FROM employees);

    # Multiple Row

    SELECT department_name
    FROM departments
    WHERE department_id IN (SELECT department_id FROM employees);

    ```

####
