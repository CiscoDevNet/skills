# Marketplace plugin packages

Each product folder is an independently installable plugin:

```text
plugins/<product>/
├── .claude-plugin/plugin.json
└── skills/<skill-name>/SKILL.md
```

Skill content is mirrored from `skills/<product>/`. Edit the canonical copy
first, update the plugin copy, and run `python3 scripts/validate_skills.py` to
detect drift.

Product plugins with only a `README.md` and manifest are reserved namespaces.
Do not advertise them as product coverage until they contain a reviewed skill.
