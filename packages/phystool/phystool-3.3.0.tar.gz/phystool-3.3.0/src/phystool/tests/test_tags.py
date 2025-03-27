from unittest import TestCase

from phystool.tags import Tags


_tags_energy = {
    'topic': ['Dynamique', 'Énergie'],
    'difficulty': ['P'],
    'cursus': ['1MDF', '2MDF'],
}
_tags_moh = {
    'topic': ['MOH', 'Énergie'],
    'difficulty': ['E'],
    'cursus': ['3MOS'],
}
_tags_notopic = {
    'difficulty': ['P'],
    'cursus': ['3CSa'],
}
_tags_notag: dict[str, list[str]] = {}


class TestTags(TestCase):
    @classmethod
    def setUp(cls):
        cls.tags_energy = Tags(_tags_energy)
        cls.tags_moh = Tags(_tags_moh)
        cls.tags_notopic = Tags(_tags_notopic)
        cls.tags_notag = Tags(_tags_notag)

    def test_dev_has_required_tags(self):
        jstags = {
            "topic": [
                "Cinématique",
                "Dynamique",
                "Hydrostatique",
                "MOH",
                "Rotation",
                "Statique",
                "Énergie"
            ],
            "cursus": [
                "1MDF",
                "1MOS",
                "2MDF",
                "2MOS",
                "3CSa",
                "3MOS"
            ],
            "difficulty": [
                "E",
                "P"
            ]
        }
        self.assertEqual(jstags, Tags.TAGS.data)

    def test_valid_tags(self):
        """
        Tags.TAGS needs to contain all the tags used in this file. To achieve
        this, the exercise database must contain all the required tags.
        """
        for test_tags in [_tags_energy, _tags_moh, _tags_notopic]:
            for category, tags in test_tags.items():
                for tag in tags:
                    self.assertTrue(Tags.TAGS.include(Tags({category: [tag]})))

    def test_default_constructor(self):
        self.assertEqual(Tags().data, {})

    def test_energy_tags(self):
        self.assertEqual(self.tags_energy.data, _tags_energy)

    def test_moh_tags(self):
        self.assertEqual(self.tags_moh.data, _tags_moh)

    def test_notopic_tags(self):
        self.assertEqual(self.tags_notopic.data, _tags_notopic)

    def test_validate(self):
        t1 = Tags.validate("MOH,Énergie,foo,E, 3MOS")
        t2 = Tags.validate("Énergie,Dynamique,P,bar ,2MDF,1MDF")
        t3 = Tags.validate("P,3CSa")
        t4 = Tags.validate("")
        self.assertEqual(t1.data, _tags_moh)
        self.assertEqual(t2.data, _tags_energy)
        self.assertEqual(t3.data, _tags_notopic)
        self.assertEqual(t4.data, _tags_notag)

    def test_contains_check_only_topic(self):
        t = Tags.validate("MOH")
        self.assertTrue(self.tags_moh._contains(t))
        self.assertFalse(self.tags_energy._contains(t))
        self.assertFalse(self.tags_notopic._contains(t))
        self.assertFalse(self.tags_notag._contains(t))

    def test_contains_check_only_difficulty(self):
        t = Tags.validate("P")
        self.assertFalse(self.tags_moh._contains(t))
        self.assertTrue(self.tags_energy._contains(t))
        self.assertTrue(self.tags_notopic._contains(t))
        self.assertFalse(self.tags_notag._contains(t))

    def test_contains_empty(self):
        t = Tags()
        self.assertTrue(self.tags_moh._contains(t))
        self.assertTrue(self.tags_energy._contains(t))
        self.assertTrue(self.tags_notopic._contains(t))
        self.assertTrue(self.tags_notag._contains(t))

    def test_contains_check_general(self):
        t1 = Tags.validate("MOH,2MOS")
        self.assertFalse(self.tags_moh._contains(t1))
        self.assertFalse(self.tags_energy._contains(t1))
        self.assertFalse(self.tags_notopic._contains(t1))
        self.assertFalse(self.tags_notag._contains(t1))

        t2 = Tags.validate("MOH,3MOS")
        self.assertTrue(self.tags_moh._contains(t2))
        self.assertFalse(self.tags_energy._contains(t2))
        self.assertFalse(self.tags_notopic._contains(t2))
        self.assertFalse(self.tags_notag._contains(t2))

        t3 = Tags.validate("Énergie,1MDF")
        self.assertFalse(self.tags_moh._contains(t3))
        self.assertTrue(self.tags_energy._contains(t3))
        self.assertFalse(self.tags_notopic._contains(t3))
        self.assertFalse(self.tags_notag._contains(t3))

        self.assertTrue(self.tags_energy._contains(Tags.validate("Énergie")))
        self.assertTrue(self.tags_energy._contains(Tags.validate("Énergie,MOH")))
        self.assertFalse(self.tags_energy._contains(Tags.validate("MOH")))
        self.assertTrue(self.tags_energy._contains(Tags.validate("Énergie,P")))
        self.assertFalse(self.tags_energy._contains(Tags.validate("Énergie,E")))
        self.assertFalse(self.tags_energy._contains(Tags.validate("Énergie,E")))

    def test_add(self):
        t1 = self.tags_energy + self.tags_moh
        t2 = Tags(self.tags_energy.data)
        t2 += self.tags_moh
        # check that the addition left the original tags untouched
        self.assertEqual(self.tags_energy.data, _tags_energy)
        self.assertEqual(self.tags_moh.data, _tags_moh)

        t = Tags.validate('Énergie,Dynamique,MOH,E,P, 2MDF, 1MDF,3MOS')
        self.assertEqual(t.data, t1.data)
        self.assertEqual(t.data, t2.data)

    def test_sub(self):
        t1 = self.tags_energy - self.tags_moh
        t2 = Tags(self.tags_energy.data)
        t2 -= self.tags_moh
        # check that the substraction left the original tags untouched
        self.assertEqual(self.tags_energy.data, _tags_energy)
        self.assertEqual(self.tags_moh.data, _tags_moh)

        t = Tags.validate('Dynamique,P,1MDF,2MDF')
        self.assertEqual(t1.data, t.data)
        self.assertEqual(t2.data, t.data)

        t1 -= t
        t2 -= t
        self.assertEqual(t1.data, {})
        self.assertEqual(t2.data, {})

    def test_bool(self):
        self.assertFalse(Tags())
        self.assertTrue(Tags({'a': 1}))
