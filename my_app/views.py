import json
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Aluno, Professor, Administrador, Leciona

class Listar(View):
  def verificaValidadoPor(self, aluno):
     if aluno.atestado_apt_validado_por:
        return aluno.atestado_apt_validado_por.user_cpf.nome
     else:
        return None

  def get(self, request, *args, **kwargs):
      try:
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

        return render(request, 'listar.html', {'alunos': alunos_data, 'professores': professores_data, 'admins': admins_data, 'turmas': turmas_data})

      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  

  def put(self, request, *args, **kwargs):
     try:
      admin_cpf = 1234 # Agostinho
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

      return JsonResponse({'mensagem': 'Aluno atualizado com sucesso!'})
     
     except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
