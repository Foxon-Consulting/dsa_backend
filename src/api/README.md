# Document Sorting Assistant API

This API provides services to suggest appropriate filenames and directories based on file content analysis.

## Features

- **Filename suggestion**: Analyzes a file and suggests an appropriate name based on its content
- **Directory suggestion**: Analyzes a file and suggests the best directory from a list of candidates

## Architecture

The API is built with FastAPI and uses two main models:

- `SuggestFilenameResponse`: Contains the filename suggestion
- `SuggestDirectoryResponse`: Contains the directory suggestion

Uploaded files are temporarily stored on the server for analysis, then immediately deleted after use.

## Endpoints

### 1. Suggest a filename

```
POST /suggest-filename
```

**Parameters**:
- `file`: The file to analyze (binary file)

**Response**:
```json
{
  "suggestion": "2023-01-01-monthly-report.pdf"
}
```

### 2. Suggest a directory

```
POST /suggest-directory
```

**Parameters**:
- `file`: The file to analyze (binary file)
- `directories`: List of candidate directories [array]

**Response**:
```json
{
  "suggestion": "Documents/Reports"
}
```

## How to use the API

### Example with cURL

```bash
# Suggest a filename
curl -X POST "http://localhost:8000/suggest-filename" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf"

# Suggest a directory
curl -X POST "http://localhost:8000/suggest-directory" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf" \
  -F "directories=Documents" \
  -F "directories=Invoices" \
  -F "directories=Reports"
```

### Example with JavaScript Fetch

```javascript
// Suggest a filename
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/suggest-filename', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data.suggestion));

// Suggest a directory
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('directories', 'Documents');
formData.append('directories', 'Invoices');
formData.append('directories', 'Reports');

fetch('http://localhost:8000/suggest-directory', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data.suggestion));
```

## Error handling

The API returns appropriate HTTP error codes in case of problems:

- `400 Bad Request`: Missing or invalid parameters
- `500 Internal Server Error`: Error processing the file

Errors are returned in JSON format:

```json
{
  "detail": "Detailed error message"
}
```
