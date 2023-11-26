import csv

# Read the text file
with open('output.txt', 'r') as file:
    lines = file.readlines()

# Process each line and write to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Writing the header of the CSV file
    csvwriter.writerow(['YearMonth', 'Keyword1', 'Keyword2', 'Keyword3', 'Keyword4'])
    
    # Processing each line
    for line in lines:
        # Splitting the line by ': ' to separate the date and the keywords
        year_month, keywords = line.strip().split(': ')
        
        # Splitting the keywords by ', ' and stripping extra spaces
        keywords_list = [keyword.strip() for keyword in keywords.split(',')]
        
        # Writing to the CSV file
        csvwriter.writerow([year_month] + keywords_list)

print("CSV file has been created successfully.")
