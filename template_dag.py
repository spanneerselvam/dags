from datetime import datetime, timedelta
import airflow, time
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator #this module is only necessary if using a BashOperator
import Template.template #This is the path to the template.py (ArithmeticOperations Class) ie: Template/template.py
from Template.template import ArithmeticOperations #importing the ArithmeticOperations Class

"""
This is a tutorial DAG. Please pull this document from GitHub and folder titled "Template".
Rename it and use this file as a template when you write dags. You will write your tasks
in here which will then be executed by airflow. This file imports the class ArithmeticOperations from the folder
template. You will edit that when you write your Python class that will be executed by the airflow task below
"""
#Insert your comments for what your file does in the triple comment block below.
"""
***INSERT DESCRIPTION HERE:****
DESCRIPTION: This is a template dag
"""
"""
This file instantiates a DAG that will run all the processes for Template as different tasks
The overview of this file:
1) default_args is a python dictionary that sets up a dag
2) dag instantiation: instantiates our Template DAG with the default_args as parameters
3) tasks are what the dag runs. In this example, we have two tasks: a task written with a PythonOperator (task_1)
    and a task written with a BashOperator (task_2) just to show the different things you can do with airflow.
4) Setting dependencies. We want task_2 to run after task_1.
"""

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['airflow@example.com'], #insert your email here
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    dag_id = "template", #rename your dag id so it's the name same as your file without the dag
    default_args=default_args,
    description = "Executes basic arithmetic operations as a demo for writing airflow dags", #write a brief description for what your dag will accomplish
    schedule_interval="@daily",
)
"""
The main function below will execute your class that you have imported. This is what the airflow's
task_1 will call on.
"""
def main(**context): #you can rename this function.
    """
    This function creates an instance of the class ArithmeticOperations from the module template
    located in the template Directory (template.py).
    Here, we will choose two random numbers, find their sum, their product, and their remainder.
    """
    demo = ArithmeticOperations()
    demo.print_sum()
    demo.print_product()
    demo.print_remainder()

"""
task_1 calls the main function. It will be executed first.
"""

task_1 = PythonOperator(
    task_id = "BasicArithmeticOperations", #rename your task
    python_callable = main,
    execution_timeout=timedelta(minutes=3),
    dag = dag,
    provide_context = True,
    op_kwargs = {
        'extra_detail': 'nothing'
    }
)
"""
task_2 simply executes the bash command, echo, to say hi!
You can rewrite task_2 to be a python function like above.
"""
task_2 = BashOperator(
    task_id = 'say_hi',
    bash_command = 'echo "Hi there!"',
    dag = dag,
)
"""
task_3 simply executes a bash script that will print "Hello World". This is how you call a bash script in Airflow.
task_3_command (lines 93-96) are executed. Line 94 is critical to open permissions for the file. Line 95 calls the bash script.
"""
task_3_command = """
sudo chmod +x /usr/local/airflow/dags/Template/hello_world.sh
sudo bash /usr/local/airflow/dags/Template/hello_world.sh
"""
task_3 = BashOperator(
    task_id = 'Hello_World',
    bash_command = task_3_command,
    dag = dag
)
"""
Here we set dependencies so that we can run certain tasks first.
We want to run task_1 before we run task_2.
"""
task_1 >> task_2 >> task_3
"""
If we had three tasks we wanted to run and task_2 and task_3 had to run after task_1,
we can write it as a list:
task_1 >> [task_2, task_3]
"""
