"""
### DataBase Configuration with Admin ###
29/05/23
Jeovani Hernandez Bastida A01749164
José Miguel Garcia Gurtubay Moreno A01373750
Sebastian Burgos Alanís A01746459
Sandra Ximena Téllez Olvera A01752142
"""

from django.contrib import admin
from .models import Pregunta, ChooseAnswer, PreguntasRespondidas, QuizUsuario
from .forms import ChooseInlineFormSet

# In this class, the admin can choose answers and create them.
class ChooseAnswersInline(admin.TabularInline):
    model = ChooseAnswer
    can_delete = False
    max_num = ChooseAnswer.MAXIMO_RESPUESTA
    min_num = ChooseAnswer.MAXIMO_RESPUESTA
    formset = ChooseInlineFormSet

#In this class,  
class AdminQuestion(admin.ModelAdmin):
    model = Pregunta
    inlines = (ChooseAnswersInline, )
    list_display = ['texto',]
    search_fields = ['texto', 'pregunta__texto']

# In this class
class AdminQuestionsAnswered(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']
    
    class Meta:
        model = PreguntasRespondidas
          
admin.site.register(Pregunta, AdminQuestion)
admin.site.register(ChooseAnswer)
admin.site.register(PreguntasRespondidas)
admin.site.register (QuizUsuario)