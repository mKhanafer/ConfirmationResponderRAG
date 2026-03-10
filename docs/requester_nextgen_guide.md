# Requester Guide: NextGen Platform

## Overview

This guide helps Auditor firms (Requesters) submit and manage confirmation requests using the Thomson Reuters NextGen Confirmation platform.

**Target Audience**: Audit professionals and audit firm IT staff

**Platform Status**: NextGen is the current production platform with enhanced features and improved user experience.

## What's New in NextGen

### Key Improvements

1. **Faster Response Times**: Average confirmation turnaround reduced from 10 days to 5-7 days
2. **Real-Time Status Updates**: Instant notifications when status changes
3. **Mobile App**: iOS and Android apps for on-the-go access
4. **AI-Assisted Matching**: Automated account matching reduces exceptions by 40%
5. **Bulk Operations**: Submit multiple confirmations at once via spreadsheet upload
6. **API Access**: Integrate confirmation workflow with your audit management system

### Enhanced Security

- **Multi-Factor Authentication (MFA)**: Required for all users
- **Biometric Login**: Fingerprint and Face ID support on mobile
- **Advanced Encryption**: End-to-end encryption for all sensitive data
- **Audit Trail**: Detailed activity logs for compliance

## Getting Started with NextGen

### Account Migration

If you're coming from CurrentGen:
1. Your account will be automatically migrated
2. You'll receive an email with new login instructions
3. All historical confirmations are preserved
4. Old confirmation numbers remain searchable

First-time users:
1. Register at https://confirmations-nextgen.thomsonreuters.com
2. Verify your email address
3. Set up MFA (required)
4. Complete firm profile

### Dashboard Overview

The NextGen dashboard provides:
- **Quick Stats**: Pending, sent, and completed confirmation counts
- **Activity Feed**: Real-time updates on your confirmations
- **Due Soon**: Confirmations approaching deadline
- **Recent**: Last 10 confirmations you worked on
- **Analytics**: Response rate trends and turnaround time metrics

## Creating Confirmation Requests

### Method 1: Single Request (Web Interface)

1. Click **New Confirmation** button
2. Select request type:
   - **Bank Account**: Checking, savings, CDs
   - **Loan/Credit**: Mortgages, lines of credit, credit cards
   - **Investment**: Brokerage, custody accounts
   - **Other**: Specialized account types

3. **Smart Client Search**:
   - Type client name - AI suggests matches from your client list
   - Auto-populates previous account information if available
   - Shows historical confirmation success rate for this client

4. **Enter Account Details**:
   ```
   Required Fields:
   - Account Holder Legal Name
   - Account Number or Last 4 Digits
   - Financial Institution Name
   - As-of Date
   - Account Type
   
   Optional Fields:
   - Branch Code/Name
   - Account Nickname
   - Expected Balance Range (helps with verification)
   - Internal Reference Number
   ```

5. **Recipient Selection**:
   - Search institution's authorized signers in the platform directory
   - Add new signer if not listed
   - Platform validates email deliverability
   - Shows previous response rate for this signer (if available)

6. **Set Priority**:
   - **Standard**: 14-day turnaround
   - **Expedited**: 7-day turnaround (additional fee may apply)
   - **Rush**: 3-day turnaround (premium fee, advance approval required)

7. **Review and Submit**:
   - AI validation checks for common errors
   - Warnings display for:
     - Account number format issues
     - Mismatched client/institution pairings
     - Duplicate recent submissions
   - Click **Submit** to send

### Method 2: Bulk Upload (Excel/CSV)

For clients with many accounts:

1. Click **Bulk Upload** → **Download Template**

2. **Template Format**:
   ```
   Client Name | Account Number | Institution | Account Type | As-of Date | Signer Email | Due Date | Notes
   ```

3. **Fill in Your Data**:
   - Maximum 500 rows per upload
   - Date format: YYYY-MM-DD
   - Required fields marked with asterisk in template

4. **Upload and Validate**:
   - Platform performs pre-submission validation
   - Shows errors by row number
   - Fix errors and re-upload or skip problematic rows

5. **Review Summary**:
   - Total confirmations to be created
   - Estimated cost (if applicable)
   - Distribution by institution

6. **Submit Batch**:
   - All confirmations submitted simultaneously
   - Batch ID created for tracking
   - Email confirmation sent

### Method 3: API Integration

For audit firms with custom software:

**Endpoint**: `POST /api/v2/confirmation-requests`

**Authentication**: OAuth 2.0 Bearer token

**Request Body**:
```json
{
  "client": {
    "name": "Example Corporation",
    "client_id": "CLT-12345"
  },
  "account": {
    "account_number": "1234567890",
    "account_holder_name": "Example Corporation",
    "account_type": "checking",
    "institution_name": "First National Bank",
    "branch_code": "001"
  },
  "confirmation_details": {
    "as_of_date": "2026-12-31",
    "due_date": "2027-01-14",
    "priority": "standard",
    "currency": "USD"
  },
  "recipient": {
    "name": "Jane Smith",
    "title": "CFO",
    "email": "jsmith@firstnational.com"
  },
  "internal_reference": "WP-2026-001",
  "special_instructions": "Please include all sub-accounts"
}
```

