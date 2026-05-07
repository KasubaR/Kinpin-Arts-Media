# Kinpin-Arts-Media

## Mailchimp Newsletter Setup

Set the following environment variables to enable newsletter sync with Mailchimp:

- `MAILCHIMP_API_KEY`
- `MAILCHIMP_AUDIENCE_ID`
- `MAILCHIMP_SERVER_PREFIX` (example: `us21`)
- `MAILCHIMP_DOUBLE_OPTIN` (`true` by default)

If any required Mailchimp value is missing, the site still accepts newsletter signups locally and stores them in the database.
If your Mailchimp free-tier contact limit is reached, signups are retained locally so leads are not lost.
