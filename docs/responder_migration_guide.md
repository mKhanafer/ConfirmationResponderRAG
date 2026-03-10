# Responder Migration Guide: CurrentGen to NextGen

## Overview

This guide helps Bank Responders migrate their AutoProcess API integrations from the Thomson Reuters CurrentGen Confirmation platform to the new NextGen platform.

**Target Audience**: Bank IT teams implementing automated confirmation processing

**Migration Timeline**: CurrentGen will be deprecated on December 31, 2026

## Key Differences Between CurrentGen and NextGen

### API Architecture
- **CurrentGen**: SOAP-based XML services
- **NextGen**: RESTful JSON APIs with OAuth 2.0 authentication

### Authentication Changes
- **CurrentGen**: API key in header (`X-API-Key`)
- **NextGen**: OAuth 2.0 Bearer tokens with token refresh

### Base URLs
- **CurrentGen**: `https://confirmations.thomsonreuters.com/api/v1`
- **NextGen**: `https://confirmations-nextgen.thomsonreuters.com/api/v2`

## Migration Checklist

### Step 1: Obtain NextGen Credentials

Contact your Thomson Reuters account manager to request:
1. Client ID
2. Client Secret  
3. API access scope permissions

**Important**: Do not share these credentials. Store them securely using a secrets management system.

### Step 2: Implement OAuth 2.0 Authentication

NextGen uses OAuth 2.0 with client credentials flow.

**Token Endpoint**: `POST https://confirmations-nextgen.thomsonreuters.com/oauth/token`

**Request Parameters**:
```json
{
  "grant_type": "client_credentials",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "scope": "confirmations:read confirmations:write"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "confirmations:read confirmations:write"
}
```

**Token Refresh**: Tokens expire after 1 hour. Implement automatic refresh logic before expiration.

### Step 3: Update API Endpoints

#### Get Pending Confirmations

**CurrentGen**:
```
GET /confirmation-requests/pending
Header: X-API-Key: YOUR_API_KEY
```

**NextGen**:
```
GET /v2/confirmation-requests?status=pending
Header: Authorization: Bearer YOUR_ACCESS_TOKEN
```

**NextGen Response Schema**:
```json
{
  "confirmation_requests": [
    {
      "request_id": "REQ-2026-001234",
      "requester_name": "Audit Firm Name",
      "account_number": "1234567890",
      "account_type": "checking",
      "as_of_date": "2026-03-10",
      "created_at": "2026-03-10T14:30:00Z",
      "due_date": "2026-03-17T23:59:59Z"
    }
  ],
  "total_count": 15,
  "page": 1,
  "page_size": 50
}
```

#### Submit Confirmation Response

**CurrentGen**:
```xml
POST /confirmation-response
Content-Type: application/xml

<ConfirmationResponse>
  <RequestID>REQ-001234</RequestID>
  <Status>confirmed</Status>
  <AccountBalance>125000.00</AccountBalance>
  <Currency>USD</Currency>
</ConfirmationResponse>
```

**NextGen**:
```
POST /v2/confirmation-responses
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "request_id": "REQ-2026-001234",
  "status": "confirmed",
  "account_balance": 125000.00,
  "currency": "USD",
  "balance_type": "actual",
  "confirmed_date": "2026-03-10"
}
```

**Response Status Codes**:
- `201 Created`: Response submitted successfully
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: Request ID not found
- `409 Conflict`: Response already submitted

### Step 4: Handle Status Updates

NextGen supports real-time status updates via webhooks (optional).

**Webhook Registration**:
```
POST /v2/webhooks
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "url": "https://your-bank.com/confirmation-webhook",
  "events": ["request.created", "request.cancelled", "response.acknowledged"],
  "secret": "your-webhook-secret"
}
```

**Webhook Payload Example**:
```json
{
  "event": "request.created",
  "timestamp": "2026-03-10T14:30:00Z",
  "data": {
    "request_id": "REQ-2026-001234",
    "account_number": "1234567890",
    "requester_name": "Audit Firm Name"
  }
}
```

## Error Handling

### Common Error Responses

**401 Unauthorized**:
```json
{
  "error": "invalid_token",
  "error_description": "The access token expired"
}
```
**Solution**: Refresh your OAuth token

**429 Too Many Requests**:
```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit of 1000 requests per hour exceeded",
  "retry_after": 3600
}
```
**Solution**: Implement exponential backoff and respect rate limits

### Rate Limits
- **Authentication endpoint**: 10 requests per minute
- **API endpoints**: 1000 requests per hour per client

## Testing Your Migration

### Sandbox Environment

Before migrating to production, test your integration in the NextGen sandbox:

**Sandbox Base URL**: `https://sandbox-confirmations-nextgen.thomsonreuters.com/api/v2`

**Test Credentials**: Request sandbox credentials from ConfirmationResponderAPI@thomsonreuters.com

### Test Scenarios

1. **Successful confirmation**: Submit a confirmed response with valid balance
2. **Exception handling**: Submit an exception with reason code
3. **Token refresh**: Test automatic token renewal
4. **Webhook delivery**: Verify webhook signature validation

## Support Resources

### Technical Support
- Email: ConfirmationResponderAPI@thomsonreuters.com
- Portal: https://support.thomsonreuters.com/confirmations
- Response Time: 24-48 hours

### API Documentation
- Interactive API Explorer: https://confirmations-nextgen.thomsonreuters.com/docs
- OpenAPI Spec: https://confirmations-nextgen.thomsonreuters.com/openapi.json

### Migration Assistance
Contact your account manager for:
- Migration planning consultation
- Extended sandbox access
- Custom integration support

## Deprecation Timeline

- **June 1, 2026**: NextGen generally available
- **September 1, 2026**: CurrentGen enters maintenance mode (bug fixes only)
- **December 31, 2026**: CurrentGen fully deprecated and shut down

**Action Required**: Complete migration by November 30, 2026 to allow time for testing.
