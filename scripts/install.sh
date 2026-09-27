#!/bin/sh

set -eu

usage() {
    printf '%s\n' \
        'Usage: install.sh [--force] <book-folder>' \
        '       install.sh [--force] --global' \
        '       install.sh [--force] -- <book-folder>' >&2
}

die() {
    printf 'install.sh: %s\n' "$1" >&2
    usage
    exit 1
}

path_exists() {
    [ -e "$1" ] || [ -L "$1" ]
}

validate_directory() {
    path=$1
    description=$2

    [ -n "$path" ] || die "$description path is empty"
    [ -d "$path" ] || die "$description is not a directory: $path"
    [ ! -L "$path" ] || die "$description must not be a symbolic link: $path"
    [ -r "$path" ] || die "$description is not readable: $path"
    [ -x "$path" ] || die "$description is not searchable: $path"
}

validate_target_path() {
    target=$1

    validate_directory "$target" 'target directory'
    [ -w "$target" ] || die "target directory is not writable: $target"
}

validate_destination_path() {
    destination=$1
    skill_name=$2

    [ -n "$destination" ] || die 'destination path is empty'
    case "$destination" in
        "$TARGET_ROOT"/*) ;;
        *) die "destination is outside the target directory: $destination" ;;
    esac
    [ "${destination%/*}" = "$TARGET_ROOT" ] || \
        die "destination is not a direct skill child: $destination"
    [ "${destination##*/}" = "$skill_name" ] || \
        die "destination name does not match the skill source: $destination"
}

