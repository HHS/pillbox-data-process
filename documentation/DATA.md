## Overview

Many developers new to working with medication-related data are unaware of potential errors and discrepancies within the data.  This document provides an overview of many issues present in the Pillbox data set.  It is intended as an educational resource to 1) help developers better understand the data, and 2) illustrate the scope and limitations of working with this data, which is critical when creating applications that identify unknown medication or provide information to clinicians, patients, and others.

It is also intended to be a starting point for discussion and further exploration of this data with the goal of improving downstream utilization by a growing community of innovative individuals and groups seeking to solve challenges related to not only medication identification and reference, but across health care.

This report is not intended to definitively confirm the presence of an error in Structured Product Labeling data supplied by a submitting firm.  Rather, it highlights potential errors, discrepancies, and data of interest based on analysis of data outlying expected parameters.  It is not intended to be comprehensive.

Pillbox’s data is derived from the Structured Product Labeling, obtained via NLM’s DailyMed and NLM’s RxNorm, a normalized naming system for generic and branded drugs.

### Data changes and transparency

Because changes are now being made to the data based on comparison of pill images to the physical characteristics data, every effort is being made to be as transparent as possible about this process.  This includes making a table of all changes made to data available for download, web pages which list every change made along with the image used for comparison, and this document which defines the scope and methodology used to make these changes.

The scope of these changes is not intended to be complete.  In situations where ambiguity exists the original data is not modified.  For records where there is no image available, it is not possible to verify the physical characteristics data.

Data changes in Pillbox do not affect the master data derived from the drug labels, available via DailyMed.

### Identification of data errors and discrepancies

Errors or discrepancies in Pillbox's data can be identified either visually (comparing pill images to data) or algorithmically (querying data based on logical assumptions about the data).

To the best of the Pillbox team's knowledge, no federal agency reviews the physical characteristics data for pills.  It is our hope that Pillbox (and the pill images produced through the project) will be a catalyst for the development of manual or automated validation systems for these data and improvement in the overall accuracy of these data.

### Three unique problems

#### Re-labeling and re-distribution

A unique type of discrepancy can occur when a pill is marketed by more than one company.  Company A may manufacture and market a drug.  They may also allow other companies to distribute and market that same drug.  Each company must submit a separate drug label and that same pill will have a different National Drug Code (NDC) in that label.  Some distribution chains may be quite large.  The small, brown, 200 mg ibuprofen, that has an imprint of "I2" for example, is distributed under almost 80 different NDCs and labels.

An upcoming data release of Pillbox will group pills by physical characteristics, ingredients and strength, and other criteria so that each unique pill has only one record.  In practice there may not be possible as some label authors have changed one or more of the physical characteristics or other data from the source label.

The benefits of organizing pills by original manufactured products extend beyond simplifying identification and improving user experience.  If an issue, such as contamination, should ever be occur with a medication, identifying all distribution points for that medication is critical for public safety.  Developers should have easy access to that information.

#### Manufacturers changing the appearance of a pill

FDA guidance requires (citation needed) that if the physical characteristics of a pill change, then that product requires a new NDC.  The most common change made to a pill is the imprint.  When a manufacturer changes the physical characteristics of a pill and does not apply for a new NDC, it creates a conflict in presenting the data, especially if there is an image for the pill.

For example, Company A has a pill with an imprint "123 10".  They then change the imprint to "A 10".  For a certain time, both pills will be available.  If the imprint in the image differs from the data, it may be difficult to determine if the imprint data is 1) incorrect or 2) the imprint has changed but the original NDC was kept.  Also, if both pills are present in the market, there should be two separate records as users could be trying to identify either pill.

#### Identifying pills that are no longer marketed

Pillbox was not designed to be an archival resource.  It was intended to reflect the current information available via its sources.  The data process which creates Pillbox takes current data from DailyMed and RxNorm and parses individual products (pills).  Cases exist however where a user is trying to identify an older medication, stored for years in a medicine cabinet.  In disaster response situations, medications which are past the expiration date may be used if certain criteria are met and tests show the medications have retained their potency.

