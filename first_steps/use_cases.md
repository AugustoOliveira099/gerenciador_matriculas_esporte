# Casos de uso para um gerenciador de matrículas em esportes

[Diagrama de casos de uso](https://lucid.app/lucidchart/675aef64-241e-4358-8ae2-89fec9fb228c/edit?viewport_loc=-37%2C-179%2C2613%2C1085%2C0_0&invitationId=inv_57e94931-0139-45d1-bef1-f46771f2f8a6)

## Ator: aluno

### Realizar cadastro
**Fluxo normal:**
1. Informar nome completo
2. Informar CPF
3. Informar e-mail
4. Informar data de nascimento
5. Informar senha
6. Sistema vefirica se as informações são condizentes

**Extensões:**
* 2a - Se o CPF for inválido, pedir novo CPF
* 3a - Se o e-mail for inválido, pedir novo e-mail
* 5a - Se a senha for inválida, pedir nova senha
* 6a - Se as informações não existirem na base de dados, retornar erro
* 6b - Se as informações não forem referentes a uma mesma pessoa, retornar erro

</br>

### Fazer login
**Fluxo normal:**
1. Aluno informa e-mail ou CPF
2. Aluno informa senha
3. Sistema faz a autenticação das informações (sublinhado)

**Extensões:**
* 3a - Se houver erro na autenticação, devolver erro

</br>

### Enviar atestado de aptidão física
**Fluxo normal:**
1. Sistema verifica se o aluno está autenticado (sublinhado)
2. Aluno seleciona o documento a ser enviado

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 2a - Se o documento passar do tamanho aceito, informar erro

</br>

### Matricular em esporte
**Fluxo normal:**
1. Sistema verifica se o aluno está autenticado (sublinhado)
2. Aluno acessa o informativo com as turmas disponíveis
3. Aluno solicita a matrícula em uma turma
4. Sistema verifica a situação do atestado de aptidão física (sublinhado)
5. A matrícula é realizada por ordem de solicitação

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 4a - Se não for válido, informar erro e pedir para cadastrar um novo atestado
* 5a - Se não houver vagas, o aluno fica na lista de espera
* 5b - Se estiver na fila de espera e surgir vaga, o aluno é maticulado automaticamente

</br>

### Desmatricular em esporte
**Fluxo normal:**
1. Sistema verifica se o aluno está autenticado (sublinhado)
2. Aluno entra na turma que está matriculado
3. Aluno pede para cancelar a matrícula
4. Aluno se autentica novamente para confirmar a operação 
5. Sistema faz uma nova autenticação do aluno (sublinhado)

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 4a - Se as credenciais estiverem erradas, retornar erro
* 5a - Se não for possível fazer autenticação, retornar erro

</br>

### Visualizar turmas
**Fluxo normal:**
1. Sistema verifica se o aluno está autenticado (sublinhado)
2. O aluno possui acesso às turmas cadastradas no sistema. Nas turmas que ele está matriculado, ele possui acesso ao horário e local que as aulas acontecem, aos participantes da turma e às faltas relacionadas àquele esporte. Além dessas coisas, também é possível visualizar um histórico contendo as turmas que ele já participou

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação

</br>
</br>

## Administrador

### Fazer login
**Fluxo normal:**
1. Administrador informa e-mail ou CPF
2. Administrador informa senha
3. Sistema faz a autenticação das informações (sublinhado)

**Extensões:**
* 3a - Se houver erro na autenticação, devolver erro

</br>

### Cadastrar funcionário
**Fluxo normal:**
1. Sistema verifica se o administrador está autenticado (sublinhado)
2. Informar nome completo
3. Informar CPF
4. Informar e-mail
5. Informar data de nascimento
6. Informar senha
7. Informar se é um professor ou um administrador
8. O administrador se autentica novamente para confirmar a operação
9. Sistema faz uma nova autenticação do administrador (sublinhado)

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 3a - Se o CPF for inválido, pedir novo CPF
* 4a - Se o e-mail for inválido, pedir novo e-mail
* 6a - Se a senha for inválida, pedir nova senha
* 8a - Se as credenciais estiverem erradas, informar erro
* 9a - Se não for possível fazer autenticação, retornar erro
* 9b - Se as informações não forem referentes a uma mesma pessoa, retornar erro

</br>

### Validar atestado de aptidão física
**Fluxo normal:**
1. Sistema verifica se o administrador está autenticado (sublinhado)
2. O administrador faz o download do atestado
3. O Administrador verifica se o atestado é válido
4. O administrador valida o atestado conforme seu conteúdo

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 3a - Se o atestado não for válido, informar irregularidade

</br>

### Visualizar turmas e informações dos usuários
**Fluxo normal:**
1. Sistema verifica se o administrador está autenticado (sublinhado)
2. O administrador possui acesso à todas turmas cadastradas no sistema, assim como os horários e locais de aula dessas turmas, os participantes de cada esporte e às faltas de todos os alunos referente a um determinado esporte. Ele também consegue visualizar as informações de cadastro - incluindo o atestado de aptidão física - de todos os usuários, incluindo professores. Além dessas coisas, também é possível visualizar um histórico contendo todas as turmas cadastradas no sistema, assim como a exclusão dela, caso tenha ocorrido

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação

</br>
</br>

## Professor

### Fazer login
**Fluxo normal:**
1. Administrador informa e-mail ou CPF
2. Administrador informa senha
3. Sistema faz a autenticação das informações (sublinhado)

**Extensões:**
* 3a - Se houver erro na autenticação, retornar erro

</br>

### Cadastrar presença
**Fluxo normal:**
1. Sistema verifica se o administrador está autenticado (sublinhado)
2. Professor acessa uma das suas turmas
3. Professor escolhe uma data menor ou igual a do dia atual
4. Professor acessa a lista de presença
5. Professor faz a chamada

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 3a - Se a data escolhida for maior que a do dia atual, pedir para escolher uma data válida
* 5a - Se o aluno tiver mais de 30% de faltas referente à quantidade total de aulas planejadas, ele é desmatriculado automaticamente

</br>

### Cadastrar nova turma
**Fluxo normal:**
1. Sistema verifica se o professor está autenticado (sublinhado)
2. O professor informa o local das aulas
3. O professor informa o horário das aulas
4. O professor informa a quantidade de vagas
5. O professor se autentica novamente para confirmar a operação
6. Sistema faz uma nova autenticação do professor (sublinhado)
7. Sistema verifica a disponibilidade do horário a partir do local informado (sublinhado)

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 5a - Se as credenciais estiverem erradas, informar erro
* 6a - Se não for possível fazer autenticação, retornar erro
* 7a - Se o horário não estiver disponível, pedir para inserir um novo horário ou um novo local

</br>

### Fechar turma existente
**Fluxo normal:**
1. Sistema verifica se o professor está autenticado (sublinhado)
2. O professor informa a turma
3. O professor se autentica novamente para confirmar a operação
4. Sistema faz uma nova autenticação do professor (sublinhado)
5. Todos os alunos deixam de estar matriculados na turma

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação
* 3a - Se as credenciais estiverem erradas, informar erro
* 4a - Se não for possível fazer autenticação, retornar erro

</br>

### Cadastrar notícia
**Fluxo normal:**
1. Sistema verifica se o professor está autenticado (sublinhado)
2. O professor entra na turma
3. Escreve a mensagem no campo apropriado

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação

</br>

### Visualizar turmas e informações dos alunos
**Fluxo normal:**
1. Sistema verifica se o professor está autenticado (sublinhado)
2. O professor possui acesso à todas turmas cadastradas no sistema. Ele têm acesso aos participantes e à presença de todos seus   os alunos. Ele também consegue visualizar as informações de cadastro - incluindo o atestado de aptidão física - de todos os seus alunos. Além dessas coisas, também é possível visualizar um histórico contendo as turmas que ele deu aula, assim como a exclusão delas, caso tenha ocorrido

**Extensões:**
* 1a - Se não estiver autenticado, pedir autenticação

</br>
</br>

## Sistema

### Autenticar usuário
**Fluxo normal:**
1. Verifica se o e-mail ou CPF está resgistrado no banco de dados
2. Compara a senha informada com a senha armazenada
3. Retornar token válido por 1 dia

**Extensões:**
* 1a - Se o e-mail ou CPF informado não esteja registrado, retornar erro
* 2b - Se a senha for diferente daquela estabelecida no cadastrado para o e-mail ou CPF informado, retornar erro

</br>

### Verificar autenticação
**Fluxo normal:**
1. Verifica se o token é válido

**Extensões:**
* 1a - Se o token não existir, retornar erro
* 1b - Se o token for inválido, retornar erro

</br>

### Verificar disponibilidade de horário a partir de um local
**Fluxo normal:**
1. Busca pelo local do esporte
2. verifica se o local está sendo utilizado naquele horário

**Extensões:**
* 1a - Se o local não existir, retornar erro
* 2a - Se o local estiver em uso no horário informado, retornar erro

</br>

### Verificar situação do atestado de aptidão física
**Fluxo normal:**
1. Verifica se existe atestado cadastrado
2. Verifica se o atestado foi cadastrado há mais de 1 ano
3. Retorna que o atestado é válido

**Extensões:**
* 1a - Se não houver atestado, retornar que o atestado é inválido
* 2a - Se o atestado foi cadastrado há mais de 1 ano, retornar que o atestado é inválido
