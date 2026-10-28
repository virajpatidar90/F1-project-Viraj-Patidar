from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parent
sys.path.append(str(ROOT/'.packages'))
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'output/figures'; FIG.mkdir(parents=True,exist_ok=True)
P=ROOT/'data/prepared'
r=pd.read_csv(P/'race_results.csv'); a=json.loads((ROOT/'data/audit.json').read_text())
plt.rcParams.update({'figure.facecolor':'#111722','axes.facecolor':'#111722','text.color':'#ffffff','axes.labelcolor':'#d5dce5','xtick.color':'#c2ccda','ytick.color':'#c2ccda','axes.edgecolor':'#455066','font.size':10,'savefig.facecolor':'#111722'})
def save(name):
    plt.tight_layout(pad=1.6); plt.savefig(FIG/(name+'.png'),dpi=160); plt.close()
d=pd.read_csv(P/'driver_summary.csv').sort_values('points',ascending=False).head(10)
fig,ax=plt.subplots(figsize=(10,4.5)); ax.bar(d.driver,d.points,color='#ef3340');ax.set_ylabel('Cumulative points');ax.tick_params(axis='x',rotation=38); save('drivers')
t=pd.read_csv(P/'team_summary.csv').sort_values('points')
fig,ax=plt.subplots(figsize=(10,4.5));ax.barh(t.team,t.points,color='#ef3340');ax.set_xlabel('Cumulative race points');save('teams')
pivot=r[r.dnf.eq(1)].pivot_table(index='driver',columns='dnf_reason',values='dnf',aggfunc='sum',fill_value=0)
fig,ax=plt.subplots(figsize=(10,5));pivot.plot.barh(stacked=True,ax=ax,colormap='Set2');ax.legend(loc='upper center',bbox_to_anchor=(.5,1.15),ncol=3,facecolor='#111722',labelcolor='white',fontsize=8);ax.set_xlabel('DNF entries');ax.set_ylabel('');save('reliability')
cs=pd.read_csv(P/'team_season_standings.csv');cs=cs[cs.team.isin(['Red Bull Racing','Mercedes','Ferrari'])]
fig,ax=plt.subplots(figsize=(10,4.5));cs.pivot(index='season',columns='team',values='points').plot.bar(ax=ax,color=['#ef3340','#59ddd1','#708af2']);ax.set_ylabel('Season championship points');ax.legend(facecolor='#111722',labelcolor='white',fontsize=9);save('championship')
ty=pd.read_csv(P/'tyre_summary.csv');fig,ax=plt.subplots(figsize=(8,4.5));ax.pie(ty.entries,labels=ty.starting_compound,autopct='%1.1f%%',colors=['#dfe5ed','#7cc59e','#f0c75e','#ef3340'],textprops={'fontsize':11});save('tyres')
country=pd.read_csv(P/'country_summary.csv').sort_values('grand_prix',ascending=False)
fig,ax=plt.subplots(figsize=(10,4.5));ax.bar(country.country,country.grand_prix,color='#7793ff');ax.tick_params(axis='x',rotation=55);ax.set_ylabel('Distinct Grand Prix');save('countries')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleF1',fontName='Helvetica-Bold',fontSize=30,leading=34,textColor=colors.HexColor('#161d2b'),spaceAfter=18))
styles.add(ParagraphStyle(name='Kicker',fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=colors.HexColor('#cf2336'),spaceAfter=12))
styles['BodyText'].fontSize=10;styles['BodyText'].leading=15;styles['BodyText'].spaceAfter=9
styles['Heading1'].fontSize=20;styles['Heading1'].leading=25;styles['Heading1'].textColor=colors.HexColor('#162133')
styles['Heading2'].fontSize=13;styles['Heading2'].leading=18
story=[]
def p(s):story.append(Paragraph(s,styles['BodyText']))
def h(s):story.append(Paragraph(s,styles['Heading1']));story.append(Spacer(1,10))
def sub(s):story.append(Paragraph(s,styles['Heading2']))
def table(rows,widths=None):
    cells=[[Paragraph(str(v),styles['BodyText']) for v in row] for row in rows]
    obj=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    obj.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8edf4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#ef3340')),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6)]));story.append(obj)
