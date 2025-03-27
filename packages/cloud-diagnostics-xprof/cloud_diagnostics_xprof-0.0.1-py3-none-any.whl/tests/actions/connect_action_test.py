import argparse
from collections.abc import Sequence
from unittest import mock

from xprofiler.src.cloud_diagnostics_xprof.actions import connect_action
from xprofiler.src.cloud_diagnostics_xprof.actions import list_action

from google3.testing.pybase import parameterized


class ConnectTest(parameterized.TestCase):

  @parameterized.named_parameters(
      (
          'single_log_directory_with_zone',
          ['gs://test-log-directory/test-subdirectory'],
          'us-central1-a',
      ),
  )
  def test_get_vms_from_log_directory_verbose(
      self,
      test_log_directories: Sequence[str],
      test_zone: str | None,
  ):
    """Test that the VM names are returned correctly when verbose is True."""
    command = connect_action.Connect()
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

  @parameterized.named_parameters(
      dict(
          testcase_name='single_log_directory_with_zone',
          vm_names=['test-vm-1'],
          expected_vm_name_list=['test-vm-1'],
      ),
      dict(
          testcase_name='multiple_log_directories',
          vm_names=['test-vm-1', 'test-vm-2'],
          expected_vm_name_list=['test-vm-1', 'test-vm-2'],
      ),
  )
  def test_get_vms_from_log_directory_returns_vm_name(
      self,
      vm_names: Sequence[str],
      expected_vm_name_list: Sequence[str],
  ):
    """Test that the VM name is returned correctly."""
    command = connect_action.Connect()
    verbose = False
    test_log_directories = ['gs://test-log-directory/test-subdirectory']
    test_zone = None
    test_list_output = 'NAME\n' + '\n'.join(vm_names) + '\n'

    # Patch list_action's run() method to return a deterministic value.
    self.enter_context(
        mock.patch.object(
            list_action.List,
            'run',
            return_value=test_list_output,
        )
    )
    vm_name_list = command._get_vms_from_log_directory(
        log_directories=test_log_directories,
        zone=test_zone,
        verbose=verbose,
    )

    self.assertEqual(
        vm_name_list,
        expected_vm_name_list,
        msg='VM name should be returned correctly.',
    )

  @parameterized.named_parameters(
      dict(
          testcase_name='test_flag-log_directory',
          flag_name='--log-directory',
          flag_attributes=dict(
              metavar='GS_PATH',
              required=True,
          ),
      ),
      dict(
          testcase_name='test_flag-zone',
          flag_name='--zone',
          flag_attributes=dict(
              metavar='ZONE_NAME',
          ),
      ),
      dict(
          testcase_name='test_flag-mode',
          flag_name='--mode',
          flag_attributes=dict(
              metavar='MODE',
              choices=['ssh', 'proxy'],
              default='ssh',
          ),
      ),
      dict(
          testcase_name='test_flag-port',
          flag_name='--port',
          flag_attributes=dict(
              metavar='LOCAL_PORT',
              default='6006',
          ),
      ),
      dict(
          testcase_name='test_flag-host-port',
          flag_name='--host-port',
          flag_attributes=dict(
              metavar='HOST_PORT',
              default='6006',
          ),
      ),
      dict(
          testcase_name='test_flag-disconnect',
          flag_name='--disconnect',
          flag_attributes=dict(
              action='store_true',
          ),
      ),
      dict(
          testcase_name='test_flag-verbose',
          flag_name='--verbose',
          flag_attributes=dict(
              action='store_true',
          ),
      ),
  )
  def test_flags_for_subparser_was_added(self, flag_name, flag_attributes):
    """Test that the subparser flags are added correctly."""
    mock_subparser = mock.Mock(spec=argparse._SubParsersAction)
    mock_parser = mock.Mock(spec=argparse.ArgumentParser)
    mock_subparser.add_parser.return_value = mock_parser
    instance_of_class = connect_action.Connect()

    instance_of_class.add_subcommand(mock_subparser)

    # Arguments were added to mock_parser using mock_parser.add_argument.
    argument_calls = mock_parser.add_argument.call_args_list

    # Check that the flag was added and correct settings are used.
    found_flag = False
    for call in argument_calls:
      args, kwargs = call
      if flag_name in args:
        found_flag = True
        for arg, value in flag_attributes.items():
          self.assertEqual(kwargs.get(arg), value)
        break
    # Assert that the flag was actually found.
    if not found_flag:
      self.fail(f'No {flag_name} argument found')

  def test_no_vm_name_found_from_log_directory(self):
    command = connect_action.Connect()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone=None,
        mode='ssh',
        port='6006',
        host_port='6006',
        disconnect=False,
        verbose=False,
    )
    # Mocked to be output of list_action.List's run() method.
    vm_names_string = 'NAME\n'

    # Patch the list_action.List() to return a deterministic value.
    with mock.patch.object(
        list_action.List,
        'run',
        return_value=vm_names_string,
    ):
      with self.assertRaises(ValueError):
        command._build_command(args)

  def test_build_command_no_log_directory(self):
    """Test that an error is raised when no log directory is specified."""
    command = connect_action.Connect()
    args = argparse.Namespace(
        log_directory=None,
        zone=None,
        mode='ssh',
        port='6006',
        host_port='6006',
        disconnect=False,
        verbose=False,
    )

    with self.assertRaises(ValueError):
      command._build_command(args)

  @parameterized.named_parameters(
      dict(
          testcase_name='test_mode-ssh',
          test_mode='ssh',
      ),
      dict(
          testcase_name='test_mode-proxy',
          test_mode='proxy',
      ),
  )
  def test_build_command_no_zone(self, test_mode):
    """Test that the command is built correctly when no zone is specified."""
    command = connect_action.Connect()
    test_log_directory = 'gs://test-bucket/test-directory/test-subdirectory'
    args = argparse.Namespace(
        log_directory=test_log_directory,
        zone=None,
        mode=test_mode,
        port='6006',
        host_port='6006',
        disconnect=False,
        verbose=False,
    )
    # Mocked to be output of list_action.List's run() method.
    vm_names_string = (
        'NAME\n'
        'test-vm-1\n'
    )

    # Patch the list_action.List() to return a deterministic value.
    # Use enter_context() to ensure the patch is cleaned up after the test.
    self.enter_context(
        mock.patch.object(
            list_action.List,
            'run',
            return_value=vm_names_string,
        )
    )
    command_list = command._build_command(args)

    expected_command = [
        command.GCLOUD_COMMAND,
        'compute',
        'ssh',
        'test-vm-1',
        (
            '--ssh-flag=-f -N -M -S /tmp/ssh_mux_socket_test-vm-1'
            ' -L 6006:localhost:6006'
        ),
    ]
    self.assertEqual(
        command_list,
        expected_command,
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      dict(
          testcase_name='test_mode-ssh',
          test_mode='ssh',
      ),
      dict(
          testcase_name='test_mode-proxy',
          test_mode='proxy',
      ),
  )
  def test_build_command_zone_specified(self, test_mode):
    """Test that the command is built correctly when a zone is specified."""
    command = connect_action.Connect()
    test_log_directory = 'gs://test-bucket/test-directory/test-subdirectory'
    args = argparse.Namespace(
        log_directory=test_log_directory,
        zone='us-central1-a',
        mode=test_mode,
        port='6006',
        host_port='6006',
        disconnect=False,
        verbose=False,
    )
    vm_names_string = (
        'NAME\n'
        'test-vm-1\n'
    )

    # Patch the list_action.List() to return a deterministic value.
    # Use enter_context() to ensure the patch is cleaned up after the test.
    self.enter_context(
        mock.patch.object(
            list_action.List,
            'run',
            return_value=vm_names_string,
        )
    )
    command_list = command._build_command(args)

    expected_command = [
        command.GCLOUD_COMMAND,
        'compute',
        'ssh',
        'test-vm-1',
        (
            '--ssh-flag=-f -N -M -S /tmp/ssh_mux_socket_test-vm-1'
            ' -L 6006:localhost:6006'
        ),
        '--zone=us-central1-a',
    ]
    self.assertEqual(
        command_list,
        expected_command,
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_build_command_extra_args(self):
    """Test that command is built correctly when extra args are specified."""
    command = connect_action.Connect()
    test_log_directory = 'gs://test-bucket/test-directory/test-subdirectory'
    args = argparse.Namespace(
        log_directory=test_log_directory,
        zone='us-central1-a',
        mode='ssh',
        port='6006',
        host_port='6006',
        disconnect=False,
        verbose=False,
    )
    vm_names_string = (
        'NAME\n'
        'test-vm-1\n'
    )
    extra_args = {'--project': 'test-project'}

    # Patch the list_action.List() to return a deterministic value.
    # Use enter_context() to ensure the patch is cleaned up after the test.
    self.enter_context(
        mock.patch.object(
            list_action.List,
            'run',
            return_value=vm_names_string,
        )
    )
    command_list = command._build_command(args, extra_args=extra_args)

    expected_command = [
        command.GCLOUD_COMMAND,
        'compute',
        'ssh',
        'test-vm-1',
        (
            '--ssh-flag=-f -N -M -S /tmp/ssh_mux_socket_test-vm-1'
            ' -L 6006:localhost:6006'
        ),
        '--zone=us-central1-a',
        '--project=test-project',
    ]
    self.assertEqual(
        command_list,
        expected_command,
        msg='Command should be built correctly. Check items and their order.',
    )

  @parameterized.named_parameters(
      dict(
          testcase_name='test_ssh_disconnect',
          test_mode='ssh',
          test_disconnect=True,
      ),
  )
  def test_build_command_disconnect(self, test_mode, test_disconnect):
    """Test that the command is built correctly when disconnect is specified."""
    command = connect_action.Connect()
    test_log_directory = 'gs://test-bucket/test-directory/test-subdirectory'
    args = argparse.Namespace(
        log_directory=test_log_directory,
        zone='us-central1-a',
        mode=test_mode,
        port='6006',
        host_port='6006',
        disconnect=test_disconnect,
        verbose=False,
    )
    vm_names_string = (
        'NAME\n'
        'test-vm-1\n'
    )

    self.enter_context(
        mock.patch.object(
            list_action.List,
            'run',
            return_value=vm_names_string,
        )
    )
    command_list = command._build_command(args)

    expected_command = [
        command.GCLOUD_COMMAND,
        'compute',
        'ssh',
        'test-vm-1',
        '--ssh-flag=-o ControlPath=/tmp/ssh_mux_socket_test-vm-1 -O exit',
        '--zone=us-central1-a',
    ]
    self.assertEqual(
        command_list,
        expected_command,
        msg='Command should be built correctly. Check items and their order.',
    )

  def test_run_command(
      self,
  ):
    """Test that a simple command is run."""
    command = connect_action.Connect()
    diag_stdout = command._run_command(['echo', 'test'])

    self.assertEqual(diag_stdout, 'test\n')

  def test_initial_ssh_add_keys(self):
    """Test that the SSH keys are added to the VM."""
    command = connect_action.Connect()
    # Mock the _run_command() method to return a deterministic value.
    with mock.patch.object(
        command,
        '_run_command',
        return_value='test',
    ) as mock_run_command:
      stdout = command._initial_ssh_add_keys()

    mock_run_command.assert_called_once_with(
        [
            'gcloud',
            'compute',
            'os-login',
            'ssh-keys',
            'add',
            '--key',
            '$(ssh-add -L | grep publickey)',
        ],
    )

  def test_run_printout_for_disconnect(self):
    """Test that the correct printout is made when disconnect is specified."""
    command = connect_action.Connect()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone=None,
        mode='ssh',
        port='6006',
        host_port='6006',
        disconnect=True,
        verbose=False,
    )
    vm_names_string = (
        'NAME\n'
        'test-vm\n'
    )

    # Patch the list_action.List() to return a deterministic value.
    with mock.patch.object(
        list_action.List,
        'run',
        return_value=vm_names_string,
    ):
      with mock.patch.object(
          command,
          '_run_command',
          return_value='test',
      ) as mock_run_command:
        command.run(args)

    mock_run_command.assert_called_once_with(
        [
            'gcloud',
            'compute',
            'ssh',
            'test-vm',
            '--ssh-flag=-o ControlPath=/tmp/ssh_mux_socket_test-vm -O exit',
        ],
        verbose=False,
    )

  def test_run_with_initial_ssh_add_keys(self):
    """Test that the SSH keys are added to the VM."""
    command = connect_action.Connect()
    args = argparse.Namespace(
        log_directory='gs://test-bucket/test-directory/test-subdirectory',
        zone=None,
        mode='ssh',
        port='6006',
        host_port='6006',
        disconnect=False,
        verbose=False,
    )
    vm_names_string = (
        'NAME\n'
        'test-vm\n'
    )

    # Patch the method calls for shell commands to return a deterministic value.
    with mock.patch.object(
        list_action.List,
        'run',
        return_value=vm_names_string,
    ):
      # Patch the method to return a deterministic value.
      with mock.patch.object(
          command,
          '_initial_ssh_add_keys',
          return_value='test',
      ) :
        with mock.patch.object(
            command,
            '_run_command',
            return_value='test',
        ):
          stdout = command.run(args)

    self.assertEqual(stdout, 'test')


if __name__ == '__main__':
  parameterized.googletest.main()
