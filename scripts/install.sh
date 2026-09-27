#!/bin/sh

set -eu

# The caller must control BASE_DIR and its ancestors for the duration of the
# install. This POSIX shell implementation rechecks path components but cannot
# hold directory descriptors against a concurrent filesystem replacement.

usage() {
    printf '%s\n' \
        'Usage: install.sh [--force] [--target target] <book-folder>' \
        '       install.sh [--force] [--target target] --global' \
        '       install.sh [--force] [--target target] -- <book-folder>' >&2
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

validate_creation_parent() {
    path=$1

    [ -n "$path" ] || die 'creation parent path is empty'
    probe=$path
    while ! path_exists "$probe"; do
        parent=${probe%/*}
        [ "$parent" != "$probe" ] || die "cannot find an existing parent for: $path"
        probe=$parent
    done
    validate_directory "$probe" 'creation parent'
    [ -w "$probe" ] || die "creation parent is not writable: $probe"
}

validate_path_components() {
    vpc_path=$1
    vpc_base=$2

    [ -n "$vpc_path" ] || die 'path to validate is empty'
    [ -n "$vpc_base" ] || die 'path validation base is empty'
    case "$vpc_path" in
        "$vpc_base") return 0 ;;
        "$vpc_base"/*) ;;
        *) die "path is outside its physical base: $vpc_path" ;;
    esac

    vpc_relative=${vpc_path#"$vpc_base"/}
    vpc_current=$vpc_base
    while [ -n "$vpc_relative" ]; do
        vpc_component=${vpc_relative%%/*}
        if [ "$vpc_component" = "$vpc_relative" ]; then
            vpc_relative=
        else
            vpc_relative=${vpc_relative#*/}
        fi
        vpc_current="$vpc_current/$vpc_component"
        [ ! -L "$vpc_current" ] || die "path component must not be a symbolic link: $vpc_current"
    done
}

ensure_directory_path() {
    edp_path=$1
    edp_base=$2
    edp_description=$3

    validate_path_components "$edp_path" "$edp_base"
    edp_relative=${edp_path#"$edp_base"/}
    edp_current=$edp_base
    while [ -n "$edp_relative" ]; do
        edp_component=${edp_relative%%/*}
        if [ "$edp_component" = "$edp_relative" ]; then
            edp_relative=
        else
            edp_relative=${edp_relative#*/}
        fi
        edp_current="$edp_current/$edp_component"
        validate_path_components "$edp_current" "$edp_base"
        if path_exists "$edp_current"; then
            validate_directory "$edp_current" "$edp_description"
        else
            mkdir "$edp_current" || die "cannot create $edp_description: $edp_current"
            validate_directory "$edp_current" "$edp_description"
        fi
    done
}

validate_target_name() {
    target_name=$1

    case "$target_name" in
        claude|agents|codex|cursor|gemini|opencode|copilot|all) ;;
        *) die "invalid target: $target_name" ;;
    esac
}

configure_target_paths() {
    selected_target=$1

    case "$selected_target" in
        claude) target_directory=.claude ;;
        agents) target_directory=.agents ;;
        codex) target_directory=.codex ;;
        cursor) target_directory=.cursor ;;
        gemini) target_directory=.gemini ;;
        opencode)
            if [ "$mode" = 'global' ]; then
                target_directory=.config/opencode
            else
                target_directory=.opencode
            fi
            ;;
        copilot) target_directory=.github ;;
        *) die "invalid target: $selected_target" ;;
    esac

    TARGET_PARENT="$BASE_DIR/$target_directory"
    TARGET_ROOT="$TARGET_PARENT/skills"
    BACKUP_ROOT="$TARGET_PARENT/skills-backup"
}

validate_destination_path() {
    target_root=$1
    destination=$2
    skill_name=$3

    [ -n "$destination" ] || die 'destination path is empty'
    case "$destination" in
        "$target_root"/*) ;;
        *) die "destination is outside the target directory: $destination" ;;
    esac
    [ "${destination%/*}" = "$target_root" ] || \
        die "destination is not a direct skill child: $destination"
    [ "${destination##*/}" = "$skill_name" ] || \
        die "destination name does not match the skill source: $destination"
}

