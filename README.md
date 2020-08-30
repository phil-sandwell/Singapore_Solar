# Solar deployment in Singapore

## Introduction

Singapore, a highly-urbanised city-state in South East Asia, has the goal of deploying 2 GWp (2,000,000 kWp) of solar photovoltaic (PV) capacity by 2030. Sitting close to the equator, Singapore receives a high level of solar irradiance - around 1,600 kWh per square metre per year - which makes solar PV an obvious choice to contribute to its renewable energy goals. PV module prices fell 86% between 2010 and 2018 and, with costs continuing to decrease, solar offers an alternative electricity source competitive with, or lower than, the tariffs of the national grid.

In this project I took a (very brief!) look into the status of solar PV deployment in Singapore. As well as learning more about deployment in the country, it also let me explore some interesting real-life data and gave me an excuse to practice some geographic and web-based visualisations which don't often come up in my usual projects. All of the code used in this project is available in the GitHub repository. 

## Data inputs

The [National Solar Repository of Singapore](https://www.solar-repository.sg/) (NSR) offers a wealth of information about the status of PV deployment in the country and, relevant to this project, a [database of PV systems](https://www.solar-repository.sg/pv-systems-database) installed in Singapore since 2008. This contains vital information about the system capacity (kWp), technology and integrator, as well as the type of the system (e.g. residential or commercial) and its location.

To investigate the geographical distribution of systems I used the Urban Redevelopment Authority's [planning area boundaries](https://data.gov.sg/dataset/master-plan-2014-planning-area-boundary-web). The URA 2014 Master Plan divided Singapore into 55 planning areas designed to assist in development, with a number of smaller areas clustered around Downtown and larger areas in the West and East. These are first-level census divisions, which are grouped into larger regions and each divided into smaller subzones. 

## Data cleaning and processing

Although the NSR provides the system location, these names do not always correspond to the URA planning areas - listing subzones instead, for example. After identifying the systems whose locations did not match a planning area, I compiled a dictionary of the listed locations and the actual planning areas to which they correspond. I then repeated the process for the systems whose locations were ambiguous - this time by using the system name as a clue to their location. These took a significant amount of online searching and cross-referencing with Google Maps, but this information is stored in two new files, `location_correct.xlsx` and `name_correct.xlsx`, for future replication. This was surprisingly effective with only five systems going unidentified, but this location reassignment process might have brought in some errors from me mis-identifying where these systems are installed. I classified the locations of unidentified systems as "Not specified". 

Two systems, in the database, `SolarNova2` and `SolarNova3`, correspond to the [SolarNova programme being implemented by the Economic Development Board and the Housing and Development Board](https://www.hdb.gov.sg/cs/infoweb/about-us/our-role/smart-and-sustainable-living/solarnova-page). Since 2014 this ongoing programme aims to grow Singapore's solar industry and deploy solar on housing blocks around the country, but these are listed as single systems in the database and assigned to a single location so I reassigned these systems' locations as "Not specified". 

As we will see only a few PV technologies have wide deployment in Singapore, but there are many individual types. Any technologies with fewer than four systems were reclassifed and grouped together as "Other". I chose to maintain the distinction between monocrystalline silicon/all-back contact/HIT modules, rather than group them together. 

Using the database of system information (`system_info`) allowed me to explore the geographical distribution and breakdown of PV deployment in Singapore, and I also exploited the date of commission information to create a running total of cumualtive PV deployment over the available time period - from January 2008 to August 2020. Let's take a look!

## Results

### System sizes

To get a broad overview of the data we can look at the entire distribution of system sizes over the total time period, from 2008 to 2020, and how the different types of systems compare.

{% include system_size_scatter.html %}



## Disclaimers

This work contains data from the National Solar Repository and is [subject to their disclaimers](https://www.solar-repository.sg/disclaimer). With respect to their conditions, the database used in this work is not included in this GitHub repository but users can download their own version for personal and non-commercial use from their website. 

The information contained in the NSR website is for general information purposes only. The information is provided by the Solar Energy Research Institute of Singapore (SERIS) as the National Solar Repository (NSR) Program Administrator and while they endeavour to keep the information up to date and correct, they make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose. Any reliance you place on such information is therefore strictly at your own risk.

This work contains information from Master Plan 2014 Planning Area Boundary accessed on 18 August 2020 from [data.gov.sg](https://data.gov.sg/dataset/master-plan-2014-planning-area-boundary-web?resource_id=2ab23cb2-b1a4-4b1a-a9e1-b9cad0ac159b) which is made available under the terms of the [Singapore Open Data Licence version 1.0](https://data.gov.sg/open-data-licence). Use of this dataset does not in a way suggest any official status or that an Agency endorses the use of the datasets.


```python

```
