from github import Github
ACCESS_TOKEN = '33cf731019ac819a3f180fc82a10aaf7140a07b5'
g = Github(ACCESS_TOKEN)
print(g.get_user().get_repos())
if __name__ == '__main__':
    keywords = input('Enter keyword(s)[e.g python, flask, postgres]: ')
keywords = [keyword.strip() for keyword in keywords.split(',')]


def search_github(keywords):
    query = '+'.join(keywords) + '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')

    max_size = 10
    print(f'Found {result.totalCount} file(s)')
    if result.totalCount > max_size:
        result = result[:max_size]

    for file in result:
        print(f'{file.clone_url}')


search_github(keywords)
