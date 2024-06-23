USE metaverse

SELECT * FROM metaverse_transactions_dataset

DESCRIBE metaverse_transactions_dataset;

-- Delete duplicates, keeping only the first occurrence
DELETE FROM metaverse_transactions_dataset
WHERE id IN (
    SELECT id FROM (
		SELECT 
			id,
			ROW NUMBER() OVER (PARTITION BY id, timestamp, hour_of_day, sending_address, receiving_address, amount, transaction_type, location_region, ip_prefix, login_frequency, session_duration, purchase_pattern, age_group, risk_score, anomaly
        FROM 
			metaverse_transactions_dataset
		) As subquery
    WHERE row_num > 1
);

DELETE FROM metaverse_transactions_dataset
WHERE sending_address IS NULL;

-- Verify the remaining records
SELECT * FROM metaverse_transactions_dataset;
