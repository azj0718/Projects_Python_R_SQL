# Project 1: Query Project

- In the Query Project, you will get practice with SQL while learning about
  Google Cloud Platform (GCP) and BiqQuery. You'll answer business-driven
  questions using public datasets housed in GCP. To give you experience with
  different ways to use those datasets, you will use the web UI (BiqQuery) and
  the command-line tools, and work with them in Jupyter Notebooks.

#### Problem Statement

- You're a data scientist at Lyft Bay Wheels (https://www.lyft.com/bikes/bay-wheels), formerly known as Ford GoBike, the
  company running Bay Area Bikeshare. You are trying to increase ridership, and
  you want to offer deals through the mobile app to do so. 
  
- What deals do you offer though? Currently, your company has several options which can change over time.  Please visit the website to see the current offers and other marketing information. Frequent offers include: 
  * Single Ride 
  * Monthly Membership
  * Annual Membership
  * Bike Share for All
  * Access Pass
  * Corporate Membership
  * etc.

- Through this project, you will answer these questions: 

  * What are the 5 most popular trips that you would call "commuter trips"? 
  
  * What are your recommendations for offers (justify based on your findings)?

- Please note that there are no exact answers to the above questions, just like in the proverbial real world.  This is not a simple exercise where each question above will have a simple SQL query. It is an exercise in analytics over inexact and dirty data. 

- You won't find a column in a table labeled "commuter trip".  You will find you need to do quite a bit of data exploration using SQL queries to determine your own definition of a communter trip.  In data exploration process, you will find a lot of dirty data, that you will need to either clean or filter out. You will then write SQL queries to find the communter trips.

- Likewise to make your recommendations, you will need to do data exploration, cleaning or filtering dirty data, etc. to come up with the final queries that will give you the supporting data for your recommendations. You can make any recommendations regarding the offers, including, but not limited to: 
  * market offers differently to generate more revenue 
  * remove offers that are not working 
  * modify exising offers to generate more revenue
  * create new offers for hidden business opportunities you have found
  * etc. 

#### All Work MUST be done in the Google Cloud Platform (GCP) / The Majority of Work MUST be done using BigQuery SQL / Usage of Temporary Tables, Views, Pandas, Data Visualizations

A couple of the goals of w205 are for students to learn how to work in a cloud environment (such as GCP) and how to use SQL against a big data data platform (such as Google BigQuery).  In keeping with these goals, please do all of your work in GCP, and the majority of your analytics work using BigQuery SQL queries.

You can make intermediate temporary tables or views in your own dataset in BigQuery as you like.  Actually, this is a great way to work!  These make data exploration much easier.  It's much easier when you have made temporary tables or views with only clean data, filtered rows, filtered columns, new columns, summary data, etc.  If you use intermediate temporary tables or views, you should include the SQL used to create these, along with a brief note mentioning that you used the temporary table or view.

In the final Jupyter Notebook, the results of your BigQuery SQL will be read into Pandas, where you will use the skills you learned in the Python class to print formatted Pandas tables, simple data visualizations using Seaborn / Matplotlib, etc.  You can use Pandas for simple transformations, but please remember the bulk of work should be done using Google BigQuery SQL.

#### GitHub Procedures

In your Python class you used GitHub, with a single repo for all assignments, where you committed without doing a pull request.  In this class, we will try to mimic the real world more closely, so our procedures will be enhanced. 

Each project, including this one, will have it's own repo.

Important:  In w205, please never merge your assignment branch to the master branch. 

Using the git command line: clone down the repo, leave the master branch untouched, create an assignment branch, and move to that branch:
- Open a linux command line to your virtual machine and be sure you are logged in as jupyter.
- Create a ~/w205 directory if it does not already exist `mkdir ~/w205`
- Change directory into the ~/w205 directory `cd ~/w205`
- Clone down your repo `git clone <https url for your repo>`
- Change directory into the repo `cd <repo name>`
- Create an assignment branch `git branch assignment`
- Checkout the assignment branch `git checkout assignment`

The previous steps only need to be done once.  Once you your clone is on the assignment branch it will remain on that branch unless you checkout another branch.

The project workflow follows this pattern, which may be repeated as many times as needed.  In fact it's best to do this frequently as it saves your work into GitHub in case your virtual machine becomes corrupt:
- Make changes to existing files as needed.
- Add new files as needed
- Stage modified files `git add <filename>`
- Commit staged files `git commit -m "<meaningful comment about your changes>"`
- Push the commit on your assignment branch from your clone to GitHub `git push origin assignment`

