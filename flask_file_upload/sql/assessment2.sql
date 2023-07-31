WITH hired_per_department AS (
    SELECT
        d.id,
        d.department,
        COUNT(DISTINCT(h.id)) as hired_2021
    FROM hired_employees AS h
        JOIN departments AS d ON h.department_id = d.id
    WHERE STRFTIME('%Y', datetime) = '2021'
    GROUP BY d.department
),

department_avg_2021 AS (
    SELECT 
        ROUND(AVG(hired_2021), 1) as avg_hired_2021
    FROM hired_per_department
)

SELECT
    hd.id,
    hd.department,
    hd.hired_2021
FROM hired_per_department as hd
LEFT JOIN department_avg_2021 as da2021
WHERE hired_2021 > avg_hired_2021
ORDER BY hired_2021 DESC