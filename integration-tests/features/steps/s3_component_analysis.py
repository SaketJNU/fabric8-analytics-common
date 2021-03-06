"""Definitions of tests for component metadata stored in the AWS S3 database."""
from behave import given, then, when
from src.attribute_checks import *
from src.s3interface import *


@then('I should find the correct component core data for package {package} version {version} '
      'from ecosystem {ecosystem}')
@then('I should find the correct component toplevel metadata for package {package} '
      'version {version} ecosystem {ecosystem} with latest version {version}')
def check_component_core_data(context, package, version, ecosystem):
    """Check the component core data read from the AWS S3 database.

    Expected format (with an example data):
        {
          "analyses": [
            "security_issues",
            "metadata",
            "keywords_tagging",
            "redhat_downstream",
            "digests",
            "source_licenses",
            "dependency_snapshot"
          ],
          "audit": null,
          "dependents_count": -1,
          "ecosystem": "pypi",
          "finished_at": "2017-10-06T13:41:43.450021",
          "id": 1,
          "latest_version": "0.2.4",
          "package": "clojure_py",
          "package_info": {
            "dependents_count": -1,
            "relative_usage": "not used"
          },
          "release": "pypi:clojure_py:0.2.4",
          "started_at": "2017-10-06T13:39:30.134801",
          "subtasks": null,
          "version": "0.2.4"
        }
    """
    data = context.s3_data

    started_at = check_and_get_attribute(data, "started_at")
    check_timestamp(started_at)

    finished_at = check_and_get_attribute(data, "finished_at")
    check_timestamp(finished_at)

    actual_ecosystem = check_and_get_attribute(data, "ecosystem")
    assert ecosystem == actual_ecosystem, "Ecosystem {e1} differs from expected " \
        "ecosystem {e2}".format(e1=actual_ecosystem, e2=ecosystem)

    actual_package = check_and_get_attribute(data, "package")
    assert package == actual_package, "Package {p1} differs from expected " \
        "package {p2}".format(p1=actual_package, p2=package)

    actual_version = check_and_get_attribute(data, "version")
    assert version == actual_version, "Version {v1} differs from expected " \
        "version {v2}".format(v1=actual_version, v2=version)

    actual_release = check_and_get_attribute(data, "release")
    release = release_string(ecosystem, package, version)
    assert actual_release == release, "Release string {r1} differs from expected " \
        "value {r2}".format(r1=actual_release, r2=release)

    # the following attributes are expected to be presented for all component toplevel metadata
    attributes_to_check = ["id", "analyses", "audit", "dependents_count", "latest_version",
                           "package_info", "subtasks"]
    check_attributes_presence(data, attributes_to_check)

    # check the attributes for the 'analyses' subnode
    analyses = data["analyses"]
    attributes_to_check = ["security_issues", "metadata", "keywords_tagging",
                           "redhat_downstream", "digests", "source_licenses",
                           "dependency_snapshot"]

    check_attributes_presence(analyses, attributes_to_check)


@then('I should find that the latest component version is {version}')
def check_component_latest_version(context, version):
    """Check the value of attribute 'latest_version' stored in component metadata."""
    data = context.s3_data

    latest_version = check_and_get_attribute(data, "latest_version")
    assert version == latest_version, "Latest version should be set to {v1}, " \
        "but {v2} has been found instead".format(v1=version, v2=latest_version)


