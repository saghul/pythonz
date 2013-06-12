# settings
if [ -z "$PYTHONZ_ROOT" ]
  set PYTHONZ_ROOT "$HOME/.pythonz"
end

if [ -z "$PYTHONZ_HOME" ]
  set PYTHONZ_HOME "$HOME/.pythonz"
end

# functions
function __pythonz_set_path
  if not contains "$PYTHONZ_ROOT/bin" $PATH
    set PATH "$PYTHONZ_ROOT/bin" $PATH
  end
end

function __pythonz_reload
  if [ -s "$PYTHONZ_ROOT/etc/pythonz.fish" ]
    . "$PYTHONZ_ROOT/etc/pythonz.fish"
  end
end

function __pythonz_update
  command pythonz $argv
  if [ $status = 0 ]
    __pythonz_reload
  end
end

function __pythonz_find_command
  for arg in $argv
    switch $arg
      case '-*'
        continue
      case '*'
        echo $arg
        return
    end
  end
end

function pythonz
  set -l command_name (__pythonz_find_command $argv)
  switch "$command_name"
    case update
      __pythonz_update $argv
    case '*'
      command pythonz $argv
  end
end

# main
__pythonz_set_path
