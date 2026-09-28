-- Staging model for customers.
--
-- Staging means: take the raw table and tidy it up just a little, so that
-- every model downstream uses the same clean version. Here we only make
-- sure signup_date is a real DATE (not text). No rows are added or removed.

select
    customer_id,
    first_name,
    last_name,
    email,
    country,
    cast(signup_date as date) as signup_date
from {{ source('raw', 'customers') }}
