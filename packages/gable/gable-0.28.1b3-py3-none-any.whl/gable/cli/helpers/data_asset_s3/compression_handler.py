import gzip
import io
import zipfile

import snappy
from gable.cli.helpers.data_asset_s3.logger import log_debug


class CompressionHandler:
    """Handles compressed S3 files by detecting and decompressing their content."""

    SUPPORTED_FILE_TYPES = {"json", "csv", "tsv", "parquet", "orc", "avro"}
    COMPRESSION_EXTENSIONS = {"gz", "snappy", "zip"}

    @staticmethod
    def is_compressed(file_key: str) -> bool:
        """Check if the file contains a known compression extension, in any order."""
        extensions = set(file_key.lower().split("."))
        is_compressed = any(
            ext in CompressionHandler.COMPRESSION_EXTENSIONS for ext in extensions
        )
        log_debug(f"Compression detected for '{file_key}': {is_compressed}")
        return is_compressed

    @staticmethod
    def get_original_format(file_key: str) -> str:
        """
        Extracts the original format (e.g., .csv, .tsv) from a compressed file name, handling both orders.
        If the format cannot be determined, it returns an empty string instead of raising an error.
        """
        try:
            parts = file_key.split(".")
            file_format = next(
                (p for p in parts if p in CompressionHandler.SUPPORTED_FILE_TYPES), None
            )
            if not file_format:
                raise ValueError(
                    f"Could not determine original file format from: {file_key}"
                )
            return f".{file_format}"
        except ValueError as e:
            print(f"Warning: {e}")  # Log the warning but do not stop execution
            return ""

    @staticmethod
    def decompress(file_key: str, file_content: bytes) -> tuple[io.BytesIO, str]:
        """
        Decompresses a file and returns a BytesIO object with decompressed data.
        Also returns the **original file format**.
        """
        try:
            log_debug(f"Starting decompression for: {file_key}")
            original_file_key = CompressionHandler.get_original_format(file_key)

            if ".gz" in file_key:
                log_debug(f"Decompressing GZ file: {file_key}")
                decompressed_data = gzip.decompress(file_content)
                log_debug(
                    f"Decompressed GZ file: {file_key}, Size: {len(decompressed_data)} bytes"
                )
                return io.BytesIO(decompressed_data), original_file_key

            elif ".snappy" in file_key:
                log_debug(f"Decompressing Snappy file: {file_key}")
                decompressed_content = snappy.decompress(file_content)

                if isinstance(decompressed_content, str):
                    decompressed_content = decompressed_content.encode(
                        "utf-8"
                    )  # Ensure bytes

                log_debug(
                    f"Decompressed Snappy file: {file_key}, Size: {len(decompressed_content)} bytes"
                )
                return io.BytesIO(decompressed_content), original_file_key

            elif ".zip" in file_key:
                log_debug(f"Decompressing ZIP file: {file_key}")
                with zipfile.ZipFile(io.BytesIO(file_content), "r") as z:
                    file_names = z.namelist()
                    if not file_names:
                        raise ValueError("ZIP archive is empty.")

                    file_name = file_names[0]  # Assume single file inside ZIP
                    log_debug(f"Extracting file '{file_name}' from ZIP archive.")

                    with z.open(file_name) as zip_file:
                        decompressed_data = zip_file.read()
                        log_debug(
                            f"Decompressed ZIP file: {file_name}, Size: {len(decompressed_data)} bytes"
                        )
                        return io.BytesIO(decompressed_data), file_name

            else:
                raise ValueError(f"Unsupported compression format: {file_key}")

        except zipfile.BadZipFile:
            log_debug(f"Failed to decompress ZIP file: {file_key} (Invalid ZIP format)")
            raise
        except snappy.UncompressError:
            log_debug(
                f"Failed to decompress Snappy file: {file_key} (Invalid Snappy format)"
            )
            raise
        except Exception as e:
            log_debug(f"Decompression failed for '{file_key}': {e}")
            raise