Once you are done, go to the GitHub web interface and create a pull request comparing the assignment branch to the master branch.  Add your instructor, and only your instructor, as the reviewer.  The date and time stamp of the pull request is considered the submission time for late penalties. 

If you decide to make more changes after you have created a pull request, you can simply close the pull request (without merge!), make more changes, stage, commit, push, and create a final pull request when you are done.  Note that the last data and time stamp of the last pull request will be considered the submission time for late penalties.

Make sure you receive the emails related to your repository! Your project feedback will be given as comment on the pull request. When you receive the feedback, you can address problems or simply comment that you have read the feedback. 
AFTER receiving and answering the feedback, merge you PR to master. Your project only counts as complete once this is done.

---

## Parts 1, 2, 3

We have broken down this project into 3 parts, about 1 week's work each to help you stay on track.

**You will only turn in the project once at the end of part 3!**

- In Part 1, we will query using the Google BigQuery GUI interface in the cloud.

- In Part 2, we will query using the Linux command line from our virtual machine in the cloud.

- In Part 3, we will query from a Jupyter Notebook in our virtual machine in the cloud, save the results into Pandas, and present a report enhanced by Pandas output tables and simple data visualizations using Seaborn / Matplotlib.

---

## Part 1 - Querying Data with BigQuery

### SQL Tutorial

Please go through this SQL tutorial to help you learn the basics of SQL to help you complete this project.

SQL tutorial: https://www.w3schools.com/sql/default.asp

### Google Cloud Helpful Links

Read: https://cloud.google.com/docs/overview/

BigQuery: https://cloud.google.com/bigquery/

Public Datasets: Bring up your Google BigQuery console, open the menu for the public datasets, and navigate to the the dataset san_francisco.

- The Bay Bike Share has two datasets: a static one and a dynamic one.  The static one covers an historic period of about 3 years.  The dynamic one updates every 10 minutes or so.  THE STATIC ONE IS THE ONE WE WILL USE IN CLASS AND IN THE PROJECT. The reason is that is much easier to learn SQL against a static target instead of a moving target.

- (USE THESE TABLES!) The static tables we will be using in this class are in the dataset **san_francisco** :

  * bikeshare_stations

  * bikeshare_status

  * bikeshare_trips

- The dynamic tables are found in the dataset **san_francisco_bikeshare**

### Some initial queries

Paste your SQL query and answer the question in a sentence.  Be sure you properly format your queries and results using markdown. 

- What's the size of this dataset? (i.e., how many trips)

SQL Query:

```sql
SELECT count(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```

Answer: There are a total of 983648 trips in the dataset.

- What is the earliest start date and time and latest end date and time for a trip?

SQL Query:

```sql
SELECT min(start_date), max(end_date) FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```

Answer: The earliest start date and time for a trip was on 2013-08-29 09:08:00 UTC and the latest end date and time for a trip was on 2016-08-31 23:48:00 UTC.

- How many bikes are there?

SQL Query:

```sql
SELECT count(distinct bike_number) FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```

Answer: There are a total of 700 bikes.

### Questions of your own
- Make up 3 questions and answer them using the Bay Area Bike Share Trips Data.  These questions MUST be different than any of the questions and queries you ran above.

- Question 1: Which type of subscriber made more trips - Customers or Subscribers?
  * Answer: Since customers made 136809 trips and subscribers made 846839 trips, subscribers made more trips.
  * SQL query:

```sql
SELECT count(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE subscriber_type = 'Customer'
```

```sql
SELECT count(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE subscriber_type = 'Subscriber'
```

- Question 2: What was the highest and lowest duration of a trip?
  * Answer: The lowest duration of a trip was 60 seconds and the highest duration of a trip was 17270400 seconds.
  * SQL query:

```sql
 SELECT min(duration_sec), max(duration_sec) FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```

- Question 3: How many unique zip codes are in the dataset?
  * Answer: There are a total of 8830 zip codes in the dataset.
  * SQL query:

```sql
 SELECT count(distinct zip_code) FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```

### Bonus activity queries (optional - not graded - just this section is optional, all other sections are required)

