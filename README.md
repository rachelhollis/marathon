# Marathon

First Python Script I created to automate a routine task.

## Overview

When a new Asset, Customer Account, or SWD is added, a manual process was done that took hours upon hours. Automating the process allows time to be spent on a less tedious task.

The Process to automate:

- Generate combinations of the new entries with all the existing entries
- Combinations requirements: The asset and swd must have the same district. i.e north or south. The Asset, SWD, and Customer Accounts must be for the Bakken Region
- For each combination, calculate the distance between the Asset and SWD
- Based on the distance calculated, assign a mileage band 
- Mileage band requirements: the asset well phase must equal the well phase of the mileage band
- Based on the mileage band and customer account, assign a unit rate
- Upload all finished combinations into the TMSMileageBands table
- Change flag of new assets, swds, and customer accounts to add them to the existing assets, swds, and customer accounts

## Process



### Get the ID of the Bakken Region and the ID of Water Hauling

![resources/1-2.PNG](resources/1-2.PNG)

- The region will be used to obtain the correct Assets, Customer Accounts, and SWD
- The only Customer Accounts we are interested in are those that have the Water Hauling ID

### Gather Customer Account, Asset, and SWD Items

#### New Customer

![resources/3.1.PNG](resources/3.1.PNG)

- Obtain information on any new Customer Accounts
- New Customer Accounts has a AWS_MileageBand flag equal to -1
- The same process is used to obtain the existing Customer Accounts with a AWS_MileageBand flag not equal to -1

#### New SWD

![resources/3.2.PNG](resources/3.2.PNG)

#### New Assets

![resources/3.3.PNG](resources/3.3.PNG)

##### New Asset Example

![resources/newasset.PNG](resources/newasset.PNG)

### Generate Combinations of Bands

![resources/4.PNG](resources/4.PNG)

- Generate combinations of new records with the existing records
- The districts must match (North and North or South and South) for Assets and SWDs

### Calculate Distances

![resources/5.PNG](resources/5.PNG)

- Using the generated combinations, the distance between the SWD and Asset is calculated and rounded to the nearest whole number

### Get Mileage Bands and Assign them to the combinations

![resources/6-7.PNG](resources/6-7.PNG)

- The mileage band table is gathered and reformatted
- Requirements to assign mileageband: The well phase of the asset must match the well phase of the mileage band and the distance must fall inbetween a max and min of the mileage band

#### mileage band table

![resources/mbtable.PNG](resources/mbtable.PNG)

- This is the mileage band table that is being referenced

### Get and Assign Unit Rate

![resources/8.PNG](resources/8.PNG)

- The unit rates are gathered
- The unit rate table is merged with the distance table based on the mileage band and the customer account
- Records with null values are dropped

### Export to TMSMileageBand table

![resources/9.PNG](resources/9.PNG)

- The completed records are uploaded to the TMSMileageBand Table

### Change flags of new CA, Asset, and SWD to false

![resources/10.PNG](resources/10.PNG)

- The AWS_MileageBands flag is changed so the next time the script is run, they will be recorded as existing records not new
