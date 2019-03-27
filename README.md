# ofac-rek

This Elasticsearch cluster is hosted on AWS.
The ACCESS_KEY, SECRET_KEY and HOST are in the environment file.
The XML_FILE in the prompt is downloaded and saved in the local directory, and named in the environment file.

To deploy, run the bash script `deploy.sh`.

There are some arguments that are passed to the function, including the ones in the environment file mentioned above.
The arguments are assigned in `main` -  a more advanced version of this would allow the user to define the dict at the command line or in the bash script.

In the case of the `search_ofac_data` module, the search terms are defined in a valid python dictionary.
The key represents the field to search, (`all` means search all fields), while the value is a list of values to search for in the field. A more advanced version of this module would make better use of Query DSL.
