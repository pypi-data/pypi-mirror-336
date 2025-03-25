# Contributing to Flask-GWS

Thank you for considering contributing to Flask-GWS!

## Setup for Development

1. Fork and clone the repository
2. Create a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install development dependencies:
   ```
   pip install -e ".[uwsgi]"
   pip install -r dev-requirements.txt
   ```

## Installing uWSGI with WebSocket Support

For WebSocket support, uWSGI must be installed with SSL:

### For Ubuntu/Debian:
```bash
CFLAGS="-I/usr/include/openssl" LDFLAGS="-L/usr/lib/x86_64-linux-gnu" UWSGI_PROFILE_OVERRIDE=ssl=true pip install --no-cache-dir uwsgi --no-binary :all:
```

### For macOS (Apple Silicon):
```bash
CFLAGS="-I/opt/homebrew/opt/openssl@3/include" \
LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib" \
UWSGI_PROFILE_OVERRIDE=ssl=true pip install --no-cache-dir uwsgi --no-binary :all:
```

## Testing

After making changes, run the tests:

```
pytest tests/
```

## Pull Request Process

1. Ensure any new feature or bug fix includes test coverage
2. Update the README.md with details of changes to the interface, if applicable
3. The version number will be updated as part of the release process
4. Submit a Pull Request with a clear description of the changes

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

## License

By contributing to Flask-GWS, you agree that your contributions will be licensed under the project's MIT License. 