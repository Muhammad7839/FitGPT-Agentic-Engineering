#!/usr/bin/env bash
set -euo pipefail

temporary_directory=''

cleanup() {
  if [[ -n "$temporary_directory" && -d "$temporary_directory" ]]; then
    rm -rf -- "$temporary_directory"
  fi
}

usage() {
  printf '%s\n' 'Usage: memory-secret-scan.sh --working-tree [PATH] | --staged' >&2
  exit 64
}

contains_sensitive_value() {
  local file=$1

  if LC_ALL=C grep -Eiq -- 'sk-[A-Za-z0-9_./+=-]{10,}' "$file"; then
    return 0
  fi

  if LC_ALL=C grep -Eiq -- "(^|[^[:alnum:]_])(password|passwd|secret|token|api[_-]?key|apikey)[[:space:]]*[:=][[:space:]]*[\"']?[A-Za-z0-9_./+@=-]{4,}" "$file"; then
    return 0
  fi

  if LC_ALL=C grep -Eiq -- '-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----' "$file"; then
    return 0
  fi

  if LC_ALL=C grep -Eq -- '(^|[^A-Z0-9])(AKIA|ASIA)[0-9A-Z]{16}([^A-Z0-9]|$)' "$file"; then
    return 0
  fi

  return 1
}

report_blocked_file() {
  printf 'MEMORY SECRET SCAN BLOCKED: %s\n' "$1"
}

scan_working_tree() {
  local scan_root=$1
  local file
  local display_path
  local blocked=0

  [[ -d "$scan_root" ]] || usage

  while IFS= read -r -d '' file; do
    if contains_sensitive_value "$file"; then
      case "$scan_root" in
        .memory)
          display_path=$file
          ;;
        */.memory)
          display_path=".memory/${file#"$scan_root"/}"
          ;;
        *)
          display_path=${file#"$scan_root"/}
          ;;
      esac
      report_blocked_file "$display_path"
      blocked=1
    fi
  done < <(find "$scan_root" -type f -print0)

  if [[ $blocked -eq 1 ]]; then
    printf '%s\n' 'Remove the suspected sensitive value before continuing.'
    return 2
  fi
}

scan_staged() {
  local repository_root
  local staged_path
  local staged_mode
  local staged_copy
  local blocked=0

  repository_root=$(git rev-parse --show-toplevel 2>/dev/null) || usage
  cd "$repository_root"

  temporary_directory=$(mktemp -d "${TMPDIR:-/tmp}/memory-secret-scan.XXXXXX")
  trap cleanup EXIT

  while IFS= read -r -d '' staged_path; do
    staged_mode=$(git ls-files -s -- "$staged_path" | awk 'NR == 1 { print $1 }')
    [[ "$staged_mode" == '120000' ]] && continue

    staged_copy="$temporary_directory/staged-file"
    git show ":$staged_path" > "$staged_copy"

    if contains_sensitive_value "$staged_copy"; then
      report_blocked_file "$staged_path"
      blocked=1
    fi
  done < <(git diff --cached --name-only --diff-filter=ACMR -z -- .memory/)

  if [[ $blocked -eq 1 ]]; then
    printf '%s\n' 'Remove the suspected sensitive value before continuing.'
    return 2
  fi
}

case ${1-} in
  --working-tree)
    [[ $# -le 2 ]] || usage
    scan_working_tree "${2:-.memory}"
    ;;
  --staged)
    [[ $# -eq 1 ]] || usage
    scan_staged
    ;;
  *)
    usage
    ;;
esac
