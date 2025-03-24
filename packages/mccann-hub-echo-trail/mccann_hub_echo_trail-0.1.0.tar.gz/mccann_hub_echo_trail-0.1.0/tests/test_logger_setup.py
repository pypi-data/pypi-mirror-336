import logging
import unittest
from unittest.mock import MagicMock, patch

from mccann_hub.echo_trail import logger_setup
from mccann_hub.echo_trail.defaults import DEFAULT_METADATA, LOG_DIR


class TestLoggerSetup(unittest.TestCase):

    def setUp(self):
        """Ensure the root logger starts fresh for each test."""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        root_logger.setLevel(logging.INFO)

        # Reset the LogRecord factory before each test
        logging.setLogRecordFactory(logging.LogRecord)

    @patch("os.makedirs")
    @patch("logging.getLogger")
    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_root_logger_setup_creates_handlers(
        self, mock_rotating_handler, mock_get_logger, mock_makedirs
    ):
        """Test that logger_setup configures the root logger with the correct handlers."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = False  # Simulate no existing handlers

        logger_setup()

        mock_makedirs.assert_called_once_with(LOG_DIR, exist_ok=True)
        self.assertEqual(mock_logger.setLevel.call_args[0][0], logging.INFO)
        self.assertTrue(mock_logger.addHandler.called)  # At least one handler added

    @patch("os.makedirs")
    @patch("logging.getLogger")
    @patch(
        "mccann_hub.echo_trail.setup.RotatingFileHandler"
    )  # Mock RotatingFileHandler directly
    def test_logger_setup_creates_rotating_file_handler(
        self, mock_rotating_handler, mock_get_logger, mock_makedirs
    ):
        """Test that a rotating file handler is correctly configured."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = False  # Simulate no existing handlers

        # Mock RotatingFileHandler instance
        mock_file_handler_instance = MagicMock()
        mock_rotating_handler.return_value = mock_file_handler_instance

        logger_setup(log_file="logs/custom.log", max_bytes=1024, backup_count=2)

        # Ensure RotatingFileHandler was created with correct args
        mock_rotating_handler.assert_called_once_with(
            "logs/custom.log", maxBytes=1024, backupCount=2
        )

        # Confirm the mock handler was added to the logger
        mock_logger.addHandler.assert_called_with(mock_file_handler_instance)

    @patch("os.makedirs")
    @patch("logging.getLogger")
    def test_logger_setup_with_custom_handlers(self, mock_get_logger, mock_makedirs):
        """Test that custom handlers are applied when provided."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = False  # Simulate no existing handlers

        custom_handler = MagicMock()
        logger_setup(custom_handlers=[custom_handler])

        custom_handler.setFormatter.assert_called_once()
        mock_logger.addHandler.assert_called_with(custom_handler)

    @patch("os.makedirs")
    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_logger_setup_injects_default_metadata(
        self, mock_rotating_handler, mock_makedirs
    ):
        """Test that default metadata is injected into log records."""
        logger_setup()

        # Write log record and verify metadata
        logger = logging.getLogger("test_logger")
        # logger.info("Hello World")
        with self.assertLogs(logger, level="INFO") as log_capture:
            logger.info("Test log message")

        log_output = log_capture.records[0]
        self.assertIn("program", vars(log_output))
        self.assertIn("hostname", vars(log_output))
        self.assertEqual(log_output.program, DEFAULT_METADATA["program"])
        self.assertEqual(log_output.hostname, DEFAULT_METADATA["hostname"])

    @patch("os.makedirs")
    @patch("mccann_hub.echo_trail.setup.RotatingFileHandler")
    def test_logger_setup_injects_extra_metadata(
        self, mock_rotating_handler, mock_makedirs
    ):
        """Test that extra metadata is merged with DEFAULT_METADATA."""
        logger_setup(extra_metadata={"env": "production", "version": "1.0.0"})

        # Write log record and verify metadata
        logger = logging.getLogger("test_logger")
        # logger.info("Hello World")
        with self.assertLogs(logger, level="INFO") as log_capture:
            logger.info("Test log message")

        log_output = log_capture.records[0]
        self.assertEqual(log_output.env, "production")
        self.assertEqual(log_output.version, "1.0.0")

    @patch("os.makedirs")
    @patch("logging.getLogger")
    def test_logger_setup_avoids_duplicate_handlers(
        self, mock_get_logger, mock_makedirs
    ):
        """Test that duplicate handlers are not created when logger_setup is called multiple times."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.hasHandlers.return_value = True  # Simulate existing handlers

        logger_setup()

        # Ensure no new handlers are added
        mock_logger.addHandler.assert_not_called()


if __name__ == "__main__":
    unittest.main()
