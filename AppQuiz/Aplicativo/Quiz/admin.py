from django.contrib import admin
from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas, QuizUsuario
from .forms import ElegirInlineFormSet

#Sebastian Burgos
class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAXIMO_RESPUESTA
    min_num = ElegirRespuesta.MAXIMO_RESPUESTA
    formset = ElegirInlineFormSet
    
class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline, )
    list_display = ['texto',]
    search_fields = ['texto', 'pregunta__texto']

# Jeovani Hernandez    
class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']
    
    class Meta:
        model = PreguntasRespondidas
          
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(PreguntasRespondidas)
admin.site.register(QuizUsuario)