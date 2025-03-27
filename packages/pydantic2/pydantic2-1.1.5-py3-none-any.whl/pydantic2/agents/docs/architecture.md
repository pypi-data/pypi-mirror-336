# Architecture Overview

This document outlines the architecture of the Pydantic AI Form Processor framework.

## Core Components

The framework consists of several key components that work together to provide a seamless form processing experience:

```
┌───────────────────┐      ┌───────────────────┐
│  FormProcessor    │◄────►│     FormTools     │
└───────┬───────────┘      └─────────┬─────────┘
        │                            │
        │                            │
        ▼                            ▼
┌───────────────────┐      ┌───────────────────┐
│  BaseAnalytics    │      │  LLM Provider     │
└───────────────────┘      └───────────────────┘
```

### FormProcessor

The `FormProcessor` is the main entry point and orchestrates the entire form processing flow. It:

- Manages user sessions
- Coordinates between form tools and analytics
- Provides a simple API for applications to integrate with
- Handles state management for form completion

### FormTools

The `FormTools` class is responsible for the actual form filling process. It:

- Tracks form completion progress
- Extracts field values from user messages
- Validates data against the Pydantic model
- Generates appropriate prompts for the LLM
- Manages the form state

### BaseAnalyticsTools

The `BaseAnalyticsTools` class provides analysis of completed forms. It:

- Analyzes form data using LLM
- Generates insights based on the analysis
- Uses template method pattern for easy customization
- Handles errors gracefully

### LLM Provider Interface

The `LLMProvider` interface abstracts away the details of interacting with different LLM APIs. It:

- Provides a unified interface for different LLM providers
- Handles request formatting and response parsing
- Manages API keys and authentication
- Implements error handling and retries

## Data Flow

```
┌──────────┐     ┌───────────────┐     ┌──────────────┐     ┌─────────────┐
│  User    │────►│FormProcessor  │────►│  FormTools   │────►│LLM Provider │
│ Message  │     │               │     │              │     │             │
└──────────┘     └───────┬───────┘     └──────┬───────┘     └──────┬──────┘
                         │                    │                    │
                         │                    ▼                    ▼
                         │             ┌──────────────┐    ┌──────────────┐
                         │             │ Current Form │    │  LLM Response│
                         │             │    State     │    │              │
                         │             └──────┬───────┘    └──────┬───────┘
                         │                    │                   │
                         │                    ◄───────────────────┘
                         ▼                    │
                  ┌─────────────┐            │
                  │ Analytics   │◄───────────┘
                  │   Tools     │
                  └─────┬───────┘
                        │
                        ▼
                  ┌─────────────┐
                  │  Insights   │
                  │             │
                  └─────────────┘
```

1. User sends a message to the `FormProcessor`
2. `FormProcessor` passes the message to `FormTools`
3. `FormTools` generates a prompt and sends it to the `LLMProvider`
4. `LLMProvider` sends a request to the LLM API and returns the response
5. `FormTools` updates the form state based on the response
6. If the form is complete, `FormProcessor` passes the data to `BaseAnalyticsTools`
7. `BaseAnalyticsTools` analyzes the data and generates insights
8. `FormProcessor` returns the response, including any insights

## Key Design Patterns

The framework uses several design patterns to achieve flexibility and maintainability:

### Template Method Pattern

Used in `BaseAnalyticsTools` to allow easy customization of specific behaviors while maintaining a consistent interface.

### Strategy Pattern

Used with `LLMProvider` to allow different implementations (OpenRouter, Anthropic, etc.) to be swapped out without changing the client code.

### Facade Pattern

`FormProcessor` provides a simplified interface to the complex subsystems of form filling and analysis.

### Builder Pattern

Form state is built up incrementally by `FormTools` as the user provides information.

## Extension Points

The framework is designed to be extensible in several ways:

1. **Custom Analytics**: Inherit from `BaseAnalyticsTools` and override methods
2. **New LLM Providers**: Implement the `LLMProvider` interface
3. **Custom Form Tools**: Extend `FormTools` to add specialized behavior
4. **Schema Conversion**: Customize how JSON schemas are converted to Pydantic models

## Implementation Details

### Session Management

Sessions are identified by UUIDs and can be persisted across multiple interactions. The session contains:

- Form state (completed fields, validation errors)
- Conversation history
- Analytics results (if available)

### Error Handling

The framework has multiple layers of error handling:

- API-level errors (connection issues, rate limits)
- Validation errors (invalid data types, constraint violations)
- LLM response parsing errors

### Performance Considerations

- Conversation history is pruned to minimize token usage
- Field extraction is optimized to minimize API calls
- Form state is cached to reduce redundant processing
