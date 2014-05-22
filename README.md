## Pillbox for Developers
### Pillbox Data Process

Pillbox, an initiative of the National Library of Medicine at the National Institutes of Health, provides data and images for prescription, over-the-counter, homeopathic, and veterinary oral solid dosage medications (pills) marketed in the United States of America. This data set contains information about pills such as how they look, their active and inactive ingredients, and many other criteria.

Pillbox's primary data source (FDA drug lables) is complex and does not organize information based on individual pills. Additionally, there are very few pill images available in the source data. The Pillbox initative has focused on restructuring the source data, incorporating data from other related data sets, and creating a library of pill images.

A major function of the initiative was the development of a data process which ingests the source data and produces an easy-to-use, "pill-focused" dataset.

This repository contains the code for that process. It is intended to begin to give developers greater flexibility in using this data as well as expand the scope of and refine the data process. This repository will continue to grow as well as access to the data will continue to improve. 

### Get started using or contributing to the code

  - [Read more](https://github.com/HHS/pillbox-data-process/blob/master/documentation/SETUP.md) about setting up your local environment
  - Start [contributing](https://github.com/HHS/pillbox-data-process/blob/master/CONTRIBUTING.md) to the development

### Uses of this data

  - Identify unknown pills based on their physical appearance
  - Assist in development of electronic health records, medication information systems, and adherence/reminder/tracking tools
  - Support research in areas such as informatics and image processing

### Warning

Pillbox's source data is known to have errors and inconsistencies. Read this document before working with Pillbox's API, data, and images.

[Read more about Pillbox](https://github.com/HHS/pillbox-data-process/blob/master/documentation/ABOUT.md).
