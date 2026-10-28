# Planned 5-7 minute demonstration

Record after the native Tableau dashboard/story is completed. Replace future-tense cues with the actual visible actions. Do not state that pending authoring or publishing has already happened.

## 0:00-0:45 - Introduction and problem

Hello, my name is Viraj Patidar. This project explores Formula 1 race intelligence using the dataset supplied for the SkillWallet Tableau capstone. The aim is to compare driver and team performance, identify reliability patterns, inspect starting tyre choices and communicate findings through a dashboard and a nine-scene story. The intended users are team strategists, broadcasters and technical analysts.

## 0:45-1:45 - Source and quality

Show the five-sheet Excel file and the audit. There are 13,748 combined rows. The main race sheet has 6,464 entries and 42 original columns, covering 334 race IDs and 17 seasons. A race entry is one recorded driver-team result, so it is not the same as a distinct race. The circuit catalog has 29 circuits but the race results contain 24. The data has anomalies, including Carlos Sainz listed for two teams in the same race. I preserved source entries and documented these limitations instead of guessing corrections. The findings describe the supplied teaching data, not verified historical results.

## 1:45-2:45 - Preparation and model

Show prepare_data.py and prepared CSVs. The workflow parses dates, validates keys and circuit references, retains DNF records, and preserves missing finish positions and gaps. It adds podium and completion flags and a clear display category for finished entries. Annual championship standings remain separate to avoid multiplying season totals through race-level joins. All 311 driver-season totals reconcile. Explain the Top N parameter and the role of context filters in ranking the selected season's drivers.

## 2:45-4:30 - Dashboard demonstration

Show the completed native Tableau dashboard. Begin with the four KPIs and explain the difference between catalog circuits and active race circuits. Demonstrate a season selection, a DNF category, Top N 5 and Top N 10, then reset. Explain the map as participating drivers by host country, not nationality. Show driver ranking and team ranking. In the unfiltered data Max Verstappen has 4,640 points, ahead of Lewis Hamilton by 149. Red Bull leads Mercedes by 216 points, but Mercedes has more podium entries and a higher completion rate. Show reliability categories; engine is the largest category with 73 of 396 DNFs. Point out why a failure rate is more informative than a raw count when drivers have different numbers of entries.

## 4:30-5:30 - Story and insights

Move through the nine story scenes. Explain how scale leads to geography, reliability, driver ranking, team ranking and annual trajectories. The tyre chart measures the starting compound per entry, not every tyre stint. Country participation counts distinct race IDs. Podium bubbles identify the distribution of podium entries across driver-team combinations. These comparisons are descriptive; tyre performance cannot be attributed causally without controlling for weather, circuits and team strength.

## 5:30-6:30 - Integration, testing and conclusion

Show the published Tableau URL and Flask page, switching between dashboard and story. Show the actual performance results and data checks. Explain that the app embeds the published interactive views and retains their filters. Conclude with the benefits of consistent definitions, preserving source quality issues, and verifying every headline metric. Show the real repository and submission links only after they exist.
