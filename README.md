# End to End Data Engineer Project - AWS
![image](https://github.com/user-attachments/assets/d66cfb32-3428-4577-b70c-610acf255cc9)


**Project Overview:**

In this project, we aim to securely manage, streamline, and perform comprehensive analysis on structured and semi-structured YouTube video data, focusing on video categories and trending metrics. The project involves building a scalable ETL pipeline using various AWS services to transform and analyze data, ultimately creating a dashboard for insightful visualizations. 

**[View the final dashboard here](https://eu-north-1.quicksight.aws.amazon.com/sn/embed/share/accounts/017820663920/dashboards/d6dfb408-c9b4-4d49-98e3-905ca955abb2?directory_alias=vanessandersson).**

### Embedding the Dashboard in HTML

To view the dashboard directly on a webpage, you can use the following embedded code:

<iframe
    width="960"
    height="720"
    src="https://eu-north-1.quicksight.aws.amazon.com/sn/embed/share/accounts/017820663920/dashboards/d6dfb408-c9b4-4d49-98e3-905ca955abb2?directory_alias=vanessandersson">
</iframe>

### **Architecture:**
The architecture involves multiple steps, beginning with the ingestion of raw data into an AWS S3 bucket. The data undergoes various transformations using AWS Glue ETL and AWS Lambda, converting it into a structured parquet format. The transformed data is then stored in a separate S3 bucket. Subsequently, two tables—created from JSON and CSV data—are joined to form the final dataset, which is visualized using AWS QuickSight. This architecture ensures a robust, scalable, and efficient data pipeline.

### **Project Goals:**
1. **Data Ingestion:** Develop a mechanism to ingest and store data from different sources into AWS S3.
2. **ETL System:** Implement an ETL pipeline to clean, transform, and structure the raw data.
3. **Data Lake:** Establish a centralized repository on AWS S3 to store structured and semi-structured data.
4. **Scalability:** Ensure the system can scale efficiently as the data volume increases.
5. **Cloud Utilization:** Leverage AWS cloud services for processing large datasets that exceed local computing capabilities.
6. **Reporting:** Build a dashboard using AWS QuickSight to visualize key insights and metrics derived from the data.

### **Technologies Used:**
- **Amazon S3:** Object storage service used for storing raw and processed data.
- **AWS IAM:** Manages user identities and access to AWS resources.
- **AWS Glue:** Serverless data integration service for discovering, preparing, and combining data.
- **AWS Lambda:** Serverless computing service for running code in response to events, used for data transformation.
- **AWS Athena:** Interactive query service for analyzing data stored in S3 using standard SQL.
- **AWS QuickSight:** Business intelligence (BI) service used to create visualizations and dashboards.

### **Dataset Used:**
The dataset used is from Kaggle, which includes statistics on daily popular YouTube videos across various regions. The data comprises video titles, channel names, publication times, views, likes, comments, and other relevant metrics, along with a `category_id` field linked to JSON files for each region.

### **Project Implementation:**
1. **Setting Up AWS IAM and CLI:** Create an IAM user with necessary permissions and set up AWS CLI for interaction with AWS services.
![image](https://github.com/user-attachments/assets/5566d13a-ef08-408b-90f3-54bae56f0b40)

2. **Data Upload to S3:** Upload the Kaggle dataset to an S3 bucket, organizing it by region and format.
![image](https://github.com/user-attachments/assets/78142865-5407-46ea-99af-35883c73dc6f)
![image](https://github.com/user-attachments/assets/4c1574f0-4f7e-4a6f-85dd-e28fc3339650)
![image](https://github.com/user-attachments/assets/47c5e68e-531e-4b33-99f0-8533594caca8)

3. **Data Transformation:**
   - **AWS Glue Crawler:** Create a schema for JSON data using AWS Glue Crawler.
   - **AWS Lambda:** Convert JSON data into parquet format using AWS Lambda, handling nested arrays and complex data structures.
   - **AWS Glue ETL:** Transform CSV data into parquet format, ensuring schema compatibility for data joining.
4. **Data Querying:** Use AWS Athena to query the transformed data and perform joins between different datasets.
5. **Automation:** Set up triggers in AWS Lambda to automatically process new data as it arrives in S3.
6. **Final Data Preparation:** Join cleaned datasets using AWS Glue ETL to create a comprehensive analytics table.
7. **Data Visualization:** Import the final dataset into AWS QuickSight and create dashboards for visual analysis.

### **Final Outcome:**
Through this project, we successfully created a scalable and efficient ETL pipeline that ingests, processes, and analyzes YouTube video data. The final output is a set of insightful visualizations in AWS QuickSight, providing valuable metrics on video popularity and trends. This project showcases the effective use of AWS services to manage and analyze large-scale data, enabling data-driven decision-making. **[Check out the Data Ops for looking at the tickets for this project](https://github.com/users/van-essa/projects/3/views/1).**


---
### **Bug Report: `No module named 'awswrangler'` Error in AWS Lambda**

#### **Issue Summary**
After updating the Python runtime version of an AWS Lambda function from Python 3.8 to Python 3.12, an error occurred when invoking the function:
```
"errorMessage": "Unable to import module 'lambda_function': No module named 'awswrangler'"
```
This error was unexpected since the `awswrangler` module had been installed and added as a layer to the Lambda function.

#### **Root Cause Analysis**
The issue was due to the Lambda function being unable to locate the `awswrangler` module in the specified layer. The following potential causes were identified:

1. **Layer Configuration**: The layer might not have been properly attached to the Lambda function.
2. **Python Version Compatibility**: The `awswrangler` module or its version might not have been compatible with Python 3.12.
3. **Packaging Issues**: There could have been an issue with how the `awswrangler` module was packaged in the layer, leading to an incorrect directory structure.

#### **Steps to Resolve**

1. **Verify Layer Attachment**:
   - Checked the Lambda function's configuration to ensure the layer containing `awswrangler` was properly attached.
   - Confirmed that the correct layer was listed under the "Layers" section of the function's configuration.

2. **Check Layer Content and Structure**:
   - Verified that the layer was packaged correctly and contained the `awswrangler` module in the appropriate directory structure:
     ```
     layer.zip
     └── python
         ├── awswrangler
         └── ...
     ```

   - If the layer was not correctly structured, it was repackaged using the following steps:
     ```bash
     mkdir python
     pip install awswrangler -t python/
     zip -r layer.zip python
     ```
   - Uploaded the repackaged `layer.zip` as a new Lambda layer.

3. **Ensure Python 3.12 Compatibility**:
   - Verified that the installed version of `awswrangler` was compatible with Python 3.12. If necessary, installed a version of `awswrangler` that is known to work with Python 3.12.

4. **Detach and Reattach the Layer**:
   - Detached the layer from the Lambda function and saved the configuration.
   - Reattached the layer to ensure it was correctly recognized by the Lambda runtime.

5. **Test Locally**:
   - Tested the Lambda function code locally using Python 3.12 to ensure that the `awswrangler` module was functioning as expected.

6. **Re-deploy and Verify**:
   - After making these changes, redeployed the Lambda function and verified that the error was resolved.

#### **Conclusion**
The issue was resolved by verifying the layer's attachment, ensuring the correct packaging of the `awswrangler` module, and confirming compatibility with Python 3.12. After reattaching the layer and redeploying the function, the Lambda function successfully imported the `awswrangler` module and executed without errors.
