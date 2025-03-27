import argparse
from unittest import mock

from xprofiler.src.cloud_diagnostics_xprof.actions import capture_action

from google3.testing.pybase import parameterized


class CaptureTest(parameterized.TestCase):

  def test_subparser_was_added(self):
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = capture_action.Capture()

    instance_of_class.add_subcommand(mock_subparser)

    mock_subparser.add_parser.assert_called_once_with(
        name='capture',
        help='Capture a profile from a hosted TensorBoard instance.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

  def test_build_command_one_host(self):
    """Test that the command is built correctly when one host is specified."""
    command = capture_action.Capture()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone='us-central1-a',
        hosts=['test-vm-1'],
        host='test-vm-1',
        experiment_name='test-experiment',
        run_name='test-run',
        port='6006',
        duration='2000',
        profile_script='python3 dummy_script.py --flag0 --flag1 value1',
    )

    command_list = command._build_command(args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'tpus',
            'tpu-vm',
            'ssh',
            'test-vm-1',
            '--zone',
            'us-central1-a',
            '--worker=all',
            '--command',
            'python3 dummy_script.py --flag0 --flag1 value1',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      dict(
          testcase_name='single_host',
          hosts=['test-vm-1'],
          host='test-vm-1',
      ),
      dict(
          testcase_name='multiple_hosts',
          hosts=['test-vm-1', 'test-vm-2'],
          host='test-vm-1',
      ),
      dict(
          testcase_name='specified_host_not_in_host_list',
          hosts=['test-vm-1', 'test-vm-2'],
          host='new-test-vm-100',
      ),
      dict(
          testcase_name='no_hosts',
          hosts=[],
          host='test-vm',
      ),
  )
  def test_build_command_uses_host_specified(self, hosts, host):
    """Test that the command is built correctly when one host is specified."""
    command = capture_action.Capture()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone='us-central1-a',
        hosts=hosts,
        host=host,
        experiment_name='test-experiment',
        run_name='test-run',
        port='6006',
        duration='2000',
        profile_script='python3 dummy_script.py --flag0 --flag1 value1',
    )

    command_list = command._build_command(args)

    self.assertEqual(
        command_list,
        [
            command.GCLOUD_COMMAND,
            'compute',
            'tpus',
            'tpu-vm',
            'ssh',
            host,
            '--zone',
            'us-central1-a',
            '--worker=all',
            '--command',
            'python3 dummy_script.py --flag0 --flag1 value1',
        ],
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_run_single_host_pytorch(self):
    """Test that the command is run correctly when one host is specified."""
    command = capture_action.Capture()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone='us-central1-a',
        hosts=['test-vm-1'],
        experiment_name='test-experiment',
        run_name='test-run',
        port='6006',
        duration='2000',
        framework='pytorch',
    )
    with mock.patch.object(
        command,
        '_run_command',
        return_value='fake_output;',
    ):
      stdout = command.run(args)

    # Two outputs (one for uploading the script and one for running the script)
    self.assertEqual(
        stdout,
        'fake_output;fake_output;',
        msg='Command should be run correctly.',
    )

  def test_run_single_host_jax(self):
    """Test that the command is run correctly when one host is specified."""
    command = capture_action.Capture()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone='us-central1-a',
        hosts=['test-vm-1'],
        experiment_name='test-experiment',
        run_name='test-run',
        port='6006',
        duration='2000',
        framework='jax',
    )
    with mock.patch.object(
        command,
        '_run_command',
        return_value='fake_output;',
    ):
      stdout = command.run(args)

    # Two outputs (one for uploading the script and one for running the script)
    self.assertEqual(
        stdout,
        'fake_output;',
        msg='Command should be run correctly.',
    )

  def test_run_multiple_hosts_pytorch(self):
    """Test that the command is run correctly when multiple hosts are specified."""
    command = capture_action.Capture()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone='us-central1-a',
        hosts=['test-vm-1', 'test-vm-2'],
        experiment_name='test-experiment',
        run_name='test-run',
        port='6006',
        duration='2000',
        verbose=False,
        framework='pytorch',
    )

    with mock.patch.object(
        command,
        '_run_command',
        # return_value='fake_output;',
        side_effect=[
            'fake_output-upload-1;fake_output-profile-1;\n',
            'fake_output-upload-2;fake_output-profile-2;',
        ],
    ):
      stdout = command.run(args).strip()

    self.assertEqual(
        stdout,
        (
            'fake_output-upload-1;fake_output-profile-1;\n'
            'fake_output-upload-2;fake_output-profile-2;'
        ),
        msg='Command should be run correctly.',
    )


def test_run_multiple_hosts_with_error(self):
    command = capture_action.Capture()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone='us-central1-a',
        hosts=['test-vm-1', 'test-vm-2'],
        experiment_name='test-experiment',
        run_name='test-run',
        port='6006',
        duration='2000',
        verbose=False,
    )

    # First host succeeds, second host fails.
    with mock.patch.object(
        command,
        '_run_command',
        side_effect=[
            'fake_output-upload-1;fake_output-profile-1;\n',
            'fake_output-upload-2;fake_output-profile-2;\n',
        ],
    ):
      with self.assertRaises(RuntimeError):
        command.run(args)

if __name__ == '__main__':
  parameterized.googletest.main()
