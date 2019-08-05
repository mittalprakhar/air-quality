"""

To Do:

1. Update Data
2. Update Calc function to:
    a) Add 7 new Avg columns for each pollutant in both Raw and Calc tables
    b) Add new row with primary key (Year, "Average") with average values for each year in both Raw and Calc tables
3. Create functions to Add, Modify and Delete Data to/from Raw Tables (and automatically update Calc Tables)
4. Add -1 in cells without value and ignore -1 during calculations, trends and predictions
5. Link Calc Tables and Chart through Category column
6. Create function to See Data: Either the entire table OR Values for a particular city and year (and season, optional)
7. Create function to Display Info: Either the entire chart OR According to AQI for a particular city, year and season
8. Create function to allow admin to run direct SQL commands
9. Create Graph function with parameters:
    a) City = "Delhi" / "Gurgaon" / "Both" (default)
    b) Start Year = Earliest Year in Corresponding City's / Cities' table(s)
    b) End Year = Latest Year in Corresponding City's / Cities' table(s)
    c) Season = "Spring" / "Summer" / "Monsoon" / "Winter" / "Average" (default)
    d) Columns = 3 (Min, Max, Avg) x 8 (7 pollutants + 1 AQI) = 24 possibilities
10. Create Regression function
11. Create Predict function that:
    a) Uses Regression to predict 5 (4 seasons + 1 average) x 5 (2019-23) = 25 rows, each with 14 Raw values
    b) Uses Calc to calculate corresponding 7 Raw Avg + 21 Calc + 3 AQI values (Min, Max, Avg) + Assign category
    c) Updates all 4 tables with new predicted values
    d) Uses Graph to display predictions

"""


import pyaqilib as lib

mysql_password = 'PyAQI@42'

admins = [('Prakhar', 'PM'), ('Keshav', 'KA')]

data_delhi = [
    (2009, "Spring", 57, 185, 23, 105, 9, 44, 18, 37, 16, 44, 0.2, 1.5, 16, 29),
    (2010, "Spring", 55, 186, 28, 134, 13, 60, 15, 42, 19, 63, 0.3, 1.4, 22, 33),
    (2011, "Spring", 61, 205, 39, 154, 18, 70, 16, 38, 21, 71, 0.2, 1.4, 20, 35),
    (2012, "Spring", 54, 217, 34, 148, 17, 66, 12, 40, 18, 64, 0.2, 1.5, 19, 35),
    (2013, "Spring", 57, 212, 47, 162, 20, 70, 11, 29, 25, 78, 0.3, 1.7, 24, 44),
    (2014, "Spring", 65, 239, 53, 171, 25, 72, 14, 38, 23, 70, 0.3, 1.6, 23, 41),
    (2015, "Spring", 68, 215, 60, 175, 26, 78, 12, 36, 26, 81, 0.3, 1.8, 27, 50),
    (2016, "Spring", 68, 243, 55, 159, 23, 80, 8, 28, 31, 96, 0.4, 2.0, 29, 53),
    (2017, "Spring", 73, 264, 52, 162, 20, 73, 11, 34, 33, 98, 0.3, 1.9, 30, 56),
    (2018, "Spring", 72, 275, 55, 161, 24, 70, 9, 29, 32, 102, 0.4, 2.0, 32, 59),

    (2009, "Summer", 53, 274, 20, 211, 13, 58, 13, 28, 18, 67, 0.2, 0.6, 14, 47),
    (2010, "Summer", 50, 300, 23, 208, 14, 56, 10, 26, 18, 63, 0.2, 0.5, 14, 42),
    (2011, "Summer", 57, 298, 24, 217, 15, 61, 9, 23, 19, 66, 0.2, 0.5, 16, 46),
    (2012, "Summer", 60, 326, 21, 231, 15, 64, 7, 18, 21, 69, 0.3, 0.6, 17, 59),
    (2013, "Summer", 69, 346, 25, 246, 16, 63, 8, 20, 20, 71, 0.2, 0.7, 19, 61),
    (2014, "Summer", 62, 342, 26, 248, 17, 68, 6, 17, 25, 80, 0.3, 0.8, 19, 64),
    (2015, "Summer", 63, 368, 26, 251, 16, 71, 6, 18, 24, 78, 0.5, 0.7, 18, 67),
    (2016, "Summer", 68, 370, 25, 258, 18, 71, 5, 14, 24, 82, 0.4, 0.6, 20, 78),
    (2017, "Summer", 67, 392, 28, 280, 20, 76, 3, 12, 27, 85, 0.4, 0.7, 22, 81),
    (2018, "Summer", 72, 413, 30, 285, 20, 80, 4, 14, 27, 100, 0.5, 0.9, 22, 87),

    # To Update
    (2009, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2010, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2011, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2012, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2013, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2014, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2015, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2016, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2017, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),
    (2018, "Monsoon", 36, 174, 37, 137, 22, 56, 4, 18, 20, 98, 0.2, 1.4, 8, 29),

    # To Update
    (2009, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2010, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2011, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2012, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2013, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2014, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2015, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2016, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2017, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129),
    (2018, "Winter", 98, 634, 54, 325, 42, 121, 4, 15, 20, 102, 0.6, 2.2, 54, 129)
]

