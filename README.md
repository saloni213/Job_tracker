# Job_tracker
A company is tasked with tracking job postings for its French clients. The goal is to list job postings published on a specific day and, with a sample of postings from several months, create overall statistics on the job market trends across various municipalities and departments in France.

## Overview

This project interacts with the [France Travail API](https://francetravail.io/data/api) to retrieve job postings data for Civision's French clients. The application allows you to:

- Fetch job postings published on a specific day.
- Fetch historical job postings spanning several months.
- Visualize trends in the job market across various municipalities and departments in France.

The data is visualized using **matplotlib** and **seaborn** to produce bar charts that show the distribution of job postings across different communes and departments.

## Technologies Used

- **Python** 3.x
- **Requests**: To make API requests.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib** and **Seaborn**: For data visualization.

## Getting Started

### Prerequisites

Make sure you have Python 3.x installed on your machine. You also need to install the following dependencies:

- `requests`
- `pandas`
- `matplotlib`
- `seaborn`

### You can install them using `pip`:

    ```bash
    pip install requests pandas matplotlib seaborn

## Configuration

You need to provide your client_id and client_secret from the France Travail API in the code, otherwise, it will throw an error.

## Running the Script

1. Single Day Data: To retrieve job postings for a specific keyword on the current day:

    ```bash
    single_day_data = job_postings.get_single_day_data("Software")
    print("Single day data:", single_day_data)

2. Historical Data: To retrieve historical job postings for the last 6 months:

    ```bash
    historical_data = job_postings.get_historical_job_postings()
    print("Historical data:", historical_data)

3. Visualizing Data: To visualize job postings trends across communes and departments:

    ```bash
    job_postings.visualize_data(historical_data)

## Example Output

- Top 10 Communes by Number of Job Postings
- Top 10 Departments by Number of Job Postings
- Job Postings Trends over the Last 6 Months

<img width="1394" alt="image" src="https://github.com/user-attachments/assets/b66c326c-b49c-41e2-882a-f1900bac125c">

## Code Structure

- JobPostings class: Handles the connection to the France Travail API and includes methods for retrieving and visualizing job postings data.
    - get_access_token(): Fetches an access token using client credentials.
    - fetch_data_with_pagination(): Fetches paginated job posting data.
    - get_single_day_data(): Fetches job postings for a specific day.
    - get_historical_job_postings(): Fetches job postings for the past 6 months.
    - visualize_data(): Visualizes the data using matplotlib and seaborn.

## Notes
- The script uses pagination when fetching large amounts of job posting data.
- Ensure that you replace "YOUR_CLIENT_ID" and "YOUR_CLIENT_SECRET" with your actual credentials from the API.
