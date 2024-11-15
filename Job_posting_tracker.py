import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime, timedelta
import urllib.parse
import pandas as pd

class JobPostings:
    def __init__(self, client_id, client_secret, scope, base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.base_url = base_url
        self.access_token = self.get_access_token()
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
            'Cookie': 'BIGipServerVS_EX035-VIPA-A4PMEX_HTTP.app~POOL_EX035-VIPA-A4PMEX_HTTP=4143319562.9038.0000'
        }

    def get_access_token(self):
        url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
        payload = f'grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}&scope={self.scope}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get('access_token')


    def fetch_data_with_pagination(self, params, base_url):
        job_data = []
        start_index = 0
        end_index = 149

        while True:
            params['range'] = f"{start_index}-{end_index}"
            encoded_params = urllib.parse.urlencode(params)
            full_url = f"{base_url}?{encoded_params}"

            response = requests.get(full_url, headers=self.headers)
            # print(int(response.headers['Content-Range'].split('/')[1]))

            if response.status_code == 200:
                page_data = response.json()
                if 'resultats' in page_data:
                    job_data.extend(page_data['resultats'])
                else:
                    job_data.extend(page_data)
            elif response.status_code == 206:
                page_data = response.json()
                if 'resultats' in page_data:
                    print("Data:",page_data['resultats'])
                    job_data.extend(page_data['resultats'])
                else:
                    job_data.extend(page_data)
            else:
                print(f"Limit has been reached: {response.status_code}")
                break

            total_results = int(response.headers['Content-Range'].split('/')[1])
            if len(job_data) >= total_results:
                break

            start_index = len(job_data)
            end_index = min(start_index + 149, total_results - 1)

        return job_data

    # Usage in get_single_day_data method
    def get_single_day_data(self, keyword):
        today = datetime.utcnow()
        start_date = today.replace(hour=0, minute=0, second=0)
        formatted_start_date = start_date.strftime("%Y-%m-%dT00:00:00Z")
        end_date = today.replace(hour=23, minute=59, second=59)
        formatted_end_date = end_date.strftime("%Y-%m-%dT23:59:59Z")

        params = {
            "motsCles": keyword,
            "minCreationDate": formatted_start_date,
            "maxCreationDate": formatted_end_date,
        }

        return self.fetch_data_with_pagination(params, self.base_url)

    # Usage in get_historical_job_postings method
    def get_historical_job_postings(self):
        today = datetime.utcnow()
        start_date = today - timedelta(days=180)
        formatted_start_date = start_date.strftime("%Y-%m-%dT00:00:00Z")
        end_date = today.replace(hour=23, minute=59, second=59)
        formatted_end_date = end_date.strftime("%Y-%m-%dT23:59:59Z")

        params = {
            "minCreationDate": formatted_start_date,
            "maxCreationDate": formatted_end_date,
        }

        return self.fetch_data_with_pagination(params, self.base_url)

    def visualize_data(self, job_data):
            df = pd.DataFrame(job_data)

            commune_counts = df['lieuTravail'].apply(lambda x: x.get('commune', None)).value_counts()
            department_counts = df['lieuTravail'].apply(lambda x: x['libelle'].split(',')[0] if 'libelle' in x else None).value_counts()

            top_10_communes = commune_counts.nlargest(20)
            # other_communes = pd.Series({'Other': commune_counts.drop(top_10_communes.index).sum()})
            # commune_counts_top_10 = pd.concat([top_10_communes, other_communes])

            top_10_departments = department_counts.nlargest(20)
            # other_departments = pd.Series({'Other': department_counts.drop(top_10_departments.index).sum()})
            # department_counts_top_10 = pd.concat([top_10_departments, other_departments])

            df['dateCreation'] = pd.to_datetime(df['dateCreation'])
            df['month'] = df['dateCreation'].dt.to_period('M')
            monthly_counts = df.groupby('month').size()

            plt.figure(figsize=(14, 8))

            plt.subplot(2, 2, 1)
            sns.barplot(x=top_10_communes.index, y=top_10_communes.values, palette='viridis')
            plt.title('Top 10 Communes by Number of Job Postings')
            plt.xlabel('Commune')
            plt.ylabel('Number of Job Postings')
            plt.xticks(rotation=90)

            plt.subplot(2, 2, 2)
            sns.barplot(x=top_10_departments.index, y=top_10_departments.values, palette='viridis')
            plt.title('Top 10 Departments by Number of Job Postings')
            plt.xlabel('Department')
            plt.ylabel('Number of Job Postings')
            plt.xticks(rotation=90)

            plt.tight_layout()
            plt.show()


# Example usage
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT"
scope = "api_offresdemploiv2%20o2dsoffre"
base_url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

job_postings = JobPostings(client_id, client_secret, scope, base_url)

# Retrieve single day data
single_day_data = job_postings.get_single_day_data("Software")
print("Single day data:",single_day_data)

# Retrieve historical job postings
historical_data = job_postings.get_historical_job_postings()
print("Historical data:",historical_data)
# Visualize data
job_postings.visualize_data(historical_data)