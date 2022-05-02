# Config upload action

Github action for uploading configuration files to extraction pipelines in Cognite Data Fusion. Takes a root directory and recursively uploads config files to extraction pipelines matching their name. E.g. "my-extpipe.yml" gets uploaded to extraction pipeline with external id "my-extpipe".

## Usage

Available options are

 - `api-key`, CDF api key.
 - `base-url`, CDF base url, defaults to `https://api.cognitedata.com`
 - `token-url`, IDP token url, for fetching OAuth2 tokens.
 - `cdf-project-name`, name of CDF project.
 - `scopes`, space separated list of OAuth2 scopes.
 - `audience`, OAuth2 audience.
 - `client-id`, OAuth2 client id.
 - `client-secret`, OAuth2 client secret.
 - `deploy`, set this to true to deploy configs to CDF.
 - `root-folder`, Root folder to start recursively looking for configuration files.
 - `revision-message`, The "description" field on created config revisions.

For example:

```yaml
- name: Deploy
  uses: cognitedata/upload-config-action@v1
  with:
    base-url: ${{ secrets.BASE_URL }}
    token-url: ${{ secrets.TOKEN_URL }}
    cdf-project-name: ${{ secrets.PROJECT }}
    client-id: ${{ secrets.CLIENT_ID }}
    client-secret: ${{ secrets.CLIENT_SECRET }}
    root-folder: "test_root_dir/"
    deploy: "true"
    revision-message: "${{ github.event.head_commit.message }}"
```

