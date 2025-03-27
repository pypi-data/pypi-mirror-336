"""Parameterized tests for Delete subclass of action.Command.

Tests that `xprofiler delete ...` is working as expected.
"""

import argparse
from collections.abc import Mapping, Sequence
import itertools
from typing import Any
from unittest import mock

from xprofiler.src.cloud_diagnostics_xprof.actions import delete_action
from xprofiler.src.cloud_diagnostics_xprof.actions import list_action

from google3.testing.pybase import parameterized

# Define valid test parameters for delete command.
_DELETE_OPTIONS: Mapping[str, Mapping[str, Any]] = {
    # either --log-directory or --vm-name is required
    '--log-directory': {
        'metavar': 'GS_PATH',
        'nargs': '+',
    },
    '--vm-name': {
        'metavar': 'VM_NAME',
        'nargs': '+',
    },
    # --zone is required
    '--zone': {
        'metavar': 'ZONE_NAME',
    },
    # --verbose is optional
    '--verbose': {
        'action': 'store_true',
    },
}

# Helpful for testing log directory flags.
_LOG_DIRECTORY_TEST_CASES: Sequence[tuple[str, Sequence[str]]] = (
    (
        'single_log_directory',
        ['gs://test-log-directory/test-subdirectory'],
    ),
    (
        'multiple_log_directories',
        [
            'gs://test-log-directory/test-subdirectory0',
            'gs://test-log-directory2/test-subdirectory1',
            'gs://test-log-directory3/test-subdirectory2',
        ],
    ),
    (
        'multiple_log_directories_with_repeats',
        [
            'gs://test-log-directory/test-subdirectory0',
            'gs://test-log-directory2/test-subdirectory0',
            'gs://test-log-directory2/test-subdirectory1',
        ],
    ),
)

# Helpful for testing VM name flags.
_VM_NAME_TEST_CASES: frozenset[tuple[str, frozenset[str]]] = frozenset([
    (
        'single_vm_name',
        frozenset([
            'test-vm-1',
        ]),
    ),
    (
        'multiple_vm_names',
        frozenset([
            'test-vm-1',
            'test-vm-2',
            'test-vm-3',
        ]),
    ),
    (
        'multiple_vm_names_with_repeats',
        frozenset(['test-vm-1', 'test-vm-2', 'test-vm-2']),
    ),
])

# Helpful for testing zones flags.
_ZONE_TEST_CASES: frozenset[tuple[str, str | None]] = frozenset([
    ('no_zone', None),
    ('zone_specified', 'us-central1-a'),
])


