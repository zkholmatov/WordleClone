from django.contrib import admin
from .models import Answer, Guess, User

# Register your models here.
admin.site.register(User)
admin.site.register(Answer)
admin.site.register(Guess)
