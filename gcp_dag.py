
from datetime import datetime, timedelta
import airflow, time
from airflow import DAG, settings
from airflow.models import Connection
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator #this module is only necessary if using a BashOperator
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'email':[''],
    #'email_on_failure': True,
    #'email_on_success': True,
    'start_date': airflow.utils.dates.days_ago(2),
    'retries': 0,
}

def add_gcp_connection(ds, **kwargs):
    """"Add a airflow connection for GCP"""
    json_data = json.loads(open('/usr/local/airflow/gcp.json').read())
    new_conn = Connection(
        conn_id='AirflowGCPKey',
        conn_type='google_cloud_platform',
    )
    scopes = [
        "https://www.googleapis.com/auth/pubsub",
        "https://www.googleapis.com/auth/datastore",
        "https://www.googleapis.com/auth/bigquery",
        "https://www.googleapis.com/auth/devstorage.read_write",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/cloud-platform",
    ]
    conn_extra = {
        "extra__google_cloud_platform__scope": ",".join(scopes),
        "extra__google_cloud_platform__project": "<insert your project platform>",
        "extra__google_cloud_platform__key_path": '/usr/local/airflow/gcp.json',
        "extra__google_cloud_platform__key_json":  json_data
    }
    conn_extra_json = json.dumps(conn_extra)
    new_conn.set_extra(conn_extra_json)

    session = settings.Session()
    if not (session.query(Connection).filter(Connection.conn_id == new_conn.conn_id).first()):
        session.add(new_conn)
        session.commit()
    else:
        msg = '\n\tA connection with `conn_id`={conn_id} already exists\n'
        msg = msg.format(conn_id=new_conn.conn_id)
        print(msg)
dag = DAG(
    'gcp_dag',
    default_args=default_args,
    schedule_interval="@once")

# Task to add a connection
t1 = PythonOperator(
    dag=dag,
    task_id='add_gcp_connection_python',
    python_callable=add_gcp_connection,
    provide_context=True,
)
