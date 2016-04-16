from django.contrib.auth.models import User
from choicapp.models import Value, Voter, Item_Voted


User.objects.create_user(username='pins', email='pins@pins.pins',
                         password='pins')
User.objects.create_user(username='kek', email='kek@kek.kek', password='kek')
val1 = Value(description='bienveillance', definition='Be nice')
val1.save()
val2 = Value(description='mechancete', definition='Be bad')
val2.save()
v1 = Voter(user=User.objects.all()[0])
v1.save()
v2 = Voter(user=User.objects.all()[1])
v2.save()

i1 = Item_Voted(voter=v1, item=val1)
i1.save()
i2 = Item_Voted(voter=v2, item=val1)
i2.save()

v1.item_voted_set.get(item=val1)





#################