**Response**:
```json
{
  "confirmation_id": "CNF-2026-987654",
  "status": "pending_submission",
  "created_at": "2026-03-10T14:30:00Z",
  "estimated_completion": "2026-03-24T23:59:59Z"
}
```

## Tracking and Monitoring

### Real-Time Status Updates

NextGen provides instant status notifications:

**Sent** → **Opened** → **In Progress** → **Completed**

Each transition triggers:
- Email notification (if enabled)
- Mobile push notification (if app installed)
- API webhook (if configured)
- Dashboard update

### Status Meanings

#### Pending Submission
- Confirmation created but not yet sent
- Can edit or cancel freely
- Appears in "Drafts" folder

#### Sent
- Email delivered to financial institution
- Awaiting acknowledgment
- Delivery confirmed via tracking

#### Opened
- Recipient has opened the confirmation email
- Timestamp shows when
- Indicates engagement

#### In Progress
- Institution is actively working on the response
- May show substatus: "Documents Requested", "Under Review", "Awaiting Approval"

#### Completed
- Response received and available for download
- Balance confirmed or exception noted
- Automatically filed in your workspace

#### Exception
- Issue prevents completion
- **Common exception types**:
  - **E01**: Account not found
  - **E02**: Incorrect account number
  - **E03**: Authorization required
  - **E04**: Account closed
  - **E05**: Insufficient information
  - **E99**: Other (see notes)

- **Smart Exception Handling**: NextGen suggests corrections based on exception type

#### Cancelled
- Request withdrawn before completion
- Can be reinstated within 7 days

### Advanced Filtering

Filter confirmations by:
- Status (multi-select)
- Client (type-ahead search)
- Institution
- Date range (sent date, as-of date, due date)
- Assigned team member
- Account type
- Priority level
- Entity/office
- Custom tags

**Saved Filters**: Save frequently used filter combinations for quick access

## Managing Responses

### Viewing Confirmation Details

Click any confirmation to see:
- **Timeline**: Visual timeline showing all status changes
- **Details**: All account and request information
- **Messages**: Communication thread with institution
- **Documents**: Attached correspondence or supporting docs
- **Audit Trail**: Complete activity log

### Downloading Confirmations

**Individual Download**:
- Click **Download PDF** on confirmation detail page
- Options:
  - Standard format (audit-ready)
  - Letterhead version (with institution branding)
  - Summary only
  - Full package (includes all correspondence)

**Bulk Download**:
- Select multiple confirmations (checkbox)
- Click **Download Selected**
- Generates ZIP file with all PDFs
- Includes manifest CSV for easy indexing

**Workpaper Integration**:
NextGen integrates with popular audit platforms:
- CaseWare
- CCH ProSystem fx
- Thomson Reuters CS Professional Suite
- Wolters Kluwer Teammate

Click **Send to Workpapers** to automatically file confirmation in your audit file.

### Exception Resolution

When you receive an exception:

1. **Review Smart Suggestions**:
   - NextGen AI analyzes the exception
   - Suggests likely corrections
   - Shows similar successfully completed confirmations

2. **Correction Options**:
   - **Quick Fix**: One-click correction for common issues
   - **Edit and Resubmit**: Modify details and resubmit
   - **Message Institution**: Send clarifying message
   - **Request Call**: Schedule phone call with institution

3. **Alternative Procedures**:
   - Platform tracks exception resolution methods
   - Suggests alternative audit procedures if needed
   - Links to audit standards for non-response situations

## Collaboration Features

### Team Management

**Assign Confirmations**:
- Assign individual confirmations to team members
- Set permission levels (View, Edit, Submit)
- Track who's responsible for follow-ups

**Workload View**:
- See team member confirmation load
- Rebalance assignments
- Identify bottlenecks

**Comments and Notes**:
- Add internal notes visible only to your team
- @mention team members for attention
- Thread conversations about tricky confirmations

### Client Collaboration

**Client Portal** (Optional Feature):
- Give clients read-only access to their confirmation status
- Reduces "status update" emails
- Clients can't see other clients' information

## Advanced Features

### Automated Reminders

Configure automatic follow-ups:
- First reminder: 7 days after submission (if no response)
- Second reminder: 12 days after submission
- Escalation: 15 days after submission (send to backup contact)

Customize reminder timing and content per institution.

### Performance Analytics

**Dashboard Metrics**:
- Response rate by institution (last 12 months)
- Average turnaround time
- Exception rate trends
- Success rate by signer
- Peak processing times

**Use Analytics to**:
- Identify which institutions respond fastest
- Submit to high-performers first during crunch time
- Avoid institutions with high exception rates

### Custom Templates

Create templates for recurring confirmation requests:
- Quarterly confirmations
- Monthly loan balance requests
- Year-end packages

Templates save:
- Client information
- Institution details
- Standard instructions
- Recipient contacts

