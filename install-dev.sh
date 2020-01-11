#!/usr/bin/env sh


_projectAbspath="$(dirname "$(readlink -f "$0")")"
_venvDirname="venv"
_venvDirAbspath="$_projectAbspath/$_venvDirname"


[ -d "$_venvDirAbspath" ] || python3 -m venv "$_venvDirAbspath"


__isVenv()
{
    python -c "import os; exit(0) if os.environ.get('VIRTUAL_ENV') == '$_venvDirAbspath' else exit(1)"

    return $?
}


__activateVenv()
{
    # shellcheck disable=SC1090
    . "$_venvDirAbspath/bin/activate"
}


__install()
{
    if ! __isVenv ; then
        __activateVenv
        if ! __isVenv ; then
            printf %s\\n "Failed to detect / activate virtualenv, exiting."
            return 1
        fi
    fi

    if pip list | grep clapps ; then
        pip uninstall -y clapps
    fi

    # Install package locally from source in "editable mode".
    pip install -e "$_projectAbspath"

    return $?
}


__install
