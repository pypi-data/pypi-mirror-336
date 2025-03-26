# Copyright (c) 2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for the OpenTestFactory schemas."""

from typing import Any, Dict, Optional, Tuple

import json
import logging
import os

from jsonschema import Draft201909Validator, ValidationError
from yaml import safe_load

import opentf.schemas


########################################################################
# Schemas

SERVICECONFIG = 'opentestfactory.org/v1beta2/ServiceConfig'
SSHSERVICECONFIG = 'opentestfactory.org/v1alpha2/SSHServiceConfig'
EVENTBUSCONFIG = 'opentestfactory.org/v1alpha1/EventBusConfig'
PROVIDERCONFIG = 'opentestfactory.org/v1beta1/ProviderConfig'

SUBSCRIPTION = 'opentestfactory.org/v1/Subscription'

WORKFLOW = 'opentestfactory.org/v1/Workflow'
WORKFLOWCANCELLATION = 'opentestfactory.org/v1/WorkflowCancellation'
WORKFLOWCOMPLETED = 'opentestfactory.org/v1/WorkflowCompleted'
WORKFLOWCANCELED = 'opentestfactory.org/v1/WorkflowCanceled'
WORKFLOWRESULT = 'opentestfactory.org/v1alpha1/WorkflowResult'

GENERATORCOMMAND = 'opentestfactory.org/v1alpha1/GeneratorCommand'
GENERATORRESULT = 'opentestfactory.org/v1/GeneratorResult'

PROVIDERCOMMAND = 'opentestfactory.org/v1/ProviderCommand'
PROVIDERRESULT = 'opentestfactory.org/v1/ProviderResult'

EXECUTIONCOMMAND = 'opentestfactory.org/v1/ExecutionCommand'
EXECUTIONRESULT = 'opentestfactory.org/v1alpha1/ExecutionResult'
EXECUTIONERROR = 'opentestfactory.org/v1alpha1/ExecutionError'

AGENTREGISTRATION = 'opentestfactory.org/v1alpha1/AgentRegistration'

NOTIFICATION = 'opentestfactory.org/v1alpha1/Notification'

ALLURE_COLLECTOR_OUTPUT = 'opentestfactory.org/v1alpha1/AllureCollectorOutput'

CHANNEL_HOOKS = 'opentestfactory.org/v1alpha1/ChannelHandlerHooks'

QUALITY_GATE = 'opentestfactory.org/v1alpha1/QualityGate'
RETENTION_POLICY = 'opentestfactory.org/v1alpha1/RetentionPolicy'
TRACKER_PUBLISHER = 'opentestfactory.org/v1alpha1/TrackerPublisher'
INSIGHT_COLLECTOR = 'opentestfactory.org/v1alpha1/InsightCollector'


########################################################################
# JSON Schema Helpers

_schemas: Dict[str, Dict[str, Any]] = {}
_validators: Dict[str, Draft201909Validator] = {}

SCHEMAS_ROOT_DIRECTORY = list(opentf.schemas.__path__)[0]


def get_schema(name: str) -> Dict[str, Any]:
    """Get specified schema.

    # Required parameters

    - name: a string, the schema name (its kind)

    # Returned value

    A _schema_.  A schema is a dictionary.

    # Raised exceptions

    If an error occurs while reading the schema, the initial exception
    is logged and raised again.
    """
    if name not in _schemas:
        try:
            with open(
                os.path.join(SCHEMAS_ROOT_DIRECTORY, f'{name}.json'),
                'r',
                encoding='utf-8',
            ) as schema:
                _schemas[name] = json.loads(schema.read())
        except Exception as err:
            logging.error('Could not read schema "%s": %s', name, err)
            raise
    return _schemas[name]


def _validator(schema: str) -> Draft201909Validator:
    if schema not in _validators:
        _validators[schema] = Draft201909Validator(get_schema(schema))
    return _validators[schema]


def validate_schema(
    schema: str, instance: Dict[str, Any]
) -> Tuple[bool, Optional[str]]:
    """Return (True, None) if instance validates schema.

    # Required parameters

    - schema: a string, the schema name (its kind)
    - instance: a dictionary

    # Returned value

    A (bool, Optional[str]) pair.  If `instance` is a valid instance of
    `schema`, returns `(True, None)`.  If not, returns `(False, error)`.
    """
    try:
        _validator(schema).validate(instance=instance)
    except ValidationError as err:
        return False, str(err)
    return True, None


def read_and_validate(filename: str, schema: str) -> Dict[str, Any]:
    """Read and validate a JSON or YAML file.

    # Required parameters

    - filename: a string, the file name
    - schema: a string, the schema to validate the file content

    # Returned value

    A dictionary, the definition.

    # Raised exceptions

    An _OSError_ exception is raised if the file cannot be read.

    A _ValueError_ exception is raised if the JSON or YAML file is
    invalid.
    """
    with open(filename, 'r', encoding='utf-8') as cnf:
        config = safe_load(cnf)

    if not isinstance(config, dict):
        raise ValueError('File is not a JSON object.')
    valid, extra = validate_schema(schema or SERVICECONFIG, config)
    if not valid:
        raise ValueError(f'Invalid content: {extra}.')
    return config