## Mobile App Features

Download "TR Confirmations" from App Store or Google Play.

**Mobile Capabilities**:
- View confirmation status on the go
- Receive push notifications
- Download confirmation PDFs to device
- Scan and attach supporting documents
- Quick approve pending requests (Manager/Partner role)
- Emergency contact institution via in-app messaging

**Offline Mode**:
- View cached confirmations without internet
- Queue actions to sync when online

## Integration and API

### Audit Software Integration

Pre-built connectors for:
- **CCH ProSystem fx Engagement**: Direct engagement sync
- **CaseWare Cloud**: Automatic workpaper filing
- **Thomson Reuters CS Professional Suite**: Native integration
- **Wolters Kluwer Teammate**: Two-way data sync

### Custom API Integration

API documentation: https://confirmations-nextgen.thomsonreuters.com/api-docs

**Available Endpoints**:
- Create confirmation requests
- Query confirmation status
- Download confirmation PDFs
- Manage client and contact lists
- Retrieve analytics data

**Webhook Support**:
Register webhooks for real-time updates:
```json
POST /api/v2/webhooks
{
  "url": "https://your-firm.com/webhooks/confirmations",
  "events": [
    "confirmation.sent",
    "confirmation.opened",
    "confirmation.completed",
    "confirmation.exception"
  ],
  "secret": "your-webhook-secret-key"
}
```

## Best Practices for NextGen

### Maximize Response Rates

1. **Use the Signer Directory**: Verified signers respond 60% faster
2. **Complete "Expected Balance" Field**: Helps institutions validate quickly
3. **Submit Before Wednesday**: Confirmations submitted Mon-Wed get faster responses
4. **Avoid Month-End**: Submit confirmations mid-month when possible

### Year-End Optimization

1. **Submit Early December**: Beat the rush, aim for December 1-10
2. **Use Expedited Priority**: Extra fee is worth faster turnaround
3. **Pre-Stage Templates**: Have all client info ready before December
4. **Schedule Follow-Ups**: Use automated reminder feature aggressively

### Reduce Exceptions

1. **Verify Account Numbers**: Double-check with client before submitting
2. **Use Previous Confirmations**: Reference last year's successful confirmation
3. **Complete Optional Fields**: More information = fewer exceptions
4. **Update Contact Information**: Keep signer contacts current year-round

## Troubleshooting

### Cannot Login

**Solutions**:
- Clear browser cache and cookies
- Try incognito/private browsing mode
- Reset MFA device in account settings
- Contact support to reset password

### Confirmation Stuck in "Sent" Status

**After 48 Hours**:
1. Check "Opened" status - if not opened, institution may not have received it
2. Use "Resend Email" feature
3. Verify signer email address is correct
4. Contact institution's confirmation department directly

**NextGen Advantage**: Platform provides alternate contacts for major institutions

### Unable to Download PDF

**Solutions**:
- Disable popup blockers for confirmations-nextgen.thomsonreuters.com
- Try different browser (Chrome recommended)
- Check if PDF was already downloaded (check Downloads folder)
- Contact support if corrupted file

### Bulk Upload Failing

**Common Issues**:
- File format must be .xlsx or .csv (not .xls)
- Date format must be YYYY-MM-DD
- No blank rows in data range
- Special characters in account numbers may need escaping
- File size limit: 10 MB

**Solution**: Download a fresh template and copy data carefully

## Support and Training

### Technical Support

- **Email**: NextGenSupport@thomsonreuters.com
- **Phone**: 1-800-555-NEXT (1-800-555-6398)
- **Live Chat**: Available 8 AM - 10 PM EST, Monday-Friday
- **Response Time**: < 1 hour for urgent issues, < 4 hours for standard

### Training Resources

- **Interactive Tutorials**: Built into platform (Help → Guided Tours)
- **Video Library**: 50+ how-to videos
- **Webinars**: Weekly live training sessions
- **Certification Program**: Become a NextGen Power User (free)

### Community

- **User Forum**: Share tips with other audit firms
- **Feature Requests**: Vote on upcoming features
- **Release Notes**: Monthly platform updates
- **User Conference**: Annual TR Confirmations Summit

## Pricing

Contact ConfirmationRequestHelp@thomsonreuters.com for pricing details.

**Typical Plans**:
- **Starter**: $2,000/year + $5 per confirmation
- **Professional**: $10,000/year, includes 500 confirmations
- **Enterprise**: $50,000/year, unlimited confirmations + API access
- **Volume Discounts**: Available for 1,000+ confirmations/year

**Free Trial**: 30 days, up to 25 confirmations

## Migration from CurrentGen

If you're migrating from CurrentGen:

1. **Your data is safe**: All historical confirmations migrate automatically
2. **Training provided**: Free 1-hour onboarding webinar
3. **Parallel access**: Run both platforms during transition period (optional)
4. **No data re-entry**: Client and contact lists transfer automatically
5. **Same support team**: Your account manager remains your contact

**Migration Timeline**: Most firms complete transition in 1-2 weeks.
