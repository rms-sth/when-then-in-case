'''
Conditional Expressions
 => let you use if … elif … else logic within filters, annotations, aggregations, and updates.
 => Using a When() object is similar to using the filter() method.
 		* condition can be specified using field lookups or Q objects
 		* result is provided using the then keyword.
'''


# A Case() expression is like the if … elif … else statement in Python

from django.db.models import Q, When, Case, CharField, Value, Count
from datetime import date, timedelta
from when_then_app.models import Client







# give discount according to account_type status
Client.objects.annotate(
	discount=Case(
		When(account_type=Client.REGULAR, then=Value('3%')),
		When(account_type=Client.GOLD, then=Value('5%')),
		When(account_type=Client.PLATINUM, then=Value('10%')),
		output_field=CharField()
	)
).values_list('name', 'discount', 'account_type')

# >>> vars(z)
# >>> str(z.query)
# 'SELECT "when_then_app_client"."name", "when_then_app_client".
# "account_type", CASE WHEN "when_then_app_client"."account_type
# " = R THEN 3% WHEN "when_then_app_client"."account_type" = G T
# HEN 5% WHEN "when_then_app_client"."account_type" = P THEN 10%
#  ELSE NULL END AS "discount" FROM "when_then_app_client"'











# get the discount based on how long the Client has been with us
a_month_ago = date.today() - timedelta(days=30)
a_year_ago = date.today() - timedelta(days=365)
five_year_ago = date.today() - timedelta(days=365 * 5)

y = Client.objects.annotate(
	discount=Case(
		When(registered_on__lte=five_year_ago, then=Value('10%')),
		When(registered_on__lte=a_year_ago, then=Value('5%')),
		default=Value('1%'),
		output_field=CharField(),
	)
).values_list('name', 'discount', 'registered_on')


# >>> str(y.query)
# 'SELECT "when_then_app_client"."name", "when_then_app_client".
# "registered_on", CASE WHEN "when_then_app_client"."registered_
# on" <= 2014-10-22 THEN 10% WHEN "when_then_app_client"."regist
# ered_on" <= 2018-10-21 THEN 5% ELSE 1% END AS "discount" FROM
# "when_then_app_client"'



# wrong ✖
Client.objects.annotate(
	discount=Case(
		When(registered_on__gte=five_year_ago, then=Value('10%')),
		When(registered_on__gte=a_year_ago, then=Value('5%')),
		default=Value('1%'),
		output_field=CharField(),
	)
).values_list('name', 'discount', 'registered_on')

# wrong ✖
Client.objects.annotate(
	discount=Case(
		When(registered_on__gte=a_month_ago, then=Value('1%')),
		When(registered_on__gte=a_year_ago, then=Value('5%')),
		default=Value('10%'),
		output_field=CharField(),
	)
).values_list('name', 'discount', 'registered_on')


# little different than above => None if registered < month ago
Client.objects.annotate(
	discount=Case(
		When(registered_on__lte=five_year_ago, then=Value('10%')),
		When(registered_on__lte=a_year_ago, then=Value('5%')),
		When(registered_on__lte=a_month_ago, then=Value('1%')),
		output_field=CharField()
	)
).values_list('name', 'discount')











# find gold clients that registered more than a month ago
# and platinum clients that registered more than a year ago
Client.objects.filter(
	registered_on__lte=Case(
		When(account_type=Client.GOLD, then=a_month_ago),
		When(account_type=Client.PLATINUM, then=a_year_ago),
	)
).values_list('name', 'account_type', 'registered_on')

# >>> str(i.query)
# 'SELECT "when_then_app_client"."name", "when_then_app_client"."ac
# count_type", "when_then_app_client"."registered_on" FROM "when_th
# en_app_client" WHERE "when_then_app_client"."registered_on" <= (C
# ASE WHEN "when_then_app_client"."account_type" = G THEN 2019-09-2
# 1 WHEN "when_then_app_client"."account_type" = P THEN 2018-10-21
# ELSE NULL END)'







# find out how many clients there are for each account_type ?
Client.objects.aggregate(
	regular=Count('pk', filter=Q(account_type=Client.REGULAR)),
	gold=Count('pk', filter=Q(account_type=Client.GOLD)),
	platinum=Count('pk', filter=Q(account_type=Client.PLATINUM)),
)

# SQL 2003 Equivalent
# SELECT count('id') FILTER (WHERE account_type=1) as regular,
#        count('id') FILTER (WHERE account_type=2) as gold,
#        count('id') FILTER (WHERE account_type=3) as platinum
# FROM clients;



# equivalent to above ✔
Client.objects.aggregate(
	regular=Count('pk', Q(account_type=Client.REGULAR)),
	gold=Count('pk', Q(account_type=Client.GOLD)),
	platinum=Count('pk', Q(account_type=Client.PLATINUM)),
)




# total wrong ✖
Client.objects.aggregate(
	regular=Count('pk', account_type=Client.REGULAR),
	gold=Count('pk', account_type=Client.GOLD),
	platinum=Count('pk', account_type=Client.PLATINUM),
)










# change the account_type for our clients to match their registration dates
# has a little problem. Where ?? 🤔
Client.objects.update(
	account_type=Case(
		When(registered_on__lte=five_year_ago, then=Value(Client.PLATINUM)),
		When(registered_on__lte=a_year_ago, then=Value(Client.GOLD)),
		default=Value(Client.REGULAR)
	)
)

Client.objects.values_list('name', 'account_type', 'registered_on')

# doesn't work => because we need to give default value 😒 ✖
Client.objects.update(
	account_type=Case(
		When(registered_on__lte=five_year_ago, then=Value(Client.PLATINUM)),
		When(registered_on__lte=a_year_ago, then=Value(Client.GOLD)),
		When(registered_on__lte=a_month_ago, then=Value(Client.REGULAR)),
	)
)












# fixed that little problem here 😊
Client.objects.update(
	account_type=Case(
		When(registered_on__lte=five_year_ago, then=Value(Client.PLATINUM)),
		When(registered_on__lte=a_year_ago, then=Value(Client.GOLD)),
		default='account_type'
	)
)
