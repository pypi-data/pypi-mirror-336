import os
import yaml
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Type
from contextlib import contextmanager

# Base class for language templates
class LanguageTemplate:
    """Base class for language-specific workflow templates"""
    
    @classmethod
    def get_name(cls) -> str:
        """Get the name of the language this template supports"""
        raise NotImplementedError("Subclasses must implement get_name")
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        """Get the workflow template for this language"""
        raise NotImplementedError("Subclasses must implement get_workflow")
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        """Get file patterns to identify this language in a repo"""
        return []
    
    @classmethod
    def can_handle_repo(cls, repo_path: str) -> bool:
        """Check if this template can handle the repository"""
        return True


# Python template implementation
class PythonTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "python"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "Python Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {
                                "python-version": "3.x"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "python -m pip install --upgrade pip\npip install pytest\nif [ -f requirements.txt ]; then pip install -r requirements.txt; fi"
                        },
                        {
                            "name": "Test with pytest",
                            "run": "pytest --junitxml=junit/test-results.xml"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.py", "requirements.txt", "setup.py"]


# Java template implementation
class JavaTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "java"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "Java Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up JDK",
                            "uses": "actions/setup-java@v3",
                            "with": {
                                "distribution": "temurin",
                                "java-version": "17"
                            }
                        },
                        {
                            "name": "Build with Maven",
                            "run": "mvn -B test --file pom.xml"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.java", "pom.xml", "build.gradle"]


# JavaScript template implementation
class JavaScriptTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "javascript"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "Node.js Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Use Node.js",
                            "uses": "actions/setup-node@v3",
                            "with": {
                                "node-version": "16.x"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "npm ci || npm install"
                        },
                        {
                            "name": "Run tests",
                            "run": "npm test"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.js", "package.json"]


# TypeScript template implementation
class TypeScriptTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "typescript"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "TypeScript Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Use Node.js",
                            "uses": "actions/setup-node@v3",
                            "with": {
                                "node-version": "16.x"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "npm ci || npm install"
                        },
                        {
                            "name": "Run tests",
                            "run": "npm test"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.ts", "tsconfig.json"]


# Go template implementation
class GoTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "go"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "Go Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Go",
                            "uses": "actions/setup-go@v4",
                            "with": {
                                "go-version": "^1.20"
                            }
                        },
                        {
                            "name": "Test",
                            "run": "go test -v ./..."
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.go", "go.mod"]


# Rust template implementation
class RustTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "rust"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "Rust Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Build",
                            "run": "cargo build --verbose"
                        },
                        {
                            "name": "Run tests",
                            "run": "cargo test --verbose"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.rs", "Cargo.toml"]


# C# template implementation
class CSharpTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "c#"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "C# Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Setup .NET",
                            "uses": "actions/setup-dotnet@v3",
                            "with": {
                                "dotnet-version": "7.0.x"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "dotnet restore"
                        },
                        {
                            "name": "Test",
                            "run": "dotnet test --logger:\"junit;LogFilePath=TestResults/test-results.xml\""
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.cs", "*.csproj", "*.sln"]


# C++ template implementation
class CPlusPlusTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "c++"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "C++ Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Configure CMake",
                            "run": "cmake -B build -DCMAKE_BUILD_TYPE=Debug"
                        },
                        {
                            "name": "Build",
                            "run": "cmake --build build"
                        },
                        {
                            "name": "Test",
                            "run": "cd build && ctest --output-on-failure"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.cpp", "*.hpp", "*.h", "CMakeLists.txt"]


# C template implementation
class CTemplate(LanguageTemplate):
    @classmethod
    def get_name(cls) -> str:
        return "c"
    
    @classmethod
    def get_workflow(cls) -> Dict[str, Any]:
        return {
            "name": "C Template Test",
            "on": "push",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Configure CMake",
                            "run": "cmake -B build -DCMAKE_BUILD_TYPE=Debug"
                        },
                        {
                            "name": "Build",
                            "run": "cmake --build build"
                        },
                        {
                            "name": "Test",
                            "run": "cd build && ctest --output-on-failure"
                        }
                    ]
                }
            }
        }
    
    @classmethod
    def get_file_patterns(cls) -> List[str]:
        return ["*.c", "*.h", "CMakeLists.txt"]


