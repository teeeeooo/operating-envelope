#!/usr/bin/env bash
# Optional pre-commit guard for the report lifecycle convention.
#
# Role: commit-time, local-only. The guard validates the *names* of the
# staged report files. It does NOT enforce that a commit must include a
# report — that decision belongs to the project's own commit policy.
#
# Install:
#   cp pre-commit-report-guard.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Bypass (use sparingly):
#   git commit --no-verify ...
#
# Customize: override REPORT_ROOT, REPORT_PATTERN if your project uses
# different paths.

set -euo pipefail

REPORT_ROOT="${REPORT_LIFECYCLE_ROOT:-result_reports}"
REPORT_PATTERN='^[0-9]{3}_[a-z0-9]+(-[a-z0-9]+)*\.md$'

# Collect staged adds/renames under the report folders.
staged=$(git diff --cached --name-only --diff-filter=AR \
    | grep -E "^${REPORT_ROOT}/(active|archive)/" || true)

if [ -z "${staged}" ]; then
    exit 0
fi

violations=()
seen_ordinals=()

# Existing ordinals in the working tree (active + archive).
if [ -d "${REPORT_ROOT}" ]; then
    while IFS= read -r path; do
        base=$(basename "${path}")
        ord=${base:0:3}
        seen_ordinals+=("${ord}:${path}")
    done < <(find "${REPORT_ROOT}/active" "${REPORT_ROOT}/archive" \
        -maxdepth 1 -type f -name '*.md' 2>/dev/null || true)
fi

while IFS= read -r path; do
    base=$(basename "${path}")
    if ! [[ "${base}" =~ ${REPORT_PATTERN} ]]; then
        violations+=("name: ${path} does not match NNN_<kebab-slug>.md")
        continue
    fi
    ord="${base:0:3}"
    # Detect duplicate ordinal against another staged report or an
    # existing file at a different path.
    duplicate_count=0
    for entry in "${seen_ordinals[@]}"; do
        existing_ord="${entry%%:*}"
        existing_path="${entry#*:}"
        if [ "${existing_ord}" = "${ord}" ] && [ "${existing_path}" != "${path}" ]; then
            duplicate_count=$((duplicate_count + 1))
            violations+=("ordinal: ${path} reuses ordinal ${ord} from ${existing_path}")
        fi
    done
    seen_ordinals+=("${ord}:${path}")
done <<< "${staged}"

if [ "${#violations[@]}" -gt 0 ]; then
    echo "report-lifecycle pre-commit guard: ${#violations[@]} violation(s)" >&2
    for msg in "${violations[@]}"; do
        echo "  - ${msg}" >&2
    done
    echo "Fix the names, or rerun with --no-verify if intentional." >&2
    exit 1
fi

exit 0