This issue will also be addressed by the upcoming data release will pills will be grouped by physical characteristics.  It has yet to be determined how far back in time to go, looking for unique pills.  Also, without images it will be difficult to verify the accuracy of the physical characteristics used to group the pills.  This will results is a greater number of groups, with some groups being created based on inaccurate data.  Groupings based on accurate data will be unaffected.

### Visually identifying data issues

FDA publishes guidance for coding the physical characteristics (imprint, color, shape, size, score) of pills.  Based on a review of the 2,159 images available via Pillbox as of July 2013, changes were made to the physical characteristics data of approximately 17% (359) of records for which there was an image.

As Pillbox increases the number of standardized, high quality images available, those images will be compared to data for each product to ensure physical characteristics (imprint, color, shape, size, score) data match the images.  While many of these errors are more easily identified than others (a round pill listed as square), some criteria are more subjective or nuanced.

Where data is modified, the goals are to improve search results without introducing ambiguity and to accurately represent the text that appears on a pill.  All changes made to the data are listed in the trade_dress_change_log table.

#### Imprint

Before continuing, you should read the FDA form and submission requirements for "imprint":http://www.fda.gov/Drugs/DevelopmentApprovalProcess/FormsSubmissionRequirements/ElectronicSubmissions/DataStandardsManualmonographs/ucm071810.htm.

Imprint is perhaps the single best identifier for a pill and presents challenges when developing search logic.  While relatively few errors of commission (typographic errors) have been found in the data based on a comparison to available pill images, a number of other factors are present.

Issues encountered:
* Company or drug names are sometimes omitted from the imprint data.
* Descriptive text is included in the imprint value (ex: "A;10;company logo")
* Imprint has been changed by the manufacturer
* Some imprint values are formatted inconsistently in a way that may affect search results

Additional rules:
* Trailing semi-colons in the data are removed (ex: "A;10;" changed to "A;10")
* Dashes, decimal points, slashes and spaces are replaced with semi-colons
* Stylized single letters (which often appear on pills) are entered as part of the imprint value
* Text that appears on separate line or is separated by a score line is separated in the imprint value by semi-colons
* If text is repeated on an pill (ex: a scored pill with the number 10 on both sides or a pill with the letter A appearing multiple times around the edge of a pill) it is entered as separate text.  This will increase the likelihood of an exact match while not interfering with search strings that only include one iteration of repeated text and errs on the side of an accurate representation of the look of the pill.
* Text the crosses itself (ex: BAYER written vertically and horizontally, crossing at the Y) is entered as separate values, separated by a semi-colon.

One additional area of concern related to imprint values are characters which look similar.  Text on a pill is often small and the various imprinting processes may render text that is difficult to read.  Users may not be able to accurately identify a character in situations like these.

* lower-case L vs the number one (1)
* Upper-case O vs the number zero (0)

#### Color

Before continuing, you should read the FDA form and submission requirements for "color":http://www.fda.gov/Drugs/DevelopmentApprovalProcess/FormsSubmissionRequirements/ElectronicSubmissions/DataStandardsManualmonographs/ucm071794.htm.

Color is the most subjective of the physical characteristics, however it is one of the most likely to be used by an individual describing a pill.  Existing guidance specifies RGB values for each of the 12 colors.  Color perception varies greatly among individuals and is subject to ambient lighting conditions (indoor fluorescent and incandescent light sources, sunlight, reflected light, etc.).  As such, similarly colored pills may be listed as a variety of similar colors, such as red/orange/brown or blue/turquoise/green.

Issues encountered:
* Pills listed as a color that is obviously different from the predominant color present in the image.  In these situations the color value was changed to that of the predominant color.  The new color is subject to the subjectivity described previously.

