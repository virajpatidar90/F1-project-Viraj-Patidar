"""Reproducible, non-destructive preparation of the supplied teaching dataset."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data' / 'F1 Racing Project Dataset.xlsx'
OUT = ROOT / 'data' / 'prepared'
OUT.mkdir(exist_ok=True)
sheets = pd.read_excel(SOURCE, sheet_name=None)
r = sheets['race_results'].copy()
r['race_date'] = pd.to_datetime(r['race_date'], errors='raise')
assert not r.duplicated(['race_id', 'driver', 'team']).any(), 'Duplicate race-driver-team grain'
assert not sheets['circuits']['circuit_id'].duplicated().any()
assert set(r.circuit_id) <= set(sheets['circuits'].circuit_id)
assert set(r.dnf.unique()) <= {0, 1}
assert r.loc[r.dnf.eq(1), 'finish_position'].isna().all()
assert r.loc[r.dnf.eq(1), 'dnf_reason'].notna().all()
r['dnf_reason_display'] = r['dnf_reason'].fillna('Finished')
r['podium_flag'] = r.finish_position.between(1, 3).astype(int)
r['race_entry'] = 1
r['completed_flag'] = 1 - r.dnf
r['race_driver_key'] = r.race_id + '|' + r.driver + '|' + r.team
# Preserve missing finish position and gap. Missing is not zero.
r.to_csv(OUT / 'race_results.csv', index=False, date_format='%Y-%m-%d')
for name, frame in sheets.items():
    if name != 'race_results':
        frame.to_csv(OUT / (name + '.csv'), index=False)
drivers = r.groupby('driver').agg(points=('points','sum'), starts=('race_id','size'), dnfs=('dnf','sum'), podiums=('podium_flag','sum'))
drivers['completion_rate'] = 1 - drivers.dnfs / drivers.starts
drivers['points_per_start'] = drivers.points / drivers.starts
drivers.sort_values('points',ascending=False).to_csv(OUT / 'driver_summary.csv')
teams = r.groupby('team').agg(points=('points','sum'), starts=('race_id','size'), dnfs=('dnf','sum'), podiums=('podium_flag','sum'))
teams['completion_rate'] = 1 - teams.dnfs / teams.starts
teams.sort_values('points',ascending=False).to_csv(OUT / 'team_summary.csv')
r.groupby(['season','team'],as_index=False).agg(points=('points','sum')).to_csv(OUT/'team_season_race_points.csv',index=False)
sheets['championship_standings'].groupby(['season','team'],as_index=False).agg(points=('points','sum')).to_csv(OUT/'team_season_standings.csv',index=False)
r.groupby(['driver','dnf_reason_display'],as_index=False).agg(entries=('race_id','size'),dnfs=('dnf','sum')).to_csv(OUT/'reliability.csv',index=False)
r.groupby('country').agg(race_entries=('race_id','size'),grand_prix=('race_id','nunique'),distinct_drivers=('driver','nunique')).to_csv(OUT/'country_summary.csv')
r.groupby('starting_compound').agg(entries=('race_id','size'),mean_points=('points','mean'),dnfs=('dnf','sum')).to_csv(OUT/'tyre_summary.csv')
r[r.podium_flag.eq(1)].groupby(['driver','team']).size().rename('podiums').to_csv(OUT/'podium_summary.csv')
comparison = r.groupby(['season','driver']).points.sum().rename('race_points').reset_index().merge(sheets['championship_standings'][['season','driver','points']],on=['season','driver'],how='outer',indicator=True)
comparison['difference'] = comparison['race_points'] - comparison['points']
comparison.to_csv(OUT/'standings_reconciliation.csv',index=False)
audit = {
    'source_url':'https://docs.google.com/spreadsheets/d/1x-RIZzVA_9xfKgnXQgBv8s9pANqzgiNJ/edit',
    'sheets':{n:{'rows':len(f),'columns':len(f.columns),'duplicate_rows':int(f.duplicated().sum()),'nulls':{c:int(v) for c,v in f.isna().sum().items() if v}} for n,f in sheets.items()},
    'combined_rows':sum(len(f) for f in sheets.values()),
    'metrics':{'race_entries':len(r),'distinct_races':int(r.race_id.nunique()),'seasons':int(r.season.nunique()),'teams':int(r.team.nunique()),'drivers':int(r.driver.nunique()),'catalog_circuits':len(sheets['circuits']),'active_circuits':int(r.circuit_id.nunique()),'host_countries':int(r.country.nunique()),'dnfs':int(r.dnf.sum()),'completion_rate':float(1-r.dnf.mean()),'podiums':int(r.podium_flag.sum()),'points':int(r.points.sum())},
    'dnf_reasons':r.loc[r.dnf.eq(1),'dnf_reason'].value_counts().to_dict(),
    'date_min':str(r.race_date.min().date()),'date_max':str(r.race_date.max().date()),
    'standings_mismatches':int(comparison['difference'].fillna(1).ne(0).sum()),
    'duplicate_race_driver_keys':int(r.duplicated(['race_id','driver']).sum()),
    'standings_missing_matches':comparison['_merge'].value_counts().to_dict(),
    'notes':[
        'The source contains contemporary drivers in 2010 and placeholder Driver_N/Team_N qualifying values. Treat results as supplied educational data, not verified historical Formula 1 results.',
        'country is the race host country; no driver nationality column is present. The map measures driver participation in host countries, not nationality.',
        '29 circuits exist in the catalog, but only 24 occur in race_results.',
        'race_results has 42 original columns, not the 41 stated in the brief.',
        'starting_compound counts one starting tyre compound per race entry. It is not the count of all tyres or laps used.',
        'Keep annual championship standings separate from race-level data. Never join the two facts on season alone.',
        'Carlos Sainz occurs for Ferrari and Williams within the same races (334 repeated race-driver keys). Preserve distinct source entries but disclose this source anomaly. Driver totals aggregate both teams.',
        'Race data grain is race_id + driver + team. Qualifying requires the same keys; lap data lacks team and must remain separate to avoid ambiguous links.'
    ]
}
(ROOT/'data'/'audit.json').write_text(json.dumps(audit,indent=2,default=int),encoding='utf-8')
print(json.dumps(audit,indent=2,default=int))
print('\nDRIVER LEADERS\n',drivers.sort_values('points',ascending=False).head().to_string())
print('\nTEAM LEADERS\n',teams.sort_values('points',ascending=False).head().to_string())
