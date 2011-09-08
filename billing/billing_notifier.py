# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

import nova.context
from nova import flags
from nova import rpc
from nova import log as logging


FLAGS = flags.FLAGS
flags.DEFINE_string('notification_topic', 'notification',
                    'RabbitMQ topic used for Nova notifications')

def notify(message):
    """Notifies the recipient of the desired event given the model.
    Log notifications using nova's default logging system"""
    context = nova.context.get_admin_context()
    message['method'] = 'notify'
    priority = message.get('priority',
                           FLAGS.default_notification_level)
    priority = priority.lower()
    logger = logging.getLogger(
            'billing.notification.%s' % message['event_type'])
    getattr(logger, priority)(json.dumps(message))
    rpc.cast(context, FLAGS.notification_topic, {'method':'notify','args':{'message':message}})