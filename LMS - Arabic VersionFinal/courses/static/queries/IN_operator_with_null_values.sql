-- 
-- The IN operator result in a strange behaviour when using it with NULL values
-- NOTE: if we're using the IN operator to check if some value are available in a subquery that contains null values, 
-- therefore all values will checked to be available and evaluate to true unless we exclude null results
-- EXAMPLES:
SELECT 1 WHERE 1 NOT IN (2, 3); -- => Returns 1
SELECT 1 WHERE 1 NOT IN (2, 3, null); -- => Returns nothing
-- Soln): SELECT id ... WHERE id NOT IN (2, 3) AND id is NOT NULL;

