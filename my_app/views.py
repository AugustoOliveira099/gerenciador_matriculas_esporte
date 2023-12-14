import re
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Aluno, Professor, Administrador, Leciona, Usuario
from .forms import FormCPF, FormAptFisica, UsuarioCadastroForm


class Admin(View):
  template_name = 'adm_inicial'
  template_file = 'admin.html'

  def verificaValidadoEm(self, aluno):
      if aluno.atestado_apt_validado_em:
          return aluno.atestado_apt_validado_em.strftime('%d/%m/%Y')
      else:
          return None
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
                        'turma': aluno.turma_id.id if aluno.turma_id else None,
                        'validado_por': self.verificaValidadoPor(aluno),
                        'validado_em': self.verificaValidadoEm(aluno),
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

        return render(request, self.template_file, {'alunos': alunos_data, 
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
        aluno.atestado_apt_validado_em = timezone.now()
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
          # Garante que tem apenas números
          cpfNovoAdmCleaned = re.sub(r'\D', '', cpfNovoAdm) 

          usuario = get_object_or_404(Usuario, cpf=cpfNovoAdmCleaned)
          admin_que_cadastrou = get_object_or_404(Administrador, 
                                                  user_cpf=admin_que_cadastrou_cpf)

          if usuario or admin_que_cadastrou:
            novo_administrador = Administrador(
              user_cpf=usuario,
              cadastrado_por=admin_que_cadastrou
            )
            novo_administrador.save()

          return redirect(self.template_name)
      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class UsuarioCadastroView(View):
    template_name = 'cadastro_user'
    template_file = 'cadastro_user.html'

    def get(self, request, *args, **kwargs):
        form = UsuarioCadastroForm()
        return render(request, self.template_file, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UsuarioCadastroForm(request.POST)

        if form.is_valid():
            novo_usuario = form.save(commit=False)
            novo_usuario.status_aprovacao = False
            novo_usuario.save()

            # return redirect('adm_inicial')
            return JsonResponse({'cadastro_sucesso': True})
        else:
            return render(request, self.template_file, {'form': form})

class AlunoView(View):
    template_file = 'aluno.html'
    template_name = 'aluno_inicial'
    # TODO: remover isso
    user_email = 'jaugustox21@gmail.com'

    def verificaValidadeAtestado(self, aluno):
     if aluno.atestado_apt_validado_em:
        data_atual = timezone.now()
        diferença = data_atual - aluno.atestado_apt_validado_em

        # Faz menos de 1 ano desde que o atestado foi cadastrado
        if diferença < timedelta(days=366):
          return aluno.atestado_apt_validado_em.strftime('%d/%m/%Y')
        else:
           # Agora o aluno precisa atualizar o seu atestado, pois está defasado
           aluno.atestado_apt_validado_em = None
           aluno.atestado_apt = None
           aluno.save()
           return None
     else:
        return None

    def get(self, request, *args, **kwargs):
      form = FormAptFisica()
      aluno = Aluno.objects.filter(user_cpf__email=self.user_email).first()

      print(f"aluno: {aluno}")
      if aluno:
          aluno = {'nome': aluno.user_cpf.nome, 
                   'atestado_apt': self.verificaValidadeAtestado(aluno)}
      print(f"aluno 2: {aluno}")
      
      return render(request, self.template_file, {'form': form, 'aluno': aluno})

    def post(self, request, *args, **kwargs):
        try:
            form = FormAptFisica(request.POST)
            aluno = Aluno.objects.filter(user_cpf__email=self.user_email).first()

            if form.is_valid():
                usuario = get_object_or_404(Usuario, email=self.user_email)
                atestado_apt = form.cleaned_data['atestado']
                print(f"aluno: {aluno}")
                if aluno:
                    aluno.atestado_apt = atestado_apt
                else:
                    aluno = Aluno(
                        user_cpf = usuario,
                        atestado_apt = atestado_apt
                    )
                aluno.save()

                return redirect(self.template_name) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
