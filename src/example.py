
import anonfile
# create anonfile object
# if an API-Key is provided it uploads directly in your anonfile account. (provide with: api_key=1234abc)
af = anonfile.Anonfile()
# upload a file
response = af.upload('test.txt')
# access specific member of response
print(response.url_short)
print(response.file_id)
# get full response as dictionary
res_dict = response.getfullres()
for k, v in res_dict.items():
    print(k, v)

# ye