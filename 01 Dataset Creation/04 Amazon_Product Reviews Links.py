import os
import pandas as pd
from tqdm import tqdm

dir_name = r"C:/Users/likhi/Documents/01 Pycharm Code Folder/001 Master Thesis/01 Dataset/01 Amazon/"
destination_dir = r"C:/Users/likhi/Documents/02 Pycharm Datasets/01 Master Thesis/08 Review Data/"
folders = ['02 Product Urls', '02a Product Urls_to COLAB']

review_ending_string_part1 = '/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&pageNumber='
review_ending_string_part2 = '&pageSize=20'

total_urls = []

for folder in folders:
    print(folder)
    folder_path = os.path.join(dir_name, folder)
    csv_files = [i for i in os.listdir(folder_path) if '.csv' in i]

    for csv_file in tqdm(csv_files):
        csv_data = pd.read_csv(os.path.join(folder_path, csv_file))

        for url in csv_data.urls.tolist():
            if '/dp/' in url:
                for i in range(1,6):
                    review_url = url.replace('/dp/', '/product-reviews/') + review_ending_string_part1 + str(i) + review_ending_string_part2
                    total_urls.append(review_url)


print(len(total_urls))

total_urls = list(set(total_urls))

print(len(total_urls))

with open(destination_dir + "Amazon product Review Links.txt", 'w') as f:
    f.write("\n".join(total_urls))
    f.close()
print("Finished saving as a text file!")

total_urls_df = pd.DataFrame(total_urls, columns=['urls'])
# total_urls_df.to_excel(destination_dir + "Amazon product Review Links.xlsx", index=False)
# print('Finished saving as an Excel file!')

# total_urls_df.to_csv(destination_dir + "Amazon product Review Links.csv", index=False)
# print('Finished saving as an CSV file!')

for i,chunk in enumerate(pd.read_csv(destination_dir + "Amazon product Review Links.csv", chunksize=100000)):
    chunk.to_csv(destination_dir + 'Amazon product Review Links chunk {}.csv'.format(i), index=False)

print('Finished saving as chunks of CSV files!')
#
