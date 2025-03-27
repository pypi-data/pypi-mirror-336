"""Parameterized tests for create subclass of action.Command.

Tests that `xprofiler create ...` is working as expected.
"""

import argparse
from typing import Any
from unittest import mock
import uuid

from xprofiler.src.cloud_diagnostics_xprof.actions import create_action

from google3.testing.pybase import parameterized

_TEST_LOG_DIRECTORY = 'gs://test-bucket/test-directory/test-subdirectory'
_TEST_ZONE = 'us-central1-a'
_TEST_UUID = 'test-uuid'
_TEST_VM_NAME = 'test-vm-name'
# Define valid test parameters for create command.
_CREATE_OPTIONS: frozenset[tuple[str, frozenset[tuple[str, Any]]]] = frozenset([
    # --log-directory is required
    (
        '--log-directory',
        frozenset([
            ('metavar', 'GS_PATH'),
            ('required', True),
        ]),
    ),
    # --zone is optional
    (
        '--zone',
        frozenset([
            ('metavar', 'ZONE_NAME'),
        ]),
    ),
    # --vm-name is optional
    (
        '--vm-name',
        frozenset([
            ('metavar', 'VM_NAME'),
        ]),
    ),
    # --verbose is optional
    (
        '--verbose',
        frozenset([
            ('action', 'store_true'),
        ]),
    ),
])

class CreateTest(parameterized.TestCase):

  def test_subparser_was_added(self):
    """Test that the parser is added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = create_action.Create()

    instance_of_class.add_subcommand(mock_subparser)

    mock_subparser.add_parser.assert_called_once_with(
        name='create',
        help='Create a hosted TensorBoard instance.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

  @parameterized.named_parameters(
      (flag_name, flag_name, flag_options)
      for flag_name, flag_options in _CREATE_OPTIONS
  )
  def test_flags_for_subparser_was_added(self, flag_name, flag_options):
    """Test that the subparser flags are added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = create_action.Create()

    instance_of_class.add_subcommand(mock_subparser)

    # Arguments were added to mock_parser using mock_parser.add_argument.
    argument_calls = mock_parser.add_argument.call_args_list

    # Check that the flag was added and correct settings are used
    found_flag = False
    for call in argument_calls:
      args, kwargs = call
      if flag_name in args:
        found_flag = True
        for items in flag_options:
          arg, value = items
          self.assertEqual(kwargs.get(arg), value)
        break
    # Assert that the flag was actually found.
    if not found_flag:
      self.fail(f'No {flag_name} argument found')

  def test_build_command_zone_specified(self):
    """Test that the command is built correctly when a zone is specified."""
    test_deterministic_label_string = (
        'log_directory=fake-label-string'
    )
    args = argparse.Namespace(
        log_directory=_TEST_LOG_DIRECTORY,
        zone=_TEST_ZONE,
        vm_name=None,
        verbose=False,
    )

    # Patch uuid.uuid4() to return a deterministic value in _build_command().
    with mock.patch.object(uuid, 'uuid4', return_value=_TEST_UUID):
      # Assuming the format_label_string() is working correctly, we can patch it
      # to return a deterministic value for testing.
      command = create_action.Create()
      with mock.patch.object(
          command,
          '_format_label_string',
          return_value=test_deterministic_label_string,
      ):
        command_list = command._build_command(args)

    startup_script = create_action.startup_script_string(
        _TEST_LOG_DIRECTORY,
        f'{command.VM_BASE_NAME}-{_TEST_UUID}',
        _TEST_ZONE,
    )

    startup_script_flag = f'--metadata=startup-script={startup_script}'
    # Zone information before extra args (labels)
    expected_command_wihout_startup_script = [
        command.GCLOUD_COMMAND,
        'compute',
        'instances',
        'create',
        f'{command.VM_BASE_NAME}-{_TEST_UUID}',
        f'--zone={_TEST_ZONE}',
    ]
    expected_command_wihout_startup_script.extend([
        f'{arg}={value}'
        for arg, value in create_action._DEFAULT_EXTRA_ARGS.items()
    ])
    expected_command_wihout_startup_script.extend([
        '--labels=log_directory=fake-label-string',
        startup_script_flag,
    ])

    self.assertEqual(
        command_list,
        expected_command_wihout_startup_script,
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_run_command_success(self):
    """Test that the describe command is built correctly when a zone is specified."""
    args = argparse.Namespace(
        log_directory=_TEST_LOG_DIRECTORY,
        zone=_TEST_ZONE,
        vm_name=None,
        verbose=False,
    )
    command = create_action.Create()
    with mock.patch.object(
        command,
        '_run_command',
        side_effect=['abc', '{"labels" : {"tb_backend_id": "12345"}}'],
    ):
      command_output = command.run(args)
      self.assertEqual(command_output, '')

  def test_run_command_success_with_vm_name(self):
    """Test that the describe command is built correctly when a zone is specified."""
    args = argparse.Namespace(
        log_directory=_TEST_LOG_DIRECTORY,
        zone=_TEST_ZONE,
        vm_name="vm_name",
        verbose=False,
    )
    command = create_action.Create()
    with mock.patch.object(
        command,
        '_run_command',
        side_effect=['abc', '{"labels" : {"tb_backend_id": "12345"}}'],
    ):
      command_output = command.run(args)
      self.assertEqual(command_output, '')

  def test_run_command_create_failure(self):
    args = argparse.Namespace(
        log_directory=_TEST_LOG_DIRECTORY,
        zone=_TEST_ZONE,
        vm_name=None,
        verbose=False,
    )
    command = create_action.Create()
    with mock.patch.object(
        command,
        '_run_command',
        side_effect=[RuntimeError,
                     '{"labels" : {"tb_backend_id": "12345"}}'],
    ):
      with self.assertRaises(RuntimeError):
        _ = command.run(args)

  def test_run_command_describe_failure(self):
    args = argparse.Namespace(
        log_directory=_TEST_LOG_DIRECTORY,
        zone=_TEST_ZONE,
        vm_name=None,
        verbose=False,
    )
    command = create_action.Create()
    with mock.patch.object(
        command,
        '_run_command',
        side_effect=['abc', RuntimeError],
    ):
      with self.assertRaises(RuntimeError):
        _ = command.run(args)

  def test_run_command_missing_labels_with_timeout(self):
    args = argparse.Namespace(
        log_directory=_TEST_LOG_DIRECTORY,
        zone=_TEST_ZONE,
        vm_name=None,
        verbose=False,
    )

    create_action._MAX_WAIT_TIME_IN_SECONDS = 1
    command = create_action.Create()

    with mock.patch.object(
        command,
        '_run_command',
        side_effect=['abc', '{"labels" : {"bad_label": "12345"}}'],
    ):
      command_output = command.run(args)
      self.assertEqual(command_output, 'abc')


if __name__ == '__main__':
  parameterized.googletest.main()
