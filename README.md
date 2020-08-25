<h3 align="center">
  Desafio: Medicar
</h3>

<p align="center">Sistema para gestão de consultas em uma clínica médica</p>

<p> Front End Angular</p>
<ul>
  <li> Acesse a pasta frontend e digite 'npm install' na linha de comando para instalar as dependências do node</li>
  <li> Após instalada as dependências, digite 'ng serve' para executar a aplicação. Ela estará disponível no link: http://localhost:4200 </li>
</ul>

<p> Back End Python - Django</p>
<ul>
  <li> Acesse a pasta backend/intmed e digite 'pip install -r requirements.txt' para baixar todas as dependências necessárias pro projeto Django</li>
  <li>O banco configurado é o Oracle, você pode mudar o host e o usuario e senha no arquivo settings.py. Caso queira usar o SQLite, basta comentar a conexão do Oracle e descomentar a do SQLite, que fica logo abaixo.</li>
  <li>Para excutar as migrations digite 'python manage.py migrate'</li>
  <li>Para criar um super usuário digite 'python manage.py createsuperuser' na linha de comando e siga as instruções. Com esse usuario você irá conseguir acessar a interface administrativa</li>
  <li> Após instalada as dependências e feitas as migrations, digite 'python manage.py runserver' para executar a aplicação. A interface administrativa estará disponível no link: http://localhost:8000/admin </li>
</ul>
