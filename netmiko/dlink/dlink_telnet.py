from netmiko.cisco_base_connection import CiscoSSHConnection
import re
import time

class DlinkTelnet(CiscoSSHConnection):
    def session_preparation(self):
        self._test_channel_read()
        self.set_base_prompt()
        self.enable()
        self.disable_paging()
    #     self.send_command_timing("disable cli prompting")
    #     # Clear the read buffer
        time.sleep(.3 * self.global_delay_factor)
        self.clear_buffer()

    def set_base_prompt(self, pri_prompt_terminator='user#', alt_prompt_terminator='admin#', delay_factor=1):
        delay_factor = self.select_delay_factor(delay_factor)
        self.clear_buffer()
        self.write_channel(self.RETURN)
        time.sleep(.5 * delay_factor)

        prompt = self.read_channel()
        prompt = self.normalize_linefeeds(prompt)
        # If multiple lines in the output take the last line
        prompt = prompt.split(':')[-1]
        prompt = prompt.strip()
        # Check that ends with a valid terminator character
        if not prompt in (pri_prompt_terminator, alt_prompt_terminator):
            raise ValueError("Router prompt not found: {0}".format(prompt))


        self.base_prompt = prompt

        return self.base_prompt


    def enable(self, cmd='enable admin', pattern='ssWord', re_flags=re.IGNORECASE):
        """Enter enable mode."""
        self.base_prompt = 'admin#'
        return super(DlinkTelnet, self).enable(cmd=cmd, pattern=pattern, re_flags=re_flags)

    def check_enable_mode(self, check_string='admin#'):
        """Checks whether in configuration mode. Returns a boolean."""
        return super(DlinkTelnet, self).check_config_mode(check_string=check_string)

    def exit_config_mode(self, exit_config=''):
        """No configuration mode on Extreme."""
        return ''

    def disable_paging(self, command="disable clipaging", delay_factor=1):
        return super(DlinkTelnet, self).disable_paging(command=command)

    def save_config(self, cmd='save', confirm=False):
        """Saves configuration."""
        return super(DlinkTelnet, self).save_config(cmd=cmd, confirm=confirm)