validate_staging_path() {
    staging=$1
    target_root=$2
    staging_parent=${staging%/*}
    target_parent=${target_root%/*}

    [ -n "$staging" ] || die 'staging path is empty'
    [ "$staging" != "$target_root" ] || die 'staging path is the target directory'
    [ "$staging_parent" = "$target_parent" ] || \
        die "staging path is not a sibling of the target: $staging"
    case "$staging" in
        "$target_root".staging-[0-9]*|"$target_root".staging-[0-9]*.[0-9]*) ;;
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

    if [ "$exit_status" -ne 0 ] && [ "$MUTATION_STARTED" -eq 1 ] &&
        [ "$TARGET_COUNT" -gt 1 ]; then
        printf '%s\n' \
            'install.sh: warning: multi-target installation is not transactional; earlier targets may remain installed' >&2
    fi

    exit "$exit_status"
}

force=0
mode=
book_folder=
target_name=claude
target_selected=0

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
        --target)
            [ "$target_selected" -eq 0 ] || die 'duplicate --target option'
            [ "$#" -gt 0 ] || die 'missing value for --target'
            target_name=$1
            shift
            validate_target_name "$target_name"
            target_selected=1
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

if [ "$mode" = 'global' ] && [ "$target_name" = 'copilot' ]; then
    die 'copilot target is project-only and cannot be used with --global'
fi

if [ "$target_name" = 'all' ]; then
    TARGETS='claude agents'
else
    TARGETS=$target_name
fi

TARGET_COUNT=0
for selected_target in $TARGETS; do
    TARGET_COUNT=$((TARGET_COUNT + 1))
done
[ "$TARGET_COUNT" -gt 0 ] || die 'no installation targets selected'

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
    BASE_DIR=$HOME_DIR
else
    [ -d "$book_folder" ] || die "book folder does not exist: $book_folder"
    [ ! -L "$book_folder" ] || die "book folder must not be a symbolic link: $book_folder"
    BOOK_DIR=$(CDPATH= cd -P "$book_folder" 2>/dev/null && pwd) || \
        die "cannot resolve book folder: $book_folder"
    validate_directory "$BOOK_DIR" 'book folder'
    BASE_DIR=$BOOK_DIR
fi

STAGING_DIR=
STAGING_VALIDATED=0
MUTATION_STARTED=0
trap cleanup 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

backup_timestamp=$(date +%s) || die 'cannot determine backup timestamp'
case "$backup_timestamp" in
    ''|*[!0-9]*) die "invalid backup timestamp: $backup_timestamp" ;;
esac

for selected_target in $TARGETS; do
    configure_target_paths "$selected_target"

    [ -n "$TARGET_PARENT" ] || die 'target parent path is empty'
    validate_path_components "$TARGET_PARENT" "$BASE_DIR"
    if path_exists "$TARGET_PARENT"; then
        validate_directory "$TARGET_PARENT" 'target parent'
        [ -w "$TARGET_PARENT" ] || die "target parent is not writable: $TARGET_PARENT"
    else
        validate_creation_parent "$TARGET_PARENT"
    fi

    validate_path_components "$TARGET_ROOT" "$BASE_DIR"
    if path_exists "$TARGET_ROOT"; then
        validate_target_path "$TARGET_ROOT"
    else
        validate_creation_parent "$TARGET_ROOT"
    fi

    validate_path_components "$BACKUP_ROOT" "$BASE_DIR"

    for skill_source in "$SOURCE_ROOT"/*; do
        if ! path_exists "$skill_source"; then
            continue
        fi

        skill_name=${skill_source##*/}
        destination="$TARGET_ROOT/$skill_name"
        validate_destination_path "$TARGET_ROOT" "$destination" "$skill_name"

        if path_exists "$destination" && [ "$force" -eq 0 ]; then
            if path_exists "$BACKUP_ROOT"; then
                validate_directory "$BACKUP_ROOT" 'backup directory'
                [ -w "$BACKUP_ROOT" ] || die "backup directory is not writable: $BACKUP_ROOT"
            else
                validate_creation_parent "$BACKUP_ROOT"
            fi
        fi
    done
done

for selected_target in $TARGETS; do
    configure_target_paths "$selected_target"

    validate_path_components "$TARGET_PARENT" "$BASE_DIR"
    validate_path_components "$TARGET_ROOT" "$BASE_DIR"
    validate_path_components "$BACKUP_ROOT" "$BASE_DIR"

    if ! path_exists "$TARGET_PARENT"; then
        MUTATION_STARTED=1
        ensure_directory_path "$TARGET_PARENT" "$BASE_DIR" 'target parent'
    fi
    validate_directory "$TARGET_PARENT" 'target parent'
    [ -w "$TARGET_PARENT" ] || die "target parent is not writable: $TARGET_PARENT"

    if ! path_exists "$TARGET_ROOT"; then
        MUTATION_STARTED=1
        ensure_directory_path "$TARGET_ROOT" "$BASE_DIR" 'target directory'
    fi
    validate_target_path "$TARGET_ROOT"

    staging_suffix=0
    while :; do
        if [ "$staging_suffix" -eq 0 ]; then
            candidate="$TARGET_ROOT.staging-$$"
        else
            candidate="$TARGET_ROOT.staging-$$.$staging_suffix"
        fi
        validate_staging_path "$candidate" "$TARGET_ROOT"
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
        validate_path_components "$TARGET_PARENT" "$BASE_DIR"
        validate_path_components "$TARGET_ROOT" "$BASE_DIR"
        validate_destination_path "$TARGET_ROOT" "$TARGET_ROOT/$skill_name" "$skill_name"
        [ ! -e "$staged_skill" ] && [ ! -L "$staged_skill" ] || \
            die "staging skill path already exists: $staged_skill"

        cp -R "$skill_source" "$STAGING_DIR" || die "cannot stage skill: $skill_source"
        [ -d "$staged_skill" ] || die "staged skill is missing: $staged_skill"
        [ ! -L "$staged_skill" ] || die "staged skill is a symbolic link: $staged_skill"

        evals_path="$staged_skill/evals"
        if [ -d "$evals_path" ] && [ ! -L "$evals_path" ]; then
            case "$evals_path" in
                "$STAGING_DIR"/*/evals) ;;
                *) die "invalid top-level evals path: $evals_path" ;;
            esac
            [ "${evals_path%/*}" = "$staged_skill" ] || \
                die "invalid top-level evals path: $evals_path"
            [ -d "$staged_skill" ] && [ ! -L "$staged_skill" ] || \
                die "staged skill changed before cleanup: $staged_skill"
            rm -rf "$evals_path" || die "cannot omit top-level evals directory: $evals_path"
        fi
    done

    for skill_source in "$SOURCE_ROOT"/*; do
        if ! path_exists "$skill_source"; then
            continue
        fi

        skill_name=${skill_source##*/}
        destination="$TARGET_ROOT/$skill_name"
        staged_skill="$STAGING_DIR/$skill_name"
        validate_destination_path "$TARGET_ROOT" "$destination" "$skill_name"
        [ -d "$staged_skill" ] || die "staged skill is missing: $staged_skill"

        if path_exists "$destination"; then
            if [ "$force" -eq 1 ]; then
                validate_path_components "$TARGET_PARENT" "$BASE_DIR"
                validate_path_components "$TARGET_ROOT" "$BASE_DIR"
                MUTATION_STARTED=1
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
                validate_path_components "$TARGET_PARENT" "$BASE_DIR"
                validate_path_components "$TARGET_ROOT" "$BASE_DIR"
                validate_path_components "$BACKUP_ROOT" "$BASE_DIR"
                if ! path_exists "$BACKUP_ROOT"; then
                    mkdir "$BACKUP_ROOT" || die "cannot create backup directory: $BACKUP_ROOT"
                fi
                [ -d "$BACKUP_ROOT" ] && [ ! -L "$BACKUP_ROOT" ] || \
                    die "backup directory is not a plain directory: $BACKUP_ROOT"
                MUTATION_STARTED=1
                mv "$destination" "$backup" || die "cannot create backup: $backup"
            fi
        fi

        MUTATION_STARTED=1
        validate_path_components "$TARGET_PARENT" "$BASE_DIR"
        validate_path_components "$TARGET_ROOT" "$BASE_DIR"
        mv "$staged_skill" "$destination" || die "cannot install skill: $destination"
    done

    rmdir "$STAGING_DIR" || die "cannot remove staging directory: $STAGING_DIR"
    STAGING_VALIDATED=0
    STAGING_DIR=
done

exit 0
