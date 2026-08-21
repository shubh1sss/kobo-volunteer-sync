# KoboToolbox → Form 2 Automatic Volunteer List

This package keeps `volunteers.csv` synchronized with Form 1 submissions.

Flow:
Form 1 submission → Kobo API → GitHub Actions → volunteers.csv → Form 2 Select One from File

## Required Kobo fields
The script reads:
- volunteer_id
- volunteer_name
- investigator_id
- investigator_name

## GitHub setup
1. Create a private GitHub repository.
2. Put `update_volunteers.py`, `.github/workflows/update-volunteers.yml`, and `volunteers.csv` in the repository.
3. In the repository, open Settings → Secrets and variables → Actions → New repository secret.
4. Create:
   - KOBO_API_KEY = your Kobo API key
   - KOBO_ASSET_UID = Form 1 asset UID
5. Run the workflow manually once from Actions to test it.
6. The workflow then runs every 5 minutes.

## Kobo Form 2 setup
Your XLSForm should continue to use:
select_one_from_file volunteers.csv

In Form 2 → Settings → Media, remove the manually uploaded `volunteers.csv` if present, then add the direct RAW URL of the repository's `volunteers.csv`.

The raw URL must end in `/volunteers.csv`.

Then redeploy Form 2.

Kobo may cache the external file briefly; Kobo's documentation says updates at the same URL are reflected after a short delay and recommends regular redeployment for more consistent updates.

## Security
Never put the Kobo API key inside the script or CSV.
Store it only as a GitHub Actions secret.
Do not send the API key to ChatGPT or anyone else.
