"""Parameterized tests for subclasses of action.Command.

Tests that Command (abstract class) is working as expected.
"""

import argparse
from collections.abc import Mapping, Sequence
import io
from unittest import mock

from xprofiler.src.cloud_diagnostics_xprof.actions import action

from google3.testing.pybase import parameterized


# Create a concrete subclass for testing.
class ConcreteCommand(action.Command):

  def __init__(self, name: str, description: str):
    super().__init__(name=name, description=description)

  def add_subcommand(self, subparser: argparse._SubParsersAction) -> None:
    pass

  def _build_command(
      self,
      args: argparse.Namespace,
      extra_args: Mapping[str, str] | None = None,
      verbose: bool = False,
  ) -> Sequence[str]:
    return ['echo', 'test']  # Simple command to test with


class CheckTest(parameterized.TestCase):

  def test_run_command(
      self,
  ):
    """Test that a simple command is run."""
    command = ConcreteCommand(
        name='test_command',
        description='A test command',
    )
    diag_stdout = command._run_command(['echo', 'test'])

    self.assertEqual(diag_stdout, 'test\n')

  def test_run_calls_build_command(self):
    """Test that the command is run."""
    command_instance = ConcreteCommand(
        name='test_command',
        description='A test command',
    )
    command_instance._build_command = mock.MagicMock(
        return_value=['echo', 'test'],
    )
    args_mock = mock.MagicMock()

    command_instance.run(args=args_mock)

    command_instance._build_command.assert_called_once_with(
        args_mock,
        None,
        False,
    )

  def test_run_verbose(self):
    """Test that the command is run with verbose."""
    command_instance = ConcreteCommand('test', 'Test command')
    args_mock = mock.MagicMock()

    with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
      command_instance.run(
          args=args_mock,
          verbose=True,
      )
      # Note new lines are are added to the end due to the print command.
      expected_output = (
          'Command to run: [\'echo\', \'test\']\n'
          'Command [\'echo\', \'test\'] succeeded.\n'
          'Output: test'
      )
      self.assertEqual(
          first=mock_stdout.getvalue().strip(),
          second=expected_output,
          msg='Output should be command output.',
      )

  def test_run_error(self):
    """Test that an error is raised when the command fails."""
    command_instance = ConcreteCommand('test', 'Test command')
    args_mock = mock.MagicMock()
    command_instance._build_command = mock.MagicMock(
        return_value=['false'],
    )
    # Allow the ValueError to be raised.
    with self.assertRaises(ValueError):
      command_instance.run(args=args_mock)

    with mock.patch('sys.stdout', new_callable=io.StringIO):
      with self.assertRaises(ValueError):
        command_instance.run(
            args=args_mock,
            verbose=True,
        )

  def test_format_label_string_no_bucket(self):
    """Test that the label string correctly formatted when no bucket given."""
    command_instance = ConcreteCommand('test', 'Test command')
    labels = {
        'key1': 'value1',
        'key2': 'value2',
    }

    self.assertEqual(
        command_instance._format_label_string(labels),
        'key1=value1,key2=value2',
    )

  @parameterized.named_parameters(
      (
          'log_directory_only',
          {
              'log_directory': 'gs://test-bucket/directory/subdirectory',
          },
          'log_directory=test-bucket--slash--directory--slash--subdirectory',
      ),
      (
          'log_directory_and_other_keys_at_start',
          {
              'key1': 'value1',
              'key2': 'value2',
              'log_directory': 'gs://test-bucket/directory/subdirectory',
          },
          'key1=value1,key2=value2,log_directory=test-bucket--slash--directory--slash--subdirectory',
      ),
      (
          'log_directory_and_other_keys_in_middle',
          {
              'key1': 'value1',
              'log_directory': 'gs://test-bucket/directory/subdirectory',
              'key2': 'value2',
          },
          'key1=value1,log_directory=test-bucket--slash--directory--slash--subdirectory,key2=value2',
      ),
      (
          'log_directory_and_other_keys_at_end',
          {
              'log_directory': 'gs://test-bucket/directory/subdirectory',
              'key1': 'value1',
              'key2': 'value2',
          },
          'log_directory=test-bucket--slash--directory--slash--subdirectory,key1=value1,key2=value2',
      ),
      (
          'log_directory_only_with_ending_slash',
          {
              'log_directory': 'gs://test-bucket/directory/subdirectory/',
          },
          'log_directory=test-bucket--slash--directory--slash--subdirectory',
      ),
  )
  def test_format_label_string_with_bucket(self, labels, expected_string):
    """Test that the label string correctly formatted when bucket given."""
    command_instance = ConcreteCommand('test', 'Test command')

    self.assertEqual(
        command_instance._format_label_string(labels),
        expected_string,
    )

  @parameterized.named_parameters(
      dict(
          testcase_name='no_replacements',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=None,
          expected_string='key1=value1,key2=value2,key3=value3',
      ),
      dict(
          testcase_name='missed_replacements',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('5', 'five'),
          ),
          expected_string='key1=value1,key2=value2,key3=value3',
      ),
      dict(
          testcase_name='missed_replacement_superset',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('10', 'ten'),
          ),
          expected_string='key1=value1,key2=value2,key3=value3',
      ),
      dict(
          testcase_name='key_only_one_replacement_start',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('key1', 'key1_replaced'),
          ),
          expected_string='key1_replaced=value1,key2=value2,key3=value3',
      ),
      dict(
          testcase_name='key_only_one_replacement_end',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('key3', 'key3_replaced'),
          ),
          expected_string='key1=value1,key2=value2,key3_replaced=value3',
      ),
      dict(
          testcase_name='key_only_one_replacement_middle',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('key2', 'key2_replaced'),
          ),
          expected_string='key1=value1,key2_replaced=value2,key3=value3',
      ),
      dict(
          testcase_name='value_only_one_replacement',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('value2', 'value2_replaced'),
          ),
          expected_string=(
              'key1=value1,key2=value2_replaced,key3=value3'
          ),
      ),
      dict(
          testcase_name='key_and_value_one_replacement',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('key2', 'key2_replaced'),
              action.Command.Replacement('value2', 'value2_replaced'),
          ),
          expected_string=(
              'key1=value1,key2_replaced=value2_replaced,key3=value3'
          ),
      ),
      dict(
          testcase_name='multiple_replacements',
          labels={
              'key1': 'value1',
              'key2': 'value2',
              'key3': 'value3',
          },
          replacements=(
              action.Command.Replacement('2', '-two-'),
          ),
          expected_string=(
              'key1=value1,key-two-=value-two-,key3=value3'
          ),
      ),
  )
  def test_format_label_string_with_custom_replacements(
      self,
      labels,
      replacements,
      expected_string,
  ):
    """Test that the label string correctly formatted with replacements."""
    command_instance = ConcreteCommand('test', 'Test command')

    self.assertEqual(
        command_instance._format_label_string(
            labels=labels,
            replacements=replacements,
        ),
        expected_string,
    )


if __name__ == '__main__':
  parameterized.googletest.main()
