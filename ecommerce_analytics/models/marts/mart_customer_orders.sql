-- Mart: customer order summary. One row per customer.
--
-- A "mart" is a finished, business-ready table: the kind of thing you would
-- plug straight into a dashboard. This one answers: "Who are our best
-- customers, and how much has each one spent?"
--
-- How it works, step by step:
--   1. Take only completed orders (cancelled or refunded orders are not revenue).
--   2. For each order line, multiply quantity by the product's unit price
--      to get the money that line brought in.
--   3. Group everything by customer and add it up.

with order_lines as (
    select
        o.customer_id,
        o.order_id,
        o.order_date,
        o.quantity * p.unit_price as line_total
    from {{ ref('stg_orders') }} as o
    join {{ ref('stg_products') }} as p
        on o.product_id = p.product_id
    where o.status = 'completed'
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.country,
    count(ol.order_id) as total_orders,
    -- coalesce turns "no orders" (NULL) into a clean 0.
    coalesce(sum(ol.line_total), 0) as total_spent,
    min(ol.order_date) as first_order_date,
    max(ol.order_date) as last_order_date,
    case
        when count(ol.order_id) > 0
        then round(coalesce(sum(ol.line_total), 0) / count(ol.order_id), 2)
        else 0
    end as avg_order_value
from {{ ref('stg_customers') }} as c
-- LEFT JOIN keeps customers who never ordered: they show up with zeros
-- instead of disappearing.
left join order_lines as ol
    on c.customer_id = ol.customer_id
group by
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.country
