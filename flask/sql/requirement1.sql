SELECT
    d.department,
    j.job,
    (CAST(STRFTIME('%m', datetime) AS INT) - 1) / 3 + 1 AS Quarter,
    COUNT(DISTINCT(h.id)) as N

FROM hired_employees AS h
    JOIN departments AS d ON h.department_id = d.id 
    LEFT JOIN jobs AS j ON h.job_id = j.id 

WHERE STRFTIME('%Y', datetime) = '2021'

GROUP BY 
    d.department,
    j.job,
    (CAST(STRFTIME('%m', datetime) AS INT) - 1) / 3 + 1