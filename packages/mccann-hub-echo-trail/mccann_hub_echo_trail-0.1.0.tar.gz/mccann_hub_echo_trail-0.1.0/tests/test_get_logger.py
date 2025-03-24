import logging
import unittest
from unittest.mock import MagicMock, patch

from mccann_hub.echo_trail import get_logger, logger_setup
from mccann_hub.echo_trail.defaults import DEFAULT_METADATA


class TestGetLogger(unittest.TestCase):

    def setUp(self):
        """Ensure a clean logger state before each test."""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        root_logger.setLevel(logging.NOTSET)

        # Reset the LogRecord factory before each test
        logging.setLogRecordFactory(logging.LogRecord)

    @patch("logging.getLogger")
    def test_get_logger_returns_logger_instance(self, mock_get_logger):
        """Test that get_logger() returns a logger instance."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger = get_logger("test_logger")
        self.assertEqual(logger, mock_logger)

        mock_get_logger.assert_called_once_with("test_logger")

    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_get_logger_injects_default_metadata(self, mock_rotating_handler):
        """Test that default metadata is injected into log records."""
        logger_setup()
        logger = get_logger("test_logger")

        with self.assertLogs(logger, level="INFO") as log_capture:
            logger.info("Test log message")

        log_output = log_capture.records[0]  # Captured log output
        for key in DEFAULT_METADATA:
            self.assertIn(key, vars(log_output))

    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_get_logger_injects_additional_metadata(self, mock_rotating_handler):
        """Test that additional metadata is injected into log records."""
        logger_setup()
        additional_metadata = {"user_id": "12345", "env": "test"}
        logger = get_logger("test_logger", additional_metadata=additional_metadata)

        with self.assertLogs(logger, level="INFO") as log_capture:
            logger.info("Test log with extra metadata")

        log_output = log_capture.records[0]
        for k, v in additional_metadata.items():
            self.assertIn(k, vars(log_output))
            self.assertEqual(getattr(log_output, k), v)

    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_get_logger_does_not_duplicate_metadata(self, mock_rotating_handler):
        """Test that calling get_logger() multiple times does not duplicate metadata."""
        logger_setup()
        logger = get_logger("test_logger", additional_metadata={"version": "1.0"})
        logger = get_logger("test_logger", additional_metadata={"version": "2.0"})

        with self.assertLogs(logger, level="INFO") as log_capture:
            logger.info("Test log with updated metadata")

        # Ensure updated metadata is applied and old metadata is replaced
        log_output = log_capture.records[0]
        self.assertIn("version", vars(log_output))
        self.assertEqual(log_output.version, "2.0")

    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_get_logger_with_no_metadata(self, mock_rotating_handler):
        """Test that get_logger() behaves correctly when no additional metadata is provided."""
        logger_setup()
        logger = get_logger("test_logger")

        with self.assertLogs(logger, level="INFO") as log_capture:
            logger.info("Test log without additional metadata")

        log_output = log_capture.records[0]
        for key in DEFAULT_METADATA:
            self.assertIn(
                key, vars(log_output)
            )  # Confirms default metadata is still present


if __name__ == "__main__":
    unittest.main()
