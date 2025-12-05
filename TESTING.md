# Testing Guide

This document provides information about running tests for the MTG Mulligan Trainer application.

## Overview

The application includes comprehensive tests for both the backend (Python/Flask) and frontend (Vue.js) components:

- **Backend**: Unit tests and API integration tests using pytest
- **Frontend**: Component tests, API client tests, and store tests using Vitest

## Backend Testing

### Setup

Install test dependencies:

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov
```

Run tests in verbose mode:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

Run specific test:
```bash
pytest tests/test_auth.py::TestAuth::test_hash_password
```

### Test Structure

```
backend/tests/
├── conftest.py              # Test fixtures and configuration
├── test_auth.py            # Authentication function tests
├── test_models.py          # Model unit tests
├── test_api_auth.py        # Auth API endpoint tests
├── test_api_decklists.py   # Decklist API endpoint tests
├── test_api_scenarios.py   # Scenario API endpoint tests
└── test_api_votes.py       # Vote API endpoint tests
```

### Test Coverage

Backend tests cover:
- ✅ Password hashing and verification
- ✅ JWT token generation and decoding
- ✅ User, Decklist, Scenario, and Vote models
- ✅ User registration and login endpoints
- ✅ Decklist CRUD operations
- ✅ Scenario creation and retrieval
- ✅ Voting functionality and vote counting

### Mocking

Tests use `mongomock` to mock MongoDB operations, ensuring tests run quickly without requiring a real database.

## Frontend Testing

### Setup

Install test dependencies:

```bash
cd frontend
npm install
```

### Running Tests

Run all tests:
```bash
npm test
```

Run tests in watch mode:
```bash
npm test -- --watch
```

Run tests with UI:
```bash
npm run test:ui
```

Run tests with coverage:
```bash
npm run test:coverage
```

### Test Structure

```
frontend/src/tests/
├── MtgCard.test.js         # MtgCard component tests
├── scryfall.test.js        # Scryfall API client tests
└── store.test.js           # Pinia store tests
```

### Test Coverage

Frontend tests cover:
- ✅ MtgCard component rendering and states
- ✅ Scryfall API integration and caching
- ✅ Auth store (register, login, logout)
- ✅ Decklist store operations
- ✅ Scenario store and voting
- ✅ API client mocking

### Testing Tools

- **Vitest**: Fast unit test framework
- **Vue Test Utils**: Official testing library for Vue components
- **Happy DOM**: Lightweight DOM implementation for testing
- **Mocking**: All API calls are mocked for isolated unit tests

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
```

## Writing New Tests

### Backend Test Example

```python
# tests/test_example.py
import pytest

class TestExample:
    def test_something(self, client, mongo, auth_headers):
        """Test description."""
        # Arrange
        data = {'key': 'value'}

        # Act
        response = client.post(
            '/api/endpoint',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        assert response.get_json()['key'] == 'value'
```

### Frontend Test Example

```javascript
// src/tests/example.test.js
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Component from '../components/Component.vue'

describe('Component', () => {
  it('renders correctly', () => {
    const wrapper = mount(Component, {
      props: { value: 'test' }
    })

    expect(wrapper.text()).toContain('test')
  })
})
```

## Test Best Practices

1. **Isolate Tests**: Each test should be independent and not rely on others
2. **Mock External Dependencies**: Use mocks for API calls, databases, and external services
3. **Clear Test Names**: Use descriptive names that explain what is being tested
4. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
5. **Test Edge Cases**: Include tests for error conditions and boundary cases
6. **Keep Tests Fast**: Use mocks and avoid real I/O operations
7. **Maintain Tests**: Update tests when code changes to prevent false failures

## Troubleshooting

### Backend Tests Failing

- Ensure MongoDB mock is properly configured in `conftest.py`
- Check that all required dependencies are installed
- Verify Python version compatibility (3.11+)

### Frontend Tests Failing

- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check for API mock issues - ensure all API calls are mocked
- Verify Node version (20+)

## Coverage Goals

- **Backend**: Aim for 80%+ coverage
- **Frontend**: Aim for 75%+ coverage
- **Critical Paths**: 100% coverage for auth and voting logic

## Running Tests in Docker

### Backend Tests

```bash
docker-compose run --rm backend sh -c "pip install -r requirements-test.txt && pytest"
```

### Frontend Tests

```bash
docker-compose run --rm frontend npm test
```
