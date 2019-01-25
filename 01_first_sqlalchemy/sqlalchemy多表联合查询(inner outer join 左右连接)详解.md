```
#按用户名摸糊查询
trans_details.query.join(Uses).filter(Users.username.like('%xx%'))
#select xxx from trans_details inner join trans_details on users.id=trans_details.user_id where users.username like '%xx%'


#左外联接(left join)
trans_details.query.outerjoin(Uses).filter(Users.username.like('%xx%'))
#select xxx from trans_details left outer join trans_details on users.id=trans_details.user_id where users.username like '%xx%'


#以上是已经设置好外键,它自动找到关联的字段.也可以自己指定:
trans_details.query.join(Uses,trans_details.user_id==Users.id).filter(Users.username.like('%xx%'))
#select xxx from trans_details inner join trans_details on users.id=trans_details.user_id where users.username like '%xx%'


#另外一个更复杂的例子:
q=db.session.query(Credit_bills_details.no,Credit_bills_details.amount,Cards.no).outerjoin(Card_trans_details,
Credit_bills_details.no==Card_trans_details.trans_no).join(Cards,Card_trans_details.to_card_id==Cards.id)\
.filter(Credit_bills_details.credit_bill_id==3)



#SELECT credit_bills_details.no AS credit_bills_details_no, credit_bills_details.amount AS credit_bills_details_amount, cards.no AS cards_no
# FROM credit_bills_details LEFT OUTER JOIN card_trans_details ON credit_bills_details.no = card_trans_details.trans_no INNER JOIN cards
# ON card_trans_details.to_card_id = cards.id  WHERE credit_bills_details.credit_bill_id = %s

```
