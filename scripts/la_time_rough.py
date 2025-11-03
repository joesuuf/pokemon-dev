import sys
from datetime import datetime, timezone

def _to_la(dt_utc: datetime) -> datetime:
    try:
        from zoneinfo import ZoneInfo
        la = ZoneInfo("America/Los_Angeles")
        return dt_utc.astimezone(la)
    except Exception:
        try:
            import pytz
            la = pytz.timezone("America/Los_Angeles")
            return pytz.utc.localize(dt_utc.replace(tzinfo=None)).astimezone(la)
        except Exception:
            # Fallback: return UTC if tzdata is unavailable
            return dt_utc

def _format_la_timestamp(dt_la: datetime) -> str:
    return dt_la.strftime("%Y%m%d-%H%M%S")

def cloudflare_close_time_utc() -> datetime:
    try:
        import ntplib
        client = ntplib.NTPClient()
        # Cloudflare NTP host; NTP gives a close approximation for naming
        response = client.request("time.cloudflare.com", version=3)
        return datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    except Exception:
        # Fallback to local UTC if NTP fails
        return datetime.now(timezone.utc)

def la_timestamp_from_cloudflare() -> str:
    dt_utc = cloudflare_close_time_utc()
    dt_la = _to_la(dt_utc)
    return _format_la_timestamp(dt_la)

def notebook_name(branch_alias: str) -> str:
    ts = la_timestamp_from_cloudflare()
    return f"{branch_alias}-{ts}.ipynb"

if __name__ == "__main__":
    branch = sys.argv[1] if len(sys.argv) > 1 else "dev"
    print(notebook_name(branch))