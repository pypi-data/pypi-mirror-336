# Get access to push data


The user must be allowed to push files and STAC objects into the spatial data infrastructure.

To get the required permission, the user must perform a [merge request](https://docs.gitlab.com/ee/user/project/merge_requests/) 
in [this repository](https://forgemia.inra.fr/cdos-pub/admin/cdos-ops), modifying the policies in the `policies.yaml` file of the repository.

```yaml
rules:
- user: user_name
  collections:
  - nom-collection-1
  - nom-collection-2
  storages:
  - https://s3-data.meso.umontpellier.fr/bucket1/prefixe1
  - https://s3-data.meso.umontpellier.fr/bucket1/prefixe2
  - https://s3-data.meso.umontpellier.fr/bucket2

```

Note that `collections` and `storages` are completely independent.
