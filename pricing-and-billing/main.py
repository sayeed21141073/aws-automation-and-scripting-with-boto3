"""Billing with Cost Expolorer"""

import boto3

client = boto3.client('ce')

"""Task01: Calculate cost and usage over last 90 days"""
#start_date = 90 days ago's date
#end_date = today's date

from datetime import datetime, timedelta

start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

response = client.get_cost_and_usage(
    TimePeriod={'Start': start_date, 'End': end_date},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost','UsageQuantity']
)
#print(response)

"""Task02: What services I used in the last 3 months."""
#Note: get_dimension_values method will be used

results = client.get_dimension_values(
        TimePeriod={'Start': start_date, 'End': end_date},
        Dimension = 'SERVICE'

)
#print(results)
"""for service in results['DimensionValues']:
    #print(service['Value'])"""

"""Task03: How much I spent on Each service (Task01 and Task02 combined)"""

cost_on_each_service = client.get_cost_and_usage(
    TimePeriod={'Start': start_date, 'End': end_date},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy = [
        {
            'Type':'DIMENSION',
            'Key':'SERVICE'
        }
    ]
)
#print(cost_on_each_service)

"""Task04: Cost Forecast for next 90 days"""
# new_start_date = today
# new_end_date = today+ 90 days

new_start_date = datetime.now().strftime('%Y-%m-%d')
new_end_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')

cost_forecast = client.get_cost_forecast(
    TimePeriod={'Start': new_start_date, 'End': new_end_date},
    Granularity='MONTHLY',
    Metric='UNBLENDED_COST' 
)
#print(cost_forecast)









