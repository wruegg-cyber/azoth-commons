from __future__ import annotations

import unittest

from tools.validate_portfolio import load_portfolio, validate


class PortfolioTests(unittest.TestCase):
    def test_repository_portfolio_is_valid(self) -> None:
        self.assertEqual(validate(load_portfolio()), [])

    def test_cycle_is_rejected(self) -> None:
        data = load_portfolio()
        by_id = {project["id"]: project for project in data["projects"]}
        by_id["shared-provenance"]["depends_on"] = ["device-registry"]
        errors = validate(data)
        self.assertTrue(any("dependency cycle" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

