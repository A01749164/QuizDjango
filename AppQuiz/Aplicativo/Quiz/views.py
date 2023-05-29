"""
### Views Configuration ###
29/05/23
Jeovani Hernandez Bastida A01749164
José Miguel Garcia Gurtubay Moreno A01373750
Sebastian Burgos Alanís A01746459
Sandra Ximena Téllez Olvera A01752142
"""
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroFormulario, UsuarioLoginFormulario
from .models import QuizUsuario, Pregunta, PreguntasRespondidas

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
def jugar(request):

	QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)

	if request.method == 'POST':
		pregunta_pk = request.POST.get('pregunta_pk')
		pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
		respuesta_pk = request.POST.get('respuesta_pk')

		try:
			opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
		except ObjectDoesNotExist:
			raise Http404

		QuizUser.validar_intento(pregunta_respondida, opcion_selecionada)

		return redirect('resultado', pregunta_respondida.pk)

	else:
		pregunta = QuizUser.obtener_nuevas_preguntas()
		if pregunta is not None:
			QuizUser.crear_intentos(pregunta)

		context = {
			'pregunta':pregunta
		}

	return render(request, 'play/jugar.html', context)

# In this Function, 
def resultado_pregunta(request, pregunta_respondida_pk):
      respondida=get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

      context={
            'respondida':respondida
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