def chart(name,height=225):story.append(Image(str(FIG/(name+'.png')),width=490,height=height));story.append(Spacer(1,10))
def page():story.append(PageBreak())
story.append(Paragraph('SKILLWALLET CAPSTONE / DATA ANALYTICS WITH TABLEAU',styles['Kicker']))
story.append(Paragraph('Formula 1<br/>Race Intelligence',styles['TitleF1']))
p('Analysis and implementation documentation | 2010-2026')
p('Revised version prepared by Viraj Patidar | 28 October 2026')
story.append(Spacer(1,20))
table([['Race entries','Distinct races','Seasons','Teams'],['6,464','334','17','10']],[125,125,125,115])
story.append(Spacer(1,20))
sub('Executive finding')
p('In the supplied dataset, Max Verstappen leads cumulative driver points with 4,640, ahead of Lewis Hamilton at 4,491. Red Bull Racing leads team points with 8,006, while Mercedes has more podium entries (289 versus 284) and a higher completion rate (95.66% versus 93.11%).')
p('There are 396 DNF entries, giving a completion rate of 93.87%. Engine is the largest recorded DNF category, with 73 entries (18.43% of DNFs). These are descriptive associations, not causal findings.')
sub('Scope and completion status')
p('Completed: source inspection, reproducible preparation, metric reconciliation, analytical figures, report, story plan, demonstration script and Flask integration code. Pending: native Tableau workbook/dashboard/story creation, Tableau performance measurements, Tableau Public publication, final embedding verification, recorded demonstration, GitHub publication and SkillWallet submission.')
p('The supplied file contains internal anomalies and appears to be educational or simulated. Results describe this file and must not be presented as verified historical Formula 1 statistics. Charts in this report were generated with Python; they are not screenshots of a completed Tableau workbook.')
page();h('01 / Problem and approach')
sub('Business problem')
p('A race strategist needs to compare teams, understand reliability and inspect starting tyre patterns. A broadcaster needs fast driver and podium summaries. A technical analyst needs failure-category counts and completion rates. The project turns five source sheets into consistent metrics and an interactive Tableau analysis.')
sub('Business requirements')
p('Provide nine analytical views, four prominent KPI cards, a season filter, DNF-reason filtering and a Top N driver parameter. Preserve source data, separate incompatible fact grains, document missing values, publish the dashboard and story, and expose both through Flask.')
sub('Literature and method')
p('Tableau recommends relationships for tables at different levels of detail because joins can duplicate measures. This source requires particular caution: annual standings, race entries, qualifying rows and sampled lap records do not have interchangeable keys. The initial race analysis therefore uses the race fact with validated circuit metadata, while annual standings remain separate.')
p('Tableau context filters are evaluated before Top N filters. Season and applicable DNF filters should be put in context for a Top N-by-points implementation, so the ranking reflects the selected population. The Top N parameter defaults to 10 and should accept integers from 1 through 19.')
sub('Expected value')
p('The analysis can support comparative questions and communication. Completion rates should accompany failure counts because exposure differs by driver. Tyre choice is confounded by weather, circuit and team, so starting-compound comparisons cannot establish a faster strategy. Host-country data cannot identify driver nationality or national talent pools.')
sub('Sources')
p('Dataset: <link href="https://docs.google.com/spreadsheets/d/1x-RIZzVA_9xfKgnXQgBv8s9pANqzgiNJ/edit">SkillWallet F1 Racing Project Dataset</link>.')
p('Methods: <link href="https://help.tableau.com/current/pro/desktop/en-us/relate_tables.htm">Tableau: Relate Your Data</link>; <link href="https://help.tableau.com/current/pro/desktop/en-us/filtering_context.htm">Use Context Filters</link>; <link href="https://help.tableau.com/current/pro/desktop/en-us/public_faq.htm">Tableau Public FAQ</link>. Accessed 27 October 2026.')
page();h('02 / Collection and data quality')
table([['Sheet','Rows','Columns']]+[[n,f['rows'],f['columns']] for n,f in a['sheets'].items()],[295,95,95])
p('Combined rows: 13,748. Race-date coverage: 1 March 2010 to 2 August 2026. The final season is only covered through the last date supplied; do not imply a complete 2026 championship.')
sub('Validation results')
for text in [
 'No completely identical rows exist in any source sheet. Race-entry keys are unique only when team is included: race_id + driver + team.',
 'Carlos Sainz appears for Ferrari and Williams in the same races, producing 334 repeated race-driver keys. Preserve the distinct records because no correction authority is supplied; disclose that driver aggregation combines both teams.',
 'The circuit catalog contains 29 circuits; 24 occur in the race fact. Label the catalog KPI accurately, and use active circuits for a filtered race KPI.',
 'There are 396 missing finish positions and gaps, corresponding to DNFs. Retain them as missing; filling them with zero would create false finishing positions or fastest gaps.',
 'The 6,068 empty DNF reasons belong to completed entries. The prepared display category is Finished. The underlying DNF flag is preserved.',
 'Total race time is missing in 6,130 rows, so it is not suitable for a universal average race-time KPI.',
 'All 311 driver-season aggregates reconcile to championship_standings points. Team allocation should use the appropriate source because a driver can have more than one team label.',
 'DNF labels actually present are Engine, Hydraulics, Mechanical, Brake failure, Gearbox and Collision. Do not replace these with the different list in the course description.'
]:p(text)
page();h('03 / Preparation and model')
sub('Reproducible procedure')
p('Run prepare_data.py against the untouched Excel source. It parses race_date, validates flags and circuit references, preserves null finish positions and gaps, adds display and indicator columns, exports each sheet to CSV and writes an audit JSON. It also creates independently reconciled driver, team, country, tyre, reliability and podium summaries.')
sub('Tableau data model')
p('Use race_results as the primary fact. Relate circuits many-to-one using circuit_id, or use the already supplied circuit columns after validation. Keep championship_standings independent for season totals. Do not physically join lap or qualifying records to race records on race_id alone. Qualifying needs race_id + driver + team; the lap sheet lacks team and therefore has ambiguous Carlos Sainz links. Keep it separate unless the source is corrected.')
sub('Calculated fields')
table([['Field','Tableau expression'],['DNF Count','SUM([dnf])'],['Completion Rate','1 - SUM([dnf]) / SUM([race_entry])'],['Podium Count','SUM([podium_flag])'],['Distinct Races','COUNTD([race_id])'],['DNF Reason Display','IFNULL([dnf_reason], "Finished")'],['Points Cumulative','RUNNING_SUM(SUM([points]))'],['Top N filter','Driver Top tab: Top [Top N Parameter] by SUM(points)']],[145,340])
p('For cumulative points, address race date in chronological order and partition by driver and season. Cumulative points are not the same as summing annual championship totals repeatedly.')
sub('Interaction rules')
p('Apply season to relevant race charts. DNF reason applies to race-based charts and should be labelled clearly; annual standings do not have a DNF-reason dimension and should remain season-filtered only. The Top N parameter affects only the driver leaderboard. Report filters on each chart so a filtered subset is not mistaken for all races.')
page();h('04 / Driver and team performance');chart('drivers')
p('Max Verstappen leads with 4,640 points, 149 ahead of Lewis Hamilton. Exposure matters: use points per recorded entry alongside lifetime totals. The Carlos Sainz source anomaly must be visible when interpreting driver rankings.')
chart('teams',215)
p('Red Bull Racing leads Mercedes by 216 cumulative race points. The ranking measures point accumulation in this supplied dataset, not current real-world form.')
page();h('05 / Reliability and championships');chart('reliability',245)
p('396 of 6,464 entries are DNFs. Engine accounts for 73, Hydraulics 70, Mechanical 67, Brake failure 64, Gearbox 62 and Collision 60. Use rates as well as counts to compare drivers with unequal starts.')
chart('championship',220)
p('This view uses annual standings rather than joining them repeatedly onto each race entry. Compare each season separately before interpreting cumulative leadership. The chart shows three benchmark teams; the Tableau view should permit all ten.')
page();h('06 / Tyres and geographic coverage');chart('tyres',220)
p('The pie chart counts starting_compound once per race entry. It does not describe every compound used during a race. Full stint usage requires another grain and cannot be inferred from this chart.')
chart('countries',220)
p('Country participation counts distinct race_id per host country. Race-entry counts would be inflated by the number of competitors. The geographic driver view should be labelled as distinct participating drivers by host nation, because driver nationality is absent.')
page();h('07 / Dashboard and story specification')
table([['Scene / view','Encoding and metric'],['1. Scale','Four KPI tiles: teams, seasons, race entries and catalog circuits; distinguish filtered active circuits.'],['2. Geography','Map of host country, COUNTD(driver). Tooltip includes COUNTD(race_id).'],['3. Reliability','Stacked bars by driver and actual DNF reason, SUM(dnf).'],['4. Driver leaderboard','Vertical bars, SUM(points), Top N controlled.'],['5. Team ranking','Horizontal bars, SUM(points), descending.'],['6. Championships','Grouped season/team bars from annual standings.'],['7. Tyres','Pie of starting_compound, SUM(race_entry).'],['8. Country participation','Treemap or highlight table, COUNTD(race_id).'],['9. Podiums','Packed bubbles, driver and team, SUM(podium_flag).']],[145,340])
sub('Layout')
p('Use a black background, red accents and white text. Place the title above the KPI row and global controls. The next rows contain geography/reliability, driver/team rankings, and championship/tyre/country/podium views. Add a short source-quality note. Configure a phone layout with readable labels and vertically stacked views.')
sub('Nine-scene narration')
p('Begin with the dataset scope and limitations. Move to host coverage, then explain reliability exposure. Compare the driver leaders, then contrast team points with podiums and completion. Inspect seasonal trajectories. Explain starting tyre share without causal claims. Distinguish events from participant records. Conclude with podium distribution and the need to validate the synthetic source before operational use.')
page();h('08 / Testing, publishing and demonstration')
sub('Completed data checks')
p('Row counts, key uniqueness at race-driver-team grain, circuit referential integrity, DNF flag domain, DNF null handling, and driver/team point reconciliation were executed. These checks establish data consistency within the documented source limitations. They do not establish real-world accuracy.')
sub('Tableau tests to execute after authoring')
p('Check all-data KPIs against 6,464 entries, 17 seasons and 10 teams; verify active circuits 24 and catalog circuits 29. Check Top N values 1, 10 and 19 after selecting a season. Select each DNF reason and verify sums against prepared data. Test empty selections and reset. Confirm all nine story scenes. Inspect desktop and phone layouts. Time initial load and ten filter interactions, then record median and maximum durations with the device/browser used. No Tableau rendering timings have been measured yet.')
sub('Web integration')
p('The Flask app serves the Tableau Embedding API view through separate dashboard and story tabs. Set TABLEAU_DASHBOARD_URL and TABLEAU_STORY_URL to the actual published /views/ URLs. Only HTTPS public.tableau.com view URLs are accepted. Until configured, the page explicitly reports that publication is pending. Never insert another author\'s dashboard as this project\'s output.')
sub('Publication and submission')
p('After authoring and checking the native workbook, publish it under the student\'s Tableau Public account, verify a signed-out viewer can use the filters, download the packaged workbook for GitHub, and add the actual demo and repository URLs in SkillWallet. Mark each task done only when its corresponding deliverable exists.')
sub('Demonstration recording')
p('Record a 5-7 minute screen-share: 0:00 introduction/problem; 0:45 dataset and quality issues; 1:45 preparation and model; 2:45 dashboard/filter demonstration; 4:30 story and insights; 5:30 Flask integration and conclusion. The accompanying script provides speaking notes. Recording and final screenshots remain pending native Tableau completion.')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#ef3340'));c.line(48,42,547,42)
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#657080'));c.drawString(48,28,'FORMULA 1 RACE INTELLIGENCE | Supplied educational dataset');c.drawRightString(547,28,str(doc.page))
SimpleDocTemplate(str(OUT/'F1_Race_Intelligence_Report.pdf'),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=55).build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT/'F1_Race_Intelligence_Report.pdf')
