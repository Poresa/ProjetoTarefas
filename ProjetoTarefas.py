import pandas as pd
from matplotlib import pyplot as plt

## Lendo colunas csv do banco de dados
## Reading columns
df_tasks = pd.read_csv('rise_tasks.csv', usecols = ['id', 'title', 'description', 'project_id', 'assigned_to', 'deadline', 'status_id', 'priority_id', 'start_date', 'created_date', 'status_changed_at'])
df_projects = pd.read_csv('rise_projects.csv', usecols = ['id', 'title'])
df_status_info = pd.read_csv('rise_task_status.csv', usecols = ['id', 'title'])
df_users = pd.read_csv('rise_users.csv')

## Alterando o nome das colunas antes do merge merge
## Changing colomun name
df_projects.rename(columns = {'title': 'project_title', 'id': 'project_id'}, inplace = True)
df_status_info.rename(columns = {'title': 'status_name', 'id': 'status_id'}, inplace = True)
df_users.rename(columns = {'id': 'users_id'}, inplace = True)
df_tasks.rename(columns = {'assigned_to': 'users_id'}, inplace = True)

## Atualizando os valores do data frame tasks com merge
## Updating data frame tasks
df_tasks = pd.merge(df_tasks, df_projects, on = 'project_id', how = 'left')
df_tasks = pd.merge(df_tasks, df_status_info, on = 'status_id', how = 'left')
df_tasks = pd.merge(df_tasks, df_users, on = 'users_id', how = 'left')

## Deletando linhas baseado em um valor
## Deleting rows based on column value
df_tasks = df_tasks[df_tasks.status_name != 'To Do']

## Substituindo valores
## Replacing values
df_tasks['status_name'] = df_tasks['status_name'].replace('Done', 'Finalizada').replace('In progress', 'Em progresso')

## Listando nome dos status das tarefas
## Listing status values of projects
status_list = df_tasks['status_id'].unique().tolist()
assigned_list = df_tasks['users_id'].unique().tolist()

## Contando valores duplicados
## Counting duplicate values
df_plot_status = df_tasks.pivot_table(index = ['status_name'], aggfunc = 'size')
df_plot_users = df_tasks.query('status_name == "Em progresso"').pivot_table(index = ['first_name'], aggfunc = 'size')

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

## Chamando função de plot desejada
## Calling function to plot
plot_pautas_usuario()