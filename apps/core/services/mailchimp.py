import json
from dataclasses import dataclass
from urllib import error, request


CONTACT_LIMIT_TITLES = {
    'Member In Compliance State',
    'Resource Not Found',
}


@dataclass(frozen=True)
class MailchimpSyncResult:
    success: bool
    status: str
    message: str = ''


def subscribe_email(*, email: str, api_key: str, audience_id: str, server_prefix: str, double_optin: bool) -> MailchimpSyncResult:
    endpoint = f'https://{server_prefix}.api.mailchimp.com/3.0/lists/{audience_id}/members'
    payload = {
        'email_address': email,
        'status_if_new': 'pending' if double_optin else 'subscribed',
        'status': 'subscribed',
    }
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with request.urlopen(req, timeout=10) as resp:
            if 200 <= resp.status < 300:
                return MailchimpSyncResult(success=True, status='synced')
    except error.HTTPError as exc:
        body = _safe_decode(exc.read())
        detail = _parse_error_detail(body)
        title = detail.get('title', '')
        error_message = detail.get('detail', '')

        if exc.code == 400 and title == 'Member Exists':
            return MailchimpSyncResult(success=True, status='already_synced')
        if _is_contact_limit_error(exc.code, title, error_message):
            return MailchimpSyncResult(success=False, status='contact_limit', message=error_message)
        return MailchimpSyncResult(success=False, status='failed', message=error_message)
    except (error.URLError, TimeoutError):
        return MailchimpSyncResult(success=False, status='failed', message='Could not reach Mailchimp.')

    return MailchimpSyncResult(success=False, status='failed')


def _safe_decode(body: bytes) -> str:
    try:
        return body.decode('utf-8')
    except UnicodeDecodeError:
        return ''


def _parse_error_detail(body: str) -> dict:
    try:
        payload = json.loads(body) if body else {}
    except json.JSONDecodeError:
        payload = {}
    return {
        'title': payload.get('title', ''),
        'detail': payload.get('detail', ''),
    }


def _is_contact_limit_error(status_code: int, title: str, detail: str) -> bool:
    if status_code not in {400, 403}:
        return False
    detail_lower = detail.lower()
    return (
        title in CONTACT_LIMIT_TITLES
        or 'contact limit' in detail_lower
        or 'upgrade' in detail_lower and 'plan' in detail_lower
        or 'max contacts' in detail_lower
    )
