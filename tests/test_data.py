import unittest

from numpy.testing import assert_array_equal

from stream_online_viewer.data import generate_image, get_stream_message_data, generate_metadata


class TestUtils(unittest.TestCase):

    def test_image(self):
        expected_size_x = 1000
        expected_size_y = 2000

        image = generate_image(size_x=expected_size_x, size_y=expected_size_y)

        # Slowest changing dimension first.
        self.assertEqual(image.shape[0], expected_size_y)
        self.assertEqual(image.shape[1], expected_size_x)

    def test_metadata(self):
        beam_energy_base = 100
        repetition_rate = 112

        metadata = generate_metadata(beam_energy_base=beam_energy_base, repetition_rate=repetition_rate)

        self.assertIn("beam_energy", metadata)
        # The beam energy fluctuates from the base value to + 10% max.
        self.assertTrue(beam_energy_base <= metadata["beam_energy"] <= beam_energy_base*1.1)

        self.assertIn("repetition_rate", metadata)
        self.assertEqual(metadata["repetition_rate"], repetition_rate)

    def test_stream_simulated_data(self):
        expected_size_x = 1024
        expected_size_y = 512
        beam_energy_base = 50
        repetition_rate = 25

        image = generate_image(size_x=expected_size_x, size_y=expected_size_y)
        metadata = generate_metadata(beam_energy_base=beam_energy_base, repetition_rate=repetition_rate)

        stream_data = get_stream_message_data(image=image, metadata=metadata)

        assert_array_equal(stream_data["image"], image)

        self.assertEqual(stream_data["image_size_x"], expected_size_x)
        self.assertEqual(stream_data["image_size_y"], expected_size_y)

        self.assertEqual(stream_data["image_profile_x"].shape, (expected_size_x,))
        self.assertEqual(stream_data["image_profile_y"].shape, (expected_size_y,))

        self.assertTrue(beam_energy_base <= metadata["beam_energy"] <= beam_energy_base * 1.1)
        self.assertEqual(metadata["repetition_rate"], repetition_rate)
