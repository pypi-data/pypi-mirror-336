import logging
from typing import Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel, Field, field_validator
from quicpro.exceptions import EncryptionError

logger = logging.getLogger(__name__)


class TLSConfig(BaseModel):
    key: bytes = Field(
        ...,
        min_length=32,
        max_length=32,
        description="32-byte (256-bit) symmetric key for AES-GCM encryption."
    )
    iv: bytes = Field(
        ...,
        min_length=12,
        max_length=12,
        description="12-byte static IV for nonce derivation."
    )

    @field_validator("key")
    def validate_key(cls, v: bytes) -> bytes:
        if len(v) != 32:
            raise ValueError("Key must be exactly 32 bytes (256 bits).")
        return v

    @field_validator("iv")
    def validate_iv(cls, v: bytes) -> bytes:
        if len(v) != 12:
            raise ValueError("IV must be exactly 12 bytes.")
        return v


class TLSEncryptor:
    """
    Production-grade TLSEncryptor that encrypts a QUIC packet using AES-GCM,
    emulating a TLS 1.3 encryption layer.
    This implementation derives per-record nonces using a static IV and a monotonically
    increasing sequence number. The nonce is computed as:
         nonce = static_iv XOR (sequence_number encoded as 12-byte big-endian)
    The encrypted record prepends an 8-byte sequence number to the ciphertext.
    """
    def __init__(self, udp_sender: Any, config: TLSConfig) -> None:
        """
        Initializes the TLSEncryptor with a validated TLS configuration.

        Args:
            udp_sender (Any): An object with a send(packet: bytes) method.
            config (TLSConfig): TLS configuration containing the encryption key and IV.
        """
        self.udp_sender = udp_sender
        self.config = config
        self.aesgcm = AESGCM(self.config.key)
        self._sequence_number = 0

    def _compute_nonce(self) -> bytes:
        """
        Computes the per-record nonce based on the current sequence number and the static IV.

        Returns:
            bytes: The computed nonce.
        """
        seq_bytes = self._sequence_number.to_bytes(12, byteorder='big')
        return bytes(iv_byte ^ seq_byte for iv_byte, seq_byte in zip(self.config.iv, seq_bytes))

    def encrypt(self, quic_packet: bytes) -> None:
        """
        Encrypts the provided QUIC packet and sends the result via UDP.
        The encryption uses AES-GCM with a nonce derived in TLS 1.3 style.
        An 8-byte sequence number is prepended to the ciphertext for record tracking.

        Args:
            quic_packet (bytes): The QUIC packet payload to encrypt.

        Raises:
            EncryptionError: If encryption or transmission fails.
        """
        try:
            nonce = self._compute_nonce()
            ciphertext = self.aesgcm.encrypt(nonce, quic_packet, None)
            record = self._sequence_number.to_bytes(8, byteorder='big') + ciphertext
            logger.info("TLSEncryptor produced encrypted packet with sequence number %d", self._sequence_number)
            self.udp_sender.send(record)
        except Exception as e:
            logger.exception("TLSEncryptor encryption failed: %s", e)
            raise EncryptionError(f"TLSEncryptor encryption failed: {e}") from e
        finally:
            self._sequence_number += 1