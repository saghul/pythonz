declare -A _pythonz_context

_pythonz_complete(){
    local option command commands type types types_regex command_option
    local available_versions installed_versions unique_versions installed_regex known_versions
    local logfile

    COMPREPLY=()

    types="cpython stackless pypy pypy3 jython"
    commands="cleanup help install list locate uninstall update version"

    if [ $COMP_CWORD -eq 1 ]; then
      _pythonz_context["pythonz"]="-h"
      _pythonz_compreply $commands ${_pythonz_context["pythonz"]}
    elif [ $COMP_CWORD -eq 2 ]; then
      _pythonz_context["type"]="cpython"
      _pythonz_context["install"]="-t -f -v -h --run-tests --framework --universal --shared --file --url --reinstall -C --configure"
      _pythonz_context["uninstall"]="-t -h"
      _pythonz_context["cleanup"]="-a -h"
      _pythonz_context["list"]="-a -h"
      _pythonz_context["locate"]="-t -h"
      _pythonz_context["update"]="--dev -h"
      _pythonz_context["version"]="-h"
      command=${COMP_WORDS[COMP_CWORD-1]}
      _pythonz_handle_command $command
    elif [ $COMP_CWORD -ge 3 ]; then
      command=${COMP_WORDS[1]}
      command_option=${COMP_WORDS[COMP_CWORD-1]}
      _pythonz_handle_command_option $command_option
    fi
    return 0
  }

_pythonz_handle_command(){
  command=$*

  case "$command" in

    help|-h)
      commands=$( echo $commands | sed -e "s/help\|-h//g" )
      _pythonz_compreply $commands
      ;;
    install)
      _pythonz_install
      ;;
    uninstall)
      _pythonz_uninstall
      ;;
    locate)
      _pythonz_locate
      ;;
    list|cleanup|update|version)
      _pythonz_compreply  ${_pythonz_context["$command"]}
      ;;
    *)
      ;;
  esac
}

_pythonz_handle_command_option(){
  option=$1

  case "$option" in
    -h)
      ;;
    -t)
      _pythonz_update_command_options
      _pythonz_compreply $types
      ;;
    cpython|stackless|pypy|pypy3|jython)
      _pythonz_context["type"]=$option
      _pythonz_handle_command $command
      ;;
    --file)
      _pythonz_update_command_options
      _pythonz_handle_file
      ;;
    --url)
      _pythonz_update_command_options
      _pythonz_handle_url
      ;;
    *)
      _pythonz_update_command_options
      _pythonz_handle_command $command
      ;;
  esac
}

_pythonz_handle_file(){
  COMPREPLY=( $(compgen -f -- ${COMP_WORDS[COMP_CWORD]} ) )
  compopt -o plusdirs
}

_pythonz_handle_url(){
  COMPREPLY=( $(compgen -W "http:// https:// file:// ftp://" -- ${COMP_WORDS[COMP_CWORD]} ) )
  compopt -o nospace
}

_pythonz_update_command_options(){
  if [[ $option == -* ]];then
    _pythonz_context["$command"]=$( echo ${_pythonz_context["$command"]} |sed -e "s/ /\n/g" |sed -e "s/^$option/ /" )
  fi
}

_pythonz_install(){
  _pythonz_available_versions
  _pythonz_compreply ${_pythonz_context["install"]} $available_versions
}

_pythonz_uninstall(){
  _pythonz_installed_versions
  _pythonz_compreply ${_pythonz_context["uninstall"]} $installed_versions
}

_pythonz_locate(){
  _pythonz_installed_versions
  _pythonz_compreply ${_pythonz_context["locate"]} $installed_versions
}

_pythonz_available_versions(){
    _pythonz_installed_regex
    _pythonz_known_versions

    if [ -n "$installed_regex" ];then
        available_versions=$( echo $known_versions | sed -e "s/$installed_regex/ /g" )
    else
        available_versions=$known_versions
    fi

}

_pythonz_installed_versions(){
    type=${_pythonz_context["type"]}
    if [ -n "$type" ]; then
      installed_versions=$( pythonz list |egrep -i $type | awk '{print tolower($0)}' | sed -e "s/^.*$type-//g" )
    fi
}

_pythonz_installed_regex(){
    _pythonz_installed_versions

    installed_regex=""
    if [ -n "$installed_versions" ];then
        unique_versions=$( echo $installed_versions | sed -e 's/ /\n/g'| sed -e 's/\(.*\)/ \1 /g' )
        installed_regex=$( echo $unique_versions |sed -e "s/ /|/g" -e "s/|$//" -e "s/|/ \\\| /g" -e "s/^/ /" -e "s/$/ /") 
    fi
}

_pythonz_known_versions(){
    type=${_pythonz_context["type"]}
    if [ -n "$type" ]; then
      known_versions=$( pythonz list -a |sed -n -e "/$type/,/#.*:/p" |sed  -e "/#.*:/d" |awk '{print $1}' )
    fi

}

_pythonz_compreply(){
    COMPREPLY=( $( compgen -W "$*" -- ${COMP_WORDS[COMP_CWORD]}) )
}

complete -F _pythonz_complete pythonz
