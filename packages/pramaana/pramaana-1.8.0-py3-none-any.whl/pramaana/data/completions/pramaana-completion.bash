_pramaana_complete() {
    local cur prev cmd
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmd="${COMP_WORDS[1]}"

    # List of all commands
    local commands="new edit find grep import export ls mv cp ln rm trash show open clean abs rel"

    # If we're completing the command name (first argument)
    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi

    # Get pramaana data directory from config
    local data_dir=$(python3 -c '
import json
import os
with open(os.path.expanduser("~/.pramaana/config.json")) as f:
    print(os.path.expanduser(json.load(f)["pramaana_path"]))
')

    # Get list of templates
    local templates=$(python3 -c '
import os
from pathlib import Path
templates = []
template_dir = Path(os.path.expanduser("~/.pramaana/templates"))
if template_dir.exists():
    templates.extend(f.stem for f in template_dir.glob("*.bib"))
print(" ".join(templates))
')

    # Check if we're working with template option
    if [[ "$cur" == "-"* ]]; then
        if [[ "$cur" == "--temp"* ]]; then
            COMPREPLY=( $(compgen -W "--template --template=" -- "$cur") )
            return 0
        fi
    elif [[ "$cur" == *"="* ]]; then
        local opt=${cur%%=*}
        local val=${cur#*=}
        if [ "$opt" = "--template" ]; then
            COMPREPLY=( $(compgen -W "$templates" -- "$val") )
            COMPREPLY=( "${COMPREPLY[@]/#/--template=}" )
            return 0
        fi
    elif [ "$prev" = "--template" ]; then
        COMPREPLY=( $(compgen -W "$templates" -- "$cur") )
        return 0
    fi

    # Handle command-specific completions
    case "${cmd}" in
        show)
            if [ "$prev" = "show" ] || [[ "$prev" =~ ^(-r|--recursive)$ ]]; then
                # Complete with paths from pramaana data directory
                local paths=$(cd "$data_dir" && compgen -f -- "${cur}")
                COMPREPLY=( $(printf "%s\n" "${paths}") )
            elif [[ "$cur" == -* ]]; then
                # Show command options
                COMPREPLY=( $(compgen -W "-r --recursive" -- "$cur") )
            fi
            ;;
        clean)
            if [ "$prev" = "clean" ] || [[ "$prev" =~ ^(-r|--recursive|--dry-run)$ ]]; then
                # Complete with paths from pramaana data directory
                local paths=$(cd "$data_dir" && compgen -f -- "${cur}")
                COMPREPLY=( $(printf "%s\n" "${paths}") )
            elif [[ "$cur" == -* ]]; then
                # Clean command options
                COMPREPLY=( $(compgen -W "-r --recursive --dry-run" -- "$cur") )
            fi
            ;;
        ls|rm|trash|open|edit|new|find|grep|mv|cp|ln|abs|rel)
            # Complete with paths from pramaana data directory
            local paths=$(cd "$data_dir" && compgen -f -- "${cur}")
            COMPREPLY=( $(printf "%s\n" "${paths}") )
            ;;
        import)
            if [ "$prev" = "--via" ]; then
                COMPREPLY=( $(compgen -W "ln cp mv" -- ${cur}) )
            else
                # Complete both directories and .bib files
                local files=( $(compgen -f -X '!*.bib' -- "${cur}") )
                local dirs=( $(compgen -d -- "${cur}") )
                COMPREPLY=( "${files[@]}" "${dirs[@]}" )
            fi
            ;;
        export)
            # If no args yet, complete with export names from config
            if [ $COMP_CWORD -eq 2 ]; then
                local exports=$(python3 -c '
import json
import os
with open(os.path.expanduser("~/.pramaana/config.json")) as f:
    config = json.load(f)
    print(" ".join(config["exports"].keys()))
')
                COMPREPLY=( $(compgen -W "${exports}" -- ${cur}) )
            fi
            ;;
        *)
            ;;
    esac

    return 0
}

complete -F _pramaana_complete pramaana