class TemplateWorkflowManager:
    """Manages creation and cleanup of template workflows"""
    
    # Register template classes here
    _templates: List[Type[LanguageTemplate]] = [
        PythonTemplate,
        JavaTemplate,
        JavaScriptTemplate,
        TypeScriptTemplate,
        GoTemplate,
        RustTemplate,
        CSharpTemplate,
        CPlusPlusTemplate,
        CTemplate,
    ]
    
    # Dictionary for fast language lookup
    _language_map: Dict[str, Type[LanguageTemplate]] = {
        template.get_name(): template for template in _templates
    }
    
    @classmethod
    def register_template(cls, template_class: Type[LanguageTemplate]) -> None:
        """Register a new template class"""
        cls._templates.append(template_class)
        cls._language_map[template_class.get_name()] = template_class
        logging.debug(f"Registered template for {template_class.get_name()}")
    
    @classmethod
    def get_template_for_language(cls, language: str) -> Optional[Type[LanguageTemplate]]:
        """Get template class for a given language"""
        language = language.lower()
        return cls._language_map.get(language)
    
    @classmethod
    def detect_language(cls, repo_path: str) -> Optional[str]:
        """Try to detect the language from repo content"""
        for template_class in cls._templates:
            patterns = template_class.get_file_patterns()
            if not patterns:
                continue
                
            # Check if any files match the patterns
            for pattern in patterns:
                for path in Path(repo_path).rglob(pattern):
                    if path.is_file():
                        return template_class.get_name()
        
        return None
    
    @classmethod
    @contextmanager
    def create_temp_workflow(cls, repo_path: str, language: str) -> Optional[str]:
        """
        Context manager for creating a temporary workflow file
        
        Args:
            repo_path: Path to the repository
            language: Repository language
            
        Yields:
            Optional[str]: Path to the created workflow file or None if not supported
        """
        temp_workflow_path = None
        
        try:
            # Try to find template for language
            template_class = cls.get_template_for_language(language)
            
            # If language not supported, try to detect from repo contents
            if not template_class:
                detected_language = cls.detect_language(repo_path)
                if detected_language:
                    template_class = cls.get_template_for_language(detected_language)
                    logging.info(f"Detected language {detected_language} for repo")
            
            if not template_class:
                logging.warning(f"No template workflow available for language: {language}")
                yield None
                return
            
            # Check if the template can handle this repo
            if not template_class.can_handle_repo(repo_path):
                logging.warning(f"Template for {language} cannot handle this repository")
                yield None
                return
                
            # Create GitHub workflows directory if it doesn't exist
            workflow_dir = os.path.join(repo_path, ".github", "workflows")
            os.makedirs(workflow_dir, exist_ok=True)
            
            # Create the template workflow file
            temp_workflow_path = os.path.join(workflow_dir, f"template-test-crawler.yml")
            
            # Get the template for the language
            workflow_content = template_class.get_workflow()
            
            # Write the workflow to file
            with open(temp_workflow_path, "w") as f:
                yaml.dump(workflow_content, f)
            
            logging.info(f"Created template workflow for {language} at {temp_workflow_path}")
            yield temp_workflow_path
            
        except Exception as e:
            logging.error(f"Error creating template workflow: {str(e)}")
            yield None
            
        finally:
            # Clean up the template workflow file
            if temp_workflow_path and os.path.exists(temp_workflow_path):
                try:
                    os.remove(temp_workflow_path)
                    logging.info(f"Removed template workflow: {temp_workflow_path}")
                except Exception as e:
                    logging.warning(f"Failed to remove template workflow: {e}")


def create_template_workflow(repo_path: str, language: str) -> Optional[str]:
    """
    Legacy function for backward compatibility.
    Creates a template workflow file for a repository.
    
    Args:
        repo_path: Path to the repository
        language: Repository language
        
    Returns:
        Optional[str]: Path to the created workflow file or None if not supported
    """
    template_class = TemplateWorkflowManager.get_template_for_language(language)
    if not template_class:
        logging.warning(f"No template workflow available for language: {language}")
        return None
    
    try:
        # Create GitHub workflows directory if it doesn't exist
        workflow_dir = os.path.join(repo_path, ".github", "workflows")
        os.makedirs(workflow_dir, exist_ok=True)
        
        # Create the template workflow file
        template_workflow_path = os.path.join(workflow_dir, f"template-test-crawler.yml")
        
        # Get the template for the language
        workflow_content = template_class.get_workflow()
        
        # Write the workflow to file
        with open(template_workflow_path, "w") as f:
            yaml.dump(workflow_content, f)
        
        logging.info(f"Created template workflow for {language} at {template_workflow_path}")
        return template_workflow_path
    
    except Exception as e:
        logging.error(f"Error creating template workflow: {str(e)}")
        return None


def is_using_template_workflow(workflow_path: str) -> bool:
    """
    Check if a workflow is a template workflow created by this module
    
    Args:
        workflow_path: Path to the workflow file
        
    Returns:
        bool: True if it's a template workflow
    """
    return os.path.basename(workflow_path).startswith("template-test-crawler") 