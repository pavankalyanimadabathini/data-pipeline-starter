-- Staging model for orders.
--
-- Light tidying only: make sure order_date is a real DATE and quantity
-- is a whole number. Everything else passes through unchanged.

select
    order_id,
    customer_id,
    product_id,
    cast(quantity as integer) as quantity,
    cast(order_date as date) as order_date,
    status
from {{ source('raw', 'orders') }}