The bike share dynamic dataset offers multiple tables that can be joined to learn more interesting facts about the bike share business across all regions. These advanced queries are designed to challenge you to explore the other tables, using only the available metadata to create views that give you a broader understanding of the overall volumes across the regions(each region has multiple stations)

We can create a temporary table or view against the dynamic dataset to join to our static dataset.

Here is some SQL to pull the region_id and station_id from the dynamic dataset.  You can save the results of this query to a temporary table or view.  You can then join the static tables to this table or view to find the region:
```sql
#standardSQL
select distinct region_id, station_id
from `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`
```

- Top 5 popular station pairs in each region

- Top 3 most popular regions(stations belong within 1 region)

- Total trips for each short station name in each region

- What are the top 10 used bikes in each of the top 3 region. these bikes could be in need of more frequent maintenance.

---

## Part 2 - Querying data from the BigQuery CLI 

- Use BQ from the Linux command line:

  * General query structure

    ```
    bq query --use_legacy_sql=false '
        SELECT count(*)
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```

### Queries

1. Rerun the first 3 queries from Part 1 using bq command line tool (Paste your bq
   queries and results here, using properly formatted markdown):

  * What's the size of this dataset? (i.e., how many trips)

SQL Query: 

```
bq query --use_legacy_sql=false 'SELECT count(*) FROM `bigquery-public-data.san_francisco.bikeshare_trips`'


Result: 

(base) jupyter@python-20210503-203155:~/w205$ bq query --use_legacy_sql=false 'SELECT count(*) FROM `bigquery-public
-data.san_francisco.bikeshare_trips`'
Waiting on bqjob_r54177230dd7566ed_000001797d795a91_1 ... (0s) Current status: DONE   
+--------+
|  f0_   |
+--------+
| 983648 |
+--------+
```


  * What is the earliest start time and latest end time for a trip?

SQL Query:

```
bq query --use_legacy_sql=false 'SELECT min(start_date), max(end_date) FROM `bigquery-public-data.san_francisco.bikeshare_trips`'

Result: 

(base) jupyter@python-20210503-203155:~/w205$ bq query --use_legacy_sql=false 'SELECT min(start_date), max(end_date)
 FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
Waiting on bqjob_r43133e051bf9a8cf_000001797d7a4a13_1 ... (0s) Current status: DONE   
+---------------------+---------------------+
|         f0_         |         f1_         |
+---------------------+---------------------+
| 2013-08-29 09:08:00 | 2016-08-31 23:48:00 |
+---------------------+---------------------+
```

  * How many bikes are there?

SQL Query: 

```
bq query --use_legacy_sql=false 'SELECT count(distinct bike_number) FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
 
Result: 

(base) jupyter@python-20210503-203155:~/w205$ bq query --use_legacy_sql=false 'SELECT count(distinct bike_number) FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
Waiting on bqjob_r295d45210547a53e_000001797d7adcd8_1 ... (0s) Current status: DONE   
+-----+
| f0_ |
+-----+
| 700 |
+-----+
```

2. New Query (Run using bq and paste your SQL query and answer the question in a sentence, using properly formatted markdown):

SQL Query: 

