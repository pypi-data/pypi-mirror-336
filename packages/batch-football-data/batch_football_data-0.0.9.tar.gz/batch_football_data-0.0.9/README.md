# Batch Football Data

Python Data Models for interacting with the Football Stats Database.

## Modules

The Football Data library contains two modules:

* Models
* Repositories

### Models Module

The Models Module contains ORM Classes representing the tables within the database mapped for use in SQL Alchemny. The following Data Classes
are available:

* Players - Represents a player in the league.
* Position - Lookup for the Player's Position
* Schedule - Represents a given game played during the week in a season.
* Statistic - A Ststistic for either a player or a Team
* StatisticCategory - Category of Statistic (Defense, Offense)
* StatisticCode - Code Value related to the Statistic (Passing Yard, Rushing Yards, etc)
* Team - Team in the League
* TypeCode - Defines the Season type for a schedule entry (Preseason, Regular, Post Season)
* TeamStaff - Establishes a relationship for a Player to a Team for a given Year
* League - Defines a League for teams
* TeamLeague - Establishes a linkage between a Team and League.

### Repositories Module

The repositories module contains individual repository class for each of the Model classes for interacting with items in the database.
Each repository contains methods for saving single and multiple items. They also contain methods for validating the item is present or not in the 
database.