import pandas as pd
from matplotlib import pyplot as plt

## Lendo colunas csv do banco de dados
## Reading columns
df_tasks = pd.read_csv('rise_tasks.csv', usecols = ['id', 'title', 'description', 'project_id', 'assigned_to', 'deadline', 'status_id', 'priority_id', 'start_date', 'created_date', 'status_changed_at'])
df_projects = pd.read_csv('rise_projects.csv', usecols = ['id', 'title'])
df_status_info = pd.read_csv('rise_task_status.csv', usecols = ['id', 'title'])
df_users = pd.read_csv('rise_users.csv', usecols = ['id', 'first_name'])
df_clients = pd.read_csv('rise_clients.csv', usecols = ['id', 'company_name'])
df_priority = pd.read_csv('rise_task_priority.csv', usecols = ['id', 'title'])

## Alterando o nome das colunas antes do merge merge
## Changing colomun name
df_projects.rename(columns = {'title': 'project_title', 'id': 'project_id'}, inplace = True)
df_status_info.rename(columns = {'title': 'status_name', 'id': 'status_id'}, inplace = True)
df_users.rename(columns = {'id': 'users_id'}, inplace = True)
df_tasks.rename(columns = {'assigned_to': 'users_id'}, inplace = True)
df_clients.rename(columns = {'id': 'project_id'}, inplace = True)
df_priority.rename(columns = {'id': 'priority_id', 'title': 'priority_title'}, inplace = True)

## Atualizando os valores do data frame tasks com merge
## Updating data frame tasks
df_tasks = pd.merge(df_tasks, df_projects, on = 'project_id', how = 'left')
df_tasks = pd.merge(df_tasks, df_status_info, on = 'status_id', how = 'left')
df_tasks = pd.merge(df_tasks, df_users, on = 'users_id', how = 'left')
df_tasks = pd.merge(df_tasks, df_clients, on = 'project_id', how = 'left')
df_tasks = pd.merge(df_tasks, df_priority, on = 'priority_id', how = 'left')

## Deletando linhas baseado em um valor
## Deleting rows based on column value
# df_tasks = df_tasks[df_tasks.status_name != 'To Do']

## Substituindo valores
## Replacing values
df_tasks['status_name'] = df_tasks['status_name'].replace('Done', 'concluído').replace('In progress', 'em progresso').replace('Em Revisão', 'em revisão')

## Salvando um arquivo filtrado para trabalhar no Power BI
## Saving file to use in Power BI
df_tasks.to_excel('sistema_filtrado_bi.xlsx', index=False)

## Listando nome dos status das tarefas
## Listing status values of projects
status_list = df_tasks['status_id'].unique().tolist()
assigned_list = df_tasks['users_id'].unique().tolist()

## Contando valores duplicados
## Counting duplicate values
df_plot_status = df_tasks.pivot_table(index = ['status_name'], aggfunc = 'size')
df_plot_users = df_tasks.query('status_name == "em progresso"').pivot_table(index = ['first_name'], aggfunc = 'size')

## Criando variáveis do plot 
## Creating variables to plot
column_status_name = df_plot_status.index
column_status_frequency = df_plot_status.values
column_user_name = df_plot_users.index
column_progresso = df_plot_users.values

## Criando funções para plotar dados
## Creating functions to plot data
def plot_pautas_usuario():
	plt.barh(column_user_name, column_progresso)
	plt.ylabel('Nome')
	plt.xlabel('Número de tarefas')
	plt.title('Quantidade de tarefas em progresso')
	plt.show()

def plot_status_tarefa():
	plt.barh(column_status_name, column_status_frequency)
	plt.ylabel('Nome do status')
	plt.xlabel('Número de tarefas')
	plt.title('Quantidade de tarefas por status')
	plt.show()

## Transformando em tempo para calcular
## Transforming to datetime to calculate
df_tasks['deadline'] = pd.to_datetime(df_tasks['deadline'])
df_tasks['created_date'] = pd.to_datetime(df_tasks['created_date'])

## Criando a coluna de idade da tarefa
## Creating the column age for the tasks 
df_tasks['task_age'] = df_tasks['deadline'] - df_tasks['created_date']
df_tasks['task_age'] = df_tasks['task_age'].dt.days

## Filtrando por idade e status
## Filtering by age and status
df_age_progress = df_tasks.query('status_name == "em progresso" and task_age > 30')[['project_title', 'title', 'task_age']]
df_age_revision = df_tasks.query('status_name == "em revisão" and task_age > 30')[['project_title', 'title', 'task_age']]

## Contando quantas das tarefas acima são do mesmo projeto
## Status Em progresso
## Status in progress
df_plot_age_progress = df_age_progress.pivot_table(index = ['project_title'], aggfunc = 'size')
df_plot_age_revision = df_age_revision.pivot_table(index = ['project_title'], aggfunc = 'size')

## Status Em Revisão
## Status in revision
df_plot_age_revision = df_age_revision.pivot_table(index = ['project_title'], aggfunc = 'size')

## Verificando informações sobre a idade das pautas
## Removando valores NaT antes
df_tasks.dropna(subset = ['task_age'], inplace = True)

def print_relatorio():
	df_resolvidas_dia = df_tasks.loc[(df_tasks['task_age'] == 0) & (df_tasks['status_name'] == 'Finalizada')]
	print('##############################')
	print('#### RELATÓRIO DO SISTEMA')
	print()

	print('#### GERAL')
	## Tarefas totais do sistema
	print(f'> Número de tarefas cadastradas no sistema: {len(df_tasks)} tarefas')
	print()

	print('#### RESOLVIDAS')
	## Tarefas que foram resolvidas no mesmo dia
	print(f'> Tarefas lançadas e resolvidas no mesmo dia: {len(df_resolvidas_dia)} tarefas, que representa {(len(df_resolvidas_dia)/len(df_tasks))*100:.0f}% das tarefas totais.')
	print()

	print('#### ATRASADAS')
	## Tarefas atrasadas
	print(f'> Número de tarefas atrasadas no sistema: {len(df_tasks.loc[(df_tasks["task_age"] > 30)])} tarefas, que representa {len(df_tasks.loc[(df_tasks["task_age"] > 30)])/len(df_tasks)*100:.0f}% das tarefas totais.')
	print(f'> Número de tarefas atrasadas com status "em progresso":  {len(df_age_progress)} tarefas, que representa {(len(df_age_progress)/len(df_tasks))*100:.0f}% das tarefas totais.')
	print(f'> Número de tarefas atrasadas com status "em revisão":  {len(df_age_revision)} tarefas, que representa {(len(df_age_revision)/len(df_tasks))*100:.1f}% das tarefas totais.')
	print()

	print('#### ESTATÍSTICAS')
	## Média das idades das tarefas
	mean_task_age = df_tasks['task_age'].mean()
	print(f'> A média da idade das tarefas é: {mean_task_age:.0f} dias')

	## Mediana das idades
	median_task_age = df_tasks['task_age'].median()
	print(f'> A mediana das idade das tarefas é: {median_task_age:.0f} dias')