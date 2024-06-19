USE metaverse
SELECT * FROM metaverse_transactions_dataset

-- a base criteria to separate the non-fraudulent and fraudulent transactions
SELECT 
        sending_address,
        AVG(amount) AS avg_amount,
		STDDEV(amount) AS stddev_amount
    FROM 
        metaverse_transactions_dataset
    GROUP BY 
        sending_address;

-- Return all fraudulent transactions with the sending addresses--
WITH classified_transactions AS (
    SELECT 
        sending_address,
        amount,
        transaction_type,
        AVG(amount) OVER() AS avg_amount,
        STDDEV(amount) OVER() AS stddev_amount,
        CASE 
            WHEN amount > AVG(amount) OVER() + 2 * STDDEV(amount) OVER() THEN 'Fraudulent'
            ELSE 'Not Fraudulent'
        END AS transaction_status
    FROM 
        metaverse_transactions_dataset
)

-- Return the top ten fraudulent transactions by amount--
SELECT 
    sending_address,
    amount,
    transaction_type,
    transaction_status
FROM 
    classified_transactions
WHERE
    transaction_status = 'Fraudulent'
ORDER BY 
    amount DESC 
LIMIT 10;


-- Return transactions that are highly risky with their locations
SELECT 
	transaction_type,
    age_group,
    location_region,
    amount,
    anomaly
FROM metaverse_transactions_dataset
WHERE
	anomaly = 'high_risk'
;	
SELECT 
	anomaly,
	COUNT(*) AS transactions,
    SUM(amount) AS transfer_amount
FROM 
	metaverse_transactions_dataset
WHERE 
	transaction_type = 'phish'
GROUP BY
	anomaly
;


-- Identifying addresses that are scamming clients 
SELECT 
	COUNT(*) AS scams,
    SUM(amount) AS Total_scam_amount
FROM  
	metaverse_transactions_dataset
WHERE 
	anomaly = 'high_risk' 
    AND transaction_type = 'scam'
;

-- User Behavior Analysis--
SELECT 
	purchase_pattern, AVG(session_duration) as average_session_duration,
    login_frequency, AVG(amount) as average_amount
FROM 
	metaverse_transactions_dataset
GROUP BY 
	purchase_pattern,
    login_frequency;


-- Geographical Analysis
SELECT 
	location_region, COUNT(*) as transaction_count,
    AVG(amount) as average_amount
FROM 
	metaverse_transactions_dataset
GROUP BY 
	location_region;
    
    -- To be continued--
	-- To be linked with power BI--
    -- To see the output just run the queries or navigate to the power BI visualization--
