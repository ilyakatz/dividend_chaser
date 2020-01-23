from dividend_chaser.orm import orm     

symbol = "SS"
d = orm.Dividendable.first_or_create(symbol=symbol)
d.save()

div = orm.Dividend.first_or_new()    
div.dividendable_id = d.id
div.save()