data_gurgaon = [
    (2009, "Spring", 47, 179, 32, 87, 30, 63, 19, 66, 25, 48, 0.6, 2.0, 19, 30),
    (2010, "Spring", 48, 230, 44, 99, 35, 69, 18, 60, 27, 45, 0.6, 2.3, 18, 35),
    (2011, "Spring", 50, 205, 39, 103, 33, 75, 15, 62, 23, 55, 0.6, 2.0, 17, 31),
    (2012, "Spring", 54, 216, 40, 100, 35, 83, 18, 59, 29, 50, 0.8, 2.4, 20, 37),
    (2013, "Spring", 58, 230, 49, 95, 34, 82, 16, 50, 26, 59, 0.7, 2.3, 22, 40),
    (2014, "Spring", 63, 235, 46, 93, 38, 79, 16, 54, 31, 64, 0.7, 2.5, 26, 42),
    (2015, "Spring", 67, 274, 55, 110, 40, 89, 15, 52, 34, 63, 0.8, 2.6, 19, 39),
    (2016, "Spring", 68, 298, 62, 123, 45, 91, 13, 43, 32, 70, 0.7, 2.7, 24, 40),
    (2017, "Spring", 71, 302, 63, 127, 46, 95, 12, 47, 34, 74, 0.9, 2.7, 26, 46),
    (2018, "Spring", 74, 345, 67, 133, 50, 100, 14, 42, 36, 78, 0.9, 3.0, 26, 47),

    (2009, "Summer", 47, 274, 17, 230, 12, 62, 16, 28, 17, 61, 0.3, 0.9, 18, 54),
    (2010, "Summer", 53, 300, 21, 227, 16, 63, 16, 26, 16, 62, 0.3, 0.9, 19, 51),
    (2011, "Summer", 51, 298, 29, 240, 19, 69, 15, 23, 18, 66, 0.2, 0.9, 22, 52),
    (2012, "Summer", 58, 326, 33, 239, 21, 76, 15, 18, 20, 69, 0.4, 1.0, 25, 58),
    (2013, "Summer", 63, 346, 39, 243, 28, 74, 16, 20, 23, 71, 0.5, 1.3, 29, 63),
    (2014, "Summer", 65, 342, 40, 254, 34, 82, 14, 17, 22, 80, 0.4, 1.2, 30, 68),
    (2015, "Summer", 71, 368, 38, 269, 28, 85, 12, 18, 24, 78, 0.5, 1.4, 34, 71),
    (2016, "Summer", 73, 370, 44, 258, 36, 97, 10, 14, 25, 82, 0.4, 1.4, 35, 82),
    (2017, "Summer", 81, 392, 46, 280, 40, 101, 9, 12, 24, 85, 0.5, 1.5, 36, 91),
    (2018, "Summer", 85, 438, 53, 330, 49, 126, 7, 22, 29, 101, 0.6, 1.7, 39, 102),

    # To Update
    (2009, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2010, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2011, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2012, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2013, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2014, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2015, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2016, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2017, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),
    (2018, "Monsoon", 41, 181, 24, 141, 12, 38, 5, 18, 13, 59, 0.3, 1.5, 5, 30),

    # To Update
    (2009, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2010, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2011, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2012, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2013, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2014, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2015, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2016, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2017, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140),
    (2018, "Winter", 97, 831, 69, 362, 38, 119, 5, 12, 19, 92, 0.7, 2.5, 56, 140)
]

data_aqi = [
    (1, "Good", 0, 50, "People are not exposed to any health risk because the quality of air is pure."),
    (2, "Satisfactory", 51, 100, "Pollution may cause minor discomfort to sensitive people."),
    (3, "Moderately Polluted", 101, 200, "Pollution may cause breathing discomfort to people with lung disease, asthma, heart disease, and to children and older adults."),
    (4, "Poor", 201, 300, "Pollution may cause breathing discomfort to people on prolonged exposure."),
    (5, "Very Poor", 301, 400, "Pollution may cause respiratory illness to people on prolonged exposure. Effect may be more pronounced in people with lung and heart diseases."),
    (6, "Severe", 401, 500, "Pollution may cause respiratory impact even on healthy people, and serious health impacts on people with lung/heart disease.")
]

# If database is already set up
# db, cursor = lib.init(password=mysql_password)

# If database is not set up
db, cursor = lib.reset(data_delhi, data_gurgaon, data_aqi, password=mysql_password)

lib.home(admins)

db.close()