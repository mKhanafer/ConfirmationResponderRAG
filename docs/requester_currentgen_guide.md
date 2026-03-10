# Requester Guide: CurrentGen Platform

## Overview

This guide helps Auditor firms (Requesters) submit and manage confirmation requests using the Thomson Reuters CurrentGen Confirmation platform.

**Target Audience**: Audit professionals and audit firm IT staff

**Platform Status**: CurrentGen is currently in production. NextGen migration is optional but recommended.

## Getting Started

### Account Setup

1. **Register Your Firm**: Contact Thomson Reuters to set up your audit firm account
2. **Add Team Members**: Invite audit team members with appropriate role permissions
3. **Configure Client List**: Import your audit client companies

### User Roles

- **Partner**: Full access, can approve all confirmation requests
- **Manager**: Create and submit requests, view all team confirmations
- **Senior/Staff**: Create draft requests, view assigned confirmations only
- **Observer**: Read-only access for quality review

## Submitting Confirmation Requests

### Step 1: Create New Request

1. Navigate to **Dashboard** → **New Confirmation Request**
2. Select your audit client from the dropdown
3. Choose the financial institution (bank) to send the request to

### Step 2: Enter Request Details

**Required Information**:
- **Account Holder Name**: Exact legal name on the account
- **Account Number**: Full account number (will be partially masked in confirmations)
- **Account Type**: Checking, Savings, Loan, Credit Card, Investment, etc.
- **As-of Date**: Date for which balance should be confirmed (typically year-end)
- **Currency**: USD, EUR, CAD, GBP, etc.

**Optional Information**:
- **Branch Name/Address**: If known, helps bank locate account faster
- **Special Instructions**: Any specific information needed for account identification
- **Internal Reference Number**: Your firm's engagement reference

### Step 3: Specify Recipient

Enter the **Signer Email Address** at the financial institution. This is typically:
- Chief Financial Officer (CFO)
- Treasurer
- Bank relationship manager
- Authorized account custodian

**Important**: Verify the email address is correct. Incorrect addresses will delay confirmations.

### Step 4: Set Due Date

- **Standard Timeline**: 2 weeks from submission
- **Year-End Rush Period** (Dec-Feb): Allow 3 weeks
- **Urgent Requests**: Contact the financial institution directly first

### Step 5: Review and Submit

1. Click **Preview** to review all details
2. Verify account information is accurate
3. Click **Submit Request**
4. Confirmation number will be generated (format: `CR-2026-XXXXXX`)

## Tracking Request Status

### Status Indicators

Requests move through the following statuses:

#### Pending
- Request has been created but not yet sent
- Can still edit or cancel
- **Action**: Review and submit when ready

#### Sent
- Request has been delivered to the financial institution
- Email sent to designated signer
- **Action**: Wait for response

#### In Progress
- Financial institution has opened/acknowledged the request
- Typically means they are preparing the response
- **Action**: No action needed, monitor for updates

#### Completed
- Response received from financial institution
- Balance confirmation or exception details provided
- **Action**: Download confirmation letter for audit workpapers

#### Exception
- Financial institution cannot complete the request
- Common reasons:
  - Account not found
  - Account closed
  - Incorrect account number
  - Missing authorization
- **Action**: Review exception reason and resubmit with corrections if needed

#### Cancelled
- Request was cancelled before completion
- Can be cancelled by requester or financial institution
- **Action**: Create new request if still needed

### Dashboard Views

**My Confirmations**: Shows only confirmations you created

**Team Confirmations**: Shows all confirmations for your engagement or firm (role-dependent)

**Filter Options**:
- Status (Pending, Sent, Completed, etc.)
- Client name
- Date range
- Financial institution
- Assigned auditor

## Managing Responses

### Downloading Confirmations

1. Navigate to the confirmation detail page
2. Click **Download PDF** to get the official confirmation letter
3. Save to your audit workpapers system

**PDF Format**:
- Official Thomson Reuters header
- Financial institution letterhead and signature
- Account details and balance information
- Unique confirmation ID for verification
- Timestamp and audit trail

### Handling Exceptions

If a request returns an exception:

1. **Review the Exception Reason**:
   - Account number mismatch → Verify correct account number with client
   - Signer unauthorized → Get correct signer contact from client
   - Account closed → Confirm with client, update records
   - Additional documentation needed → Provide requested information