class DeleteTest(parameterized.TestCase):

  def test_subparser_was_added(self):
    """Test that the parser is added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = delete_action.Delete()

    instance_of_class.add_subcommand(mock_subparser)

    mock_subparser.add_parser.assert_called_once_with(
        name='delete',
        help='Delete a hosted TensorBoard instance.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

  @parameterized.named_parameters(
      (flag_name, flag_name, flag_options)
      for flag_name, flag_options in _DELETE_OPTIONS.items()
  )
  def test_flags_for_subparser_was_added(self, flag_name, flag_options):
    """Test that the subparser flags are added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = delete_action.Delete()

    instance_of_class.add_subcommand(mock_subparser)

    # Arguments were added to mock_parser using mock_parser.add_argument.
    argument_calls = mock_parser.add_argument.call_args_list

    # Check that the flag was added and correct settings are used.
    found_flag = False
    for call in argument_calls:
      args, kwargs = call
      if flag_name in args:
        found_flag = True
        for arg, value in flag_options.items():
          self.assertEqual(kwargs.get(arg), value)
        break
    # Assert that the flag was actually found.
    if not found_flag:
      self.fail(f'No {flag_name} argument found')

  def test_no_log_diretory_no_vm_name(self):
    """Test that error is raised when log directory or VM are not provided."""
    command = delete_action.Delete()
    args = argparse.Namespace(
        log_directory=[],
        vm_name=[],
        zone=None,
    )

    with self.assertRaises(ValueError):
      command._build_command(args)

  def test_build_command_no_zone(self):
    """Test that the command defines zone as None when not is specified."""
    command = delete_action.Delete()
    # Note this assumes the parser is passing in the correct arguments for
    # _build_command(). If _build_command() is called directly, functionality is
    # not guaranteed.
    args = argparse.Namespace(
        log_directory=None,
        zone=None,
        vm_name=['test-vm-1'],
    )

    command_list = command._build_command(args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'delete',
            '--quiet',
            '--zone=None',
            'test-vm-1',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_build_command_zone_specified(self):
    """Test that the command is built correctly when a zone is specified."""
    command = delete_action.Delete()
    args = argparse.Namespace(
        log_directory=None,
        vm_name=['test-vm-1'],
        zone='us-central1-a',
    )

    command_list = command._build_command(args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'delete',
            '--quiet',
            '--zone=us-central1-a',
            'test-vm-1',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      (f'{log_test_name}-{vm_test_name}', log_directories, vm_names)
      for (log_test_name, log_directories), (vm_test_name, vm_names) in
      itertools.product(_LOG_DIRECTORY_TEST_CASES, _VM_NAME_TEST_CASES)
  )
  def test_build_command_multiple_vms_with_zone(
      self,
      log_directories: Sequence[str],
      vm_names: Sequence[str],
  ):
    """Test that the command is built correctly for a zone & multiple VMs."""
    command = delete_action.Delete()
    args = argparse.Namespace(
        log_directory=log_directories,
        vm_name=vm_names,
        zone='us-central1-a',
    )
    # Mocked to be output of list_action.List's run() method.
    vm_names_string = (
        'NAME\n'
        'test-vm-1\n'
        'test-vm-2\n'
    )
    vm_names_after_list_action_run = ['test-vm-1', 'test-vm-2']

    # Patch the list_action.List() to return a deterministic value.
    # Use enter_context() to ensure the patch is cleaned up after the test.
    mock_list_run = self.enter_context(
        mock.patch.object(
            list_action.List,
            'run',
            return_value=vm_names_string,
        )
    )
    command_list = command._build_command(args)

    # VM names come after the last flag
    expected_command = [
        command.GCLOUD_COMMAND,
        'compute',
        'instances',
        'delete',
        '--quiet',
        '--zone=us-central1-a',
    ]
    # VM names from log directory are before the specified VM names.
    expected_command.extend(vm_names_after_list_action_run)
    expected_command.extend(vm_names)
    self.assertEqual(
        command_list,
        expected_command,
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_build_command_extra_args(self):
    """Test that the command is built correctly when extra args are provided."""
    command = delete_action.Delete()
    args = argparse.Namespace(
        log_directory=None,
        vm_name=['test-vm-1'],
        zone='us-central1-a',
    )
    extra_args = {'--project': 'test-project'}

    command_list = command._build_command(args, extra_args)

    # VM names come after the last flag.
    expected_command = [
        command.GCLOUD_COMMAND,
        'compute',
        'instances',
        'delete',
        '--quiet',
        '--zone=us-central1-a',
        '--project=test-project',
        'test-vm-1',
    ]
    self.assertEqual(
        command_list,
        expected_command,
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      (f'{log_test_name}-{zone_test_name}', log_directories, zones)
      for (log_test_name, log_directories), (zone_test_name, zones) in
      itertools.product(_LOG_DIRECTORY_TEST_CASES, _ZONE_TEST_CASES)
  )
  def test_get_vms_from_log_directory_verbose(
      self,
      test_log_directories: Sequence[str],
      test_zone: str | None,
  ):
    """Test that the VM names are returned correctly when verbose is True."""
    command = delete_action.Delete()
    verbose = True
    # Make the number of VMs depened on number of log directories for realism.
    expected_vm_names = [
        f'test-vm-{i}'
        for i in range(len(test_log_directories))
    ]
    test_list_output = 'NAME\n' + '\n'.join(expected_vm_names) + '\n'

    # Patch list_action's run() method to return a deterministic value.
    with mock.patch.object(
        list_action.List,
        'run',
        return_value=test_list_output,
    ):
      vm_names = command._get_vms_from_log_directory(
          log_directories=test_log_directories,
          zone=test_zone,
          verbose=verbose,
      )

    self.assertEqual(
        vm_names,
        expected_vm_names,
        msg='VM names should be returned correctly.',
    )

if __name__ == '__main__':
  parameterized.googletest.main()
