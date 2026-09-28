-- Staging model for products.
--
-- Same idea as the other staging models: light tidying only.
-- We cast unit_price to DECIMAL(10, 2) so money math stays exact
-- (no floating point surprises like 19.99 becoming 19.989999).

select
    product_id,
    product_name,
    category,
    cast(unit_price as decimal(10, 2)) as unit_price
from {{ source('raw', 'products') }}
