# Atividade 1

**Os bytes passaram por quantos lugares? (cliente → API → banco e storage)**

Os bytes passam pela API, que envia o arquivo para o banco de dados e para o storage.

**O que acontece com a memória da API se 100 alunos enviarem vídeos de 1 GB ao mesmo tempo?**

O consumo de memória pode ficar muito alto, causando lentidão ou até a queda da API.

**Por que o backup do banco fica pesado quando guardamos arquivos nele?**

Porque os arquivos ocupam muito espaço e aumentam o tamanho do backup.

**Se o `put_object` funcionar e o `INSERT` falhar, o que sobra? (Dica: Atividade 5.)**

O arquivo fica no storage, mas não existe registro correspondente no banco de dados.

---

# Atividade 2

**Abra o script: a chave e o segredo do storage estão no código do cliente. Se isso fosse um app web ou mobile, quem teria acesso a eles?**

Qualquer pessoa que conseguisse acessar o código do aplicativo poderia encontrar essas credenciais.

**Com essas credenciais, o cliente poderia apagar arquivos dos outros? Listar o bucket inteiro?**

Sim, dependendo das permissões concedidas às credenciais.

**Como a aplicação saberia de quem é esse arquivo, ou que ele existe?**

A aplicação não saberia automaticamente, pois o arquivo foi enviado diretamente ao storage, sem registro no banco de dados.

---

# Atividade 3

**Que informação o cliente recebeu? Ele consegue usar esse link para outro arquivo ou outro nome?**

O cliente recebeu uma URL pré-assinada para enviar um arquivo. Ela possui permissões e validade específicas, não permitindo acessar qualquer arquivo livremente.

**Por que esse padrão é o usado por S3, Google Cloud Storage, Azure etc. em aplicações reais?**

Porque permite transferir arquivos diretamente para o storage sem precisar passar todo o conteúdo pela API.

---

# Atividade 4

**Discuta: por que não deixar o bucket público e simplesmente devolver `http://localhost:9000/uploads/<chave>`?**

Porque um bucket público permitiria acesso aos arquivos sem controle adequado. O link pré-assinado permite acesso temporário e autorizado.

---

# Atividade 5

**Crie um "fantasma": no console do RustFS, apague manualmente um objeto da pasta `caso1/` e rode a auditoria de novo. O registro continua no banco, mas o arquivo sumiu. E o `/do-banco` desse id — ainda funciona? Por quê?**

Sim. O download pelo `/do-banco` continua funcionando porque o conteúdo do arquivo também está salvo no banco de dados, independentemente do objeto ter sido apagado do RustFS.

**Discuta: quando temos dois sistemas de armazenamento, como garantir que eles concordem? (transações, rotina de limpeza, eventos/notificações do bucket, status `pendente`).**

Podemos usar registros com status `pendente`, rotinas de limpeza e verificações para identificar arquivos sem registro ou registros sem arquivo.

---

# Atividade 6

**O que aconteceu com a coluna e com os hashes salvos?**

A coluna `hash_sha256` foi removida ao executar `alembic downgrade -1`. Com isso, os hashes armazenados nessa coluna também foram perdidos.

**Envie um arquivo pelo caso 1 agora. O que a API responde? Por quê?**

O envio falha porque o código tenta salvar o hash em uma coluna que não existe mais no banco.

**Rode `alembic upgrade head` de novo para voltar ao estado correto.**

O comando reaplica a migração, recriando a coluna e o índice para que a API volte a funcionar corretamente.

### Discuta

**Por que não basta editar o `CREATE TABLE` e recriar o banco? (Pense em um banco de produção com milhões de registros.)**

Porque recriar o banco pode apagar dados existentes. As migrações permitem modificar a estrutura preservando os dados.

**Por que a migração vai para o Git junto com o código?**

Para registrar as mudanças no banco e permitir que outras pessoas reproduzam a mesma estrutura.

**O que aconteceria se dois alunos criassem migrações diferentes a partir da `0001` e juntassem o código? Rode `alembic heads` para investigar.**

Poderiam existir duas migrações como cabeças diferentes, exigindo uma migração de junção para unificá-las.

**Por que o `downgrade()` precisa desfazer as operações na ordem inversa?**

Porque uma operação pode depender de outra. Desfazer na ordem inversa evita tentar remover algo que ainda é necessário.