# CHANGELOG

## 1.3.0

- Deprecated `threadId` and `chat` flags, instead use messages for history:

```python
class PromptMessage:
    role: Literal['user', 'model', 'system']
    content: str
```

- Updated job management to use `documentId` only

## 1.2.3

- Added the table flag for document upload and creation

- Fixed pydantic async generator type error

## 1.2.1

- Removed Create and Delete Organization (can only be done in app)

- Added export features for documents, tables and features

## 1.1.0

- Added Category API Calls

- Added `document.upload()`, convenient function that supports both client and server side uplaods

- Some Intellisense Improvements

## 1.1.25

- Normalized snake case for all inputs

- Improved Intellisense

- Dynamic Intellisense and Types for Features and Tables
