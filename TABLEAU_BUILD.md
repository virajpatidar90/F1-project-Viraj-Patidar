# Native Tableau build specification

This is an implementation plan, not evidence that a Tableau workbook exists.

## Connect and validate

Connect to `data/prepared/race_results.csv`. Set `race_date` to Date, `season` to a discrete integer dimension, IDs/driver/team/reasons/compounds to strings, and points/flags to numeric measures. Set `country` geographic role to Country/Region. Use the separate `circuits.csv` for catalog coverage and `championship_standings.csv` for annual standings.

The original five-sheet workbook is also available. Use logical relationships, not physical fact-to-fact joins. Validate a circuit relationship on `circuit_id`. Keep lap/qualifying detail independent until incompatible identities have been resolved. `race_id + driver` is not unique: Carlos Sainz appears for two teams. The prepared race key includes team.

## Calculations

```text
DNF Count: SUM([dnf])
Completion Rate: 1 - SUM([dnf]) / SUM([race_entry])
Race Entries: SUM([race_entry])
Distinct Races: COUNTD([race_id])
Podium Count: SUM([podium_flag])
DNF Reason Display: IFNULL([dnf_reason], "Finished")
Points Cumulative: RUNNING_SUM(SUM([points]))
```

Points Cumulative: order by chronological race date, partition by driver and season. A yearly standings total must never be repeatedly summed over race rows.

Create `Top N Parameter`, Integer, range 1-19, step 1, current 10. Configure the Driver dimension's Top filter to Top `[Top N Parameter]` by SUM(points). Put season and any population filters in context so Top N is evaluated within the selected data. Show the parameter on the dashboard.

## Worksheets

1. **KPIs**: COUNTD(team), COUNTD(season), SUM(race_entry), and catalog COUNTD(circuit_id) from circuits. Label the last `Catalog circuits (29)`. An active/filtered circuit KPI from race_results is 24 at baseline. Counts from different sources must not masquerade as a single filtered population.
2. **Global participation**: country geographic role, map marks, size COUNTD(driver), tooltip COUNTD(race_id). Title `Participating drivers by host country`. Do not label this driver nationality.
3. **Driver reliability**: driver rows; SUM(dnf) columns; dnf_reason on Color. Filter dnf=1; show actual six reason categories. Tooltip includes completion rates from the all-entry population, not the DNF-only denominator (use a separate rate source/view if necessary).
4. **Driver leaderboard**: driver columns; SUM(points) rows; descending sort; vertical bars; Top N parameter.
5. **Team ranking**: team rows; SUM(points) columns; descending; horizontal bars.
6. **Championships**: separate championship source; discrete season and team columns; SUM(points) rows; grouped bars; season filter only.
7. **Starting tyre usage**: Pie; starting_compound Color; SUM(race_entry) Angle and label percentage of total. All-data denominator 6,464.
8. **Host participation**: Treemap; country Color/Label; COUNTD(race_id) Size. Count distinct events, not entries.
9. **Podiums**: packed bubbles; driver and team Detail; SUM(podium_flag) Size; team Color; exclude zero podiums.

## Dashboard and story

Dark background `#0A0C10`, panels `#141922`, red `#EF3340`, white labels. Keep text at least 11 pt. Title row, KPI/filter row, paired geography/reliability and driver/team rows, final championship/tyre/country/podium row. Add phone layout with vertically stacked panels. Include source-quality note and clear filter scope. Use original visual styling rather than pretending an unofficial project is an official F1 product.

Add nine story points corresponding to the nine views. Caption each with scope, finding and interpretation. Use the findings in the report; do not introduce unsupported causal claims.

## Verification and handoff

- Baseline points 31,906; DNFs 396; completion 93.873762%; podiums 940.
- Max Verstappen 4,640 points; Lewis Hamilton 4,491; Red Bull Racing 8,006; Mercedes 7,790.
- Test parameter 1, 10, 19; individual/all seasons; all six failure categories; reset; empty population.
- DNF category selection should not imply filtering annual standings by unavailable reason data.
- Compare selected-season totals directly with prepared CSV aggregation.
- Measure initial load and ten filter interactions. Record hardware/browser and median/max duration. Do not mark this tested before observing the native view.
- Publish and download the packaged workbook; supply the actual dashboard/story URLs to Flask.

References: https://help.tableau.com/current/pro/desktop/en-us/relate_tables.htm and https://help.tableau.com/current/pro/desktop/en-us/filtering_context.htm
