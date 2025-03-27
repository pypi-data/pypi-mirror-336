# Development

## Virtualenv settings

add the following to `postactivate`

    PHYSTOOL_DIR=/path/to/git/dir
    PHYSTOOL_SRC_DIR=$PHYSTOOL_DIR/src/phystool
    cd $PHYSTOOL_SRC_DIR
    export GIT_CLIFF_WORKDIR=$PHYSTOOL_DIR
    export QT_LOGGING_RULES="qt.pyside.libpyside.warning=true"
    alias pt="python -m phystool"

the virtualenv must contain a static folder with:

+ README.md
+ themes.gitconfig (a config list of delta themes)
+ physdb_dev (a toy db that can be copied)
