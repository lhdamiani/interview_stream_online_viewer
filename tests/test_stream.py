import unittest

from multiprocessing import Process

from bsread import source

from stream_online_viewer.stream import generate_stream


class TestGenerateStream(unittest.TestCase):

    def setUp(self):
        self.stream_output_port = 8888
        self.n_images = 10

        self.stream_generator_process = Process(target=generate_stream,
                                                args=(self.stream_output_port, self.n_images))
        self.stream_generator_process.start()

    def tearDown(self):
        self.stream_generator_process.terminate()

    def test_generate_stream(self):

        message = None

        # You always need to specify the host parameter, otherwise bsread will try to access PSI servers.
        with source(host="localhost", port=self.stream_output_port, receive_timeout=1000) as input_stream:

            n_received = 1

            while n_received < self.n_images:
                message = input_stream.receive()

                # In case of receive timeout (1000 ms in this example), the received data is None.
                if message is None:
                    continue

                n_received += 1

        self.assertIsNotNone(message)

        image = message.data.data["image"].value
        image_size_x = message.data.data["image_size_x"].value
        image_size_y = message.data.data["image_size_y"].value

        self.assertEqual(image.shape[0], image_size_y)
        self.assertEqual(image.shape[1], image_size_x)

        image_profile_x = message.data.data["image_profile_x"].value
        self.assertEqual(image_profile_x.shape[0], image_size_x)

        image_profile_y = message.data.data["image_profile_y"].value
        self.assertEqual(image_profile_y.shape[0], image_size_y)

        beam_energy = message.data.data["beam_energy"].value
        self.assertGreater(beam_energy, 0)

        repetition_rate = message.data.data["repetition_rate"].value
        self.assertGreater(repetition_rate, 0)
