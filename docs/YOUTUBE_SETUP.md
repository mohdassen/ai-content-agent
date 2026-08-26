# YouTube Shorts API setup

The project supports YouTube Data API v3 uploads through OAuth 2.0 and the resumable `videos.insert` flow.

## Safe defaults
- Publishing still requires the local approval state to be explicitly approved.
- `publish_latest.py` is dry-run unless `--live` is passed.
- YouTube live upload also requires `YOUTUBE_LIVE_UPLOAD=true`.
- Initial uploads are hard-coded to `private` while onboarding and API audit are incomplete.

## Google Cloud setup
1. Create/select a Google Cloud project.
2. Enable **YouTube Data API v3**.
3. Configure the OAuth consent screen.
4. Create OAuth credentials for the account/channel that owns the YouTube channel.
5. Authorize the scope:
   `https://www.googleapis.com/auth/youtube.upload`
6. Obtain a long-lived refresh token using offline access.

## GitHub Secrets
Add these repository Actions secrets:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

Optional temporary alternative:

- `YOUTUBE_ACCESS_TOKEN`

Do **not** commit credentials or tokens to the repository.

## Production lock
Even after credentials exist, uploads remain locked until:

- the content has explicit approval;
- the publisher is invoked with `--live`; and
- `YOUTUBE_LIVE_UPLOAD=true` is present in the execution environment.

## Verification note
YouTube restricts uploads from unverified API projects created after July 28, 2020 to private viewing. Google requires an API compliance audit before that restriction can be lifted.
