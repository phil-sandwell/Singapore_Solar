# Solar deployment in Singapore

## Introduction

Singapore, a highly-urbanised city-state in South East Asia, has the goal of deploying 2 GWp (2,000,000 kWp) of solar photovoltaic (PV) capacity by 2030. Sitting close to the equator, Singapore receives a high level of solar irradiance - around 1,600 kWh per square metre per year - which makes solar PV an obvious choice to contribute to its renewable energy goals. PV module prices fell 86% between 2010 and 2018 and, with costs continuing to decrease, solar offers an alternative electricity source competitive with, or lower than, the tariffs of the national grid.

In this project I took a (very brief!) look into the status of solar PV deployment in Singapore. As well as learning more about deployment in the country, it also let me explore some interesting real-life data and gave me an excuse to practice some geographic and web-based visualisations which don't often come up in my usual projects. All of the code used in this project is available in the GitHub repository. 

## Methods

### Data inputs

The [National Solar Repository of Singapore](https://www.solar-repository.sg/) (NSR) offers a wealth of information about the status of PV deployment in the country and, relevant to this project, a [database of PV systems](https://www.solar-repository.sg/pv-systems-database) installed in Singapore since 2008. This contains vital information about the system capacity (kWp), technology and integrator, as well as the type of the system (e.g. residential or commercial) and its location.

To investigate the geographical distribution of systems I used the Urban Redevelopment Authority's [planning area boundaries](https://data.gov.sg/dataset/master-plan-2014-planning-area-boundary-web). The URA 2014 Master Plan divided Singapore into 55 planning areas designed to assist in development, with a number of smaller areas clustered around Downtown and larger areas in the West and East. These are first-level census divisions, which are grouped into larger regions and each divided into smaller subzones. 

### Data cleaning and processing

Although the NSR provides the system location, these names do not always correspond to the URA planning areas - listing subzones instead, for example. After identifying the systems whose locations did not match a planning area, I compiled a dictionary of the listed locations and the actual planning areas to which they correspond. I then repeated the process for the systems whose locations were ambiguous - this time by using the system name as a clue to their location. These took a significant amount of online searching and cross-referencing with Google Maps, but this information is stored in two new files, `location_correct.xlsx` and `name_correct.xlsx`, for future replication. This was surprisingly effective with only five systems going unidentified, but this location reassignment process might have brought in some errors from me mis-identifying where these systems are installed. I classified the locations of unidentified systems as "Not specified". 

Five systems in the database (HDB Phase 1-3 Solar Leasing, SolarNova 2 & 3) correspond to the [SolarNova programme being implemented by the Economic Development Board and the Housing and Development Board](https://www.hdb.gov.sg/cs/infoweb/about-us/our-role/smart-and-sustainable-living/solarnova-page). Since 2014 this ongoing programme aims to grow Singapore's solar industry and deploy solar on housing blocks around the country, but these are listed as single systems in the database and assigned to a single location so I reassigned these systems' locations as "Not specified". Since it would be unfair to consider them as single installations, I've generally discounted them from the analysis apart from aggregated results.  

As we will see only a few PV technologies have wide deployment in Singapore, but there are many individual types. Any technologies with fewer than four systems were reclassifed and grouped together as "Other". I chose to maintain the distinction between monocrystalline silicon/all-back contact/HIT modules, rather than group them together. 

### Reproduction

Using the database of system information (`system_info`) allowed me to explore the geographical distribution and breakdown of PV deployment in Singapore, and I also exploited the date of commission information to create a running total of cumualtive PV deployment over the available time period - from January 2008 to August 2020. All of the code to clean, process, analyse and plot the data is available open-source in the GitHub repository.

## Results

### More systems are being installed - and they're getting bigger

The NSR database lists over 300 systems installed between 2008 and 2020, with a cumulative installed capacity of more than 255 MWp (255,000 kWp). To get a broad overview of the data we can look at the entire distribution of system sizes over the total time period and how the different types of systems compare. Click on the legend to isolate certain types of systems or click and drag on the figure to zoom.

{% include system_size_scatter.html %}

Over time a greater number of systems have been installed and their average capacity is increasing (trend lines not shown to avoid overwhelming the figure). Just six systems were installed in 2008 and 12 in 2010, but 44 were installed in 2018 and 74 in 2019 - the largest number to date. Only 14 were recorded between January and August 2020, a slowdown on previous years, but this is most likely an effect of the COVID-19 situation.   

Despite a growing number of very large (2,000 kWp +) systems, the median size for each system type are much more modest: industrial systems are the largest (median of 365 kWp) followed by commercial systems (285 kWp). Educational (27 kWp) and residential (11 kWp) are both much smaller in size and fewer in number - with the latter not accounting for the (aggregated) installations from the SolarNova programme.

### The West region hosts most of Singapore's PV capacity

The figure below shows the cumulative installed capacity in each region, divided into planning areas and (further) the system type. Only systems with known locations are included. Click on a box to zoom in, or the bar at the top to reset. 

{% include treemap.html %}

The West region accounts for 57% of this capacity, with Tuas (27% of the total) and Jurong East (18%) contributing significantly to it - only Changi, in the East region, accounts for a comparable amount (also 18%). Most of the capacity in the North-East region is located in Seletar, whilst the Central and North regions have their capacity spread over a number of planning areas.

Given the relative availability of land and industrial activity in the West and East regions this distribution is expected, especially compared to the much more space-constrained Central region. 

### Tuas leads in both installed capacity and number of systems

The map below highlights the hotspots for solar installation around Singapore: Tuas, Jurong East and Changi, which each have more than 10,000 kWp, as well as other planning areas with significant capacity such as Bedok, Seletar, Punggol, the Western Water Catchment and Boon Lay (between 5,000-10,000 kWp). The colour scale is logarithmic and areas with no recorded systems are shown in grey.

{% include cumulative_map.html %}

Tuas has both the greatest installed capacity (42 MWp) and the largest number of individual systems (44). Jurong East and Changi have similar capacities (around 28 MWp) but spread over a very different number of systems, 10 and 19 respectively. Bedok (23), Boon Lay (14) and Ang Mo Kio (14) also have relatively large numbers of systems. Neighbouring Serangoon, Bishan and Hougang have a moderately high number of installations but a relatively small total capacity. 

### Polycrystalline silicon dominates installed capacity

Solar prices have continued to decrease and some of the cheapest module costs are for polycrystalline silicon, at less than USD 0.20 per Wp. This is reflected in the figure below which breaks down the cumulative installed capacity by technology type and installer (including for unidentified systems). Click on a technology to zoom in, or the centre to reset. 

{% include sunburst.html %}

Of the 44 systems installed in 2018, 37 used polycrystalline silicon. Although this dropped to just 20 of 74 systems installed in 2019, polycrystalline silicon accounts for 75% of the total cumulative capacity of the country (192 MWp out of 255 MWp). Monocrystalline silicon modules account for 22% of installed capacity, whilst others make up the remainder.

Sembcorp Solar Singapore is the largest single player in the solar market with more than 136 MWp installed in the country - more than half of the total. Their influence is split across the two major technologies, with 57% and 48% of the polycrystalline and monocrystalline markets respectively. Sunseap Group and SolarGy are the only other companies with significant shares of the total market, with around 15% each. 

### Total solar deployment is growing, but still has a long way to go

Singapore's total solar deployment has been steadily growing since 2013, amounting to more than 250 MWp across the country by August 2020 - the figure below shows this rise broken down by region and planning area, with the SolarNova systems being reintroduced in the "Not specified" grouping. Use the buttons and slider on the figure to explore different date ranges.

{% include cumulative_installations.html %}

After passing 25 MWp in July 2015, Singapore's cumulative installed capacity doubled in less than a year - and then doubled again, to more than 100 MWp, around one year later in August 2018. Two major solar installation programmes, SolarNova 2 and 3, are grouped together (as discussed previously) and both recorded in December 2018, resulting in a conspicuous increase in capacity. This jump aside, the cumulative installed capacity was steadily increasing until February 2020 and the full effects of the COVID-19 situation became realised. In the six months between March and August 2020 only seven systems were installed, totalling just 108 kWp (0.1 MWp).

Achieving a ten-fold increase in five years is certainly an impressive achievement, particularly in a highly urbanised city-state like Singapore. With the aim of achieving 2 GWp (2,000,000 MWp) by 2030, however, the solar industry will need to see another eight-fold increase in the next ten years to meet this lofty goal.


## Discussion

### Solar in Singapore is on the rise

New systems have been continuously installed around Singapore and, after a brief hiatus resulting from the country's circuit breaker measures, have begun to increase the national solar capacity once again. Three planning areas have more than 10 MWp each and several more - such as Bedok, Seletar, Punggol - could graduate to this level of deployment soon. Areas in the North and North-East regions could be good candidates for future deployment. 

A ten-fold increase in capacity from 2015-2020 is one thing, but a further eight-fold increase is quite another. Singapore's institutional support for PV deployment through SolarNova will help to achieve this, and is evident in the capacity increases to date, but further iterations of this programme will be necessary to keep this momentum going. 

### Polycrystalline silicon and large-scale systems have driven deployment

Around 75% of Singapore's installed capacity is from polycrystalline modules and, with prices as low as ever, this will likely continue. Sembcorp Solar Singapore has a solid grip on the market at present with an installed capacity more than three times greater than either of its closest competitors. 

Installations for commercial and industrial purposes have provided the largest single increases to cumulative capacity but will need to be much more numerous to acheive the 2 GWp goal. The largest single installation to date - 9.6 MWp at Jurong Port - contributes just 0.5% to this target total, so many more large systems will be needed in the future.

On the other hand, smaller systems are likely to play a greater role in the future. One of the major shortcomings in this analysis is that the SolarNova systems are grouped together as single "installations", making it impossible to know their real distribution on housing blocks and other sites around Singapore. Surely many of the areas in this work which have been shown as having no installations either have SolarNova systems or those which are not registered on the NSR database, making their actual status unknown. 

### It's not the size, it's what it can do

Tracking the number of systems and their installed capacity is an interesting exercise but it's far more meaningful to understand the impact of these systems in practice. The goal of installing solar is to benefit from the electricity it generates to reduce bills, decrease greenhouse gas emissions or increase energy independence. 

Much more work could be done around [estimating the generation potential of these systems](https://www.renewables.ninja/) and [energy system modelling](https://clover-energy.readthedocs.io/en/latest/) to estimate the electricity generation potential of these systems and the benefits they provide. A lot of great analysis has already been done on this subject (and in far more detail than I could possibly replicate in my spare time) so please [visit the NSR site to learn more](https://www.solar-repository.sg/archives) and go to SERIS - the [Solar Energy Research Institute of Singapore](http://www.seris.nus.edu.sg/) - as the primary sources of information and expertise about past, present and future solar installations in Singapore.

## Disclaimers

I undertook this project in my spare time, motivated by personal interest and to practice some data analysis and visualisation which is a little different from my usual work. This is an ongoing project and will be periodically updated with new results. Any and all opinions, viewpoints and errors are my own. This work can be reproduced under an MIT License.

This work contains data from the National Solar Repository and is [subject to their disclaimers](https://www.solar-repository.sg/disclaimer). With respect to their conditions, the database used in this work is not included in this GitHub repository but users can download their own version for personal and non-commercial use from their website. 

The information contained in the NSR website is for general information purposes only. The information is provided by the Solar Energy Research Institute of Singapore (SERIS) as the National Solar Repository (NSR) Program Administrator and while they endeavour to keep the information up to date and correct, they make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose. Any reliance you place on such information is therefore strictly at your own risk.

This work contains information from Master Plan 2014 Planning Area Boundary accessed on 18 August 2020 from [data.gov.sg](https://data.gov.sg/dataset/master-plan-2014-planning-area-boundary-web?resource_id=2ab23cb2-b1a4-4b1a-a9e1-b9cad0ac159b) which is made available under the terms of the [Singapore Open Data Licence version 1.0](https://data.gov.sg/open-data-licence). Use of this dataset does not in a way suggest any official status or that an Agency endorses the use of the datasets.
