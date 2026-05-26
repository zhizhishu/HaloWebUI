# PROJECT_ID.md

project_name: HaloWebUI
project_root: C:\Users\echo\Downloads\claude\github\HaloWebUI
project_type: code
task_file: C:\Users\echo\Downloads\claude\github\HaloWebUI\TASK.md
log_file: C:\Users\echo\Downloads\claude\github\HaloWebUI\LOG.md
legacy_task_log: C:\Users\echo\Downloads\claude\github\HaloWebUI\TASK_LOG.md

serena:
  enabled: true
  required: false
  activate: C:\Users\echo\Downloads\claude\github\HaloWebUI
  reason: true code repository; use only after activating this exact project root

ace:
  enabled: true
  required: false
  scope: C:\Users\echo\Downloads\claude\github\HaloWebUI
  reason: semantic search may be used only inside this repository

boundaries:
  parent_storage_root: C:\Users\echo\Downloads\claude
  allowed_read:
    - C:\Users\echo\Downloads\claude\github\HaloWebUI
  allowed_write:
    - C:\Users\echo\Downloads\claude\github\HaloWebUI
  forbidden_paths: []
  notes:
    - C:\Users\echo\Downloads\claude is a storage root, not this project.
    - Do not write to the parent storage root or sibling projects unless the user explicitly asks.
    - This project now uses TASK.md for current handoff and LOG.md for concise history.
    - TASK_LOG.md is retained as the legacy long-form history file.
    - Local project handoff files are not committed unless the user asks.
