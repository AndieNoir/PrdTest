# Copyright (C) 2020 AndieNoir
#
# PrdTest is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PrdTest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PrdTest.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
import random
import traceback
import uuid
from datetime import datetime

import pandas as pd
from flask import Blueprint, render_template, request, Response, send_file
from flask_breadcrumbs import register_breadcrumb

from prdtest.data import ip_geolocation
from prdtest.data.generators.comscire_f33e62d4 import ComscireF33E62D4
from prdtest.data.generators.pseudorandom_2797e9c1 import Pseudorandom2797E9C1
from prdtest.utils import create_logs_dir_if_not_exist


blueprint = Blueprint('rng_assisted_divination', __name__)
ws_blueprint = Blueprint('rng_assisted_divination_ws', __name__)

_GENERATOR_CLASSES = [
    ComscireF33E62D4,
    Pseudorandom2797E9C1,
]

_generators = [*map(lambda cls: cls(), _GENERATOR_CLASSES)]

_pseudorandom = random.Random()

# TODO use sqlite
create_logs_dir_if_not_exist()
_log_file = open('logs/rng_assisted_divination.csv', 'a')
if os.stat('logs/rng_assisted_divination.csv').st_size == 0:
    _log_file.write('timestamp,ip_address,ip_address_country_alpha2,user_agent,session_id,target,answer,rtd_ms,generator_id\n')
    _log_file.flush()

_session_ids = set()
_session_ids.update(pd.read_csv('logs/rng_assisted_divination.csv')['session_id'].unique())

_unrecorded_trials = {}


@blueprint.route('/')
@register_breadcrumb(blueprint, '.', 'RNG-Assisted Divination')
def rng_assisted_divination():
    return render_template('rng_assisted_divination.html')


@blueprint.route('/stats')
@register_breadcrumb(blueprint, '.stats', 'Statistics')
def rng_assisted_divination_stats():
    return render_template('rng_assisted_divination_stats.html')


@blueprint.route('/rng_assisted_divination.csv')
def download_generated_dataset():
    return send_file(f'{os.getcwd()}/logs/rng_assisted_divination.csv')


@blueprint.route('/api/get_session_trial_counts_and_hit_counts')
def api_get_session_trial_counts_and_hit_counts():
    df = pd.read_csv('logs/rng_assisted_divination.csv')
    df = df[(df['session_id'] == request.args.get('session_id'))]
    generator_ids = df['generator_id'].unique()
    hit_rates_and_trial_counts = []
    for generator_id in generator_ids:
        generator_df = df[df['generator_id'] == generator_id]
        hit_rates_and_trial_counts.append({
            'generator_id': generator_id,
            'trial_count': len(generator_df),
            'hit_count': len(generator_df[generator_df['target'] == generator_df['answer']])
        })
    hit_rates_and_trial_counts.sort(key=lambda item: item['generator_id'])
    return Response(json.dumps(hit_rates_and_trial_counts),  mimetype='application/json')


@blueprint.route('/api/get_overall_trial_counts_and_hit_counts')
def api_get_overall_trial_counts_and_hit_counts():
    df = pd.read_csv('logs/rng_assisted_divination.csv')
    generator_ids = df['generator_id'].unique()
    hit_rates_and_trial_counts = []
    for generator_id in generator_ids:
        generator_df = df[df['generator_id'] == generator_id]
        hit_rates_and_trial_counts.append({
            'generator_id': generator_id,
            'trial_count': len(generator_df),
            'hit_count': len(generator_df[generator_df['target'] == generator_df['answer']])
        })
    hit_rates_and_trial_counts.sort(key=lambda item: item['generator_id'])
    return Response(json.dumps(hit_rates_and_trial_counts),  mimetype='application/json')


@ws_blueprint.route('/ws')
def ws(websocket):
    session_id = None
    while not websocket.closed:
        try:
            message = websocket.receive()
            if message is not None:
                message = json.loads(message)
                action = message['action'].lower()
                if action == 'new_session':
                    session_id = str(uuid.uuid4())
                    _session_ids.add(session_id)
                    websocket.send(json.dumps({'type': 'new_session_result', 'session_id': session_id}))
                elif action == 'set_session_id':
                    if message['session_id'] in _session_ids:
                        session_id = message['session_id']
                        websocket.send(json.dumps({'type': 'set_session_id_result', 'status': 1}))
                    else:
                        websocket.send(json.dumps({'type': 'set_session_id_result', 'status': 0}))
                elif action == 'prepare_trial':
                    if session_id is not None:
                        trial_id = str(uuid.uuid4())
                        _unrecorded_trials[trial_id] = {
                            'ip_address': request.remote_addr,
                            'ip_address_country_alpha2': ip_geolocation.get_country_alpha2(request.remote_addr),
                            'user_agent': request.user_agent.string,
                            'session_id': session_id,
                            'target': _pseudorandom.randint(0, 4)
                        }
                        websocket.send(json.dumps({'type': 'prepare_trial_result', 'trial_id': trial_id}))
                elif action == 'generate_trial_answer':
                    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    trial = _unrecorded_trials[message['trial_id']]
                    if trial['session_id'] == session_id:
                        generator = _pseudorandom.choice(_generators)
                        trial['answer'] = generator.get_int_between_0_and_4()
                        trial['generator_id'] = generator.id
                        trial['timestamp'] = timestamp
                        websocket.send(json.dumps({'type': 'target_and_answer', 'target': trial['target'], 'answer': trial['answer']}))
                elif action == 'set_session_id':
                    if message['session_id'] in _session_ids:
                        session_id = message['session_id']
                        websocket.send(json.dumps({'type': 'set_session_id_result', 'status': 1}))
                    else:
                        websocket.send(json.dumps({'type': 'set_session_id_result', 'status': 0}))
                elif action == 'report_rtd':
                    trial = _unrecorded_trials[message['trial_id']]
                    if trial['session_id'] == session_id:
                        _log_file.write(f'{trial["timestamp"]},{trial["ip_address"]},{trial["ip_address_country_alpha2"] if trial["ip_address_country_alpha2"] is not None else ""},"{trial["user_agent"]}",{trial["session_id"]},{trial["target"]},{trial["answer"]},{int(message["rtd_ms"])},{trial["generator_id"]}\n')
                        _log_file.flush()
                        del _unrecorded_trials[message['trial_id']]
        except Exception as e:
            traceback.print_exc()
            websocket.close(code=1011, message=str(e))