```
#To create a view that forms new columns for dividing up the original start_date column into sections of Morning, Afternoon, Evening, and Night. If the value in the start_date column had a start_date with hours between 6 and 10, the value was considered Morning, whereas values in between 14 and 19 where considered Afternoon.

bq query --use_legacy_sql=false 'CREATE VIEW `bike_trip_data.dayofweek` AS SELECT start_date,
       EXTRACT(DAYOFWEEK FROM start_date) AS dow_int,
       CASE EXTRACT(DAYOFWEEK FROM start_date)
           WHEN 1 THEN "Sunday"
           WHEN 2 THEN "Monday"
           WHEN 3 THEN "Tuesday"
           WHEN 4 THEN "Wednesday"
           WHEN 5 THEN "Thursday"
           WHEN 6 THEN "Friday"
           WHEN 7 THEN "Saturday"
           END AS dow_str,
       CASE 
           WHEN EXTRACT(DAYOFWEEK FROM start_date) IN (1, 7) THEN "Weekend"
           ELSE "Weekday"
           END AS dow_weekday,
       EXTRACT(HOUR FROM start_date) AS start_hour,
       CASE 
           WHEN EXTRACT(HOUR FROM start_date) <= 5  OR EXTRACT(HOUR FROM start_date) >= 23 THEN "Nightime"
           WHEN EXTRACT(HOUR FROM start_date) >= 6 and EXTRACT(HOUR FROM start_date) <= 8 THEN "Morning"
           WHEN EXTRACT(HOUR FROM start_date) >= 9 and EXTRACT(HOUR FROM start_date) <= 10 THEN "Mid Morning"
           WHEN EXTRACT(HOUR FROM start_date) >= 11 and EXTRACT(HOUR FROM start_date) <= 13 THEN "Mid Day"
           WHEN EXTRACT(HOUR FROM start_date) >= 14 and EXTRACT(HOUR FROM start_date) <= 16 THEN "Early Afternoon"
           WHEN EXTRACT(HOUR FROM start_date) >= 17 and EXTRACT(HOUR FROM start_date) <= 19 THEN "Afternoon"
           WHEN EXTRACT(HOUR FROM start_date) >= 20 and EXTRACT(HOUR FROM start_date) <= 22 THEN "Evening"
           END AS start_hour_str
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
ORDER BY start_date ASC'

#SQL Query for selecting the total count of trips in the Morning (Between 6 to 10 hours in the original start_date column)

bq query --use_legacy_sql=false 'SELECT count(*) FROM bike_trip_data.dayofweek WHERE start_hour_str="Morning" OR start_hour_str="Mid Morning"'

#SQL Query for selecting the total count of trips in the Afternoon (Between 14 to 19 hours in the original start_date column)

bq query --use_legacy_sql=false 'SELECT count(*) FROM bike_trip_data.dayofweek WHERE start_hour_str="Early Afternoon" OR start_hour_str="Afternoon"'
```

  * How many trips are in the morning vs in the afternoon?

Answer: There were total of 359414 trips in the morning versus 426175 trips in the afternoon.


### Project Questions
Identify the main questions you'll need to answer to make recommendations (list
below, add as many questions as you need).

- Question 1: What are the top 10 starting point stations that have the lowest number of trips?

- Question 2: Which docking stations have less than a total of 15 dock counts?

- Question 3: Which landmark showed up the most frequently in the top 10 list of most bikes available?

- Question 4: What are the count of bike trips that have a duration of less than 5 minutes and less than 10 minutes?

- Question 5: What are the count of bike trips that had a duration of less than a hour?

- Question 6: Which day of the week has the lowest count of bike trips?

- Question 7: Which station had the lowest count of usage? 

### Answers

Answer at least 4 of the questions you identified above You can use either
BigQuery or the bq command line tool.  Paste your questions, queries and
answers below.

- Question 1: What are the top 10 starting point stations that have the lowest number of trips?
  * Answer: The top 10 starting point stations with the lowest number of trips would be Clay at Battery, Market at 10th, 2nd at South Park, Evelyn Park and Ride, Embarcadero at Vallejo, Broadway St at Battery St, Embarcadero at Bryant, Grant Avenue at Columbus Avenue, St James Park, and Spear at Folsom
 * SQL query: 

```
bq query --use_legacy_sql=false 'SELECT start_station_name, number_of_trips FROM bike_trip_data.numberoftrips WHERE number_of_trips <= 105
ORDER BY number_of_trips ASC
LIMIT 10'

Result:

+---------------------------------+-----------------+
|       start_station_name        | number_of_trips |
+---------------------------------+-----------------+
| Clay at Battery                 |             101 |
| Market at 10th                  |             101 |
| 2nd at South Park               |             102 |
| Evelyn Park and Ride            |             102 |
| Embarcadero at Vallejo          |             102 |
| Broadway St at Battery St       |             102 |
| Embarcadero at Bryant           |             102 |
| Grant Avenue at Columbus Avenue |             103 |
| St James Park                   |             103 |
| Spear at Folsom                 |             103 |
+---------------------------------+-----------------+
```

- Question 2: Which docking stations have less than a total of 15 dock counts?
  * Answer: The docking stations with less than a total of 15 dock counts would be Santa Clara at Almaden, Cowper at University, University and Emerson, and Castro Street and El Camino Real.
  * SQL query:

```
bq query --use_legacy_sql=false 'SELECT name
FROM `bigquery-public-data.san_francisco.bikeshare_stations`
WHERE dockcount < 15'

Result:

+----------------------------------+
|               name               |
+----------------------------------+
| Santa Clara at Almaden           |
| Cowper at University             |
| University and Emerson           |
| Castro Street and El Camino Real |
+----------------------------------+
```
  
