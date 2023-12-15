import re
import json
from django.db.models import Q, F
from datetime import timedelta
from django.utils import timezone
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Aluno, Professor, Administrador, Leciona, Usuario, Matricula, Noticia, Turma
from .forms import FormCPF, FormAptFisica, UsuarioCadastroForm, FormCadastraTurma, FormCadastraNoticia


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
            raise Exception('aluno_cpf não fornecido no corpo da requisição.')
        
        aluno = Aluno.objects.filter(user_cpf__cpf=aluno_cpf).first()
        admin = Administrador.objects.filter(user_cpf__cpf=admin_cpf).first()

        if aluno and admin:
          aluno.atestado_apt_validado_por = admin
          aluno.atestado_apt_validado_em = timezone.now()
          aluno.atestado_apt_esperando_validacao = False
          aluno.save()
        else:
            raise Exception('Não foi possível encontrar o aluno ou o administrador fornecido')         

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

          if usuario and admin_que_cadastrou:
            novo_administrador = Administrador(
              user_cpf=usuario,
              cadastrado_por=admin_que_cadastrou
            )
            novo_administrador.save()
          else:
             raise Exception('O usuário informado não existe ou você não foi encontrado no nosso banco de dados.')

          return redirect(self.template_name)
      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class AlunoView(View):
    template_file = 'aluno.html'
    template_name = 'aluno_inicial'
    # TODO: remover isso se houver página de login
    user_email = 'testeeee@gmail.com'

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
      try:
        turmas = []
        noticias = []
        turmas_aluno = []
        noticias_da_turma_ativa = []
        form = FormAptFisica()

        aluno = Aluno.objects.filter(user_cpf__email=self.user_email).first()
        # Captura as tuplas de Leciona que não tem uma data_termino e que a 
        # turma está aberta
        leciona_abertar = Leciona.objects.filter(Q(turma_id__is_open=True) & Q(data_termino__isnull=True))

        # Matrículas
        matricula_ativa = Matricula.objects.filter(Q(aluno_cpf=aluno) & Q(turma_id__is_open=True)).first()
        if matricula_ativa:
          noticias_da_turma_ativa = Noticia.objects.filter(turma_id=matricula_ativa.turma_id).order_by('-data_publicacao')

        # Turmas
        matriculas = Matricula.objects.filter(aluno_cpf=aluno)


        if len(noticias_da_turma_ativa) > 0:
           noticias = [{'id': noticia.id,
                        'turma_id': noticia.turma_id.id,
                        'professor': noticia.prof_cpf.user_cpf.nome,
                        'modalidade': noticia.turma_id.modalidade,
                        'horario': noticia.turma_id.horario,
                        'conteudo': noticia.conteudo,
                        'data_publicacao': noticia.data_publicacao.strftime('%H:%M:%S do dia %d/%m/%Y')
                      } for noticia in noticias_da_turma_ativa]
        
        if matriculas:
          turmas_aluno = [{
                          'id': matricula.turma_id.id,
                          'modalidade': matricula.turma_id.modalidade,
                          'professor': matricula.prof_cpf.user_cpf.nome,
                          'horario': matricula.turma_id.horario,
                          'vagas': matricula.turma_id.vagas,
                          'is_open': matricula.turma_id.is_open,
                          'semestre': matricula.turma_id.semestre
                        } for matricula in matriculas]

        if leciona_abertar:
          turmas = [{
                        'id': lec.turma_id.id,
                        'modalidade': lec.turma_id.modalidade,
                        'professor': lec.prof_cpf.user_cpf.nome,
                        'horario': lec.turma_id.horario,
                        'vagas': lec.turma_id.vagas,
                        'lec_id': lec.id
                      } for lec in leciona_abertar]

        if aluno:
            aluno = {'nome': aluno.user_cpf.nome,
                    'atestado_apt_validado_em': self.verificaValidadeAtestado(aluno),
                    'atestado_apt_esperando_validacao': aluno.atestado_apt_esperando_validacao,
                    'atestado_apt': aluno.atestado_apt if aluno.atestado_apt else None}
        
        return render(request, self.template_file, {'form': form, 
                                                    'aluno': aluno, 
                                                    'turmas': turmas,
                                                    'turmas_aluno': turmas_aluno,
                                                    'noticias': noticias})
      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        try:
            atestado_apt = json.loads(request.body).get('atestado')
            
            if not atestado_apt:
              raise Exception('Você não está registrado no nosso banco de dados.')

            usuario = Usuario.objects.filter(email=self.user_email).first()
            if not usuario:
              raise Exception('Você não está registrado no nosso banco de dados.')
            
            aluno = Aluno.objects.filter(user_cpf__email=self.user_email).first()

            if aluno:
                aluno.atestado_apt = atestado_apt
                aluno.atestado_apt_esperando_validacao = True
            else:
                aluno = Aluno(
                    user_cpf = usuario,
                    atestado_apt = atestado_apt,
                    atestado_apt_esperando_validacao = True
                )
            aluno.save()

            return redirect(self.template_name)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            lec_id = json.loads(request.body).get('lec_id')
            if not lec_id:
                raise Exception('lec_id não fornecido no corpo da requisição.')
            
            aluno = Aluno.objects.filter(user_cpf__email=self.user_email).first()

            is_matriculado = Matricula.objects.filter(aluno_cpf=aluno).exists()
            if is_matriculado:
               raise Exception('Você já está matriculado em uma turma. É possível praticar apenas um esporte na instituição.')
            
            leciona = Leciona.objects.filter(id=lec_id).first()

            if aluno and leciona:
              turma = leciona.turma_id
              if turma.vagas <= 0:
                raise Exception('Não há mais vagas na turma.')
              turma.vagas = turma.vagas - 1
              turma.save()

              nova_matricula = Matricula(
                 aluno_cpf=aluno,
                 turma_id=leciona.turma_id,
                 prof_cpf=leciona.prof_cpf
              )
              nova_matricula.save()
            else:
              raise Exception('Você não foi encontrado no nosso banco de dados ou a relação entre professor e turma informada não existe.')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class UsuarioCadastroView(View):
    template_target = 'pagina_inicial'
    template_name = 'cadastro_user'
    template_file = 'cadastro_user.html'

    def get(self, request, *args, **kwargs):
        form = UsuarioCadastroForm()
        return render(request, self.template_file, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UsuarioCadastroForm(request.POST)

        if form.is_valid():
            print('ENTROU\n')
            novo_usuario = form.save(commit=False)
            novo_usuario.status_aprovacao = False
            novo_usuario.save()

            return redirect(self.template_target)
        else:
            print('NAO ENTROU\n')
            return redirect(self.template_name)

class ProfessorView(View):
   template_name = 'professor_inicial'
   template_file = 'professor.html'
   prof_cpf_logado = 1234 # Eduardo Falcão
   
   def get(self, request, *args, **kwargs):
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
          try:
              noticias_data = []
              turma_id = request.GET.get('turma_id', None)
              leciona_ativos = Leciona.objects.filter(
                Q(prof_cpf__user_cpf__cpf=self.prof_cpf_logado) & 
                Q(turma_id__id=turma_id) &
                Q(turma_id__is_open=True)
              ).first()

              if leciona_ativos:
                noticias = Noticia.objects.filter(
                    Q(turma_id=leciona_ativos.turma_id) & 
                    Q(prof_cpf=leciona_ativos.prof_cpf)
                  ).order_by('-data_publicacao')

                noticias_data = [{'id': noticia.id,
                            'turma_id': noticia.turma_id.id,
                            'professor': noticia.prof_cpf.user_cpf.nome,
                            'modalidade': noticia.turma_id.modalidade,
                            'horario': noticia.turma_id.horario,
                            'conteudo': noticia.conteudo,
                            'data_publicacao': noticia.data_publicacao.strftime('%H:%M:%S do dia %d/%m/%Y')
                          } for noticia in noticias]
                
              return JsonResponse({'noticias': noticias_data})
          except Exception as e:
              return JsonResponse({'error': str(e)}, status=500)
      else:
          forms_turma = FormCadastraTurma()
          forms_noticia = FormCadastraNoticia()

          lec_prof_logado = Leciona.objects.filter(prof_cpf=self.prof_cpf_logado)
          if lec_prof_logado:
            turmas = [{
                'id': lec.turma_id.id,
                'modalidade': lec.turma_id.modalidade,
                'horario': lec.turma_id.horario,
                'is_open': lec.turma_id.is_open,
                'data_abertura': lec.turma_id.data_abertura.strftime('%d/%m/%Y'),
                'data_fechamento': lec.turma_id.data_fechamento.strftime('%d/%m/%Y') if lec.turma_id.data_fechamento else None,
                'semestre': lec.turma_id.semestre,
                'vagas': lec.turma_id.vagas
            } for lec in lec_prof_logado]

          return render(request, self.template_file, {'forms_turma': forms_turma, 
                                                      'forms_noticia': forms_noticia, 
                                                      'turmas': turmas})
   
   def post(self, request, *args, **kwargs):
      try:
        form = FormCadastraTurma(request.POST)
        forms_noticia = FormCadastraNoticia(request.POST)

        if form.is_valid():
          modalidade = form.cleaned_data['modalidade']
          horario = form.cleaned_data['horario']
          vagas = form.cleaned_data['vagas']
          semestre = form.cleaned_data['semestre']

          horario_already_exists = Turma.objects.filter(Q(horario=horario) & Q(is_open=True)).exists()
          if horario_already_exists:
             raise Exception('O horário já está ocupado por outra turma. Selecione outro.')

          professor = Professor.objects.filter(user_cpf__cpf=self.prof_cpf_logado).first()

          if professor:
            nova_turma = Turma(
              modalidade=modalidade,
              horario=horario,
              vagas=vagas,
              semestre=semestre,
              is_open=True
            )
            novo_leciona = Leciona(
              prof_cpf=professor,
              turma_id=nova_turma
            )
            nova_turma.save()
            novo_leciona.save()
          else:
            raise Exception('O professor informado não foi encontrado no nosso banco de dados.')
          
        elif forms_noticia.is_valid():
          turma_id = forms_noticia.cleaned_data['turma_id']
          conteudo = forms_noticia.cleaned_data['conteudo']

          professor = Professor.objects.filter(user_cpf__cpf=self.prof_cpf_logado).first()
          turma = Turma.objects.filter(id=turma_id).first()

          leciona_exists = Leciona.objects.filter(Q(prof_cpf=professor) & Q(turma_id=turma)).exists()
          if not leciona_exists:
             raise Exception('Você não é professor da turma selecionada para cadastrar uma notícia nela.')

          if professor and turma:
             nova_noticia = Noticia(
                prof_cpf=professor,
                turma_id=turma,
                conteudo=conteudo
             )
             nova_noticia.save()

        return redirect(self.template_name)
      except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
      
class PaginaInicialView(View):
    template_name = 'pagina_inicial.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)