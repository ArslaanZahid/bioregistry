"""Test utilities."""

import unittest

from bioregistry.utils import backfill, deduplicate

from bioregistry.parse_version_iri import parse_obo_version_iri


class TestDeduplicate(unittest.TestCase):
    """Test deduplication workflow."""

    def test_backfill(self):
        """Test record backfill."""
        records = [
            {"pubmed": "pmid_1"},
            {"arxiv": "arxiv_1", "doi": "doi_1"},
            {"doi": "doi_1", "pubmed": "pmid_1", "title": "yup"},
            {"pubmed": "pmid_1"},
        ]
        res = backfill(records, keys=["pubmed", "doi", "pmc", "arxiv"])
        self.assertEqual(
            [
                {
                    "arxiv": "arxiv_1",
                    "doi": "doi_1",
                    "pubmed": "pmid_1",
                },
                {
                    "arxiv": "arxiv_1",
                    "doi": "doi_1",
                    "pubmed": "pmid_1",
                },
                {
                    "arxiv": "arxiv_1",
                    "doi": "doi_1",
                    "pubmed": "pmid_1",
                    "title": "yup",
                },
                {
                    "arxiv": "arxiv_1",
                    "doi": "doi_1",
                    "pubmed": "pmid_1",
                },
            ],
            res,
        )

    def test_deduplicate(self):
        """Test record deduplication."""
        records = [
            {"arxiv": "arxiv_1", "doi": "doi_1"},
            {"doi": "doi_1", "pubmed": "pmid_1", "title": "yup"},
            {"pubmed": "pmid_1", "pmc": "pmc_1"},
            {"pubmed": "pmid_1"},
        ]
        res = deduplicate(records, keys=["pubmed", "doi", "pmc", "arxiv"])
        self.assertEqual(
            [
                {
                    "arxiv": "arxiv_1",
                    "doi": "doi_1",
                    "pubmed": "pmid_1",
                    "title": "yup",
                    "pmc": "pmc_1",
                },
            ],
            res,
        )

    def test_parse_obo_version_iri(self):
        """Test parsing version IRIs."""
        for version in [
            "2023-10-18",
            "1.0.0",
        ]:
            for iri in [
                # long
                f"http://purl.obolibrary.org/obo/mp/releases/{version}",
                f"http://purl.obolibrary.org/obo/mp/releases/{version}/",
                f"http://purl.obolibrary.org/obo/mp/releases/{version}/mp.owl",
                f"http://purl.obolibrary.org/obo/mp/releases/{version}/mp.obo",
                f"http://purl.obolibrary.org/obo/mp/releases/{version}/mp.json",
                f"http://purl.obolibrary.org/obo/mp/releases/{version}/mp.ofn",
                # short
                f"http://purl.obolibrary.org/obo/mp/{version}",
                f"http://purl.obolibrary.org/obo/mp/{version}/",
                f"http://purl.obolibrary.org/obo/mp/{version}/mp.owl",
                f"http://purl.obolibrary.org/obo/mp/{version}/mp.obo",
                f"http://purl.obolibrary.org/obo/mp/{version}/mp.json",
                f"http://purl.obolibrary.org/obo/mp/{version}/mp.ofn",
            ]:
                parse_result = parse_obo_version_iri(iri, "MP")
                self.assertIsNotNone(parse_result)
                self.assertEqual(version, parse_result.version)
            for iri in [
                f"http://purl.obolibrary.org/obo/mp/releases/{version}/mp.nope",
                f"http://purl.obolibrary.org/obo/mp/{version}/mp.nope",
            ]:
                self.assertIsNone(parse_obo_version_iri(iri, "MP"))

        for iri in [
            "http://purl.obolibrary.org/obo/fobi/fobi.owl",
            "http://purl.obolibrary.org/fobi.owl",
        ]:
            self.assertIsNone(parse_obo_version_iri(iri, "FOBI"))