Additional rules:
* Though the guidance specifies that there should be only one value present for color, it is common to see two colors listed.  This practice is upheld in Pillbox's data.
* For pills that have more than one distinct color (a capsule with a pink cap and white base), the secondary color is added.
* If the labeler lists a single color and the pill could also be described by a second color, that color may be added.
* When more than one color is listed, if there is a predominant color (such as a yellow pill with a small white section in the middle) the predominant color is listed first.  This provides the potential to enhance search and more accurately describe the pill without negatively affecting search results.
* Double color listings (ex: white/white) were change to a single value of that color.

The NLM Pillbox SPLIMAGE pill image specification creates images under standardized lighting conditions.  It is hoped that these images will lead to development of an automated system to accurately define the predominant color of a pill and create a pallet of colors that is representative of the colors present.

#### Shape

Before continuing, you should read the FDA form and submission requirements for "shape":http://www.fda.gov/Drugs/DevelopmentApprovalProcess/FormsSubmissionRequirements/ElectronicSubmissions/DataStandardsManualmonographs/ucm071802.htm.

The guidance for shape have two specific nuances that may not be obvious.  First, when dealing with multi-sided shapes, such as pentagons (5-sided) or hexagons (6-sided), the sides do not need to be equal in length.  Also, sides do no need to be straight.  Thus a 

Issues encountered:
* Shapes listed as freeform that are actually multi-sided shapes
* Capsules (two-part capsules) listed as oval.
* Oval tablets listed as capsule.  Even if the medication name includes the word "capsule" if it is not a two-part capsules and banded two-part capsule it should be listed as oval.

#### Size

Before continuing, you should read the FDA form and submission requirements for "size":http://www.fda.gov/Drugs/DevelopmentApprovalProcess/FormsSubmissionRequirements/ElectronicSubmissions/DataStandardsManualmonographs/ucm071800.htm.

Without having a pill to measure it is difficult to identify inaccuracies in the size values.  The NLM Pillbox SPLIMAGE pill image specification includes a ruler in the image.  Some size values however are present.

Issues encountered:
* Pills which size value differs from the ruler present in the image.

Additional rules:
* If the size as measured in an SPLIMAGE spec image varies by more than 2 mm from the size value provided, it is changed to match the value as measured in the image.

#### Score

Before continuing, you should read the FDA form and submission requirements for "score":http://www.fda.gov/Drugs/DevelopmentApprovalProcess/FormsSubmissionRequirements/ElectronicSubmissions/DataStandardsManualmonographs/ucm071805.htm. 

Issues encountered:
* Incorrect score values entered
* Pills with different score values on either side
* Though the guidance states score refers to the pill being broken into "equal sized pieces" there exists a pill that is scored to be broken into unequal sized pieces (different dosages)
* Some score lines are faint or only present near the edges of the pill (not a continuous line across the pill)

Additional rules:
* When a pill is scored differently on either side (one side can be divided into two pieces, the other side can be divided into three pieces), the higher score value is entered.  This is consistent with the one known example.

### Algorithmically identifying data issues

Logical assumptions about the data and relationships between data can identify potential issues.  These issues are not addressed in Pillbox's data unless there is an image present.

#### NULL values

On occasion, certain values in the data are NULL. 

#### Capsules with score = 1

#### Size outliers

* Pills with extremely large (30+ mm) or small (0 or 1 mm) size values

#### Size with a decimal point

#### Pills listed a REMAINDER

#### DEA schedule is NULL

NULL is a valid value for DEA schedule.  It implies that the drug is not scheduled.  However, when you see a NULL value you cannot definitively know if the drug is not scheduled or the labeler forgot to list the value.  There are records for drugs that are on the DEA schedule but some of the records lists the DEA schedule as NULL.

#### Duplicate records

### Other techniques for identifying issues in the data

#### Data which is not normalized (inactive ingredients, author)

#### Comparison of records believed to be redistributed products

#### Faceting via OpenRefine