FORBIDDEN_COMMANDS = [
    "rm -rf",
    "shutdown",
    "reboot",
    "sudo",
    "mkfs",
]

class CommandGuard:

    def validate(self, command):

        for forbidden in FORBIDDEN_COMMANDS:

            if forbidden in command:
                return False

        return True

command_guard = CommandGuard()