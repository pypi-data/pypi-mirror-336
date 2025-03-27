"""Parameterized tests for list subclass of action.Command.

Tests that `xprofiler list ...` is working as expected.
"""

import argparse
from collections.abc import Mapping, Sequence
from unittest import mock

from xprofiler.src.cloud_diagnostics_xprof.actions import list_action

from google3.testing.pybase import parameterized

# Define valid test parameters for delete command.
_LIST_OPTIONS: frozenset[tuple[str, frozenset[tuple[str, str]]]] = frozenset([
    # --zone is optional
    (
        '--zone',
        frozenset([
            ('metavar', 'ZONE_NAME'),
        ]),
    ),
    # --filter is optional
    (
        '--filter',
        frozenset([
            ('metavar', 'FILTER_NAME'),
            ('nargs', '+'),
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


class ListTest(parameterized.TestCase):

  def test_subparser_was_added(self):
    """Test that the parser is added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = list_action.List()

    instance_of_class.add_subcommand(mock_subparser)

    mock_subparser.add_parser.assert_called_once_with(
        name='list',
        help='List all hosted TensorBoard instances.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

  @parameterized.named_parameters(
      (flag_name, flag_name, flag_options)
      for flag_name, flag_options in _LIST_OPTIONS
  )
  def test_flags_for_subparser_was_added(self, flag_name, flag_options):
    """Test that the subparser flags are added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = list_action.List()

    instance_of_class.add_subcommand(mock_subparser)

    # Arguments were added to mock_parser using mock_parser.add_argument.
    argument_calls = mock_parser.add_argument.call_args_list

    # Check that the flag was added and correct settings are used.
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

  def test_build_command_no_zone_no_filter(self):
    """Test that the command is built correctly when no zone is specified.

    This assumes the parser is passing in the correct arguments (even if they
    are not provided by the user). This does not test the situation of where
    the _build_command() is called directly (and therefore some args attributes
    are missing).
    """
    command = list_action.List()
    # Note this assumes the parser is passing in the correct arguments for
    # _build_command(). If _build_command() is called directly, functionality is
    # not guaranteed.
    # Use the default values (no flags passed by user).
    args = argparse.Namespace(
        zone=None,
        log_directory=None,
        filter=None,
        verbose=False,
    )

    # Patch _format_filter_string() to return a deterministic value.
    test_deterministic_label_string = 'filter_key=test-filter-string'
    with mock.patch.object(
        command,
        '_format_filter_string',
        return_value=test_deterministic_label_string,
    ):
      command_list = command._build_command(args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'list',
            f'--filter={test_deterministic_label_string}',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_build_command_zone_specified(self):
    """Test that the command is built correctly when zone is specified."""
    command = list_action.List()
    # Note this assumes the parser is passing in the correct arguments for
    # _build_command(). If _build_command() is called directly, functionality is
    # not guaranteed.
    # Use the default values (no flags passed by user).
    test_zone = 'us-central1-a'
    args = argparse.Namespace(
        zone=test_zone,
        log_directory=None,
        filter=None,
        verbose=False,
    )

    # Patch _format_filter_string() to return a deterministic value.
    test_deterministic_label_string = 'filter_key=test-filter-string'
    with mock.patch.object(
        command,
        '_format_filter_string',
        return_value=test_deterministic_label_string,
    ):
      command_list = command._build_command(args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'list',
            f'--zones={test_zone}',
            f'--filter={test_deterministic_label_string}',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      (
          'single_filter',
          {
              'filter_key': [
                  'test-filter-string',
              ],
          },
      ),
      (
          'multiple_filters_2_keys',
          {
              'filter_key': [
                  'test-filter-string',
              ],
              'filter_key2': [
                  'test-filter-string2',
              ],
          },
      ),
      (
          'multiple_filters_2_keys_with_same_value',
          {
              'filter_key': [
                  'test-filter-string',
              ],
              'filter_key2': [
                  'test-filter-string',
              ],
          },
      ),
      (
          'multiple_filters_3_keys',
          {
              'filter_key': [
                  'test-filter-string',
              ],
              'filter_key2': [
                  'test-filter-string2',
              ],
              'filter_key3': [
                  'test-filter-string3',
              ],
          },
      ),
      (
          'multiple_values_for_same_key',
          {
              'filter_key': [
                  'test-filter-string',
                  'test-filter-string2',
              ],
          },
      ),
      (
          'multiple_values_for_same_key_and_different_key',
          {
              'filter_key': [
                  'test-filter-string',
                  'test-filter-string2',
              ],
              'filter_key2': [
                  'test-filter-string3',
              ],
          },
      ),
      (
          'multiple_values_for_same_key_and_different_keys_with_same_values',
          {
              'filter_key': [
                  'test-filter-string',
                  'test-filter-string2',
              ],
              'filter_key2': [
                  'test-filter-string2',
              ],
              'filter_key3': [
                  'test-filter-string',
              ],
          },
      ),
  )
  def test_build_command_filter_specified_with_log_directory(
      self,
      test_filter: Mapping[str, Sequence[str]],
  ):
    """Test that the command is built correctly when filter is specified."""
    command = list_action.List()
    test_log_directory = 'gs://test-log-directory/test-subdirectory'
    # Set up the filter list as expected by the parser.
    test_filter_list = []
    for key, values_list in test_filter.items():
      for value in values_list:
        test_filter_list.append(f'{key}={value}')
    # Note this assumes the parser is passing in the correct arguments for
    # _build_command(). If _build_command() is called directly, functionality is
    # not guaranteed.
    args = argparse.Namespace(
        zone=None,
        log_directory=[test_log_directory],
        filter=test_filter_list,
        verbose=False,
    )

    command_list = command._build_command(args)

    # Log directory at filter string's end; doesn't override other filters.
    test_filter |= {
        'labels.log_directory': [
            # Using internal method to format string with replacements.
            command._format_string_with_replacements(
                original_string=test_log_directory,
                replacements=command._DEFAULT_STRING_REPLACEMENTS,
            ),
        ],
    }
    # Note that the filter string is formatted by _format_filter_string().
    expected_filter_string = command._format_filter_string(test_filter)
    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'list',
            f'--filter={expected_filter_string}',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      (
          'single_log_directory-single_filter',
          ['gs://test-log-directory/test-subdirectory'],
          dict(
              filter_key=[
                  'test-filter-string',
              ],
          ),
          (
              '--filter=(filter_key~"test-filter-string") AND'
              ' (labels.log_directory~"test-log-directory--slash--test-subdirectory")'
          ),
      ),
      (
          'single_log_directory-multiple_filters_2_keys',
          ['gs://test-log-directory/test-subdirectory'],
          dict(
              filter_key=[
                  'test-filter-string',
              ],
              filter_key2=[
                  'test-filter-string2',
              ],
          ),
          (
              '--filter=(filter_key~"test-filter-string") AND '
              '(filter_key2~"test-filter-string2") AND '
              '(labels.log_directory~"test-log-directory--slash--test-subdirectory")'
          ),
      ),
      (
          'single_log_directory-multiple_values_for_same_key',
          ['gs://test-log-directory/test-subdirectory'],
          dict(
              filter_key=[
                  'test-filter-string2',
              ],
          ),
          (
              '--filter=(filter_key~"test-filter-string2") AND '
              '(labels.log_directory~"test-log-directory--slash--test-subdirectory")'
          ),
      ),
      (
          'single_log_directory-multiple_values_for_same_key_and_different_key',
          ['gs://test-log-directory/test-subdirectory'],
          dict(
              filter_key=[
                  'test-filter-string2',
              ],
              filter_key2=[
                  'test-filter-string3',
              ],
          ),
          (
              '--filter=(filter_key~"test-filter-string2") AND '
              '(filter_key2~"test-filter-string3") AND '
              '(labels.log_directory~"test-log-directory--slash--test-subdirectory")'
          ),
      ),
      (
          'multiple_log_directories',
          [
              'gs://test-log-directory/test-subdirectory0',
              'gs://test-log-directory2/test-subdirectory1',
              'gs://test-log-directory3/test-subdirectory2',
          ],
          dict(
              filter_key=[
                  'test-filter-string',
              ],
          ),
          (
              '--filter=(filter_key~"test-filter-string") AND '
              '(labels.log_directory~"test-log-directory--slash--test-subdirectory0"'
              ' OR '
              'labels.log_directory~"test-log-directory2--slash--test-subdirectory1"'
              ' OR '
              'labels.log_directory~"test-log-directory3--slash--test-subdirectory2")'
          ),
      ),
      (
          'multiple_log_directories_with_repeats',
          [
              'gs://test-log-directory/test-subdirectory0',
              'gs://test-log-directory2/test-subdirectory0',
              'gs://test-log-directory2/test-subdirectory1',
          ],
          dict(
              filter_key=[
                  'test-filter-string',
              ],
          ),
          (
              '--filter=(filter_key~"test-filter-string") AND '
              '(labels.log_directory~"test-log-directory--slash--test-subdirectory0"'
              ' OR '
              'labels.log_directory~"test-log-directory2--slash--test-subdirectory0"'
              ' OR '
              'labels.log_directory~"test-log-directory2--slash--test-subdirectory1")'
          ),
      ),
  )
  def test_build_command_filter_specified_with_multiple_log_directories(
      self,
      test_log_directories: Sequence[str],
      test_filter: Mapping[str, Sequence[str]],
      expected_filter_string: str,
  ):
    """Test that the command is built correctly when filter is specified."""
    command = list_action.List()
    # Set up the filter list as expected by the parser.
    test_filter_list = []
    for key, values_list in test_filter.items():
      for value in values_list:
        test_filter_list.append(f'{key}={value}')
    # Note this assumes the parser is passing in the correct arguments for
    # _build_command(). If _build_command() is called directly, functionality is
    # not guaranteed.
    args = argparse.Namespace(
        zone=None,
        log_directory=test_log_directories,
        filter=test_filter_list,
        verbose=False,
    )

    command_list = command._build_command(args)

    # Log directory at filter string's end; doesn't override other filters.
    test_filter |= {
        'labels.log_directory': [
            # Using internal method to format string with replacements.
            command._format_string_with_replacements(
                original_string=test_log_directory,
                replacements=command._DEFAULT_STRING_REPLACEMENTS,
            )
            for test_log_directory in test_log_directories
        ],
    }
    # Note that the filter string is formatted by _format_filter_string().
    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'list',
            expected_filter_string,
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      (
          'single_filter',
          {
              'filter_key': [
                  'test-filter-string',
              ],
          },
      ),
      (
          'multiple_filters_2_keys',
          {
              'filter_key': [
                  'test-filter-string',
              ],
              'filter_key2': [
                  'test-filter-string2',
              ],
          },
      ),
      (
          'multiple_filters_2_keys_with_same_value',
          {
              'filter_key': [
                  'test-filter-string',
              ],
              'filter_key2': [
                  'test-filter-string',
              ],
          },
      ),
      (
          'multiple_filters_3_keys',
          {
              'filter_key': [
                  'test-filter-string',
              ],
              'filter_key2': [
                  'test-filter-string2',
              ],
              'filter_key3': [
                  'test-filter-string3',
              ],
          },
      ),
      (
          'multiple_values_for_same_key',
          {
              'filter_key': [
                  'test-filter-string',
                  'test-filter-string2',
              ],
          },
      ),
      (
          'multiple_values_for_same_key_and_different_key',
          {
              'filter_key': [
                  'test-filter-string',
                  'test-filter-string2',
              ],
              'filter_key2': [
                  'test-filter-string3',
              ],
          },
      ),
      (
          'multiple_values_for_same_key_and_different_keys_with_same_values',
          {
              'filter_key': [
                  'test-filter-string',
                  'test-filter-string2',
              ],
              'filter_key2': [
                  'test-filter-string2',
              ],
              'filter_key3': [
                  'test-filter-string',
              ],
          },
      ),
  )
  def test_build_command_filter_specified_no_log_directory(
      self,
      test_filter: Mapping[str, Sequence[str]],
  ):
    """Test that the command is built correctly when filter is specified."""
    command = list_action.List()
    # Set up the filter list as expected by the parser.
    test_filter_list = []
    for key, values_list in test_filter.items():
      for value in values_list:
        test_filter_list.append(f'{key}={value}')
    # Note this assumes the parser is passing in the correct arguments for
    # _build_command(). If _build_command() is called directly, functionality is
    # not guaranteed.
    args = argparse.Namespace(
        zone=None,
        log_directory=None,
        filter=test_filter_list,
        verbose=False,
    )

    command_list = command._build_command(args)

    # Note that the filter string is formatted by _format_filter_string().
    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'list',
            f'--filter={command._format_filter_string(test_filter)}',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_build_command_extra_args(self):
    """Test that the command is built correctly when extra args are provided."""
    command = list_action.List()
    args = argparse.Namespace(
        zone=None,
        log_directory=None,
        filter=None,
        verbose=False,
    )
    extra_args = {'--project': 'test-project'}

    # Patch _format_filter_string() to return a deterministic value.
    test_deterministic_label_string = 'filter_key=test-filter-string'
    with mock.patch.object(
        command,
        '_format_filter_string',
        return_value=test_deterministic_label_string,
    ):
      command_list = command._build_command(args, extra_args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'instances',
            'list',
            f'--filter={test_deterministic_label_string}',
            '--project=test-project',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )


if __name__ == '__main__':
  parameterized.googletest.main()
