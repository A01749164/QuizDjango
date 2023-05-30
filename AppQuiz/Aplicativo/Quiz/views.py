"""
### Views Configuration ###
29/05/23
Jeovani Hernandez Bastida A01749164
José Miguel Garcia Gurtubay Moreno A01373750
Sebastian Burgos Alanís A01746459
Sandra Ximena Téllez Olvera A01752142
"""
from django.shortcuts import redirect, render, get_object_or_404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroFormulario, UsuarioLoginFormulario
from .models import QuizUsuario, Pregunta, PreguntasRespondidas, ChooseAnswer
from random import *

# In this Function, 
def inicio(request):
    context = {
        'bienvenido': 'Bienvenido'
    }
    
    return render(request, 'inicio.html', context)

# In this Function, 
def HomeUsuario(request):
    return render(request, 'Usuario/home.html')


# In this Function, 
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pregunta, QuizUsuario, PreguntasRespondidas, ChooseAnswer

# def jugar(request):
#     cantidad_preguntas = request.GET.get('cantidad_preguntas')
#     quiz_user, created = QuizUsuario.objects.get_or_create(usuario=request.user)

#     if cantidad_preguntas is not None:
#         cantidad_preguntas = int(cantidad_preguntas)
#         preguntas_respondidas = PreguntasRespondidas.objects.filter(quizUser=quiz_user)
#         preguntas_disponibles = Pregunta.objects.exclude(preguntasrespondidas__quizUser=quiz_user).exclude(pk__in=preguntas_respondidas.values('pregunta__pk'))
#         preguntas = random.sample(list(preguntas_disponibles), cantidad_preguntas)

#         if request.method == 'POST':
#             pregunta_actual = preguntas_respondidas.count()

#             if pregunta_actual < cantidad_preguntas:
#                 pregunta_respondida = preguntas_respondidas[pregunta_actual]
#                 respuesta_pk = request.POST.get(f'respuesta_{pregunta_respondida.pregunta.pk}')
#                 respuesta_seleccionada = get_object_or_404(ChooseAnswer, pk=respuesta_pk)
#                 quiz_user.validar_intento(pregunta_respondida, respuesta_seleccionada)

#             pregunta_actual += 1

#             if pregunta_actual < cantidad_preguntas:
#                 pregunta_siguiente = preguntas[pregunta_actual]
#                 context = {
#                     'pregunta': pregunta_siguiente,
#                     'pregunta_actual': pregunta_actual,
#                 }
#             else:
#                 pregunta_siguiente = None
#                 context = {
#                     'pregunta': None,
#                     'pregunta_siguiente': None,
#                 }

#             return render(request, 'play/jugar.html', context)

#     else:
#         preguntas = None

#     context = {
#         'preguntas': preguntas,
#         'cantidad_preguntas': cantidad_preguntas,
#     }
#     return render(request, 'play/jugar.html', context)

def seleccionarPreguntas(request):
    if request.method == 'POST':
        cantidad_preguntas = int(request.POST.get('cantidad_preguntas'))    
        return redirect('jugar', cantidad_preguntas=cantidad_preguntas)

    return render(request, 'play/seleccionar_preguntas.html')

# En la función jugar(request, cantidad_preguntas), después de obtener la siguiente pregunta
# y antes de redirigir a los resultados, verifica si se ha alcanzado el número máximo de preguntas respondidas
# In this Function, 
def jugar(request, cantidad_preguntas):
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        if cantidad_preguntas>0:
            pregunta_pk = request.POST.get('pregunta_pk')
            pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
            respuesta_pk = request.POST.get('respuesta_pk')

            try:
                opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
            except ObjectDoesNotExist:
                raise Http404

            QuizUser.validar_intento(pregunta_respondida, opcion_seleccionada)

            # Obtener la siguiente pregunta o redirigir al resultado si no hay más preguntas
            siguiente_pregunta = QuizUser.obtener_nuevas_preguntas(cantidad_preguntas)
            if siguiente_pregunta is not None:
                QuizUser.crear_intentos(siguiente_pregunta)
                return HttpResponseRedirect(f'/resultado/{pregunta_respondida.pk}?cantidad_preguntas={cantidad_preguntas}')
                return redirect('resultado', pregunta_respondida.pk)
            else:
                # return HttpResponseRedirect(f'/resultado/{pregunta_respondida.pk}?cantidad_preguntas={cantidad_preguntas}')
                return redirect('tablero')#pregunta_respondida.pk

    else:
        pregunta = QuizUser.obtener_nuevas_preguntas(cantidad_preguntas)
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)

        context = {
            'pregunta': pregunta
        }

        return render(request, 'play/jugar.html', context)


# In this Function, 
def resultado_pregunta(request, pregunta_respondida_pk):
      cantidad_preguntas = str(int(request.GET.get('cantidad_preguntas'))-1)
      respondida=get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

      context={
            'respondida':respondida,
            'cantidad_preguntas':cantidad_preguntas
      }
      return render(request, 'play/resultados.html', context)

# In this Function, 
def tablero(request):
	total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
	contador = total_usaurios_quiz.count()

	context = {
		'usuario_quiz':total_usaurios_quiz,
		'contar_user':contador
	}
	return render(request, 'play/tablero.html', context)

# In this Function, 
def loginView(request):
    titulo = 'login'
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username = username, password = password)
        login(request, usuario)
        return redirect('HomeUsuario')
    
    context = {
        'form' : form,
        'titulo' : titulo
    }
    return render(request, 'Usuario/login.html', context)

# In this Function, 
def registro(request):
    
    titulo = 'Crea una Cuenta'
    if request.method == 'POST':
        form  = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroFormulario()
        
    context = {
        'form':form,
        'titulo': titulo
    }
    
    return render(request, 'Usuario/registro.html', context)

def logout_vista(request):
    logout(request)
    return redirect('/')