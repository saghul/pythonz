
from pythonz.commands import Command, command_map
from pythonz.log import logger


class HelpCommand(Command):
    name = "help"
    usage = "%prog [COMMAND]"
    summary = "Show available commands"

    def run_command(self, options, args):
        if args:
            command = args[0]
            if command not in command_map:
                self.parser.error("Unknown command: `%s`" % command)
                return
            command = command_map[command]
            command.parser.print_help()
            return
        self.parser.print_help()
        logger.log("\nCommands available:")
        commands = [command_map[key] for key in sorted(command_map.keys())]
        for command in commands:
            logger.log("  %s: %s" % (command.name, command.summary))
        logger.log("\nFurther Instructions:")
        logger.log("  https://github.com/saghul/pythonz")

HelpCommand()

