#import requests
from github import Github
import pprint
import os
import csv
from datetime import datetime

# GITHUB_CONFIG = {
#     'URL': 'https://api.github.com/repos/microsoft/vscode/pulls',
#     'HEADERS': {
#         ' Accept': 'Application/vnd-github+json*',
#         'Authorization': ''
#         },
#     ' PARAMS': {
#         'state': 'all',
#         'per_page': '5'
#         }
# }
token = os.environ['GITHUB_TOKEN']

repoResponse = Github(token).get_repo('microsoft/vscode')
pulls = repoResponse.get_pulls(state='closed', sort=' created', direction='desc*')
# response = requests-get(GITHUB_CONFIG[ 'URL'], headers-GITHUB_CONFIG[ "HEADERS']. params-GITHUB_CONFIG[ 'PARAMS' ])

# if response.status_code == 200:
# else:
#     raise Exception(f"request inválida: {response.text}")
# responseData = response-json()
for pull in pulls[:1]:
    pprint.pprint(vars(pull))
    # if pull.merged_at:
    #     cycle = (pull.merged_at - pull.created_at).total_seconds() / 3600

    #     print(f"PR: #{pull.number} - {pull.title}")
    #     print(f"Autor: #{pull.user.login}")
    #     print(f"Criado em: #{pull.created_at}")
    #     print (f"Merged em: #{pull.merged_at}")
    #     print(f"Estado: #{pull.state}")
    #     print(f"Tempo de ciclo: {cycle:.2f} horas")
    #     print("\n\n\n")
    # else:
    #     print(f"PR: #{pull.number} - {pull.title} ainda nao mergeado")
    #     print(f"Estado: #{pull.state}")

with open('PRs_vscode.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'number', 
        'title', 
        'author', 
        'created_at', 
        'merged_at', 
        'state', 
        'cycle time', 
        'reviews',
        'has_description',
        'additions',
        'deletions'
    ])

    for pull in pulls[:10]:
        if pull.merged_at:

            cycle = (pull.merged_at - pull.created_at).total_seconds() / 3600
            substringDesc = pull.body

            try:
                defaultCommentStart = pull.body.index('<!--')
                defaultCommentEnd = pull.body.index('-->') + 3
                tempStart = pull.body[:defaultCommentStart]
                tempEnd = pull.body[defaultCommentEnd:]
                substringDesc = tempStart + tempEnd
            except ValueError:
                print('caractere nao encontrado')

            substringDesc = substringDesc.strip()
            writer.writerow([
                pull.number,
                pull.title,
                pull.user.login,
                pull.created_at,
                pull.merged_at,
                pull.state,
                str(round(cycle, 2)) + ' horas',
                pull.get_reviews().totalCount,
                'Sim' if len(substringDesc) > 1 else 'Não',
                pull.additions,
                pull.deletions
            ])
    else:
        print(f"ainda nao mergeado")
