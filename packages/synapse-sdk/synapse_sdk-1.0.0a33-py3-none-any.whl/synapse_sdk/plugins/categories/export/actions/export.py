from abc import ABC, abstractmethod
from typing import Any, Literal

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.i18n import gettext as _
from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod
from synapse_sdk.utils.storage import get_pathlib


class ExportTargetHandler(ABC):
    """
    Abstract base class for handling export targets.

    This class defines the blueprint for export target handlers, requiring the implementation
    of methods to validate filters, retrieve results, and process collections of results.
    """

    @abstractmethod
    def validate_filter(self, value: dict, client: Any):
        """
        Validate filter query params to request original data from api.

        Args:
            value (dict): The filter criteria to validate.
            client (Any): The client used to validate the filter.

        Raises:
            PydanticCustomError: If the filter criteria are invalid.

        Returns:
            dict: The validated filter criteria.
        """
        pass

    @abstractmethod
    def get_results(self, client: Any, filters: dict):
        """
        Retrieve original data from target sources.

        Args:
            client (Any): The client used to retrieve the results.
            filters (dict): The filter criteria to apply.

        Returns:
            tuple: A tuple containing the results and the total count of results.
        """
        pass

    @abstractmethod
    def get_export_item(self, results):
        """
        Providing elements to build export data.

        Args:
            results (list): The results to process.

        Yields:
            generator: A generator that yields processed data items.
        """
        pass


class AssignmentExportTargetHandler(ExportTargetHandler):
    def validate_filter(self, value: dict, client: Any):
        if 'project' not in value:
            raise PydanticCustomError('missing_field', _('Project is required for Assignment.'))
        try:
            client.list_assignments(params=value)
        except ClientError:
            raise PydanticCustomError('client_error', _('Unable to get Assignment.'))
        return value

    def get_results(self, client: Any, filters: dict):
        return client.list_assignments(params=filters, list_all=True)

    def get_export_item(self, results):
        for result in results:
            yield {
                'data': result['data'],
                'files': result['file'],
                'id': result['id'],
            }


class GroundTruthExportTargetHandler(ExportTargetHandler):
    def validate_filter(self, value: dict, client: Any):
        if 'ground_truth_dataset_version' not in value:
            raise PydanticCustomError('missing_field', _('Ground Truth dataset version is required.'))
        try:
            client.get_ground_truth_version(value['ground_truth_dataset_version'])
        except ClientError:
            raise PydanticCustomError('client_error', _('Unable to get Ground Truth dataset version.'))
        return value

    def get_results(self, client: Any, filters: dict):
        filters['ground_truth_dataset_versions'] = filters.pop('ground_truth_dataset_version')
        return client.list_ground_truth_events(params=filters, list_all=True)

    def get_export_item(self, results):
        for result in results:
            files_key = next(iter(result['data_unit']['files']))
            yield {
                'data': result['data'],
                'files': result['data_unit']['files'][files_key],
                'id': result['ground_truth'],
            }


class TaskExportTargetHandler(ExportTargetHandler):
    def validate_filter(self, value: dict, client: Any):
        if 'project' not in value:
            raise PydanticCustomError('missing_field', _('Project is required for Task.'))
        try:
            client.list_tasks(params=value)
        except ClientError:
            raise PydanticCustomError('client_error', _('Unable to get Task.'))
        return value

    def get_results(self, client: Any, filters: dict):
        filters['expand'] = 'data_unit'
        return client.list_tasks(params=filters, list_all=True)

    def get_export_item(self, results):
        for result in results:
            files_key = next(iter(result['data_unit']['files']))
            yield {
                'data': result['data'],
                'files': result['data_unit']['files'][files_key],
                'id': result['id'],
            }


class TargetHandlerFactory:
    @staticmethod
    def get_handler(target: str) -> ExportTargetHandler:
        if target == 'assignment':
            return AssignmentExportTargetHandler()
        elif target == 'ground_truth':
            return GroundTruthExportTargetHandler()
        elif target == 'task':
            return TaskExportTargetHandler()
        else:
            raise ValueError(f'Unknown target: {target}')


class ExportParams(BaseModel):
    """
    Parameters for the export action.

    Attributes:
        storage (int): The storage ID to save the exported data.
        save_original_file (bool): Whether to save the original file.
        path (str): The path to save the exported data.
        target (str): The target source to export data from. (ex. ground_truth, assignment, task)
        filter (dict): The filter criteria to apply.
    """

    storage: int
    save_original_file: bool = True
    path: str
    target: Literal['assignment', 'ground_truth', 'task']
    filter: dict

    @field_validator('storage')
    @staticmethod
    def check_storage_exists(value, info):
        action = info.context['action']
        client = action.client
        try:
            client.get_storage(value)
        except ClientError:
            raise PydanticCustomError('client_error', _('Unable to get storage from Synapse backend.'))
        return value

    @field_validator('filter')
    @staticmethod
    def check_filter_by_target(value, info):
        action = info.context['action']
        client = action.client
        target = action.params['target']
        handler = TargetHandlerFactory.get_handler(target)
        return handler.validate_filter(value, client)


@register_action
class ExportAction(Action):
    name = 'export'
    category = PluginCategory.EXPORT
    method = RunMethod.JOB
    params_model = ExportParams
    progress_categories = {
        'dataset_conversion': {
            'proportion': 100,
        }
    }

    def get_filtered_results(self, filters, handler):
        """Get filtered target results."""
        try:
            result_list = handler.get_results(self.client, filters)
            results = result_list[0]
            count = result_list[1]
        except ClientError:
            raise PydanticCustomError('client_error', _('Unable to get Ground Truth dataset.'))
        return results, count

    def start(self):
        filters = {'expand': 'data', **self.params['filter']}
        target = self.params['target']
        handler = TargetHandlerFactory.get_handler(target)

        self.params['results'], self.params['count'] = self.get_filtered_results(filters, handler)
        export_items = handler.get_export_item(self.params['results'])

        storage = self.client.get_storage(self.params['storage'])
        pathlib_cwd = get_pathlib(storage, self.params['path'])
        return self.entrypoint(self.run, export_items, pathlib_cwd, **self.params)
