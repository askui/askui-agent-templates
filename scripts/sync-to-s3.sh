#!/bin/bash
set -euo pipefail

# Prefix for the S3 bucket
s3_templates_prefix="agents/templates"
s3_templates_src_prefix="${s3_templates_prefix}/src"

# Set target bucket based on branch
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "${current_branch}" = "main" ]; then
    s3_bucket="askui-no-code"
else
    s3_bucket="askui-no-code-dev"
fi

# Get template IDs from manifest.yml
template_ids=$(yq e '.agent_templates[].id' manifest.yml)

# Create temp directory for syncing
temp_sync_dir=$(mktemp -d)

# Copy templates to sync dir
for template_id in $template_ids; do
if [ -d "src/$template_id" ]; then
    mkdir -p "${temp_sync_dir}/src/$template_id"
    cp -r "src/$template_id/"* "${temp_sync_dir}/src/$template_id/" &
fi
done
wait

# Sync template directories to S3
aws s3 sync "${temp_sync_dir}/src/" "s3://${s3_bucket}/${s3_templates_src_prefix}" --delete

# Parallel manifest creation
for template_id in $template_ids; do
{
    aws s3api list-object-versions \
        --bucket "${s3_bucket}" \
        --prefix "${s3_templates_src_prefix}/${template_id}/" \
        --query "Versions[?IsLatest==\`true\`].[Key, VersionId]" \
        --output json | \
    jq -r '.[] | "- key: \"\(.[0])\"\n  version_id: \"\(.[1])\""' > "${temp_sync_dir}/${template_id}.manifest.yml"

    sed -i '1i\objects:' "${temp_sync_dir}/${template_id}.manifest.yml"

    aws s3 cp "${temp_sync_dir}/${template_id}.manifest.yml" \
        "s3://${s3_bucket}/${s3_templates_prefix}/${template_id}.manifest.yml"
} &
done
wait

aws s3 cp manifest.yml "s3://${s3_bucket}/${s3_templates_prefix}/manifest.yml"

# Cleanup
rm -rf "${temp_sync_dir}"
