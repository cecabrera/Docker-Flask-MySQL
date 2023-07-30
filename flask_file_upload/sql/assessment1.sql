SELECT
    h.id,
    d.department,
    datetime,
    j.job
FROM hired_employees AS h
    JOIN departments AS d ON h.department_id = d.id 
    LEFT JOIN jobs AS j ON h.job_id = j.id 
