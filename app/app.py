from flask import Flask, request, render_template, redirect
from flask_apscheduler import APScheduler
import yaml
from datetime import datetime
from multiprocessing import Manager

from container import Container, create_conf
from logger import Logger

def read_conf(conf_path):
    with open(conf_path, 'r') as conf:
        data = yaml.safe_load(conf)
    return data

app = Flask(__name__)

manager = Manager()
shared_dict = manager.dict()
shared_dict['conf'] = create_conf()

log = Logger('app')

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='stop_containers', seconds=shared_dict['conf']['default']['check_interval'])
def stop_containers():
    log.debug("Launching scheduled check for stopping containers")
    default_max_lifetime = shared_dict['conf']['default']['max_lifetime']
    for c_dic in shared_dict['conf'].get('containers').values():
        c_name = c_dic['name']
        c_url = c_dic['url']
        c_max_lifetime = c_dic.get('max_lifetime')
        if c_max_lifetime:
            max_lifetime = c_max_lifetime
        else:
            max_lifetime = default_max_lifetime
        container = Container(c_name)
        last_req = shared_dict.get(c_url)
        if last_req:
            since_last_req = int(datetime.now().timestamp()) - int(float(last_req))
            if since_last_req > max_lifetime:
                log.info(f"Container {c_name} requested more than {max_lifetime}s ago ({since_last_req}s). Requesting stop")
                shared_dict[c_url] = None
                container.stop()
            else:
                pass
                log.debug(f"Container {c_name} requested less than {max_lifetime}s ago ({since_last_req}s)")
        else:
            log.debug(f"Unknown last request time for container {c_name}. Checking if stop needed")
            container.stop_if_needed(max_lifetime)

@scheduler.task('interval', id='update_conf', seconds=shared_dict['conf']['default']['update_conf_interval'])
def update_conf():
    log.debug("Launching scheduled conf update")
    shared_dict['conf'] = create_conf()

@app.route('/verif')
def index():
    orig = request.headers.get('X-Original-Host')
    log.debug(f"Received verification request with url : '{orig}'")
    container = None
    shared_dict[orig] = int(datetime.now().timestamp())
    for c_id in shared_dict['conf'].get('containers'):
        c_dic = shared_dict['conf']['containers'][c_id]
        if c_dic['url'] == orig:
            log.debug(f"Found corresponding container {c_dic['name']}")
            container_wait_time = c_dic.get('wait_page_time')
            container = Container(c_dic['name'])
    if not container:
        log.warning(f"Did not found corresponding container with wakontainer.url' : '{orig}'")
        return "Container not found in config", 401
    status = container.status()
    if ['req_state'] == 'error':
        return "Container does not exist", 401
    if not status['running']:
        log.debug(f"Containr '{ c_dic['name']}' not running. Returning 401")
        return "Container is not running", 401
    log.debug(f"Container '{ c_dic['name']}' already running. Returning 200")
    return "Container is running"

@app.route('/start')
def start():
    orig = request.headers.get('X-Original-Host')
    log.debug(f"Received starting request with 'X-Original-Host' : '{orig}'")
    default_wait_time = shared_dict['conf']['default']['wait_page_time']
    container = None
    for c_dic in shared_dict['conf'].get('containers').values():
        if c_dic['url'] == orig:
            log.debug(f"Found corresponding container {c_dic['name']}")
            container = Container(c_dic['name'])
            container_wait_time = c_dic.get('wait_page_time')
    if not container:
        log.warning(f"Did found corresponding container with wakontainer.url : '{orig}'")
        return render_template('404.html')
    status = container.status()
    if status['req_state'] == 'error':
        return "Container does not exist, check syntax"
    log.debug(f"Requesting start for container '{ c_dic['name']}'")
    s = container.start()
    if s['state'] == 'success' and s['msg'] == 'Already running':
        log.debug(f"Container '{ c_dic['name']}' was already running")
        return redirect('/')
    if container_wait_time:
        wait_time = container_wait_time
    else:
        wait_time = default_wait_time
    log.debug(f"Container '{ c_dic['name']}' successfully started, returning wait page")
    return render_template('wait.html', app_name=orig, wait_time=wait_time)