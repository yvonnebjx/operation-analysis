# Field Mapping Memory

This file stores reusable field-to-business-meaning mappings for cross-border ecommerce operating analysis.

Update this file after the user confirms ambiguous fields. Keep old mappings if they are still useful, but mark project-specific ones clearly.

## How to use

Before analysis:

1. inspect workbook headers
2. compare them with this file
3. map known fields automatically
4. list unknown or risky fields for user confirmation
5. update this file after confirmation

## Core business subjects

These are the preferred semantic targets:

- channel
- channel_detail
- date
- region
- brand
- model
- spu
- product_line
- category_level
- category_name
- qty
- gmv
- discount
- vat
- refund
- revenue
- purchase
- headship
- overseas_warehouse
- ads
- commission
- delivery_fee
- storage_fee
- other_platform_fee
- abnormal_fee
- gross_profit

## Default mappings from current demo workbook

### Budget-side

- `渠道` -> `channel`
- `地区` -> `region`
- `产品型号` -> `model`
- `大品类` -> `product_line`
- `新三级类目` -> `category_name`
- `类目等级` -> `category_level`
- `月份` -> `date`
- `预算销售数量` -> `qty`
- `预算GMV` -> `gmv`
- `预算折扣金额` -> `discount`
- `预算VAT` -> `vat`
- `预算退款金额` -> `refund`
- `预算营业收入` -> `revenue`
- `预算采购金额` -> `purchase`
- `预算头程成本 + 预算二程配送费 + 预算关税` -> `headship`
- `预算海外仓费用` -> `overseas_warehouse`
- `预算广告费用` -> `ads`
- `预算平台佣金` -> `commission`
- `预算FBA配送费 + 预算FBM配送费` -> `delivery_fee`
- `预算平台仓储费` -> `storage_fee`
- `预算平台其他费用 + 预算异常费用` -> `other_platform_fee`
- `预算运营毛利` -> `gross_profit`

### Actual-side

- `渠道` -> `channel`
- `渠道明细` -> `channel_detail`
- `日期` -> `date`
- `地区` -> `region`
- `MODEL` -> `model`
- `SPU` -> `spu`
- `产品线` -> `product_line`
- `三级分类` -> `category_name`
- `类目等级` -> `category_level`
- `销售数量` -> `qty`
- `GMV` -> `gmv`
- `折扣金额合计` -> `discount`
- `VAT费用合计` -> `vat`
- `退货额合计` -> `refund`
- `销售收入` -> `revenue`
- `采购成本合计` -> `purchase`
- `运费成本合计` -> `headship`
- `海外仓费用` -> `overseas_warehouse`
- `广告费用合计` -> `ads`
- `订单佣金` -> `commission`
- `订单FBA费用` -> `delivery_fee`
- `平台仓储费合计` -> `storage_fee`
- `其他费用合计` -> `other_platform_fee`
- `销售毛利` -> `gross_profit`

## Known limitations

- Some workbooks may not separate `delivery_fee` into FBA and FBM on the actual side.
- Some workbooks may not separate `headship` from second-leg or customs on the actual side.
- Some workbooks may include offline or manual adjustment channels that do not map cleanly to standard ecommerce structures.

## Uncertain field log

Use this section for fields that need confirmation.

- none yet
