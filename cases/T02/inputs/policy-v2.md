# 政策 v2（替代v1）
1. 同一order_id先保留revision最大的记录，较旧记录排除，原因duplicate_older_revision。例外文件中的order_id写被排除记录的原始order_id，不追加revision后缀。
2. 仅统计status为paid的记录，其他记录排除，原因not_paid。
3. amount和refund必须是非负合法数字，否则排除，原因invalid_number。
4. refund超过amount时排除，原因refund_exceeds_amount。
5. 净金额=amount-refund；按region汇总净金额及有效订单条数。金额以十进制计算。检查按条款1到4顺序，每条排除记录只写第一个适用原因代码。
