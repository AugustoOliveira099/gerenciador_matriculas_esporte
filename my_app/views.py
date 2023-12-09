from django.views import View
from django.shortcuts import render
from .models import Aluno, Professor

class Listar(View):
  def get(self, request, *args, **kwargs):
      
      alunos = []
      professores = []

      if 'listar_profs' in request.GET:
        professores = Professor.objects.all()
      if 'listar_alunos' in request.GET:
        alunos = Aluno.objects.all()

      return render(request, 'listar.html', {'alunos': alunos, 'professores': professores})
