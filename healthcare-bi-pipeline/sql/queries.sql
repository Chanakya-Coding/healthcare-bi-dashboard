-- ============================================
-- Healthcare BI Pipeline - Analytical Queries
-- ============================================

-- Query 0: Exploratory Query
SELECT *
FROM encounters
LIMIT 50;

-- Query 1: Readmission rate by age group
SELECT
    age,
    COUNT(*) AS total_encounters,
    SUM(CASE WHEN readmitted != 'NO' THEN 1 ELSE 0 END) AS readmitted_count,
    ROUND(
        100.0 * SUM(CASE WHEN readmitted != 'NO' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS readmission_rate_pct
FROM encounters
GROUP BY age
ORDER BY age;


-- Query 2: Average length of stay by primary diagnosis (top 20 most common)
SELECT
    diag_1,
    COUNT(*) AS encounter_count,
    ROUND(AVG(time_in_hospital), 2) AS avg_length_of_stay
FROM encounters
GROUP BY diag_1
ORDER BY encounter_count DESC
LIMIT 20;


-- Query 3: Admissions by admission type
SELECT
    admission_type_id,
    COUNT(*) AS total_admissions,
    ROUND(AVG(time_in_hospital), 2) AS avg_stay,
    ROUND(AVG(num_medications), 2) AS avg_medications
FROM encounters
GROUP BY admission_type_id
ORDER BY total_admissions DESC;


-- Query 4: Patient-level readmission (accounts for repeat encounters)
SELECT
    patient_nbr,
    COUNT(*) AS total_encounters,
    MAX(CASE WHEN readmitted != 'NO' THEN 1 ELSE 0 END) AS was_ever_readmitted
FROM encounters
GROUP BY patient_nbr
HAVING COUNT(*) > 1
ORDER BY total_encounters DESC
LIMIT 20;


-- Query 5: Diabetes medication change impact on readmission
SELECT
    change,
    "diabetesMed",
    COUNT(*) AS total_encounters,
    ROUND(
        100.0 * SUM(CASE WHEN readmitted != 'NO' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS readmission_rate_pct
FROM encounters
GROUP BY change, "diabetesMed"
ORDER BY readmission_rate_pct DESC;