- Question 3: Which landmark showed up the most frequently in the top 10 list of most bikes available?
  * Answer: As you can see from the top 10 of the results, San Francisco showed up 5 times whereas San Jose showed up 3 times and Redwood City showed up 2 times.
  * SQL query:

```
bq query --use_legacy_sql=false 'SELECT distinct(bikeshare_stations.landmark), bikeshare_status.bikes_available FROM bigquery-public-data.san_francisco.bikeshare_status INNER JOIN bigquery-public-data.san_francisco.bikeshare_stations ON bikeshare_status.station_id=bikeshare_stations.station_id
ORDER BY bikes_available DESC'

Result:

+---------------+-----------------+
|   landmark    | bikes_available |
+---------------+-----------------+
| San Francisco |              29 |
| San Francisco |              28 |
| San Jose      |              27 |
| San Francisco |              27 |
| San Jose      |              26 |
| San Francisco |              26 |
| Redwood City  |              26 |
| San Francisco |              25 |
| San Jose      |              25 |
| Redwood City  |              25 |
```
For Questions 4 and 5, I have created a view in Google BigQuery with the following SQL statement:


```sql
select
    trip_id,
    CAST(ROUND(duration_sec / 60.0) AS INT64) AS duration_minutes,
    CAST(ROUND(duration_sec / 3600.0) AS INT64) AS duration_hours_rounded,
    EXTRACT(DAYOFWEEK from start_date) AS dow_int,
    CASE EXTRACT(DAYOFWEEK FROM start_date)
        WHEN 1 THEN "Sunday"
        WHEN 2 THEN "Monday"
        WHEN 3 THEN "Tuesday"
        WHEN 4 THEN "Wednesday"
        WHEN 5 THEN "Thursday"
        WHEN 6 THEN "Friday"
        WHEN 7 THEN "Saturday"
        END AS dow_str,
    EXTRACT(HOUR FROM start_date) AS start_hour,
    start_date,
    end_date,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    bike_number,
    zip_code,
    subscriber_type
from `bigquery-public-data.san_francisco.bikeshare_trips`
```

- Question 4: What are the count of bike trips that have a duration of less than 5 minutes and less than 10 minutes?
  * Answer: There were 220,374 bike trips that had a duration of less than 5 minutes and 628,444 bike trips that had a duration of less than 10 minutes which shows that a majority of bike trips are very short.
  * SQL query:

```
bq query --use_legacy_sql=false 'SELECT count(*) FROM `bike_trip_data.trips_1` WHERE duration_minutes <= 5'

Result:

+--------+
|  f0_   |
+--------+
| 220374 |
+--------+
```

```
bq query --use_legacy_sql=false 'SELECT count(*) FROM `bike_trip_data.trips_1` WHERE duration_minutes <= 10'

Result:

+--------+
|  f0_   |
+--------+
| 628444 |
+--------+
```

- Question 5: What are the count of bike trips that had a duration of less than a hour?
  * Answer: There was a total of 936,280 bike trips that had a duration of less than a hour compared to 26,500 in between 1 hour and 2 hours. As shown in the query results, a majority of bike trips were less than a hour which shows that most trips are very short.
  * SQL query:

```
bq query --use_legacy_sql=false 'SELECT duration_hours_rounded, count(*) FROM `bike_trip_data.trips_1` GROUP BY duration_hours_rounded ORDER BY 1'

Result:

+------------------------+--------+
| duration_hours_rounded |  f0_   |
+------------------------+--------+
|                      0 | 936280 |
|                      1 |  26500 |
|                      2 |   7924 |
|                      3 |   4217 |
|                      4 |   2643 |
|                      5 |   1692 |
|                      6 |   1110 |
|                      7 |    757 |
|                      8 |    572 |
|                      9 |    251 |
|                     10 |    138 |
```

For Questions 6 and 7, I have created a view in Google BigQuery with the following SQL statement:

```sql
select *
from `bike_trip_data.trips_1`
where duration_minutes >= 5
        and duration_hours_rounded <= 20
```

- Question 6: Which day of the week has the lowest count of bike trips?
  * Answer: The day of week with the lowest count of bike trips was Sunday with 46,336 trips.
  * SQL Query:

