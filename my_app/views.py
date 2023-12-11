import re
import json
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Aluno, Professor, Administrador, Leciona, Usuario
from .forms import FormCPF

class Admin(View):
  def verificaValidadoPor(self, aluno):
     if aluno.atestado_apt_validado_por:
        return aluno.atestado_apt_validado_por.user_cpf.nome
     else:
        return None

  def get(self, request, *args, **kwargs):
      try:
        form = FormCPF()
        
        alunos = Aluno.objects.select_related('user_cpf').all()
        professores = Professor.objects.select_related('user_cpf').all()
        admins = Administrador.objects.select_related('user_cpf').all()
        leciona = Leciona.objects.select_related('turma_id').all()

        alunos_data = [{'nome': aluno.user_cpf.nome, 
                        'email': aluno.user_cpf.email, 
                        'cpf': aluno.user_cpf.cpf,
                        'atestado': aluno.atestado_apt,
                        'turma': aluno.turma_id.id,
                        'validado_por': self.verificaValidadoPor(aluno),
                        'nascimento': aluno.user_cpf.nascimento.strftime('%d/%m/%Y')
                      } for aluno in alunos]
        professores_data = [{'nome': prof.user_cpf.nome, 
                             'email': prof.user_cpf.email, 
                             'cpf': prof.user_cpf.cpf
                            } for prof in professores]
        admins_data = [{'nome': admin.user_cpf.nome, 
                        'email': admin.user_cpf.email, 
                        'cpf': admin.user_cpf.cpf
                      } for admin in admins]
        turmas_data = [{'id': lec.turma_id.id,
                        'modalidade': lec.turma_id.modalidade,
                        'professor': lec.prof_cpf.user_cpf.nome,
                        'horario': lec.turma_id.horario,
                        'semestre': lec.turma_id.semestre,
                        'vagas': lec.turma_id.vagas,
                        'is_open': lec.turma_id.is_open
                      } for lec in leciona]

        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #   return JsonResponse({'alunos': alunos_data, 'professores': professores_data, 'admins': admins_data, 'turmas': turmas_data})

        # if 'listar_profs' in request.GET:
        #   professores = Professor.objects.all()
        # if 'listar_alunos' in request.GET:
        #   alunos = Aluno.objects.all()

        return render(request, 'admin.html', {'alunos': alunos_data, 
                                              'professores': professores_data, 
                                              'admins': admins_data, 
                                              'turmas': turmas_data,
                                              'formulario': form
                                            })

      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  

  def put(self, request, *args, **kwargs):
     try:
      admin_cpf = 123 # Agostinho
      aluno_cpf = json.loads(request.body).get('aluno_cpf')

      if not aluno_cpf:
          return JsonResponse({'erro': 'aluno_cpf não fornecido no corpo da requisição'}, status=400)
      
      aluno = get_object_or_404(Aluno, user_cpf=aluno_cpf)
      admin = get_object_or_404(Administrador, user_cpf=admin_cpf)

      if aluno and admin:
        aluno.atestado_apt_validado_por = admin
        aluno.save()
      else:
          return JsonResponse({'erro': 'Não foi possível encontrar o aluno ou o administrador fornecido'}, status=400)         

      return JsonResponse({'mensagem': 'Atestado de aptidão física validado.'}, status=200)
     
     except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
     

  def post(self,request, *args, **kwargs):
      try:
        form = FormCPF(request.POST)
        if form.is_valid():
          admin_que_cadastrou_cpf = 1234 # Eduardo Falcão
          cpfNovoAdm = form.cleaned_data['cpf']
          print(f'cpfNovoAdm {cpfNovoAdm}')
          cpfNovoAdmCleaned = re.sub(r'\D', '', cpfNovoAdm) # Garante que tem apenas números
          print(f'cpfNovoAdmCleaned {cpfNovoAdmCleaned}')

          usuario = get_object_or_404(Usuario, cpf=cpfNovoAdmCleaned)
          admin_que_cadastrou = get_object_or_404(Administrador, user_cpf=admin_que_cadastrou_cpf)

          if usuario or admin_que_cadastrou:
            novo_administrador = Administrador(
              user_cpf=usuario,
              cadastrado_por=admin_que_cadastrou
            )
            novo_administrador.save()

          return redirect('adm_inicial')
      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
