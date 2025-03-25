# Template Workflows

This module provides default template workflows for repositories that don't have GitHub Actions workflows defined. It uses a registry pattern to make adding new language templates easy and extensible.

## How it Works

The `TemplateWorkflowManager` class coordinates:

1. Template registration for each supported language
2. Language detection from repository contents
3. Workflow creation and cleanup

## Using Template Workflows

The most convenient way to use template workflows is with the context manager:

```python
from gitbugactions.actions.templates.template_workflows import TemplateWorkflowManager

# Create a temporary workflow that will be automatically cleaned up
with TemplateWorkflowManager.create_temp_workflow(repo_path, language) as workflow_path:
    if workflow_path:
        # Do something with the workflow
        pass
    # When the context exits, the workflow file is automatically removed
```

## Supported Languages

The following languages are currently supported:

- Python
- Java
- JavaScript
- TypeScript
- Go
- Rust
- C#
- C++
- C

## Adding a New Language Template

To add support for a new language, create a subclass of `LanguageTemplate` and register it with the `TemplateWorkflowManager`:

```python
from gitbugactions.actions.templates.template_workflows import LanguageTemplate, TemplateWorkflowManager

class MyNewLanguageTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "mylanguage"
    
    @classmethod
    def get_workflow(cls) -> dict:
        return {
            "name": "My Language Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        # Define your workflow steps here
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> list:
        return ["*.mylang", "mylang.config"]
        
    @classmethod
    def can_handle_repo(cls, repo_path: str) -> bool:
        # Optional: Add custom logic to determine if this template
        # can handle this specific repository structure
        return True

# Register the template
TemplateWorkflowManager.register_template(MyNewLanguageTemplate)
```

## Advanced Customization

You can customize template selection further by implementing a custom `can_handle_repo` method that examines the repository structure and determines if a specific template can handle it.

For more complex scenarios, you can also create entirely new template managers by following the pattern in `TemplateWorkflowManager`. 