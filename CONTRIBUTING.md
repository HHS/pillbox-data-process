## Contributing to Pillbox

Welcome to the Pillbox Data Process. Below is a guide for getting started in participating in the project. Whether you are a user of the data, interested in how the data in generated, or want to improve the quality of the data, the sections below outline how to get started contributing. 

### How to contribute

There are two main ways to contribute to the project: 

1. Report on data quality or errors 
2. Improve data generation process 

### Report on Data Quality or Errors

The first way to get invovled in the Pillbox project is to participate in flagging errors or sending reports on data quality. The project uses the [Issue tracker](https://github.com/HHS/pillbox-data-process/issues) to manage and discuss reports and questions about the project. 

Here's a short list of items to consider before submitting an issue: 

  - Please search for your issue before filing it; errors or quality issues may have been already reported. 
  - If you encountered an error in the data process, write specifically what the error was and how to replicate the error.
  - Please keep issues professional and straightforward. This is an evolving effort and we look to the community to help improve the quality and the process. 
  - Please use the Labels to mark type of issue. We've pre-categorized labels we think are currently appropriate. These will help flag for context. 

### Improve Data Generation Process 

The second way to get involved in the Pillbox project is to contribute to improving the data process. The data generation process is a series of Python scripts that download, unzip, and parse FDA SPL XML data. The goal for this process is to continually improve. We see this improving in two ways: 

#### 1. Improving error handling 

The FDA SPL data consistantly experiences quality issues. Occasionally these issues can lead to breaking the data process. If you encounter your data process to be broken, please contribute back in the following ways: 

1. Debug the error and submit a Pull Request for the new code that handles the error. 
2. Submit an issue reporting the new error and any suggestions for how to improve it. 

#### 2. Improving secondary data products 

The main Pillbox product is the `spl_data.csv` file. This is the master dataset that is made available. In addition, secondary data products are being made available. This includes indidividual json file access to products, and we're growing static API access to the data. 

If you want to contribute to creating new secondary data products, you can help us in two ways: 

1. Contribute code to `api.py` or create a new python script and submit a Pull Request. 
  - This is the best way to add to the process by creating new slices of the data, or generating a unique analysis of the data. 
2. Recommend improvements in the Issue tracker. 
  - Submit a recommendation by creating a new ticket for discussion. Another developer may possibly be able to implement and contribute code based on the recommendation. 