validate_staging_path() {
    staging=$1
    staging_parent=${staging%/*}
    target_parent=${TARGET_ROOT%/*}

    [ -n "$staging" ] || die 'staging path is empty'
    [ "$staging" != "$TARGET_ROOT" ] || die 'staging path is the target directory'
    [ "$staging_parent" = "$target_parent" ] || \
        die "staging path is not a sibling of the target: $staging"
    case "$staging" in
        "$TARGET_ROOT".staging-[0-9]*|"$TARGET_ROOT".staging-[0-9]*.[0-9]*) ;;
        *) die "staging path has an invalid name: $staging" ;;
    esac
}

cleanup() {
    exit_status=$?
    trap - 0 HUP INT TERM
    set +e

    if [ "$STAGING_VALIDATED" -eq 1 ] && [ -n "$STAGING_DIR" ]; then
        rm -rf "$STAGING_DIR"
    fi

    exit "$exit_status"
}

force=0
mode=
book_folder=

while [ "$#" -gt 0 ]; do
    argument=$1
    shift

    case "$argument" in
        --)
            if [ "$mode" = 'global' ]; then
                [ "$#" -eq 0 ] || die 'global mode does not accept a book folder'
            else
                if [ "$#" -eq 0 ]; then
                    [ -n "$book_folder" ] || die 'missing book folder'
                else
                    [ "$#" -eq 1 ] || die 'expected exactly one book folder'
                    [ -z "$book_folder" ] || die 'duplicate book folder'
                    book_folder=$1
                    mode=local
                    shift
                fi
            fi
            ;;
        --global)
            [ -z "$mode" ] || die 'duplicate or conflicting installation modes'
            mode=global
            ;;
        --force)
            [ "$force" -eq 0 ] || die 'duplicate --force option'
            force=1
            ;;
        -*)
            die "unknown option: $argument"
            ;;
        *)
            [ -z "$book_folder" ] || die 'expected only one book folder'
            [ "$mode" != 'global' ] || die 'global mode does not accept a book folder'
            book_folder=$argument
            mode=local
            ;;
    esac
done

if [ -z "$mode" ]; then
    die 'missing installation mode or book folder'
fi

if [ "$mode" = 'local' ] && [ -z "$book_folder" ]; then
    die 'missing book folder'
fi

SCRIPT_DIR=$(CDPATH= cd -P "$(dirname "$0")" && pwd) || die 'cannot resolve script directory'
REPOSITORY_ROOT=${SCRIPT_DIR%/scripts}
SOURCE_ROOT="$REPOSITORY_ROOT/skills"

validate_directory "$SOURCE_ROOT" 'skill source directory'

skill_count=0
for skill_source in "$SOURCE_ROOT"/*; do
    if ! path_exists "$skill_source"; then
        continue
    fi

    skill_count=$((skill_count + 1))
    [ -d "$skill_source" ] || die "invalid skill source (not a directory): $skill_source"
    [ ! -L "$skill_source" ] || die "invalid skill source (symbolic link): $skill_source"
    [ -r "$skill_source" ] || die "invalid skill source (not readable): $skill_source"
    [ -x "$skill_source" ] || die "invalid skill source (not searchable): $skill_source"

    skill_name=${skill_source##*/}
    [ -n "$skill_name" ] || die 'invalid empty skill name'
    skill_manifest="$skill_source/SKILL.md"
    [ -f "$skill_manifest" ] || die "invalid skill source (missing SKILL.md): $skill_source"
    [ -r "$skill_manifest" ] || die "invalid skill source (unreadable SKILL.md): $skill_manifest"
done
[ "$skill_count" -gt 0 ] || die "skill source directory is empty: $SOURCE_ROOT"

if [ "$mode" = 'global' ]; then
    [ "${HOME+x}" = x ] || die 'HOME is unset in global mode'
    [ -n "$HOME" ] || die 'HOME is empty in global mode'
    HOME_DIR=$(CDPATH= cd -P "$HOME" 2>/dev/null && pwd) || \
        die "cannot resolve HOME directory: $HOME"
    validate_directory "$HOME_DIR" 'HOME directory'
    TARGET_PARENT="$HOME_DIR/.claude"
else
    [ -d "$book_folder" ] || die "book folder does not exist: $book_folder"
    [ ! -L "$book_folder" ] || die "book folder must not be a symbolic link: $book_folder"
    BOOK_DIR=$(CDPATH= cd -P "$book_folder" 2>/dev/null && pwd) || \
        die "cannot resolve book folder: $book_folder"
    validate_directory "$BOOK_DIR" 'book folder'
    TARGET_PARENT="$BOOK_DIR/.claude"
fi

[ -n "$TARGET_PARENT" ] || die 'target parent path is empty'
if path_exists "$TARGET_PARENT"; then
    [ -d "$TARGET_PARENT" ] || die "target parent is not a directory: $TARGET_PARENT"
    [ ! -L "$TARGET_PARENT" ] || die "target parent must not be a symbolic link: $TARGET_PARENT"
else
    mkdir "$TARGET_PARENT" || die "cannot create target parent: $TARGET_PARENT"
fi

TARGET_ROOT="$TARGET_PARENT/skills"
if path_exists "$TARGET_ROOT"; then
    [ -d "$TARGET_ROOT" ] || die "target directory is not a directory: $TARGET_ROOT"
    [ ! -L "$TARGET_ROOT" ] || die "target directory must not be a symbolic link: $TARGET_ROOT"
else
    mkdir "$TARGET_ROOT" || die "cannot create target directory: $TARGET_ROOT"
fi
validate_target_path "$TARGET_ROOT"
# Backups live outside skills/ so the agent never loads them as duplicate skills.
BACKUP_ROOT="$TARGET_PARENT/skills-backup"

STAGING_DIR=
STAGING_VALIDATED=0
trap cleanup 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

staging_suffix=0
while :; do
    if [ "$staging_suffix" -eq 0 ]; then
        candidate="$TARGET_ROOT.staging-$$"
    else
        candidate="$TARGET_ROOT.staging-$$.$staging_suffix"
    fi
    validate_staging_path "$candidate"
    if ! path_exists "$candidate"; then
        if mkdir "$candidate"; then
            STAGING_DIR=$candidate
            STAGING_VALIDATED=1
            break
        fi
        die "cannot create staging directory: $candidate"
    fi
    staging_suffix=$((staging_suffix + 1))
done

for skill_source in "$SOURCE_ROOT"/*; do
    if ! path_exists "$skill_source"; then
        continue
    fi

    skill_name=${skill_source##*/}
    staged_skill="$STAGING_DIR/$skill_name"
    validate_destination_path "$TARGET_ROOT/$skill_name" "$skill_name"
    [ ! -e "$staged_skill" ] && [ ! -L "$staged_skill" ] || \
        die "staging skill path already exists: $staged_skill"

    cp -R "$skill_source" "$STAGING_DIR" || die "cannot stage skill: $skill_source"
    [ -d "$staged_skill" ] || die "staged skill is not a directory: $staged_skill"
    [ ! -L "$staged_skill" ] || die "staged skill is a symbolic link: $staged_skill"

    evals_path="$staged_skill/evals"
    if [ -d "$evals_path" ] && [ ! -L "$evals_path" ]; then
        case "$evals_path" in
            "$STAGING_DIR"/*/evals) ;;
            *) die "invalid top-level evals path: $evals_path" ;;
        esac
        [ "${evals_path%/*}" = "$staged_skill" ] || \
            die "invalid top-level evals path: $evals_path"
        rm -rf "$evals_path" || die "cannot omit top-level evals directory: $evals_path"
    fi
done

backup_timestamp=$(date +%s) || die 'cannot determine backup timestamp'
case "$backup_timestamp" in
    ''|*[!0-9]*) die "invalid backup timestamp: $backup_timestamp" ;;
esac

for skill_source in "$SOURCE_ROOT"/*; do
    if ! path_exists "$skill_source"; then
        continue
    fi

    skill_name=${skill_source##*/}
    destination="$TARGET_ROOT/$skill_name"
    staged_skill="$STAGING_DIR/$skill_name"
    validate_destination_path "$destination" "$skill_name"
    [ -d "$staged_skill" ] || die "staged skill is missing: $staged_skill"

    if path_exists "$destination"; then
        if [ "$force" -eq 1 ]; then
            rm -rf "$destination" || die "cannot remove existing skill: $destination"
        else
            backup="$BACKUP_ROOT/$skill_name.bak-$backup_timestamp"
            backup_suffix=0
            while path_exists "$backup"; do
                backup_suffix=$((backup_suffix + 1))
                backup="$BACKUP_ROOT/$skill_name.bak-$backup_timestamp.$backup_suffix"
            done
            case "$backup" in
                "$BACKUP_ROOT/$skill_name".bak-[0-9]*|"$BACKUP_ROOT/$skill_name".bak-[0-9]*.[0-9]*) ;;
                *) die "invalid backup path: $backup" ;;
            esac
            [ "${backup%/*}" = "$BACKUP_ROOT" ] || die "backup is outside backup directory: $backup"
            if ! path_exists "$BACKUP_ROOT"; then
                mkdir "$BACKUP_ROOT" || die "cannot create backup directory: $BACKUP_ROOT"
            fi
            [ -d "$BACKUP_ROOT" ] && [ ! -L "$BACKUP_ROOT" ] || \
                die "backup directory is not a plain directory: $BACKUP_ROOT"
            mv "$destination" "$backup" || die "cannot create backup: $backup"
        fi
    fi

    mv "$staged_skill" "$destination" || die "cannot install skill: $destination"
done

rmdir "$STAGING_DIR" || die "cannot remove staging directory: $STAGING_DIR"
STAGING_VALIDATED=0
STAGING_DIR=
exit 0
