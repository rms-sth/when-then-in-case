age = 5  # should go to class 2

if age < 12:
    print('class 5')
elif age < 10:
    print('class 4')
elif age < 8:
    print('class 3')
elif age < 6:
    print('class 2')
else:
    print('class 1')

print('=====================================')









age = 5

if age < 6:
    print('class 2')
elif age < 8:
    print('class 3')
elif age < 10:
    print('class 4')
elif age < 12:
    print('class 5')
else:
    print('class 1')

print('=====================================')














age = 5  # should go to class 2

if age < 12:
    print('class 5')
if age < 10:
    print('class 4')
if age < 8:
    print('class 3')
if age < 6:
    print('class 2')
else:
    print('class 1')



'''
F objects:
=>  perform database operations using them without actually having to 
    pull them out of the database into Python memory.
=>  perform operation at the database level rather than on python memory
=>  overrides the standard Python operators to create an encapsulated SQL expression
=>  Python never gets to know about it - it is dealt with entirely by the database.  

'''

# without using F   
blog = Blog.objects.get(name='Tintin')
blog.like += 1
blog.save()




# using F object
from django.db.models import F

blog = Blog.objects.get(name='Tintin')
blog.stories_filed = F('stories_filed') + 1 #  SQL construct 
blog.save()

blog.refresh_from_db()


# another example
Reporter.objects.all().update(stories_filed=F('stories_filed') + 1)




# compare the value of a model field with another field on the same model
Blog.objects.filter(comment__gt=F('like'))