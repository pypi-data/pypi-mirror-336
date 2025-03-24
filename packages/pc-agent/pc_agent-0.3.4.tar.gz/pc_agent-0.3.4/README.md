# Agent Test Project

This project contains an implementation of an Agent class and associated tests.

## Running Tests

To run the tests:

```bash
pytest
```

To run the tests with coverage:

```bash
pytest --cov=.
```

## Project Structure

- `agent.py`: Contains the Agent class implementation
- `tests/`: Directory containing test files
  - `test_agent.py`: Tests for the Agent class
- `tools/`: Directory for tool implementations 

## Publishing to GitHub Packages

This project is configured to automatically build and publish to GitHub Packages when a new tag is pushed.

To publish a new version:

1. Create a new tag following semantic versioning:
   ```bash
   git tag v0.1.0
   ```

2. Push the tag to GitHub:
   ```bash
   git push origin v0.1.0
   ```

3. The GitHub Actions workflow will automatically build and publish the package.

## Installing from GitHub Packages

To install this package from GitHub Packages:

```bash
pip install --index-url https://maven.pkg.github.com/USERNAME/pc-agent pc-agent
```

Replace `USERNAME` with your GitHub username or organization name. 