```
bq query --use_legacy_sql=false 'SELECT dow_int, dow_str, count(*) FROM `bike_trip_data.trips_2` GROUP BY dow_int, dow_str ORDER BY 1'

Result:

+---------+-----------+--------+
| dow_int |  dow_str  |  f0_   |
+---------+-----------+--------+
|       1 | Sunday    |  46336 |
|       2 | Monday    | 144920 |
|       3 | Tuesday   | 157046 |
|       4 | Wednesday | 154204 |
|       5 | Thursday  | 151062 |
|       6 | Friday    | 137194 |
|       7 | Saturday  |  54333 |
+---------+-----------+--------+
```

- Question 7: Which station had the lowest count of usage?
  * Answer: Station 88 had the lowest usage with a count of 38.
  * SQL Query:

```
bq query --use_legacy_sql=false 'SELECT station_id, sum(trip_count)
FROM
(
SELECT start_station_id as station_id, count(*) as trip_count
FROM `bike_trip_data.trips_2`
GROUP BY start_station_id
UNION ALL
SELECT end_station_id as station_id, count(*) as trip_count
FROM `bike_trip_data.trips_2`
GROUP BY end_station_id
)
GROUP BY station_id order by 2'

Result:

+------------+--------+
| station_id |  f0_   |
+------------+--------+
|         88 |     38 |
|         91 |    125 |
|         89 |    157 |
|         90 |    252 |
|         21 |    303 |
|         24 |    410 |
|         23 |    511 |
|         83 |    519 |
|         26 |    757 |
|         25 |   1831 |
```
---

## Part 3 - Employ notebooks to synthesize query project results

### Get Going

Create a Jupyter Notebook against a Python 3 kernel named Project_1.ipynb in the assignment branch of your repo.

#### Run queries in the notebook 

At the end of this document is an example Jupyter Notebook you can take a look at and run.  

You can run queries using the "bang" command to shell out, such as this:

```
! bq query --use_legacy_sql=FALSE '<your-query-here>'
```

- NOTE: 
- Queries that return over 16K rows will not run this way, 
- Run groupbys etc in the bq web interface and save that as a table in BQ. 
- Max rows is defaulted to 100, use the command line parameter `--max_rows=1000000` to make it larger
- Query those tables the same way as in `example.ipynb`

Or you can use the magic commands, such as this:

```sql
%%bigquery my_panda_data_frame

select start_station_name, end_station_name
from `bigquery-public-data.san_francisco.bikeshare_trips`
where start_station_name <> end_station_name
limit 10
```

```python
my_panda_data_frame
```

#### Report in the form of the Jupter Notebook named Project_1.ipynb

- Using markdown cells, MUST definitively state and answer the two project questions:

  * What are the 5 most popular trips that you would call "commuter trips"?

Answer: The 5 most popular trips would be in the following order:

1.) Harry Bridges Plaza (Ferry Building) to 2nd at Townsend with a count of 5700 trips
2.) 2nd at Townsend to Harry Bridges Plaza (Ferry Building) with a count of 5449 trips
3.) Embarcadero at Sansome to Steuart at Market with a count of 5194 trips
4.) San Francisco Caltrain (Townsend at 4th) to Harry Bridges Plaza (Ferry Building) with a count of 5166 trips
5.) Embarcadero at Folsom to San Francisco Caltrain (Townsend at 4th) with a count of 4961 trips

SQL Query:

```sql
SELECT start_station_name, end_station_name, count(*)
FROM `bike_trip_data.trips_2`
WHERE start_station_name <> end_station_name
    and dow_int <> 1
    and dow_int <> 7
    and (start_hour >= 6 and start_hour <= 9) or (start_hour >= 16 and start_hour <= 19)
GROUP BY start_station_name, end_station_name
ORDER BY 3 desc
``` 
  
  * What are your recommendations for offers (justify based on your findings)?
    All data analysis, visualizations, and recommendations have been provided in the Jupyter Notebook (Project_1.ipynb)


- For any temporary tables (or views) that you created, include the SQL in markdown cells

- Use code cells for SQL you ran to load into Pandas, either using the !bq or the magic commands

- Use code cells to create Pandas formatted output tables (at least 3) to present or support your findings

- Use code cells to create simple data visualizations using Seaborn / Matplotlib (at least 2) to present or support your findings

### Resource: see example .ipynb file 

[Example Notebook](example.ipynb)