@then('I should find the correct dependency snapshot data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_dependency_snapshot_data(context, package, version, ecosystem):
    """Check the dependency snapshot metadata for the given component."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "dependency_snapshot", "1-0-0")
    check_status_attribute(data)
    check_summary_attribute(data)


@then('I should find {num:d} runtime details in dependency snapshot')
def check_runtime_dependency_count(context, num):
    """Check the number of runtime details for selected component."""
    data = context.s3_data

    details = check_and_get_attribute(data, "details")
    runtime = check_and_get_attribute(details, "runtime")

    cnt = len(runtime)
    assert cnt == num, "Expected {n1} runtime details, but found {n2}".format(n1=num, n2=cnt)


@then('I should find {num:d} dependencies in dependency snapshot summary')
def check_runtime_dependency_count_in_summary(context, num):
    """Check the number of dependencies in dependency snapshot summary."""
    data = context.s3_data

    summary = check_and_get_attribute(data, "summary")
    dependency_counts = check_and_get_attribute(summary, "dependency_counts")
    runtime_count = check_and_get_attribute(dependency_counts, "runtime")

    cnt = int(runtime_count)
    assert cnt == num, "Expected {n1} runtime dependency counts, but found {n2}".format(
        n1=num, n2=cnt)


@then('I should find the correct digest data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_digest_data(context, package, version, ecosystem):
    """Check the digest data for the given package, version, and ecosystem."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "digests", "1-0-0")
    check_status_attribute(data)
    check_summary_attribute(data)

    check_attribute_presence(data, "details")


@then('I should find digest metadata {selector} set to {expected_value}')
def check_component_digest_metadata_value(context, selector, expected_value):
    """Check if the digest metadata can be found for the component."""
    data = context.s3_data
    details = check_and_get_attribute(data, "details")

    for detail in details:
        actual_value = check_and_get_attribute(detail, selector)
        if actual_value == expected_value:
            return

    # nothing was found
    raise Exception('Can not find the digest metadata {selector} set to {expected_value}'.format(
        selector=selector, expected_value=expected_value))


@then('I should find the correct keywords tagging data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_keywords_tagging_data(context, package, version, ecosystem):
    """Check the keywords tagging metadata for given component."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    #  no schema to check (yet?)
    #  tracked here: https://github.com/openshiftio/openshift.io/issues/1074
    check_status_attribute(data)
    check_summary_attribute(data)


@then('I should find the correct metadata for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_metadata_data(context, package, version, ecosystem):
    """Check the basic component metadata in the AWS S3 database."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "metadata", "3-2-0")
    check_status_attribute(data)
    check_summary_attribute(data)


@then('I should find that author of this project is {author}')
def check_package_author(context, author):
    """Check the author of component."""
    details = get_details_node(context)[0]
    actual_author = check_and_get_attribute(details, "author")
    assert actual_author.startswith(author), "Expected author {a1}, " \
        "but {a2} has been found instead".format(a1=author, a2=actual_author)


@then('I should find that the project use {vcs} as a version control system')
def check_vsc(context, vcs):
    """Check the type of version control system for the component."""
    details = get_details_node(context)[0]
    code_repository = check_and_get_attribute(details, "code_repository")
    actual_vcs = check_and_get_attribute(code_repository, "type")
    assert actual_vcs == vcs.lower(), "Expected {v1} version control system type, " \
        "but {v2} has been found instead".format(v1=vcs, v2=actual_vcs)


@then('I should find that the repository can be found at {url}')
def check_repository_url(context, url):
    """Check the repository URL (if set) for the component."""
    details = get_details_node(context)[0]
    code_repository = check_and_get_attribute(details, "code_repository")
    actual_url = check_and_get_attribute(code_repository, "url")
    assert actual_url == url, "Repository URL should be set to {u1}, " \
        "but {u2} has been found instead".format(u1=url, u2=actual_url)


@then('I should find that the project homepage can be found at {url}')
def check_project_homepage(context, url):
    """Check the project homepage (if exist) for the component."""
    details = get_details_node(context)[0]
    actual_homepage = check_and_get_attribute(details, "homepage")
    assert actual_homepage == url, "Homepage URL should be set to {u1}, " \
        "but {u2} has been found instead".format(u1=url, u2=actual_homepage)


@then('I should find that the package description is {description}')
def check_project_description(context, description):
    """Check the package description existence and content."""
    details = get_details_node(context)[0]
    actual_description = check_and_get_attribute(details, "description")
    assert actual_description == description, "Description is set to {d1}, " \
        "but {d2} is expected".format(d1=actual_description, d2=description)


@then('I should find that the package name is {name} and version is {version}')
def check_package_name_and_version(context, name, version):
    """Check the package name and version."""
    details = get_details_node(context)[0]
    actual_name = check_and_get_attribute(details, "name")
    actual_version = check_and_get_attribute(details, "version")

    assert name == actual_name, "Name '{n1}' is different from " \
        "expected name '{n2}'".format(n1=actual_name, n2=name)

    assert version == actual_version, "Version {v1} is different from expected " \
        "version {v2}".format(v1=actual_version, v2=version)


@then('I should find the correct Red Hat downstream data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_redhat_downstream_data(context, package, version, ecosystem):
    """Check the basic Red Hat downstream metadata for the selected component."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "redhat_downstream", "2-2-1")
    check_status_attribute(data)
    check_summary_attribute(data)


@then('I should not find the package in Brew')
def check_package_not_in_brew(context):
    """Check that the given package can not be found in the Brew."""
    details = get_details_node(context)
    brew = check_and_get_attribute(details, "brew")
    assert not brew, "Expecting that the brew attrbute is empty list"


@then('I should not find the package in CDN')
def check_package_not_in_cdn(context):
    """Check that the given package can not be found in the CDN."""
    details = get_details_node(context)
    cdn = check_and_get_attribute(details, "pulp_cdn")
    assert not cdn, "Expecting that the pupl_cdm attrbute is empty list"


@then('I should not find the package in Red Hat Anitya')
def check_package_not_in_cdn(context):
    """Check that the given package can not be found in the Red Hat Anitya."""
    details = get_details_node(context)
    cdn = check_and_get_attribute(details, "redhat_anitya")
    assert not cdn, "Expecting that the redhat_anitya attrbute is empty list"


@then('I should find the package in Brew')
def check_package_is_in_brew(context):
    """Check that the package can be found in the Brew."""
    details = get_details_node(context)
    brew = check_and_get_attribute(details, "brew")
    assert brew, "Expecting that the brew attrbute is not empty list"


@then('I should find the package in CDN')
def check_package_is_in_cdn(context):
    """Check that the package can not find in the CDN."""
    details = get_details_node(context)
    cdn = check_and_get_attribute(details, "pulp_cdn")
    assert cdn, "Expecting that the pupl_cdm attrbute is not empty list"


@then('I should find the package in Red Hat Anitya')
def check_package_is_in_cdn(context):
    """Check that the package can be found in the Red Hat Anitya."""
    details = get_details_node(context)
    cdn = check_and_get_attribute(details, "redhat_anitya")
    assert cdn, "Expecting that the redhat_anitya attrbute is not empty list"


@then('I should find the correct security issues data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_security_issues_data(context, package, version, ecosystem):
    """Check the security issues metadata fro given component."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "security_issues", "3-0-1")
    check_status_attribute(data)
    check_summary_attribute(data)

    details = check_and_get_attribute(data, "details")
    assert type(details) is list


@then('I should find the correct source licenses data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_source_licenses_data(context, package, version, ecosystem):
    """Check that the component has assigned correct source licenses metadata."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "source_licenses", "3-0-0")
    check_status_attribute(data)
    check_summary_attribute(data)


@then('I should find that the package uses {license} license')
def check_package_license(context, license):
    """Check that the package has assigned given license."""
    details = get_details_node(context)
    licenses = check_and_get_attribute(details, "licenses")
    assert license in licenses, "Can not find license {lic}".format(lic=license)


@when('I read component toplevel metadata for the package {package} version {version} in ecosystem '
      '{ecosystem} from the AWS S3 database bucket {bucket}')
def read_core_data_from_bucket(context, package, version, ecosystem, bucket):
    """Read the component toplevel metadata."""
    key = S3Interface.component_key(ecosystem, package, version)
    s3_data = context.s3interface.read_object(bucket, key)
    assert s3_data is not None
    context.s3_data = s3_data
