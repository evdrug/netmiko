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

    def set_base_prompt(self, pri_prompt_terminator='#',
                        alt_prompt_terminator='#', delay_factor=1):

        fPrompt = self.find_prompt(delay_factor=delay_factor)
        prompt = fPrompt.split(':')
        if not prompt[-1] in ('user#', 'admin#', '3#', '4#', '5#'):
            raise ValueError("Router prompt not found: {0}".format(repr(prompt)))
        # Strip off trailing terminator
        self.base_prompt = prompt[0]

        return self.base_prompt

    def check_enable_mode(self, check_string=''):

        self.write_channel(self.RETURN)
        output = self.read_until_prompt()
        pattern = re.compile("(admin#|4#|5#)")

        return pattern.search(output) is not None

    def enable(self, cmd='enable admin', pattern=r'ss[Ww]ord', re_flags=re.IGNORECASE):

        return super(DlinkTelnet, self).enable(cmd=cmd, pattern=pattern, re_flags=re_flags)

    def disable_paging(self, command="disable clipaging", delay_factor=1):
        return super(DlinkTelnet, self).disable_paging(command=command)

    def telnet_login(self, pri_prompt_terminator=r'#\s*$', alt_prompt_terminator=r'>\s*$',
                         username_pattern=r"(?:user:|username|login|user name)",
                         pwd_pattern=r"assword",
                         delay_factor=3, max_loops=20):
        return super(DlinkTelnet, self).telnet_login( pri_prompt_terminator, alt_prompt_terminator,
                         username_pattern, pwd_pattern, delay_factor, max_loops)