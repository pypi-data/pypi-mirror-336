import ast
import re
import os
import unittest

import geojson
from tempfile import NamedTemporaryFile

from click.testing import CliRunner

from pygssearch.cli import cli, url_ok
from unittest import TestCase, skipIf

# Warn this test does not use a https Odata mockup, only real online service
# that may not be online in the near future.
remote_sample_service = "https://vision.odata.gael.fr/odata/v1"


class TestCli(TestCase):
    runner = CliRunner()
    skip_url = not url_ok(remote_sample_service)

    def test_cli_version(self):
        result = self.runner.invoke(cli, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIsNotNone(result.output)

    def test_cli_check_service(self):
        self.assertTrue(url_ok(remote_sample_service))
        self.assertFalse(url_ok("http://no_service/"))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_orig(self):
        result = self.runner.invoke(cli, ['--service', remote_sample_service])
        self.assertEqual(result.exit_code, 0)
        output = ast.literal_eval(result.output)
        self.assertEqual(len(output), 10)
        # default contains (Name, Id)
        self.assertEqual(len(output[0]), 2)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_orig_format(self):
        result = self.runner.invoke(cli, [
            '--service', remote_sample_service,
            '--format', "_"])
        self.assertEqual(result.exit_code, 0)
        output = ast.literal_eval(result.output)
        self.assertEqual(len(output), 10)
        # default contains (Name, Id)
        self.assertGreater(len(output[0]), 3)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_orig_format_selection(self):
        result = self.runner.invoke(cli, [
            '--service', remote_sample_service,
            '--format', 'Id',
            '--format', 'Name',
            '--format', 'PublicationDate'])
        self.assertEqual(result.exit_code, 0)
        output = ast.literal_eval(result.output)
        print(output)
        self.assertEqual(len(output), 10)
        # default contains (Name, Id)
        self.assertEqual(len(output[0]), 3)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--footprint', '-'])
        self.assertEqual(result.exit_code, 0)
        output = geojson.loads(result.output)
        self.assertEqual(output.get('type'), 'FeatureCollection')
        self.assertEqual(len(output.get('features')), 10)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            self.assertEqual(output.get('type'), 'FeatureCollection')
            self.assertEqual(len(output.get('features')), 10)
            feature = output.get('features')[5]
            self.assertEqual(len(feature['properties']), 2)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--format', '_',
                 '--attributes'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            self.assertEqual(output.get('type'), 'FeatureCollection')
            self.assertEqual(len(output.get('features')), 10)
            feature = output.get('features')[5]
            print(feature)
            self.assertGreater(len(feature['properties']), 3)
            self.assertIsNotNone(feature['properties'].get('coordinates'))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes_exclusion(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--attributes',
                 '--format', '_',
                 '--exclude', 'coordinates',
                 '--exclude', 'brightCover'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            feature = output.get('features')[5]
            print(feature)
            self.assertIsNone(feature['properties'].get('coordinates'))
            self.assertIsNone(feature['properties'].get('brightCover'))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes_inclusion(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--attributes',
                 '--format', 'Name',
                 '--format', 'Id',
                 '--format', 'processingDate'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            feature = output.get('features')[5]
            print(feature)
            self.assertIsNotNone(feature['properties'].get('Name'))
            self.assertIsNotNone(feature['properties'].get('Id'))
            self.assertIsNotNone(feature['properties'].get('processingDate'))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes_inclusion_all(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--attributes',
                 '--format', '_'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            feature = output.get('features')[5]
            print(feature)
            self.assertIsNotNone(feature['properties'].get('Name'))
            self.assertIsNotNone(feature['properties'].get('Id'))
            self.assertIsNotNone(feature['properties'].get('processingDate'))

    def test_cli_url_valid(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--attributes',
             '--limit', 15,
             '--skip', 1,
             '--order_by', '+ContentLength',
             '--order_by', '-PublicationDate',
             '--filter', 'ContentLength lt 10000000',
             '--show_url'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        # warn the trailer \n was added here because returned url is displayed
        # by cli with prnt command that add CRLR to the output. It is not #
        # normal case wrt the command controlled itself.
        self.assertEqual(result.output, remote_sample_service +
                         "/Products?"
                         "$filter=ContentLength lt 10000000&"
                         "$top=15&"
                         "$skip=1&"
                         "$format=json&"
                         "$expand=Attributes&"
                         "$orderby=ContentLength asc,PublicationDate desc\n")

    def test_cli_param_well_handled(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--footprint', '-',
             '--attributes',
             '--end', '2023-07-05',
             '--start', '2023-07-04',
             '--exclude', 'coordinates',
             '--exclude', 'specificationTitle',
             '--uuid', '285cdd67-713d-436a-ae92-df26e376f4d0',
             '--name', 'Toto',
             '--name', 'titi',
             '--uuid', 'an-other-uuid',
             '--instrument', 'MSI',
             '--instrument', 'SAR',
             '--mission', '1',
             '--mission', '2',
             '--cloud', '50',
             '--limit', 15,
             '--skip', 1,
             '--order_by', '+ContentLength',
             '--order_by', '-PublicationDate',
             '--filter', 'ContentLength lt 10000000',
             '--show_url'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        # warn the trailer \n was added here because returned url is displayed
        # by cli with prnt command that add CRLR to the output. It is not #
        # normal case wrt the command controlled itself.
        expected_result = (
            remote_sample_service +
            "/Products?"
            "$filter=ContentLength lt 10000000 and startswith(Name,'S2') and "
            "StringAttributes/any(d:d/Name eq 'instrumentShortName' and "
            "                       d/Value eq 'SAR') and "
            "Attributes/OData.CSC.DoubleAttribute/any(d:d/Name eq 'cloudCover'"
            "               and d/OData.CSC.DoubleAttribute/Value lt 50) and "
            "ContentDate/Start ge 2023-07-04T00:00:00.0Z and "
            "ContentDate/End lt 2023-07-05T00:00:00.0Z and "
            "(contains(Name,'Toto') or contains(Name,'titi')) and "
            "(Id eq 285cdd67-713d-436a-ae92-df26e376f4d0 or "
            " Id eq an-other-uuid)&"
            "$top=15&"
            "$skip=1&"
            "$format=json&"
            "$expand=Attributes&"
            "$orderby=ContentLength asc,PublicationDate desc\n")

        self.assertEqual(result.output, re.sub(r' +', ' ', expected_result))

    def test_cli_geometry(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--geometry',
             '((1.0,1.0),(0.0,1.0),(0.0,0.0),(1.0,0.0),(1.0,1.0))',
             '--show_url'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        expected_result = \
            ("$filter=OData.CSC.Intersects("
             "location=Footprint,area=geography'SRID=4326;"
             "Polygon((1.0 1.0,0.0 1.0,0.0 0.0,1.0 0.0,1.0 1.0))')")

        self.assertTrue(expected_result in result.output)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_count(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--count',
             '--attributes',
             '--limit', 15,
             '--skip', 1,
             '--order_by', '+ContentLength',
             '--order_by', '-PublicationDate',
             '--filter', 'ContentLength lt 10000000'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        # WARN#1: the trailer \n was added here because returned url is
        # displayed by cli with prnt command that add CRLR to the output.
        # It is not normal case wrt the command controlled itself.

        # WARN#2: Currently (31/07/2024) vision return 11 products lower than
        # 10MB and it may change.
        self.assertGreaterEqual(int(result.output), 11)


class TestCAHUReporting(TestCase):
    runner = CliRunner()
    service_url = \
        'https://cahu-catalogue.gss.software-validation.gael.fr/gss-catalogue'
    username = 'cahu-admin-user'
    password = 'FinkolA!'
    service_token_url =\
        ('http://auth.keycloak.gss.software-validation.gael.fr:28080/realms/'
         'cahu/protocol/openid-connect/token')
    service_client_id = 'odata'
    service_client_secret = 'hFpaAINvgy8T2ZxB2nDlanthVnJLssPV'

    skip_url = not url_ok(service_url)

    @unittest.skip(
        "#CAHU190: Python dependency check not possible as unittest.")
    def test_cahu_190(self):
        """
        Not able to install pygssearch with python3.12
        Cannot be tested in unitary tests: dependency problems.
        """
        self.assertTrue(False, 'Dependencies still not controlled')

    @skipIf(skip_url, "Test url not accessible")
    def test_cahu_191(self):
        """
        Login with Client_id/Client_secret method do not work
        prip online test service also implements OAuth2.0 authentication
        service in addition to basic auth.
        The objective of this test is, as far as de the basic authentication
        properly works (otherwise test is skipped), is to use cli API to
        initiate an OpenId connection and generate a token connection.

        Current status: Waiting for an up and running OAuth2.0 service.
        Reproduces: #CAHU-191
        """
        result = self.runner.invoke(
            cli,
            ['--service', self.service_url,
             '--username', self.username,
             '--password', self.password,
             '--token_url', self.service_token_url,
             '--client_id', self.service_client_id,
             '--client_secret', self.service_client_secret,
             '--format', 'Name'])
        self.assertEqual(result.exit_code, 0, f'{str(result.exception)}')
        print(result.output)

    @skipIf(skip_url, "Test url not accessible")
    def test_cahu_192(self):
        """
        Discussion about the introduction of --cloud parameters is asked to
        return also products not containing the metadata.

        Proposal probably not to be retained.

        Reproduces: #CAHU-192
        """
        result = self.runner.invoke(
            cli,
            ['--service', self.service_url,
             '--format', 'Name',
             '--start', '2021-03-11T00:00:00.000000Z',
             '--end',   '2023-01-27T23:59:59.999999Z'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        output = ast.literal_eval(result.output)
        no_restriction_count = len(output)

        result = self.runner.invoke(
            cli,
            ['--service', self.service_url,
             '--format', 'Name',
             '--format', 'cloudCover',
             '--attributes',
             '--start', '2021-03-11T00:00:00.000000Z',
             '--end', '2023-01-27T23:59:59.999999Z',
             '--cloud', '100'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        output = ast.literal_eval(result.output)
        cloud_restriction_count = len(output)

        self.assertLessEqual(cloud_restriction_count, no_restriction_count)

    @skipIf(skip_url, "Test url not accessible")
    def test_cahu_193_south_west_america(self):
        """
        Error indexing input geojson file.
        The used geojson_south_west_america_polygon.json is invalid
        and the message raised by the cli shall be a bit more explicit.

        Reproduces: #CAHU-193
        """
        geojson_file = os.path.join(os.path.dirname(__file__), 'resources',
                                    'geojson_south_west_america_polygon.json')
        result = self.runner.invoke(
            cli,
            ['--service', self.service_url,
             '--geometry', geojson_file])
        # Here error is raised because file is malformed
        self.assertEqual(result.exit_code, 1)
        msg = str(result.exception)
        self.assertTrue('is invalid' in str(result.exception),
                        f"Invalid format message not raised "
                        f"(instead: '{msg}')")

    @skipIf(skip_url, "Test url not accessible")
    def test_cahu_193_europe(self):
        """
        Error querying GSS with intersecting Europe geometry
        Reproduces: #CAHU-193
        """
        geojson_file = os.path.join(os.path.dirname(__file__), 'resources',
                                    'geojson_europe_polygon.json')
        result = self.runner.invoke(
            cli,
            ['--service', self.service_url,
             '--geometry', geojson_file])
        # Here error is raised because file is malformed
        self.assertEqual(result.exit_code, 0)

        print(result.output)
        output = ast.literal_eval(result.output)
        self.assertTrue(len(output) > 0,
                        "Not Found product covering Europe geometry")

    @skipIf(skip_url, "Test url not accessible")
    def test_cahu_193_france(self):
        """
        Error querying GSS with intersecting France geometry
        Reproduces: #CAHU-193
        """
        geojson_file = os.path.join(os.path.dirname(__file__), 'resources',
                                    'geojson_france_polygon.json')
        result = self.runner.invoke(
            cli,
            ['--service', self.service_url,
             '--geometry', geojson_file])
        # Here error is raised because file is malformed
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        output = ast.literal_eval(result.output)
        self.assertTrue(len(output) > 0,
                        "Not Found product covering France geometry")
