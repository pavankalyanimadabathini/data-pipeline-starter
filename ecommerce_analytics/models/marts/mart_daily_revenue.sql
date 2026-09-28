-- Mart: daily revenue. One row per day.
--
-- This is the table a founder would open every morning. It answers:
-- "How much money did we make each day, and is it going up or down?"
--
-- Same recipe as the customer mart: keep completed orders only, turn each
-- order line into money (quantity * unit_price), then group by day.

with order_lines as (
    select
        o.order_date,
        o.quantity * p.unit_price as line_total
    from {{ ref('stg_orders') }} as o
    join {{ ref('stg_products') }} as p
        on o.product_id = p.product_id
    where o.status = 'completed'
)

select
    order_date,
    count(*) as orders_count,
    round(sum(line_total), 2) as revenue,
    round(sum(line_total) / count(*), 2) as avg_order_value
from order_lines
group by order_date
order by order_date