2. **Resubmit the Request**:
   - Click **Create Follow-up Request**
   - Correct the identified issue
   - Add notes explaining the correction
   - Submit the updated request

3. **Alternative Procedures**:
   - If repeated exceptions occur, consider alternative audit procedures
   - Direct contact with financial institution may be needed
   - Document exception resolution in audit workpapers

## Best Practices

### Before Submitting

- **Verify client information** is current and accurate
- **Confirm account numbers** with your client before submitting
- **Check signer details** - use the most recent contact information
- **Submit early** - don't wait until the last minute, especially during year-end

### During Year-End Rush (December - February)

- **Submit by mid-December** for year-end confirmations
- **Follow up proactively** if no response after 1 week
- **Have backup procedures** ready for non-responsive institutions
- **Communicate with clients** about potential delays

### Multi-Account Confirmations

For clients with multiple accounts at the same institution:
- **Option 1**: Submit separate requests for each account (recommended for large clients)
- **Option 2**: List all accounts in special instructions of a single request
- Consult with the financial institution's preference if known

### International Confirmations

When requesting confirmations from non-US institutions:
- **Time Zones**: Account for business hour differences
- **Holidays**: Check local holiday calendars
- **Language**: Platform supports English, Spanish, French, German
- **Currency**: Ensure correct currency code is selected

## Troubleshooting

### Request Not Received by Institution

**Symptoms**: Status remains "Sent" for more than 48 hours, no acknowledgment

**Solutions**:
1. Verify the signer email address is correct
2. Ask signer to check spam/junk folders
3. Contact institution's confirmation department directly
4. Use "Resend Email" function in platform

### Cannot Find My Confirmation

**Solutions**:
1. Use search function - enter confirmation number, account number, or client name
2. Check filters - status filter may be hiding the request
3. Check "Team Confirmations" if you're looking for another team member's request
4. Contact support if confirmation has disappeared

### Signer Hasn't Responded

**Timeline Guidelines**:
- **After 1 week**: Send a polite follow-up email (available in platform)
- **After 10 days**: Call the signer directly
- **After 2 weeks**: Escalate to institution's confirmation department
- **After 3 weeks**: Consider alternative audit procedures

### Need to Update Submitted Request

**Limited Updates Available**: Once submitted, you cannot change core details (account number, client name)

**Options**:
1. Cancel the original request and create a new one with corrections
2. Add clarifying notes in the "Messages" section
3. Contact the financial institution directly to provide additional information

## Support and Resources

### Platform Support
- **Email**: ConfirmationRequestHelp@thomsonreuters.com
- **Phone**: 1-800-555-CONF (1-800-555-2663)
- **Hours**: Monday-Friday, 8 AM - 8 PM EST
- **Response Time**: 24 hours for email, immediate for phone

### Training Resources
- **Video Tutorials**: Available in Help Center
- **Webinars**: Monthly training sessions (register via platform)
- **User Guide PDF**: Download from Help → Documentation

### Audit Firm Administrator

Your firm's platform administrator can help with:
- User access and permissions
- Firm-wide settings and preferences
- Bulk operations
- Custom reporting
- Integration with audit software

Contact your firm's IT department or administrator for assistance.

## Frequently Asked Questions

### How long does a typical confirmation take?
**Standard**: 7-10 business days. Year-end period can take 2-3 weeks.

### Can I see confirmations from previous years?
**Yes**: All historical confirmations are archived and accessible via the Search function.

### What if the bank doesn't use the platform?
**Manual Process**: You'll need to send a traditional paper confirmation letter. Platform can generate the letter template for you.

### Is there a cost per confirmation?
**Pricing Varies**: Contact your Thomson Reuters account manager for pricing details. Most audit firms have annual subscription plans.

### Can I submit the same request to multiple signers?
**Not directly**: Create separate requests for each signer if you need redundancy.

### What happens if I enter the wrong account number?
**Before Submission**: Edit the request before submitting
**After Submission**: Cancel and resubmit with correct information

### How secure is the platform?
**Enterprise Security**: SOC 2 Type II certified, encrypted transmission, multi-factor authentication available, audit trail for all actions.
